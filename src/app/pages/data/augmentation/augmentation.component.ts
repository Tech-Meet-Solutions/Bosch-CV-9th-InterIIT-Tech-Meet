import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { Transforms } from 'src/app/interfaces/transforms.interface';
import { HttpService } from 'src/app/services/http.service';
import { TransformService } from 'src/app/services/transform.service';
import { DataService } from 'src/app/services/data.service';

@Component({
  selector: 'app-augmentation',
  templateUrl: './augmentation.component.html',
  styleUrls: ['./augmentation.component.scss']
})
export class AugmentationComponent implements OnInit {
  images : any;
  max_id : number;
  constructor(private ds:DataService, private transformService : TransformService, private httpService : HttpService, private router : Router) { }

  ngOnInit(): void {
    this.images = this.ds.selectedImages;
    this.max_id = this.ds.maxid;
    if (!this.images || this.images.length == 0)
    this.router.navigateByUrl('/pages/data/gallery');
  }

  getTransformed(transforms : Transforms){
    console.log("In get transformed")
    let data = {};
    data["transforms"] = transforms;
    data["ids"] = this.ds.selectedImages.map((e)=>e.id);
    this.transformService.getTransformData(data).subscribe((data : any)=>{
      console.log(data);
      this.images = data.images;
      console.log(this.images);
    });
  }

  save(event : any){
    console.log(event);
    if(event == 'inplace')
    {
      this.httpService.putMany(this.images).subscribe(data =>{
        console.log(data);
        this.router.navigateByUrl('/pages/data/gallery');
      },err =>{
        console.error(err);
      });
    }
    else if(event == 'duplicate')
    {
      this.httpService.postMany(this.images).subscribe(data =>{
        console.log(data);
        this.router.navigateByUrl('/pages/data/gallery');
      },err =>{
        console.error(err);
      });
    }
  }

}
