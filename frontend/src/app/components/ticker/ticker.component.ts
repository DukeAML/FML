import { Component, Input, OnInit } from '@angular/core';
import { DataService } from '../../services/data.service';

@Component({
  selector: 'app-ticker',
  templateUrl: './ticker.component.html',
  styleUrls: ['./ticker.component.css']
})
export class TickerComponent implements OnInit {

  @Input() assetName:string;
  @Input() percentChange:string;
  @Input() type:string;
  data:any[];


  constructor(private dataService:DataService) { }

  ngOnInit() {
    if(this.type == 'bottom'){
      this.lineColorScheme = {
        domain: ['#A10A28']
      };

    }
    this.dataService.getAssetValueOverTime(this.assetName, '5d').subscribe(result => {
      this.data = result['data'];
    })

  }

  // GRAPH FORMAT OPTIONS
  lineShowLabels: boolean = false;
  lineAnimations: boolean = false;
  lineLegendPosition: string = "right";
  lineXaxis: boolean = true;
  lineYaxis: boolean = true;
  lineShowYAxisLabel: boolean = false;
  lineShowXAxisLabel: boolean = false;
  lineXaxisLabel: string = 'Days Since Last Month';
  lineYaxisLabel: string = 'Value';
  lineTimeline: boolean = false;

    
  view: any[] = [150, 100];
  
  lineColorScheme = {
    domain: ['#5AA454']
  };

  lineOnSelect(data): void {
    // console.log('Item clicked', JSON.parse(JSON.stringify(data)));
  }

  lineOnActivate(data): void {
    // console.log('Activate', JSON.parse(JSON.stringify(data)));
  }

  lineOnDeactivate(data): void {
    // console.log('Deactivate', JSON.parse(JSON.stringify(data)));
  }

}
