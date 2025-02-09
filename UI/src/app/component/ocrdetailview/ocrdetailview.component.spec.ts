import { ComponentFixture, TestBed } from '@angular/core/testing';

import { OcrdetailviewComponent } from './ocrdetailview.component';

describe('OcrdetailviewComponent', () => {
  let component: OcrdetailviewComponent;
  let fixture: ComponentFixture<OcrdetailviewComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ OcrdetailviewComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(OcrdetailviewComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
