import { Component, OnInit } from '@angular/core';
import { MatFormField, MatOption, MatSelect } from '@angular/material'
import { NgxChartsModule } from '@swimlane/ngx-charts';
import { DataService } from '../../services/data.service';


@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css']
})
export class DashboardComponent implements OnInit {

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

}
