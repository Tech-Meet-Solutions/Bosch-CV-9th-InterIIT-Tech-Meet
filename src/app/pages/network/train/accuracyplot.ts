export var accuracyplotoptions = {
    series: [
      {
        name: "Train Accuracy",
        data: []
      },
      {
        name: "Validation Accuracy",
        data: []
      }
    ],
    chart: {
      height: 350,
      type: "line",
      zoom: {
        enabled: false
      },
      foreColor: 'white',
      toolbar:{
        tools:{
          download: false
        }
      },
    },
    dataLabels: {
      enabled: false
    },
    stroke: {
      curve: "straight"
    },
    title: {
      align: "left",
      style: {
        color: 'white'
      }
    },
    grid: {
      row: {
        colors: ["#29313A"], // takes an array which will be repeated on columns
        opacity: 0.5
      }
    },
    xaxis: {
      categories: [],
      title:{
        text: "Epochs"
      }
    },
    yaxis:{
        title:{
            text:"accuracy"
        }
    },
    tooltip:{
      fillSeriesColor: true,
      theme: 'dark'
    },
    colors: ['#007bff', '#FFA500']
  };