import { Component, ElementRef, OnDestroy, OnInit, ViewChild } from '@angular/core';
import { Subscription } from 'rxjs';
import { DataService } from 'src/app/services/data.service';
import { HttpService } from 'src/app/services/http.service';
import { Result, ResultName } from '../result.interface';
import { ResultService } from '../results.service';
import { Suggestion } from './suggestions.interface';

@Component({
  selector: 'app-suggestions',
  templateUrl: './suggestions.component.html',
  styleUrls: ['./suggestions.component.scss']
})
export class SuggestionsComponent implements OnInit, OnDestroy {

  constructor(private resultService: ResultService, private api: HttpService, private data: DataService) { }

  subscription: Subscription;
  suggestion: Suggestion;
  scroll_length = 0;
  dataSource;
  displayedColumns: string[] = ["class_name", "precision", "recall", "accuracy", "f1"];

  @ViewChild("carousel")
  carousel: ElementRef<HTMLDivElement>;

  ngOnInit(): void {
    this.subscription = this.resultService.resultChanged$.subscribe(
      result => {
        console.log(result);
        this.get_result(result);
      }
    )
    if (this.data.selected_result != undefined) {
      this.get_result(this.data.selected_result);
    }
  }

  get_result(result: ResultName){
    console.log("Here")
    this.api.get(this.api.host + "/api/getsuggestions", {net_name: result.net_name, result_name: result.result_name})
    .subscribe (
      response => {console.log(response);
        this.suggestion = response;
        this.dataSource = response["final_table"]
      },
      error => {console.log(error)}
    );
  }

  move(dir: string){
    if (dir == 'right') this.scroll_length += 450;
    else this.scroll_length -= 450;
    if (this.scroll_length < 0) this.scroll_length = 0;
    if (this.scroll_length > this.carousel.nativeElement.scrollWidth - this.carousel.nativeElement.clientWidth) this.scroll_length = this.carousel.nativeElement.scrollWidth - this.carousel.nativeElement.clientWidth;
    this.carousel.nativeElement.scrollLeft = this.scroll_length;
  }

  ngOnDestroy(){
    this.subscription.unsubscribe();
  }

}
