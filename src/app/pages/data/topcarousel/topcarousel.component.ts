import { Component, Input, OnInit } from '@angular/core';
import { HttpService } from 'src/app/services/http.service';
import { DataService } from 'src/app/services/data.service';
declare var Swiper: any;
@Component({
  selector: 'app-topcarousel',
  templateUrl: './topcarousel.component.html',
  styleUrls: ['./topcarousel.component.scss']
})
export class TopcarouselComponent implements OnInit {
  @Input() images;
  constructor(private api: HttpService,
              private ds: DataService) { }

  ngOnInit(): void {
  }

  ngAfterViewInit(){
    this.createSwiper();
  }

  createSwiper(){
    var swiper = new Swiper('.swiper-container-top', {
      observer: true,
      observeParents: true,
      allowTouchMove: false,
      spaceBetween: 40,
      pagination: {
        el: '.swiper-pagination-top',
        type: 'fraction',
      },
      navigation: {
        nextEl: '.swiper-button-next-top',
        prevEl: '.swiper-button-prev-top',
      },
      centeredSlides: true,
      slidesPerView: 2,
      effect: 'coverflow',
      noSwiping: false,
      loop : false
      
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

}
