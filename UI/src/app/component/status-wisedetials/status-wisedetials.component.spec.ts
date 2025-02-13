import { ComponentFixture, TestBed } from '@angular/core/testing';

import { StatusWisedetialsComponent } from './status-wisedetials.component';

describe('StatusWisedetialsComponent', () => {
  let component: StatusWisedetialsComponent;
  let fixture: ComponentFixture<StatusWisedetialsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ StatusWisedetialsComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(StatusWisedetialsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
