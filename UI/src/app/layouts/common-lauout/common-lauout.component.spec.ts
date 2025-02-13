import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CommonLauoutComponent } from './common-lauout.component';

describe('CommonLauoutComponent', () => {
  let component: CommonLauoutComponent;
  let fixture: ComponentFixture<CommonLauoutComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ CommonLauoutComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(CommonLauoutComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
