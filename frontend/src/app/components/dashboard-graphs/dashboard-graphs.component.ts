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
  assetData:any[] = [];
  modelData:any[] = [];
  activeAssets:any[] = [];
  activeModels:any[] = [];


  testObj:any = {
    "name": "GS",
    "series": [
      {
        "name": 10,
        "value": 237.75
      },
      {
        "name": 20,
        "value": 239.01
      },
      {
        "name": 30,
        "value": 241.94
      },
      {
          "name": 40,
          "value": 244.30
        },
        {
          "name": 50,
          "value": 241.82
        },
        {
          "name": 60,
          "value": 238
        }
    ]
  }

  ngOnInit() {
    this.populateDropdown();
  }

  populateDropdown(){
    this.dataService.getDropdownInfo().subscribe(result => {
      this.models = result['models'];
      this.assets = result['assets'];
    })
  }

  getAssetData($event){
    let newValues = $event['value'];

    // handling removal
    if(newValues.length < this.assetData.length){
      console.log('remove detected');
      console.log('new values are', newValues)

      let activeAssetsCopy = [...this.activeAssets];
      this.activeAssets = []
      let assetDataReplacement = [];
      let i;

      for(i=0; i<activeAssetsCopy.length; i++){
        if(newValues.includes(activeAssetsCopy[i])){
          assetDataReplacement.push(this.assetData[i]);
          this.activeAssets.push(activeAssetsCopy[i]);
        }
      }

      this.assetData = assetDataReplacement;
      console.log('asset data is now', this.assetData);
    }

    else{
      console.log('new value added, newValues are', newValues);
      let assetName:string;
      let i:number;
      
      for(i=0; i<newValues.length; i++){
        if(!this.activeAssets.includes(newValues[i])){
          assetName = newValues[i];
          this.activeAssets.push(assetName);
          console.log('new value detected is', assetName);
          break;
        }
      }

      this.dataService.getAssetValueOverTime(assetName).subscribe(result => {
        let tempJSON = {}
        tempJSON['name'] = assetName;
        tempJSON['series'] = result['data']
  
        let assetDataReplacement = []
        if(this.assetData){
          assetDataReplacement = [...this.assetData];
        }
        assetDataReplacement.push(tempJSON);
        this.assetData = [...assetDataReplacement];
      })
    }

  }

  getModelData($event){
    console.log('event', $event);

    let modelName = $event['value'];
    
    // this.dataService.getModelPerformanceOverTime(modelName).subscribe(result => {
    //   // do stuff here
    // })
  }

    // ----------- GRAPH OPTIONS --------------------
    lineLegend: boolean = true;
    lineShowLabels: boolean = true;
    lineAnimations: boolean = true;
    lineLegendPosition: string = "right";
    lineXaxis: boolean = true;
    lineYaxis: boolean = true;
    lineShowYAxisLabel: boolean = true;
    lineShowXAxisLabel: boolean = true;
    lineXaxisLabel: string = 'Days Since Inception';
    lineYaxisLabel: string = 'Asset Value (USD)';
    lineTimeline: boolean = true;
  
    view: any[] = [600, 400];
  
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
  
    // ----------

}
