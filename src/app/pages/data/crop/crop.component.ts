import { AfterViewInit, Component, Inject, OnInit } from '@angular/core';
import { MatDialogRef, MAT_DIALOG_DATA } from "@angular/material/dialog";
@Component({
  selector: 'app-crop',
  templateUrl: './crop.component.html',
  styleUrls: ['./crop.component.scss']
})
export class CropComponent implements OnInit, AfterViewInit {

  xy ;
  wh ;
  constructor(public dialogRef : MatDialogRef<CropComponent>,@Inject(MAT_DIALOG_DATA) public data: any) { }

  ngOnInit(): void {
  }

  ngAfterViewInit(){
    this.updateCrop()
  }

  getImageDimensions(file) {
    return new Promise (function (resolved, rejected) {
      var i = new Image()
      i.onload = function(){
        resolved({w: i.width, h: i.height})
      };
      i.src = file
    })
  }

  updateCrop(){
    this.getImageDimensions(this.data.image.b64).then((val:any)=>{
      console.log(val);
      (<any>$('#crop-select')).CropSelectJs({
        animatedBorder: true,
        aspectRatio:null,
      
        // Image
        imageSrc: this.data.image.b64,
        imageWidth: val.w,
        imageHeight: val.h,
      
        // Stub events
        selectionResize: (data)=> {
          console.log(data);
          this.wh = data;
        },
        selectionMove: (data)=> {
          console.log(data)
          this.xy = data;
        },
      });
    });
  }

  close(action : any) {
    this.dialogRef.close({action : action,id : this.data.image.id,xy : this.xy, wh : this.wh});
  }

}
