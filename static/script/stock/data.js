const data_holder = document.getElementById('data-table');


window.addEventListener("DOMContentLoaded", ()=> {
    for(var trade of trades){
        trade.update_ticker()
    }
    for(var trade of trades){
        // console.log(trade.last_value)
    }
})


async function get_quote_last_price(ticker) {
    const url = `https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=${ticker}&interval=5min&apikey=4330UMJ1ND2887X8&outputsize=compact`
    try {
        const response = await fetch(url);
        const json = await response.json();
        if (json === undefined)
            throw new Error(`Data for ${ticker} not reachable`);
        const time_series = await json['Time Series (5min)'];
        const key = Object.keys(time_series)[0];
        return time_series[key]['1. open'];
    } catch {
        // Occurs when request delay is two small.            
        return NaN;
    }
}


class Trade {

    constructor(ticker, bought_on, shares, buy_value, fees, sold_price, sold_on) {
        this.ticker = ticker;
        this.bought_on = Date.parse(bought_on);
        this.shares = this._convert_to_number(shares);
        this.buy_value = this._convert_to_number(buy_value);
        this.fees = this._convert_to_number(fees);
        this.sold_price = this._convert_to_number(sold_price);
        this.sold_on = Date.parse(sold_on);
        this.__last_value = NaN;
    }

    _convert_to_number(cell_value) {
        return Number(cell_value.replace(/(\r\n|\n|\r|\s|\$)/gm, ''));
    }

    update_ticker(){
        let attempt = 0;
        let id = setInterval(()=>{

            get_quote_last_price(this.ticker).then(result=>{
                this.__last_value = result
                if (this.__last_value !== undefined && !isNaN(result)){
                    clearInterval(id);
                    return;
                } else {
                    console.info(`Failed Attempt #${attempt} for ticker ${this.ticker}`)
                }
            });
            attempt++;
            if (attempt === 3){
                clearInterval(id);
                console.warn(`Failed to get price of ticker ${this.ticker}`)
            }
        }, 3000)
    }

    get total_value() {
        return this.shares * this.last_value
    }


    get active() {
        return isNaN(this.sold_on);
    }

    get last_value() {
        return this.__last_value;
    }


    get currency() {
        return null; // Implement
    }

    get profit() {
        if (this.last_value == NaN)
            return NaN;
        return this.shares * (this.last_value - this.bought_on);
    }

    get profit_percent() {
        if (this.last_value == NaN)
            return NaN
        return Math.round(100 * (this.last_value / this.bought_on - 1)) / 100;
    }

    get duration() {
        var offset = this.sold_on == null ? Date() : this.sold_on;
        var delta = offset.getTime() - this.bought_on.getTime();
        return delta / (24 * 60 * 60 * 1000);
    }
}


function get_trades(skip_header = true) {

    function get_data(row_el, col_index) {
        return row_el.cells[col_index].innerHTML
    }

    const rows = data_holder.rows;
    var trades = [];
    for (var i = skip_header ? 1 : 0; i < rows.length; i++) {
        trades.push(new Trade(
            get_data(rows[i], 0), // Ticker
            get_data(rows[i], 1), // Bought on
            get_data(rows[i], 2), // Shares
            get_data(rows[i], 3), // Buy Values
            get_data(rows[i], 4), // Fees
            get_data(rows[i], 5), // Sold Price
            get_data(rows[i], 6), // Sold On
        ));
    }
    return trades;
}


function get_active_total(trades) {
    var total = 0;
    for (var i = 0; i < trades.length; i++) {
        if (trades[0].active) {
            total += trades[i].total_value;
        }
    }
    return total;
}

function get_realised_gain(trades) {
    var total = 0;
    for (var i = 0; i < trades.length; i++) {
        if (!trades[0].active)
            total += trades[i].total_value;
    }
    return total;
}

function get_graph_diversification(trades) {
    const map = new Map();

    for (var i = 0; i < trades.length; i++) {
        if (isNaN(trades[i].total_value))
            continue;
        if (map.has(trades[i].ticker))
            map.set(trades[i].ticker, map.get(trades[i].ticker) + trades[i].total_value);
        else
            map.set(trades[i].ticker, trades[i].total_value);

    }
    return [
        Array.from(map.values()),
        Array.from(map.keys())
    ]
}