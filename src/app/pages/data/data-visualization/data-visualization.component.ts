import { Component, OnInit } from '@angular/core';
import { ClassData } from 'src/app/interfaces/classData.interface';
import { MatDialog, MatDialogConfig } from '@angular/material/dialog';
import { ImagesDialogComponent } from './images-dialog/images-dialog.component';
import { VisualizationService } from 'src/app/services/visualization.service';

@Component({
  selector: 'app-data-visualization',
  templateUrl: './data-visualization.component.html',
  styleUrls: ['./data-visualization.component.scss']
})
export class DataVisualizationComponent implements OnInit {

  constructor(private matDialog : MatDialog, private vizService : VisualizationService) { }
  classData: any[];

  ngOnInit(): void {
    this.vizService.getImages('__all__',1).subscribe((data : any)=>{
      this.classData = data.classes;
      console.log(this.classData);
    })
  }

  openDialog(obj){
    let dialogConfig = new MatDialogConfig();
    dialogConfig.panelClass = "dialog-dark-background";
    this.vizService.getImages(obj.class_name,5).subscribe((data : any)=>{
      dialogConfig.data = {
        title : data.classes[0].class_name,
        images : data.classes[0].pics
      }
      this.matDialog.open(ImagesDialogComponent,dialogConfig);
    })    
  }

}
