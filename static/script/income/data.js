const data_holder = document.getElementById("data-table");

class Paycheck {

    constructor(amount, hours, week, over_hours) {
        this.amount = amount;
        this.hours = hours;
        this.week = week.replace(/(\r\n|\n|\r|\s)/gm, '') == '' ? null : week;
        this.over_hours = over_hours;
    }

    hourly_rate() {
        return Math.round(this.amount / this.hours * 100) / 100;
    }
};


function get_paychecks(skip_header = true) {

    function get_data(row_el, col_index, number = true) {
        var data = row_el.cells[col_index].innerHTML;
        return number ? Number(data.replace(/(\r\n|\n|\r|\s|\$)/gm, '')) : data;
    }

    const rows = data_holder.rows;
    var paychecks = [];
    for (var i = skip_header ? 1 : 0; i < rows.length; i++) {
        paychecks.push(new Paycheck(
            get_data(rows[i], 0), // Amount
            get_data(rows[i], 1), // Hours
            get_data(rows[i], 2, false), // Week
            get_data(rows[i], 3), // Over hours
        ));
    }
    return paychecks;
}


function get_graph_data_amount_date(paychecks) {
    var data = []
    for (var i = 0; i < paychecks.length; i++) {
        data.push({
            x: paychecks[i].week, // Week
            y: paychecks[i].amount, // Amount
        })
    }
    return data;
}

function get_graph_data_hourly_rate_date(paychecks){
    var data = []
    for (var i = 0; i < paychecks.length; i++) {
        data.push({
            x: paychecks[i].week, // Week
            y: Math.round(paychecks[i].amount / paychecks[i].hours * 100) / 100, // Hourly rate
        })
    }
    return data;
}

function get_total_amount(paychecks){
    var total = 0;
    for(var i = 0; i < paychecks.length; i++){
        total += paychecks[i].amount;
    } 
    return total.toFixed(2);
}

function get_ytd_revenu(paychecks){
    const year = new Date().getFullYear();
    var total = 0;
    for(var i = 0; i < paychecks.length; i++){
        if (new Date(paychecks[i].week).getFullYear() == year){
            total += paychecks[i].amount;
        }
    }
    return total.toFixed(2);
}

function get_total_hours(paychecks){
    var total = 0;
    for (var i = 0; i < paychecks.length; i++){
        total += paychecks[i].hours
    }
    return total.toFixed(2);
}

function get_average_hours_per_week(paychecks){
    return (get_total_hours(paychecks) / paychecks.length).toFixed(2);
}


function get_average_hourly_rate(paychecks){      
    return Number(get_total_amount(paychecks) / get_total_hours(paychecks)).toFixed(2);
}