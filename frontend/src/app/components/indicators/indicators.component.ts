import { Component, OnInit, Input } from '@angular/core';

@Component({
  selector: 'app-indicators',
  templateUrl: './indicators.component.html',
  styleUrls: ['./indicators.component.css']
})
export class IndicatorsComponent implements OnInit {
  constructor() { }

  @Input() equity: string;
  indicators:string[] = [
    "Volumes",
    "Prices",
    "SMA",
    "EMA",
    "Wilder MA",
    "Upper Bolinger Band",
    "Lower Bolinger Band",
    "Accumulative Swing Index",
    "Average True Range",
    "Balance of Power",
    "Gopalakrishnan Range Index",
    "Pivot Point",
    "Pring's Know Sure Thing",
    "MACD - SMA(MACD)",
    "d KST * d TRIX",
    "TRIX - MA(TRIX)",
    "RSI",
    "MA OHLC 4 1",
    "MA OHLC 4 3",
    "MA OHLC 4 5",
    "MA OHLC 4 7",
    "MA OHLC 4 9",
    "West Texas",
    "Wilshire US Real Estate",
    "SNP"]

  ngOnInit() {
  }
  

}
