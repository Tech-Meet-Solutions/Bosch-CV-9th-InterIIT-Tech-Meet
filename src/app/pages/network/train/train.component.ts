import { Component, OnInit, Input, ViewChild, ViewEncapsulation, ElementRef } from '@angular/core';
import { MatSnackBar } from '@angular/material/snack-bar';
import * as $ from 'jquery';
import { HttpService } from 'src/app/services/http.service';
import {
  ChartComponent,
  ApexAxisChartSeries,
  ApexChart,
  ApexXAxis,
  ApexDataLabels,
  ApexTitleSubtitle,
  ApexStroke,
  ApexGrid
} from "ng-apexcharts";
import { lossplotoptions } from './lossplot';
import { accuracyplotoptions } from './accuracyplot';
import { NetworkService } from 'src/app/services/network.service';
import { NgxSpinnerService } from 'ngx-spinner';

export type ChartOptions = {
  series: ApexAxisChartSeries;
  chart: ApexChart;
  xaxis: ApexXAxis;
  dataLabels: ApexDataLabels;
  grid: ApexGrid;
  stroke: ApexStroke;
  title: ApexTitleSubtitle;
};

@Component({
  selector: 'app-train',
  templateUrl: './train.component.html',
  styleUrls: ['./train.component.scss'],
})
export class TrainComponent implements OnInit {
  chartOptions;
  inputVal = 0;
  data = []; 
  categories = [];
  socket;
  accuracyChartOptions;
  labels;
  values:any = {};
  currentSmoteLabel;
  autogen = false;
  training = false;
  id;
  total_epochs;
  epoch_factor;
  first_val;
  EPOCH_FACTORS = {"baseline" : 22/60,"mobilenet" : 28/60, "resnet": 95/60, "googlenet" : 92/60};
  @ViewChild('slider') ttslider: any;
  constructor(private api: HttpService, private _snackBar: MatSnackBar, private nservice: NetworkService, private spinner : NgxSpinnerService) { 
      this.chartOptions = lossplotoptions;
      this.accuracyChartOptions = accuracyplotoptions;
  }

  scores : any = [
      ['Epoch Count: ', '--'],
      ['ETC in minutes: ', '--']
  ]

  onSocketMessage(data){
        if(!data)
          return;
        let _jsondata = JSON.parse(data);
        if(_jsondata["type"] === "ETA" && !this.first_val) {
          this.scores[1][1] = _jsondata["value"];
          this.first_val = true;
        }
        else if(_jsondata["type"] === "epoch"){
          this.scores[0][1] = _jsondata["value"];
          this.scores[1][1] = (""+(this.total_epochs - (+this.scores[0][1])-1)*this.epoch_factor).substring(0,4);
        }
        else if(_jsondata["type"] === "train_loss"){
          let data = _jsondata["value"].split(",");
          let x_values = [];
          for(var i= 1; i<=data.length; i++) x_values.push(i);
          this.chartOptions.xaxis.categories = x_values;
          this.chartOptions.series = [{name: this.chartOptions.series[0].name, data: data}, this.chartOptions.series[1]]
        }
        else if(_jsondata["type"] === "val_loss"){
          let data = _jsondata["value"].split(",");
          let x_values = [];
          for(var i= 1; i<=data.length; i++) x_values.push(i);
          this.chartOptions.xaxis.categories = x_values;
          this.chartOptions.series = [this.chartOptions.series[0], {name : this.chartOptions.series[1].name, data: data}]
        }
        else if(_jsondata["type"] === "train_acc"){
          let data = _jsondata["value"].split(",");
          let x_values = [];
          for(var i= 1; i<=data.length; i++) x_values.push(i);
          this.accuracyChartOptions.xaxis.categories = x_values;
          this.accuracyChartOptions.series = [{name: this.accuracyChartOptions.series[0].name, data: data}, this.accuracyChartOptions.series[1]];
        }
        else if(_jsondata["type"] === "val_acc"){
          let data = _jsondata["value"].split(",");
          let x_values = [];
          for(var i= 1; i<=data.length; i++) x_values.push(i);
          this.accuracyChartOptions.xaxis.categories = x_values;
          this.accuracyChartOptions.series = [this.accuracyChartOptions.series[0], {name: this.accuracyChartOptions.series[1].name, data: data}];
      }
      else if(_jsondata["type"] === "end"){
        clearInterval(this.id);
        this.spinner.hide();
        this.training = false;
        alert("Training Completed!");
      }
  }

  ngOnInit(): void {
    this.first_val = false;
    // let sock = new WebSocket(`ws://167.71.236.236:5009`);
    // sock.onopen  = (data) => {
    //   console.log('hi')
    //   this.socket = sock;
    // };
    
    //     data format of socket message: a string
    //     {"type": "epoch" | "ETA" | "F1" | "other" , "value" : string | number}
    
    // sock.onmessage = (data) => {
    //     this.onSocketMessage(data.data); 
    // }
    // sock.onerror = (err) => {console.log(err)}
    this.nservice.getCurrNetwork().subscribe((data)=>{
      this.nservice.getNetworkParams(data.value).subscribe((data2 : any)=>{
        this.total_epochs = +data2.epochs;
        this.epoch_factor = this.EPOCH_FACTORS[data.value];
      })
    })

    this.api.get(`${this.api.host}/api/labels/`).subscribe((res) => {
      this.labels = res.data; 
      for(let i = 0; i<this.labels.length; i++){
          this.values[this.labels[i]] = 0;
      }
    });
  }

  ngAfterViewInit(){

  }

  post(filename, val){
      let formData = new FormData();
      formData.append('filename', filename);
      formData.append('value', val);
      this.api.post(formData,`${this.api.host}/api/train/`).subscribe(
          (res) => {
            this._snackBar.open("Saved Successfully", val , {
              duration: 2000,
            });
          },
          (err) => console.log(err)
      )
  }

  changeParams(filename, label, val){
      let formData:any = new FormData();
      formData.append('filename', filename);
      this.values[label] = parseInt(val);
      formData.append('value', JSON.stringify(this.values));
      this.api.post(formData, `${this.api.host}/api/train/`).subscribe(
        (res) => {
          this._snackBar.open("Saved Successfully", val , {
            duration: 2000,
          });
        },
        (err) => console.log(err)
      );
  }


  ngOnDestroy(){
    if(this.id)
      clearInterval(this.id);
    if(this.socket) this.socket.close();
  }

  setCurrentLabel(val){
    this.currentSmoteLabel = val;
  }

  startTraining(){
    this.training = true;
    this.spinner.show();
    this.getData();
    console.log(this.ttslider.nativeElement.value);
    this.nservice.getCurrNetwork().subscribe(
      (res)=> this.api.get(`${this.api.host}/api/starttrain?model_name=${res.value}&train_split=${this.ttslider.nativeElement.value}&smote_factor=${JSON.stringify(this.values)}&autogen=${this.autogen? 1: 0}`).subscribe((res) => console.log(res), (err) => console.log(err))
    );
    
  }

  autoGenerate(){
      this.autogen = !this.autogen;
  }

  getData(){
    this.id = setInterval(() =>{
      this.api.get(`${this.api.host}/api/train_data/?type=ETA`).subscribe((res) => this.onSocketMessage(res), (err) => console.log(err));
      this.api.get(`${this.api.host}/api/train_data/?type=epoch`).subscribe((res) => this.onSocketMessage(res), (err) => console.log(err));
      this.api.get(`${this.api.host}/api/train_data/?type=train_acc`).subscribe((res) => this.onSocketMessage(res), (err) => console.log(err));
      this.api.get(`${this.api.host}/api/train_data/?type=train_loss`).subscribe((res) => this.onSocketMessage(res), (err) => console.log(err));
      this.api.get(`${this.api.host}/api/train_data/?type=val_acc`).subscribe((res) => this.onSocketMessage(res), (err) => console.log(err));
      this.api.get(`${this.api.host}/api/train_data/?type=val_loss`).subscribe((res) => this.onSocketMessage(res), (err) => console.log(err));
      this.api.get(`${this.api.host}/api/train_data/?type=end`).subscribe((res) => this.onSocketMessage(res), (err) => console.log(err));

    }, 1000)
  }

}

