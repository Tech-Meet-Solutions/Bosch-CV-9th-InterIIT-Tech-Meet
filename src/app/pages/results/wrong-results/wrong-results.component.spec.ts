import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { WrongResultsComponent } from './wrong-results.component';

describe('WrongResultsComponent', () => {
  let component: WrongResultsComponent;
  let fixture: ComponentFixture<WrongResultsComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ WrongResultsComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(WrongResultsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
