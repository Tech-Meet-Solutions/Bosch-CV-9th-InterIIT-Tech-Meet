import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class VisualizationService {
  image_url : string = "http://localhost:8000/api/data_viz/"
  label_url : string = "http://localhost:8000/api/data_viz/"
  constructor(private http : HttpClient) { }

  getImages(Class : string, num : number){
    return this.http.get(this.image_url,{
      params :{
        class : Class,
        num : "" + num
      }
    })
  }

  getClasses(){
    return this.http.get(this.label_url)
  }
}
