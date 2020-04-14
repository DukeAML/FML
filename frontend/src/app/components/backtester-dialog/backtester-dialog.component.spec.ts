import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { BacktesterDialogComponent } from './backtester-dialog.component';

describe('BacktesterDialogComponent', () => {
  let component: BacktesterDialogComponent;
  let fixture: ComponentFixture<BacktesterDialogComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ BacktesterDialogComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(BacktesterDialogComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
