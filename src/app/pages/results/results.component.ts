import { Component, OnInit } from '@angular/core';
import { DataService } from 'src/app/services/data.service';
import { HttpService } from 'src/app/services/http.service';
import { NetworkService } from 'src/app/services/network.service';
import { Networks } from '../network/networks.types';
import { Result, ResultName } from './result.interface';
import { ResultService } from './results.service';

@Component({
  selector: 'app-results',
  templateUrl: './results.component.html',
  styleUrls: ['./results.component.scss']
})
export class ResultsComponent implements OnInit {
  links = [
    {
      name : 'Embeddings',
      icon : 'add_photo_alternate',
      link : 'embeddings',
    },
    {
      name : 'Wrong results',
      icon : 'Collections',
      link : 'wrongres',
    },
    {
      name : 'Suggestions',
      icon : 'trending_up',
      link : 'suggestions',
    }
  ]
  networks = Networks;
  currNetwork : any;
  results = [];
  currResult : any;
  result: Result;
  resultName: ResultName;
  constructor(private nservice : NetworkService, private api: HttpService, private resultService: ResultService, private data: DataService) { }

  ngOnInit(): void {
    this.nservice.getCurrNetwork().subscribe((data : any)=>{
      console.log(data);
      this.currNetwork = data;
      this.get_eval_results();
    })
  }

  save(){
    this.nservice.setCurrNetwork(this.currNetwork);
    this.get_eval_results();
  }

  networkComparator(obj1 : any, obj2 : any){
    return obj1.value == obj2.value;
  }

  get_eval_results(){
    this.api.get(this.api.host + "/api/getevalresults", {model_name: this.currNetwork.value})
    .subscribe (
      response => {console.log(response); this.results = response},
      error => {console.log(error)}
    );
  }

  get_result(){
    this.resultName = {
      net_name: this.currNetwork.value,
      result_name: this.currResult
    }
    this.data.selected_result = this.resultName;
    this.resultService.changeResult(this.resultName);
  }

}
