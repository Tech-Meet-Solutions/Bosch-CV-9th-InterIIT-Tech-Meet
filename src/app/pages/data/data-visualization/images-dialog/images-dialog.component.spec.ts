import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ImagesDialogComponent } from './images-dialog.component';

describe('ImagesDialogComponent', () => {
  let component: ImagesDialogComponent;
  let fixture: ComponentFixture<ImagesDialogComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ImagesDialogComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ImagesDialogComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
