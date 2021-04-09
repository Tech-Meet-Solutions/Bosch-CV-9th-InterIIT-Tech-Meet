import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-data',
  templateUrl: './data.component.html',
  styleUrls: ['./data.component.scss']
})
export class DataComponent implements OnInit {
  background = undefined;
  links = [
    {
      name : 'Upload',
      icon : 'add_photo_alternate',
      link : 'upload',
    },
    {
      name : 'Edit and Transform',
      icon : 'Collections',
      link : 'gallery',
    },
    {
      name : 'Visualize',
      icon : 'trending_up',
      link : 'visualize',
    }
  ]
  constructor(private router : Router) { }

  ngOnInit(): void {
  }

}
