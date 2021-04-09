import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { AugmentationComponent } from './augmentation.component';

describe('AugmentationComponent', () => {
  let component: AugmentationComponent;
  let fixture: ComponentFixture<AugmentationComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ AugmentationComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(AugmentationComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
