import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-pages',
  templateUrl: './pages.component.html',
  styleUrls: ['./pages.component.scss']
})
export class PagesComponent implements OnInit {
  links = [
    {
      name : 'Home',
      icon : 'my_logo',
      link : '/pages/home',
    },
    {
      name : 'Data',
      icon : 'my_data',
      link : '/pages/data',
    },
    {
      name : 'Network',
      icon : 'my_network',
      link : '/pages/network',
    },
    {
      name : 'Results',
      icon : 'my_results',
      link : '/pages/results',
    }
  ]
  constructor() { }

  ngOnInit(): void {
  }

}
