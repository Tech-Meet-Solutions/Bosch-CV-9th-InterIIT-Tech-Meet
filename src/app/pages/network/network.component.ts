import { Component, OnInit } from '@angular/core';
import { NetworkService } from 'src/app/services/network.service';
import { Networks } from './networks.types';

@Component({
  selector: 'app-network',
  templateUrl: './network.component.html',
  styleUrls: ['./network.component.scss']
})
export class NetworkComponent implements OnInit {
  background = undefined;
  links = [
    {
      name : 'Display',
      icon : 'add_photo_alternate',
      link : 'display',
    },
    {
      name : 'Modify',
      icon : 'Collections',
      link : 'modify',
    },
    {
      name : 'Train',
      icon : 'trending_up',
      link : 'train',
    }
  ]

  networks = Networks;
  currNetwork : any;
  constructor(private nservice : NetworkService) { }

  ngOnInit(): void {
    this.nservice.getCurrNetwork().subscribe((data : any)=>{
      console.log(data);
      this.currNetwork = data;
    })
  }

  save(){
    this.nservice.setCurrNetwork(this.currNetwork);
  }

  networkComparator(obj1 : any, obj2 : any){
    return obj1.value == obj2.value;
  }
}
