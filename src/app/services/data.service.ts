import { Injectable } from '@angular/core';
import { Result } from '../pages/results/result.interface';

@Injectable({
  providedIn: 'root'
})
export class DataService {

  constructor() { }
  selectedImages;
  maxid;
  embd_result: Result;
  selected_result;
}
