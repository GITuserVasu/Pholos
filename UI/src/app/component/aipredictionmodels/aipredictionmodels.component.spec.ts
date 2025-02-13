import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AIpredictionmodelsComponent } from './aipredictionmodels.component';

describe('AIpredictionmodelsComponent', () => {
  let component: AIpredictionmodelsComponent;
  let fixture: ComponentFixture<AIpredictionmodelsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ AIpredictionmodelsComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(AIpredictionmodelsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});