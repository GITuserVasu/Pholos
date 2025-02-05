import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ComprehendComponent } from './comprehend.component';

describe('ComprehendComponent', () => {
  let component: ComprehendComponent;
  let fixture: ComponentFixture<ComprehendComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ComprehendComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ComprehendComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
