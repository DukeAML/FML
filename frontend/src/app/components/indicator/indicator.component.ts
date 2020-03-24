import { Component, OnInit, Input } from '@angular/core';
import { DataService } from '../../services/data.service';


@Component({
  selector: 'app-indicator',
  templateUrl: './indicator.component.html',
  styleUrls: ['./indicator.component.css']
})
export class IndicatorComponent implements OnInit {
  
  constructor(private dataService:DataService) { }

  
  @Input() equity: string;
  @Input() indicatorName:string;
  data:any;

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

    
  view: any[] = [75, 50];
  
  lineColorScheme = {
    domain: ['#5AA454', '#A10A28', '#C7B42C', '#AAAAAA']
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

  ngOnInit() {
    console.log('indicator name in indicator is', this.indicatorName);
    // add parameter for equity
    this.dataService.getIndicatorValue(this.indicatorName).subscribe(result => {
      console.log('result in component', result);
      this.data = result['data']
    })
    // subscribe to data and set it here
    // set lineColorScheme;
  }

}
