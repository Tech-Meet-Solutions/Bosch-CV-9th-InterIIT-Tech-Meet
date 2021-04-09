import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { HttpService } from 'src/app/services/http.service';
import { DataService } from 'src/app/services/data.service';
import { MatDialog, MatDialogConfig } from '@angular/material/dialog';
import { CropComponent } from '../crop/crop.component';
import { TransformService } from 'src/app/services/transform.service';
import { Transforms } from 'src/app/interfaces/transforms.interface';
import { defaults } from '../controls/transforms.default';
import { ViewEncapsulation } from '@angular/core';
declare var $: any;
@Component({
  selector: 'app-gallery',
  templateUrl: './gallery.component.html',
  styleUrls: ['./gallery.component.scss'],
  encapsulation: ViewEncapsulation.None,
})
export class GalleryComponent implements OnInit {
  // images currently being shown on frontend
  images:any[] = [];
  labels:any[] = [];
  // all images received from backend
  imagesAll:any[] = [];
  // filter parameters
  selected_label = '';
  time_filterval = 0;
  transformedOnly = false;

  // images that are selected currently have a value true corresponding to their id
  selectedImages:boolean[] = [];
  constructor(private api: HttpService,
              private ds: DataService,
              private transformService : TransformService,
              private httpService : HttpService,
              private router: Router,
              private matDialog : MatDialog) { }

  ngOnInit(): void {
    this.getImages();
    this.api.get(`${this.api.host}/api/labels/`).subscribe((res)=>this.labels = res.data, (err)=> console.log(err));
  }

  /*
    fetch images from backend
    maxid used to set length of selectedImages array for indexing
    ds.maxid stores maxid in dataservice
  */
  getImages(link = `${this.api.host}/api/images/`){
      this.api.get(link).subscribe(
        (res) =>{
          console.log(res);
          let maxid = Math.max.apply(Math, res.results.map(function(o){return o.id}));
          this.ds.maxid = maxid;
          this.selectedImages = Array(maxid+2).fill(false);
          this.images = this.images.concat(res.results);
          this.imagesAll = this.images;
          if(res['next']!=null) this.getImages(res['next']);
        },
        (err) => {
          console.log(err);
        }
      )
  }

  /*
      Marks an image with blue circle on being selected or unselected
  */  
  select(event){
    let target:any = $(event.target);
    let id = target.attr("id");
    this.selectedImages[id] = !this.selectedImages[id]; 
  }

  /*
    Navigate to transformations page with the selected images
  */  
  sendSelectedImages(){
    let selectedImages = this.images.filter(i => this.selectedImages[i.id]);
    if(selectedImages.length === 0) {alert("No Images Selected"); return;}
    this.ds.selectedImages = selectedImages;
    this.router.navigate(["/pages/data/transformation"]);
  }

  /*
      Delete selected images from backend
  */
  deleteSelectedImages(){
    let selectedImages = [...this.selectedImages.keys()].filter(i=> this.selectedImages[i]);
    if(selectedImages.length === 0) {alert("No Images Selected"); return;}
    selectedImages.forEach((id)=>{
      this.api.delete(`${this.api.host}/api/images/${id}/`).subscribe(
        (res)=>{
          console.log(`Deleted Image number : ${id}`);
        },
        (err)=>{
          console.log(`Couldn't delete Image number : ${id}`);
        }
      )
    });
    window.location.reload();
  }

  /*
      Select all the images (imagesAll)
  */
  selectAll(){
    this.images.forEach((img)=>{
      this.selectedImages[img.id] = true;
    })
  }

  /*
      Filter images based on their labels, with the text entered on the search bar
  */
  filterImages(val){
    if(val == "none") val = "";
    this.selected_label = val;
    this.filterCombined(this.selected_label, this.time_filterval, this.transformedOnly);
  }

  /*
      returns the number of images currently selected
  */
  numTrue(){
    return this.selectedImages.filter(Boolean).length;
  }

  filterTime(_val){
    if(_val === "Last Hour") this.time_filterval = 3600;
    else if(_val === "Last Day") this.time_filterval = 86400;
    else this.time_filterval = 0;
    this.filterCombined(this.selected_label, this.time_filterval,this.transformedOnly );
  }

  filterTransformed(_switch){
      this.transformedOnly = !this.transformedOnly;
      this.filterCombined(this.selected_label, this.time_filterval, _switch);
  }

  filterCombined(_class, _time, _transformedOnly = false){
    let isInTimeLimits = (lastedit, _time) =>{
      var date:any = new Date();
      var idate:any = new Date(lastedit);
      var diff = (date-idate)/1000;
      if(diff < _time || _time == 0){ 
          return true;
      }
      return false;
    };
    if(_class == "") this.images = this.imagesAll.filter(i=> isInTimeLimits(i.lastedit, _time) && (!_transformedOnly || i.labels.trim().toLowerCase() != "original") );
    else this.images = this.imagesAll.filter(i=> (i.image_class.trim().toLowerCase().includes(_class.trim().toLowerCase()) && isInTimeLimits(i.lastedit, _time) && (!_transformedOnly || i.labels.trim().toLowerCase() != "original")));
  }
  
  openCrop(image : any){

    const dialogConfig = new MatDialogConfig();
    dialogConfig.data = {
      title : 'Crop',
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
      ],
      image : image,
      backdropClass: 'backdropBackground' ,
    }
    let dialogRef = this.matDialog.open(CropComponent, dialogConfig);
    dialogRef.afterClosed().subscribe((msg)=>{
      console.log(msg)
      let transforms : Transforms = JSON.parse(JSON.stringify(defaults));
      transforms.cropX = msg.xy.xScaledToImage;
      transforms.cropY =  msg.xy.yScaledToImage;
      transforms.cropW =  msg.wh.widthScaledToImage;
      transforms.cropH = msg.wh.heightScaledToImage;
      this.transformService.getTransformData({ids: [msg.id],transforms : transforms}).subscribe((data : any)=>{
        console.log(data);
        if(msg.action == 'inplace')
        {
          this.httpService.putMany(data.images).subscribe(data =>{
            console.log(data);
            this.images = [];
            this.getImages();
          },err =>{
            console.error(err);
          });
        }
        else if(msg.action == 'duplicate')
        {
          this.httpService.postMany(data.images).subscribe(data =>{
            console.log(data);
            this.images = [];
            this.getImages();
          },err =>{
            console.error(err);
          });
        }
      })
    });
  }
}
