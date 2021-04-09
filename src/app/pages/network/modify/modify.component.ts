import { Component, OnInit } from '@angular/core';
import { NetworkService } from 'src/app/services/network.service';
import {RightHyperparamInputs,LeftHyperparamInputs,LossInputs} from './inputs';
import { defaultInputs } from './inputs.default';
import {MatSnackBar} from '@angular/material/snack-bar';

@Component({
  selector: 'app-modify',
  templateUrl: './modify.component.html',
  styleUrls: ['./modify.component.scss']
})
export class ModifyComponent implements OnInit {

  leftHyperparamInputs  = LeftHyperparamInputs;
  lossInputs = LossInputs;
  rightHyperparamInputs = RightHyperparamInputs;
  inputs : any;
  currNetwork : any;
  constructor(private networkService : NetworkService, private _snackBar : MatSnackBar) { }

  ngOnInit(): void {
    this.networkService.getCurrNetwork().subscribe(data=>{
      this.currNetwork = data;
      this.networkService.getNetworkParams(this.currNetwork.value).subscribe(data=>this.inputs = data,err=>this.inputs={});
    })
  }

  save(){
    this.networkService.setNetworkParams(this.currNetwork.value,this.inputs).subscribe((data)=>{
      this._snackBar.open('Saved successfully', '', {
        duration: 2000,
      });
    })
  } 

}
