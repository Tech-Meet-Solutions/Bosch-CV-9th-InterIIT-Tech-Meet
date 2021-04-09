import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { forkJoin, Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class HttpService {
  url: string = "http://127.0.0.1:8000/api/images/";
  host: string = "http://0.0.0.0:8000";
  sock_host: string = "ws://0.0.0.0:5000";
  // url: string = "https://interiit.moodi.org/api/images/";
  // host: string = "https://interiit.moodi.org"
  constructor(private http: HttpClient) { }

  post(formData, url = this.url) {
    return this.http.post<any>(`${url}`, formData);
  }

  delete(url){
    return this.http.delete(url);
  }

  get(url, params={}){
    return this.http.get<any>(url, {params: params});
  }

  postMany(data : any[],url = this.url){
    let postArr: Observable<any>[] = []; 
    data.forEach((val)=>{
      delete val["id"];
      postArr.push(this.http.post(url,val));
    });

    return forkJoin(postArr);
  }
  putMany(data,url = this.url){
    let putArr: Observable<any>[] = []; 
    data.forEach((val)=>{
      let id = val["id"];
      delete val["id"];
      putArr.push(this.http.put(url+id+'/',val));
    });

    return forkJoin(putArr);
  }
}
