const paychecks = get_paychecks();

const latest_paychecks = new ApexCharts(document.querySelector("#income-chart"), {
  series: [{
    name: 'Latest Paychecks',
    data: get_graph_data_amount_date(paychecks),
  }],
  chart: {
    type: 'area',
    height: 250,
    stacked: false,
    animations: {
      enabled: false
    },
    zoom: {
      enabled: false
    },
  },
  dataLabels: {
    enabled: false
  },
  stroke: {
    curve: 'smooth',
    color: ['#56b68e', ]
  },
  fill: {
    colors: ['#56b68e'],
    opacity: 0.4,
    type: 'pattern',
    pattern: {
      style: ['fill'],
      width: 4,
      height: 1
    },
  },
  markers: {
    colors: ['#56b68e', '#000', '#ffffff'],
    size: 3,
    hover: {
      size: 4
    },
  },
  fill: {
    type: 'gradient',
    gradient: {
      shadeIntensity: 1,
      inverseColors: false,
      opacityFrom: 0.45,
      opacityTo: 0.35,
      stops: [30, 100, 100, 100],
    }
  },
  title: {
    text: 'Latest Paychecks',
  },
  tooltip: {
    intersect: true,
    shared: false
  },
  xaxis: {
    type: 'datetime',
    tickAmount: 8,
    labels: {
      rotate: -15,
    }
  },
  yaxis: {
    labels: {
      style: {
        colors: '#8e8da4',
      },
      offsetX: 0
    },
    title: {
      text: 'Net Pay ($)'
    }
  }
});


const hourly_rates = new ApexCharts(document.querySelector("#hourly-rate-chart"), {
  series: [{
    name: 'Hourly Rate Over Time',
    data: get_graph_data_hourly_rate_date(paychecks),
  }],
  chart: {
    type: 'area',
    height: 250,
    stacked: false,
    animations: {
      enabled: false
    },
    zoom: {
      enabled: false
    },
  },
  dataLabels: {
    enabled: false
  },
  stroke: {
    curve: 'smooth',
    color: ['#56b68e', ]
  },
  fill: {
    colors: ['#56b68e'],
    opacity: 0.4,
    type: 'pattern',
    pattern: {
      style: ['fill'],
      width: 4,
      height: 1
    },
  },
  markers: {
    colors: ['#56b68e', '#000', '#ffffff'],
    size: 3,
    hover: {
      size: 4
    },
  },
  fill: {
    type: 'gradient',
    gradient: {
      shadeIntensity: 1,
      inverseColors: false,
      opacityFrom: 0.45,
      opacityTo: 0.35,
      stops: [30, 100, 100, 100],
    }
  },
  title: {
    text: 'Latest Paychecks',
  },
  tooltip: {
    intersect: true,
    shared: false
  },
  xaxis: {
    type: 'datetime',
    tickAmount: 8,
    labels: {
      rotate: -15,
    }
  },
  yaxis: {
    labels: {
      style: {
        colors: '#8e8da4',
      },
      offsetX: 0
    },
    title: {
      text: 'Net Pay ($)'
    }
  }
});

latest_paychecks.render();
hourly_rates.render();