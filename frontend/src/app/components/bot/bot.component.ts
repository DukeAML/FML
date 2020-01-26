import { Component, OnInit } from '@angular/core';
import { DataService } from '../../services/data.service';

import { NgxChartsModule } from '@swimlane/ngx-charts';

@Component({
  selector: 'app-bot',
  templateUrl: './bot.component.html',
  styleUrls: ['./bot.component.css']
})
export class BotComponent implements OnInit {

  constructor(private dataService:DataService) { 
    this.getData();
  }

  single: any[];
  multi: any[]
  view: any[] = [600, 400];

  colorScheme = {
    domain: ['#5AA454', '#A10A28', '#C7B42C', '#AAAAAA']
  };

  // options
  pieGradient: boolean = true;
  pieShowLegend: boolean = false;
  pieShowLabels: boolean = true;
  pieIsDoughnut: boolean = false;
  pieLegendPosition: string = 'below';
  pieTrimLabels: boolean = false;

  lineLegend: boolean = true;
  lineShowLabels: boolean = true;
  lineAnimations: boolean = true;
  lineLegendPosition: string = "right";
  lineXaxis: boolean = true;
  lineYaxis: boolean = true;
  lineShowYAxisLabel: boolean = true;
  lineShowXAxisLabel: boolean = true;
  lineXaxisLabel: string = 'Days Since Inception';
  lineYaxisLabel: string = '% Allocation';
  lineTimeline: boolean = true;



  ngOnInit() {
  }

  getData(): void{
    this.dataService.getAssetTypeAllocation().subscribe( result => {
      this.single = result;
    })

    this.dataService.getAssetAllocationOverTime().subscribe( result => {
      this.multi = result['data'];
    })
  }


  // INTERACTIVE FUNCTIONS?
  pieOnSelect(data): void {
    console.log('Item clicked', JSON.parse(JSON.stringify(data)));
  }

  pieOnActivate(data): void {
    console.log('Activate', JSON.parse(JSON.stringify(data)));
  }

  pieOnDeactivate(data): void {
    console.log('Deactivate', JSON.parse(JSON.stringify(data)));
  }

  lineOnSelect(data): void {
    console.log('Item clicked', JSON.parse(JSON.stringify(data)));
  }

  lineOnActivate(data): void {
    console.log('Activate', JSON.parse(JSON.stringify(data)));
  }

  lineOnDeactivate(data): void {
    console.log('Deactivate', JSON.parse(JSON.stringify(data)));
  }

}
