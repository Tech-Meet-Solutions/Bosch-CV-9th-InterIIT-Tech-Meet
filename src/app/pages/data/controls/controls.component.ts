import { Component, EventEmitter, OnInit, Output } from '@angular/core';
import { Transforms } from 'src/app/interfaces/transforms.interface';
import { defaults } from './transforms.default';
import { transformTypes } from './transform_types';
import { MatDialog, MatDialogConfig } from '@angular/material/dialog';
import { DialogComponent } from 'src/app/extra-components/dialog/dialog/dialog.component';

@Component({
  selector: 'app-controls',
  templateUrl: './controls.component.html',
  styleUrls: ['./controls.component.scss']
})
export class ControlsComponent implements OnInit {

  transforms : Transforms;
  transformTypes = transformTypes;
  @Output() apply = new EventEmitter<Transforms>(); 
  @Output() save = new EventEmitter<any>();
  constructor(private matDialog : MatDialog) { }

  ngOnInit(): void {
    this.transforms = JSON.parse(JSON.stringify(defaults));
  }

  onChange(event, type){
    this.transforms[type] = event.value;
    this.onSubmit();  
    console.log(this.transforms)
  }
  onChecked(event,type){
    this.transforms[type] = event.checked; 
    this.onSubmit(); 
    console.log(this.transforms)
  }

  onSubmit(){
    console.log(this.transforms);
    this.apply.emit(this.transforms);
    console.log("Submitted");
  }

  onSave(){
    const dialogConfig = new MatDialogConfig();
    dialogConfig.data = {
      title : 'Confirm',
      content : 'Are you sure you would like to save current transformations?',
      actions : [
        {
          title : 'Save',
          msg : 'inplace',
          color : '#0088FF',
        },
        {
          title : 'Save as Duplicate',
          msg : 'duplicate',
          color : '#0088FF',
        },
        {
          title : 'Cancel',
          msg : 'cancel',
          color : '#455060',
        }
      ]
    }
    let dialogRef = this.matDialog.open(DialogComponent, dialogConfig);
    dialogRef.afterClosed().subscribe((msg)=>{
      this.save.emit(msg);
    });
  }

  reset(){
    console.log("In reset");
    this.transforms = JSON.parse(JSON.stringify(defaults));
    console.log(this.transforms)
    this.apply.emit({});
  }
}
