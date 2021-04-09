import { Component, OnInit, AfterViewInit, Input, Output, EventEmitter, ViewChild, ElementRef} from '@angular/core';
import * as $ from 'jquery';
@Component({
  selector: 'app-custom-dropdown',
  templateUrl: './custom-dropdown.component.html',
  styleUrls: ['./custom-dropdown.component.scss']
})
export class CustomDropdownComponent implements OnInit {

  constructor() { }
  @Input() label = "Label";
  @Input()
  labels;
  @Input()
  newField: boolean = false;
  @Output()
  currentLabel = new EventEmitter<string>();
  @Output()
  add = new EventEmitter<string>();


  @ViewChild('DropBtn') dropBtn : ElementRef;
  @ViewChild('DropdownContent') dropdownContent : ElementRef;
  @ViewChild('InputA') inputA : ElementRef;
  @ViewChild('LabelLink') labelLink : ElementRef;
  @ViewChild('newlabel') newLabel : ElementRef;

  ngOnInit(): void {
  }
  

  ngAfterViewInit(){
      this.jqueryStuff();
  }

  setLabel(label){
      this.label = label;
      this.currentLabel.emit(label);
  }

  addNewLabel(val){
    this.label = val;
    this.newLabel.nativeElement.value = "";
    this.add.emit(val);
  }

  jqueryStuff(){
    // this.dropdownContent.nativeElement.on('mouseover',()=>{
    //   this.dropBtn.nativeElement.classList.add('hovered')
    //   }
    // );

    // this.dropdownContent.nativeElement.on('mouseleave',function(){
    //   this.dropBtn.nativeElement.classList.remove('hovered')
    // });

    // this.dropBtn.nativeElement.on('mouseover', function(){
    //   this.dropBtn.nativeElement.classList.add('hovered');
    // });

    // this.dropBtn.nativeElement.on('mouseleave', function(){
    //   this.dropBtn.nativeElement.classList.remove('hovered')
    // });
    // this.inputA.nativeElement.on('mouseover',()=>{this.newLabel.nativeElement.classList.add('hovered')});
    // this.inputA.nativeElement.on('mouseleave',()=>{this.newLabel.nativeElement.classList.remove('hovered')});
    // this.labelLink.nativeElement.on('click', ()=>this.dropdownContent.nativeElement.style.display ="none");
  }
}
