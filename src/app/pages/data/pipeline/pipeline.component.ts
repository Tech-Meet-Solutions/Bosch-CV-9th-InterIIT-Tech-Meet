import { Component, OnInit } from '@angular/core';
import { DomSanitizer } from '@angular/platform-browser';
import { HttpService } from 'src/app/services/http.service';

@Component({
  selector: 'app-pipeline',
  templateUrl: './pipeline.component.html',
  styleUrls: ['./pipeline.component.scss']
})
export class PipelineComponent implements OnInit {

  constructor(private api: HttpService,
              private sanitizer: DomSanitizer) { }
  imageSrc;
  socket;
  socketmessage: string;
  ngOnInit(): void {
    // let filename = 'file.png';
    // this.api.get(`${this.api.host}/api/pipeline/${filename}/`)
    //       .subscribe(
    //         (res)=>{
    //         this.imageSrc = this.sanitizer.bypassSecurityTrustUrl(res.data);
    //       },
    //       (err) => console.log(err)
    //       )
    // this.initialiseSocket();
  }

  initialiseSocket(){
    let w = new WebSocket("ws://0.0.0.0:5000");
    w.onopen  = (data) => {
      this.socket = w;
      console.log("opened: ", data);
      w.send("hello world form angular");
    };
    w.onmessage = (data) => {
        // this.socketmessages.push(data.data);
        this.socketmessage = data.data;
    }
  }

  ngOnDestroy(){
    // console.log("Ondestroy");
    // this.socket.send("Closing...");
    // // 1000 represents status code OK
    // this.socket.close(1000);
  }

}
