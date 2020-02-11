import { Component, OnInit } from '@angular/core';
import { MatFormField, MatOption, MatSelect } from '@angular/material'
import { NgxChartsModule } from '@swimlane/ngx-charts';
import { DataService } from '../../services/data.service';

@Component({
  selector: 'app-dashboard-graphs',
  templateUrl: './dashboard-graphs.component.html',
  styleUrls: ['./dashboard-graphs.component.css']
})
export class DashboardGraphsComponent implements OnInit {

  constructor(private dataService:DataService) { }

  assets:string[];
  models:string[];

  ngOnInit() {
    this.populateDropdown();
  }

  populateDropdown(){
    this.dataService.getDropdownInfo().subscribe(result => {
      this.models = result['models'];
      this.assets = result['assets'];
    })
  }

  getData($event){
    console.log('event', $event);
    // this.dataService.getAssetDescriptionOverTime(assetName).subscribe(result => {
    //   // do stuff here
    // })
  }

}
