import { Component, Input, OnInit } from '@angular/core';
import { HttpService } from 'src/app/services/http.service';
import { DataService } from 'src/app/services/data.service';
declare var Swiper: any;

@Component({
  selector: 'app-bottomcarousel',
  templateUrl: './bottomcarousel.component.html',
  styleUrls: ['./bottomcarousel.component.scss'],
})
export class BottomcarouselComponent implements OnInit {
  @Input() images;
  @Input() max_id;
  selectedImages:any[] = [];
  constructor(private api: HttpService, private ds: DataService) { }

  ngOnInit(): void {
    console.log(this.images);
    console.log(this.max_id);
    this.selectedImages = Array(this.max_id).fill(false); 
  }

  ngAfterViewInit(){
    this.createSwiper();
  }

  createSwiper(){
    var swiper = new Swiper('.swiper-container-bottom', {
      observer: true,
      observeParents: true,
      slidesPerView: 8,
      spaceBetween: 20,
      freeMode: false,
      pagination: {
        el: '.swiper-pagination-bottom',
        clickable: true,
      },
      navigation: {
        nextEl: '.swiper-button-next-bottom',
        prevEl: '.swiper-button-prev-bottom',
      },
    });
  }


  // getImages(){
  //   this.api.get(`${this.api.host}/api/images/`).subscribe(
  //     (res) =>{
  //       this.images = res;
  //       this.createSwiper();
  //     },
  //     (err) => {
  //       console.log(err);
  //     }
  //   )
  // }

  select(event){
    let target:any = $(event.target);
    let id = target.attr("id");
    this.selectedImages[id] = !this.selectedImages[id]; 
    console.log(this.selectedImages);
  }
  
}
