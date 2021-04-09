import {
    ApexAxisChartSeries,
    ApexTitleSubtitle,
    ApexDataLabels,
    ApexChart,
    ApexTooltip,
    ApexTheme,
    ApexMarkers,
    ApexYAxis,
    ApexXAxis,
    ApexNoData,
    ApexPlotOptions,
    ApexLegend,
  } from "ng-apexcharts";
  
  export type ChartOptions = {
    series?: ApexAxisChartSeries;
    chart?: ApexChart;
    dataLabels?: ApexDataLabels;
    title?: ApexTitleSubtitle;
    tooltip? : ApexTooltip,
    colors?: any;
    theme? : ApexTheme,
    markers? : ApexMarkers
    yaxis? : ApexYAxis,
    xaxis? : ApexXAxis,
    nodata? : ApexNoData,
    plotOptions? : ApexPlotOptions,
    legend? : ApexLegend,
  };

 export const confMatrixOptions : ChartOptions = {
    series: [],
    nodata : {
      text : 'Loading...'
    },
    chart: {
      animations :{
        enabled :false
      },
      height: 500,
      type: "heatmap",
      toolbar : {
          show : false
      },
      events : {
          click : function(){
              console.log("hello")
          }
      },
    },
    dataLabels: {
      enabled: false
    },
    colors: ["#ffffff",'#0000ff'],
    tooltip :{
        enabled : true,
        theme : 'dark',
    },
    theme:{
        palette :'palette10'
    },
    markers :{
      size : 0,
    },
    yaxis : {
      show : true,
      reversed : true,
      labels :{
        show : false
      },
      title :{
        text : 'True class',
        style : {
          color : '#ffffff'
        }
      }
    },
    xaxis : {
      title : {
        text : 'Predicted class',
        style : {
          color : '#ffffff'
        }
      },
      labels :{
        show :false
      }
    },
    plotOptions: {

    },
    legend : {
      labels :{
        useSeriesColors : true
      }
    },
  };

export function generateData() {
  let series = []
  Array.from(Array(45).keys()).forEach((x)=>{
    let serie = {name : x , data : []};
    Array.from(Array(45).keys()).forEach((y)=>{
      serie.data.push(2*y);
    })
    series.push(serie);
  })
  return series;
}

export const imgs = []