import { Component, OnInit } from '@angular/core';
import { NetworkService } from 'src/app/services/network.service';

@Component({
  selector: 'app-display',
  templateUrl: './display.component.html',
  styleUrls: ['./display.component.scss']
})
export class DisplayComponent implements OnInit {

  constructor(private netService : NetworkService) { }

  networkData;
  network;
  currLayer;
  num_layers;

  ngOnInit(): void {
    this.netService.getCurrNetwork().subscribe(data=>{
      this.network = data;
      console.log(data)
      this.netService.getDisplayNetwork(this.network).subscribe((data)=>{
        this.networkData = data;
        this.currLayer = 0;
        this.num_layers = this.networkData.layers.length;
      })
    })
  }

  change_layer(n: number){
    this.currLayer = (this.currLayer + n + this.num_layers) % this.num_layers;
    console.log(this.currLayer)
  }

}
