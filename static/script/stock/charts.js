const trades = get_trades();

const diversification_data = get_graph_diversification(trades);
const diversification = new ApexCharts(document.querySelector('#diversification-chart'), {
    series: diversification_data[0],
    labels: diversification_data[1],
    chart: {
        type: 'pie',
        height: 250,
        
    },
    stroke: {
        show: false
    }
});

diversification.render();


get_quote_last_price('MSFT')