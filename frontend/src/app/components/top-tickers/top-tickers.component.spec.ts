import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { TopTickersComponent } from './top-tickers.component';

describe('TopTickersComponent', () => {
  let component: TopTickersComponent;
  let fixture: ComponentFixture<TopTickersComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ TopTickersComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(TopTickersComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
