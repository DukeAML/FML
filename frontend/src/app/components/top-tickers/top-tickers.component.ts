import { Component, OnInit } from '@angular/core';
import { DataService } from '../../services/data.service'

@Component({
  selector: 'app-top-tickers',
  templateUrl: './top-tickers.component.html',
  styleUrls: ['./top-tickers.component.css']
})
export class TopTickersComponent implements OnInit {

  highlights:any[]

  constructor(private dataService:DataService) { }

  ngOnInit() {

    // this.highlights = [{'asset': "NOW", 'percentChange': -3.9257333284505695, 'type': "bottom"},
    // {'asset': "CVS", 'percentChange': -2.519712032910535, 'type': "bottom"},
    // {'asset': "GE", 'percentChange': -0.1420454545454515, 'type': "bottom"},
    // {'asset': "OIL", 'percentChange': 16.35514018691589, 'type': "top"},
    // {'asset': "MS", 'percentChange': 16.824794433902582, 'type': "top"},
    // {'asset': "CVX", 'percentChange': 18.028004667444574, 'type': "top"}]
    this.dataService.getTopIndicators().subscribe( result => {
      console.log('result', result)
      this.highlights = result['data'];
    })
  }

}
