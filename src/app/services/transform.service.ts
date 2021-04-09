import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { TransformData } from '../interfaces/transformData.interface';
import { Transforms } from '../interfaces/transforms.interface';

@Injectable({
  providedIn: 'root'
})
export class TransformService {
  //url : string = "https://interiit.moodi.org/api/transform"
  url : string = "http://localhost:8000/api/transform"
  constructor(private http : HttpClient) { }

  getTransformData(transforms){
    return this.http.post<TransformData>(this.url,transforms);
  }
}
