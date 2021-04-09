import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';
import { Networks } from '../pages/network/networks.types';

@Injectable({
  providedIn: 'root'
})
export class NetworkService {
   url = "http://127.0.0.1:8000/api/curr_network/";
   displayUrl = "http://127.0.0.1:8000/api/net_dis/";
  //url = "https://interiit.moodi.org/api/curr_network/";

  currNetwork = new BehaviorSubject(Networks[0]);

  constructor(private http: HttpClient) { }

  getCurrNetwork(){
    return this.currNetwork;
  }

  setCurrNetwork(data){
    this.currNetwork.next(data);
  }

  setNetworkParams(networkKey, data){
    return this.http.post(this.url,{network : networkKey, data : data});
  }
  getNetworkParams(networkKey){
    return this.http.get(this.url,{
      params :{
        network : networkKey
      }
    });
  }

  getDisplayNetwork(network){
    return this.http.get(this.displayUrl,{
      params :{
        network : network.value
      }
    })
  }
}
