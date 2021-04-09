import { Component, OnInit, ViewEncapsulation } from '@angular/core';
import { FormBuilder } from '@angular/forms';
import { HttpService } from 'src/app/services/http.service';
@Component({
  selector: 'app-upload',
  templateUrl: './upload.component.html',
  styleUrls: ['./upload.component.scss'],
})
export class UploadComponent implements OnInit {
  displaySrc;
  progress;
  error = null;
  transform_box = false;
  selected_label;
  labels: any[] = [];
  no_label_selected:boolean= false;
  imageUploaded: any[] = [];
  uploading = false;
  newlabel = false;
  constructor(private formBuilder: FormBuilder, private api: HttpService) { }

  ngOnInit(): void {
      this.api.get(`${this.api.host}/api/labels/`).subscribe((res)=>this.labels=res.data, (err) => console.log(err));
  }

  files: any[] = [];
  filesCopy: any[] = [];
  onSelect(event) {
    this.files.push(...event.addedFiles);
    console.log(this.files);
    this.imageUploaded = Array(this.files.length).fill(false);
    this.filesCopy = [];
    this.uploading = false;
  }

  onRemove(event) {
    console.log(event);
    this.files.splice(this.files.indexOf(event), 1);
  }

  clicked(event){
    let element = event.target.parentNode;
    // index is the index in files array 
    let index = [].indexOf.call(element.parentNode.children, element)-1;
    this.displaySrc = event.target.src;
    console.log(this.selected_label);
  }

  async getBase64(file): Promise<string> {
    let reader = new FileReader();

    return new Promise((resolve,reject)=>{
      reader.readAsDataURL(file);
      reader.onload = function () {
        resolve(reader.result as string);
      };
      reader.onerror = function (error) {
        reject(`error: ${error}`);
      };
    })
 }

  async submit(){
    this.progress = 0;
    let count = 0;
    if(this.selected_label == null || this.selected_label == ""){
      alert("Select a label");
      return;
    }
    this.uploading = true;
    this.filesCopy = this.files;
    let uploaded = -1;
    for(var i=0; i<this.files.length; i++){
      const formData = new FormData();
      let b64: string = await this.getBase64(this.files[i]);
      this.files[i]["src"] = b64;
      formData.append('b64',b64);
      formData.append('image_class', `${this.selected_label}`);
      formData.append('labels', `original`);
      this.api.post(formData, `${this.api.url}`).subscribe(
        (res) =>{
          console.log(res);
          count+=1;
          this.progress = count/this.files.length*100;
          console.log(this.progress);
          if(count == this.files.length){
            this.files = [];
            // window.location.reload();
          }
          uploaded+=1;
          this.imageUploaded[uploaded] = true;
          console.log(this.imageUploaded);
        },
        (err) =>{
          console.log(err);
          if(this.error == null){
            this.error = `${i}`;
          }
          else this.error += `, ${i}`;
        }
      )      
    }
  }

  transform(){
    this.transform_box = true;
  }

  selectLabel(val){
      this.selected_label = val;
      this.no_label_selected = false;
  }

  floor(x){
    return Math.floor(x);
  }

  newLabel(val, _label = ""){
      console.log("label",_label);
      if(_label === "") return;
      let formData = new FormData();
      formData.append('label', _label);
      this.api.post(formData, `${this.api.host}/api/labels/`)
      .subscribe(
          (res)=>{
            this.labels = res.data;
          },
          (err) => console.log(err),
      )
  }
}
