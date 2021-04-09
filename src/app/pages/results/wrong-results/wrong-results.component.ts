import { AfterContentInit, AfterViewInit, Component, OnInit, ViewChild } from '@angular/core';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Router } from '@angular/router';
import { ChartComponent } from 'ng-apexcharts';
import { HttpService } from 'src/app/services/http.service';
import { ResultService } from '../results.service';
import { ChartOptions, confMatrixOptions,generateData } from './conf-matrix.options';
import { NgxSpinnerService } from 'ngx-spinner';


@Component({
  selector: 'app-wrong-results',
  templateUrl: './wrong-results.component.html',
  styleUrls: ['./wrong-results.component.scss']
})
export class WrongResultsComponent implements OnInit{
  @ViewChild("chart") chart;
  @ViewChild("ConfChart",{static : false}) confChart : ChartComponent;
  public chartOptions: Partial<ChartOptions> = JSON.parse(JSON.stringify(confMatrixOptions));

  constructor(private resService : ResultService, private _snackbar : MatSnackBar, private router : Router, private spinner : NgxSpinnerService) { 
    console.log('in constructor',this.chartOptions);
  }

  labels;
  images : any = [];
  network;
  selTrueClass;
  selPredClass;
  result;
  confMat;
  selectedImages = [false,false];
  suggestionsClicked = false;

  generateSeries(confMat){
    let series = [];
    for(let i = 0; i < confMat.length;i++){
      series.push({name : i+"",data: confMat[i]})
    }

    return series;
  }

  ngOnInit(): void {
    console.log('in constructor');
    let mergeEvent : ChartOptions = {
      chart: {
        animations :{
          enabled :false
        },
        height: 750,
        type: "heatmap",
        toolbar : {
            show : false
        },
        events : {
            click : (event, chartContext, config)=>{
                console.log(config)
                this.selTrueClass = this.labels[config.seriesIndex];
                this.selPredClass = this.labels[config.dataPointIndex];
                this.resService.getWrongResults(this.network,this.result,this.selPredClass,this.selTrueClass).subscribe((data : any)=>{
                  this.images = data;
                  this.selectedImages = new Array(this.images.imgs.length).fill(false);
                  console.log(data);
                },(err)=>{
                  this.images = [];
                  this.selectedImages = [];
                  console.log(err,"Hello");
                })
            }
        },
      },
      tooltip : {
        custom : ({series, seriesIndex, dataPointIndex, w})=>{
          return `<div style="padding : 5px;"><b>${this.confMat[seriesIndex][dataPointIndex]}</b><br>True Class : ${this.labels[seriesIndex]}<br>Predicted Class : ${this.labels[dataPointIndex]}</div>`
        }
      }
    }
    setTimeout(()=>{
      this.resService.result.subscribe((data)=>{
        this.network = data.net_name;
        this.result =  data.result_name;
        console.log(data)
        this.resService.getConfMatrix(this.network,this.result).subscribe((data:any)=>{
          console.log(data)
          this.confChart.updateSeries(this.generateSeries(data.conf));
          this.labels = data.labels;
          this.confMat = data.conf;
          this.confChart.updateOptions(mergeEvent);
        })
      })
    },100);
      
  }

  select(index : number){
    this.selectedImages[index] = !this.selectedImages[index];
  }

  submit(){
    if(!this.selectedImages.length || !this.selectedImages.includes(true))
      this._snackbar.open('Select some images to cotinue','',{
        duration : 2000
      })
    else{
      this.suggestionsClicked = true;
      let paths = this.images.paths.filter((val,ind)=>{
        return this.selectedImages[ind];
      })
      this.spinner.show();
      console.log(paths);
      this.resService.startGradcamLime(this.network,this.result,this.selTrueClass,paths).subscribe((data)=>{
        console.log(data)
        this.spinner.hide();
        this.router.navigateByUrl('/pages/results/suggestions');
      })
    }
  }
}
