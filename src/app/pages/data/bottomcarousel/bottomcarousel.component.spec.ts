import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { BottomcarouselComponent } from './bottomcarousel.component';

describe('BottomcarouselComponent', () => {
  let component: BottomcarouselComponent;
  let fixture: ComponentFixture<BottomcarouselComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ BottomcarouselComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(BottomcarouselComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
