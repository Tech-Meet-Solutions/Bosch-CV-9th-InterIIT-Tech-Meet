import { Component, OnDestroy, OnInit } from '@angular/core';
import { Subscription } from 'rxjs';
import { DataService } from 'src/app/services/data.service';
import { HttpService } from 'src/app/services/http.service';
import { Result, ResultName } from '../result.interface';
import { ResultService } from '../results.service';
import { NgxSpinnerService } from 'ngx-spinner';
import { NetworkService } from 'src/app/services/network.service';

@Component({
  selector: 'app-embeddings',
  templateUrl: './embeddings.component.html',
  styleUrls: ['./embeddings.component.scss']
})
export class EmbeddingsComponent implements OnInit, OnDestroy {

  constructor(private resultService: ResultService, private api: HttpService, 
              private data: DataService, private spinner: NgxSpinnerService,
              private nservice: NetworkService) { }

  subscription: Subscription;
  result: Result;

  ngOnInit(): void {
    this.subscription = this.resultService.resultChanged$.subscribe(
      result => {
        console.log(result);
        this.get_result(result);
      }
    )
    if (this.data.selected_result != undefined) {
      this.get_result(this.data.selected_result);
    }
  }

  ngAfterViewInit(){
  }

  get_result(result: ResultName){
    console.log("Here")
    this.api.get(this.api.host + "/api/geteval", {net_name: result.net_name, result_name: result.result_name})
    .subscribe (
      response => {console.log(response); this.result = response},
      error => {console.log(error)}
    );
  }

  ngOnDestroy(){
    this.subscription.unsubscribe();
  }

  startEvaluate(){
    this.spinner.show();
      this.nservice.getCurrNetwork().subscribe(
        (res) => {
          this.api.get(`${this.api.host}/api/starteval?model_name=${res.value}`).subscribe((res)=>{
            console.log(res);
            this.spinner.hide();
          },
          (err) => console.log(err));
        }
      )
      
  }


}
