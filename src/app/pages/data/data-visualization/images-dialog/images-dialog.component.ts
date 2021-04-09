import { Inject } from '@angular/core';
import { Component, OnInit } from '@angular/core';
import { MatDialogRef, MAT_DIALOG_DATA } from "@angular/material/dialog";
@Component({
  selector: 'app-images-dialog',
  templateUrl: './images-dialog.component.html',
  styleUrls: ['./images-dialog.component.scss']
})
export class ImagesDialogComponent implements OnInit {
  index : number;
  constructor(public dialogRef : MatDialogRef<ImagesDialogComponent>,@Inject(MAT_DIALOG_DATA) public data: any) { }

  ngOnInit(): void {
    this.index = 0;
  }

  next(){
    this.index = (this.index + 1)%this.data.images.length;
  }
  prev(){
    this.index = (this.index - 1 + this.data.images.length)%this.data.images.length;
  }

}
