import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { TopcarouselComponent } from './topcarousel.component';

describe('TopcarouselComponent', () => {
  let component: TopcarouselComponent;
  let fixture: ComponentFixture<TopcarouselComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ TopcarouselComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(TopcarouselComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
