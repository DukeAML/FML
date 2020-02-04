import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { PerformancePaneComponent } from './performance-pane.component';

describe('PerformancePaneComponent', () => {
  let component: PerformancePaneComponent;
  let fixture: ComponentFixture<PerformancePaneComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ PerformancePaneComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(PerformancePaneComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
