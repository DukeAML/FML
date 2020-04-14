import { Component, OnInit } from '@angular/core';
import { DataService } from '../../services/data.service'
import { MatProgressSpinner } from '@angular/material';

@Component({
  selector: 'app-top-tickers',
  templateUrl: './top-tickers.component.html',
  styleUrls: ['./top-tickers.component.css']
})
export class TopTickersComponent implements OnInit {

  highlights:any[]
  loaded:boolean = false;

  constructor(private dataService:DataService) { }

  ngOnInit() {

    this.dataService.getTopIndicators().subscribe( result => {
      this.loaded = true;
      console.log('result', result)
      this.highlights = result['data'];
    })
  }

}
