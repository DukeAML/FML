import { Component, OnInit } from '@angular/core';
import { DataService } from '../../services/data.service';
import { NgxChartsModule } from '@swimlane/ngx-charts';
import { MatSlider } from '@angular/material';


@Component({
  selector: 'app-performance-pane',
  templateUrl: './performance-pane.component.html',
  styleUrls: ['./performance-pane.component.css']
})
export class PerformancePaneComponent implements OnInit {

  stats:any[]
  mostRecentDay:number;
  
  constructor(private dataService:DataService) { 
  }

  ngOnInit() {
    this.getData();
  }

  getData(){
    this.dataService.getMostRecentDay().subscribe(result => {
      this.mostRecentDay = result['day'];

      this.dataService.getPerformanceStats(this.mostRecentDay).subscribe(result => {
        this.stats = result['data'];
      })
    })
  }

  getPerformanceStats($event){
    let day = $event['value'];
    this.dataService.getPerformanceStats(day).subscribe( result => {
      this.stats = result['data'];
    })
  }

  formatLabel(value:number){
    let day = Math.round(value);
    return day;
  }

}
