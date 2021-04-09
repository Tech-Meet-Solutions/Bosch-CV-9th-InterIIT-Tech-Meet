import { AfterViewInit, Component, Input, OnInit } from '@angular/core';
import { Router } from '@angular/router';

declare var Swiper : any;
@Component({
  selector: 'app-carousel',
  templateUrl: './carousel.component.html',
  styleUrls: ['./carousel.component.scss']
})
export class CarouselComponent implements OnInit, AfterViewInit {

  @Input() images : any[];
  constructor(private router : Router) { }

  ngOnInit() {
      console.log(this.images);
      // this.getImageBlob(this.images[0].b64);

  }

//   async getImageBlob(b64){
//     let img = await (await fetch(b64)).blob();
//     this.addImage(img);
//   }

//   addImage(file) {
//     var reader = new FileReader();
//     reader.onload = (event)=>{
//         var img:any = new Image();
//         img.onload = () =>{
//             this.cropImage(img);
//         }
//         img.src = event.target.result;
//     }
//     reader.readAsDataURL(file);
// }

//   cropImage(originalImage) {

//       $(originalImage).attr('id', 'fullImage');
//       $('#imageResize').html(originalImage);
//       $('#sectionDragAndDrop').addClass('hidden');
//       $('#sectionResize').removeClass('hidden');

//       // var newImage = new imageCrop('#fullImage', 200, 200);

//       // var results = newImage.crop();
//       // $('#thumbnail').html(results.img);
//       // $('#sectionResize').addClass('hidden');
//       // $('#sectionThumbnail').removeClass('hidden');

//   }
  getImageDimensions(file) {
    return new Promise (function (resolved, rejected) {
      var i = new Image()
      i.onload = function(){
        resolved({w: i.width, h: i.height})
      };
      i.src = file
    })
  }

  // updateCrop(){
  //   this.getImageDimensions(this.images[0].b64).then((val:any)=>{
  //     console.log(val);
  //     $('#crop-select').width(val.w);
  //     $('#crop-select').height(val.h);
  //     (<any>$('#crop-select')).CropSelectJs({
  //       animatedBorder: true,
  //       aspectRatio:null,
      
  //       // Image
  //       imageSrc: this.images[0].b64,
  //       imageWidth: val.w,
  //       imageHeight: val.h,
      
  //       // Stub events
  //       selectionResize: function(data) {
  //         console.log(data)
  //       },
  //       selectionMove: function(data) {
  //         console.log(data)
  //       },
  //     });
  //   });
    
  // }

  ngAfterViewInit() : void{
      this.makeGallery();
    
  }

  makeGallery(){
    var galleryThumbs = new Swiper('#galleryThumbs', {
      observer: true,
      observeParents: true,
      spaceBetween: 10,
      slidesPerView: 4,
      loop: false,//looped slides should be the same
      watchSlidesVisibility: true,
      watchSlidesProgress: true,
    });
    var galleryTop = new Swiper('#galleryTop', {
      effect: 'coverflow',
      observer: true,
      observeParents: true,
      allowTouchMove: false,
      spaceBetween: 10, //looped slides should be the same
      navigation: {
        nextEl: '.swiper-button-next',
        prevEl: '.swiper-button-prev',
      },
      thumbs: {
        swiper: galleryThumbs,
      },
      centeredSlides : true,
    });
  }

}
