import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { BacktesterComponent } from './backtester.component';

describe('BacktesterComponent', () => {
  let component: BacktesterComponent;
  let fixture: ComponentFixture<BacktesterComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ BacktesterComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(BacktesterComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
