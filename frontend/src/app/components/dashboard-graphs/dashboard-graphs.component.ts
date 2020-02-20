import { Component, OnInit } from '@angular/core';
import { MatChip, MatChipInputEvent, MatChipList, MatError, MatFormField, MatOption, MatPlaceholder, MatSelect } from '@angular/material';
import {COMMA, ENTER} from '@angular/cdk/keycodes';
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
  invalidAssetField:boolean = false;

  readonly separatorKeysCodes: number[] = [ENTER, COMMA];



  ngOnInit() {
    this.populateDropdown();
  }

  populateDropdown(){
    this.dataService.getDropdownInfo().subscribe(result => {
      this.models = result['models'];
    })
  }


  getAssetData($event: MatChipInputEvent){
    console.log('event just took place')
    let newValues = $event['value'];
    let input = $event.input;
    let value = $event.value.toUpperCase();

    console.log('input', input);
    console.log('value', value);

    // now add them to the array, if no match, then pop up model asking for valid ticker
    this.dataService.getAssetValueOverTime(value).subscribe(result => {
      
      if(result['data']){
        this.invalidAssetField = false;
        if(input){ input.value = ''; }

        let data = result['data']
        let tempObj = {'name': value, 'series': data}
        console.log('tempObj', tempObj)
        let assetDataCopy = [...this.assetData];
        assetDataCopy.push(tempObj);
        this.assetData = assetDataCopy;
      }
      else{
        this.invalidAssetField = true;
        // handle invalid asset
      }
    })
  }

  remove(ticker){
    this.invalidAssetField = false;

    console.log('ticker to remove', ticker)
    console.log('assetData', this.assetData);
    let i=0;
    let tickerIndex;
    let assetDataCopy = [...this.assetData];

    for(i=0; i<assetDataCopy.length; i++){
      if(assetDataCopy[i]['name'] == ticker){
        tickerIndex = i;
        break;
      }
    }
    // MAKE SURE SPLICE CORRECTLY MODIFIES THE ARRAY
    assetDataCopy.splice(tickerIndex, 1);
    this.assetData = assetDataCopy;
  }

  getModelData($event){
    console.log('event', $event);

    let modelName = $event['value'];
    
    // this.dataService.getModelPerformanceOverTime(modelName).subscribe(result => {
    //   // do stuff here
    // })
  }

    // ----------- FORMFIELD OPTIONS ---------------
    visible: boolean = true;
    selectable: boolean = true;
    removable: boolean = true;
    addOnBlur: boolean = true;

    // ----------- GRAPH OPTIONS --------------------
    lineLegend: boolean = true;
    lineShowLabels: boolean = true;
    lineAnimations: boolean = true;
    lineLegendPosition: string = "right";
    lineXaxis: boolean = true;
    lineYaxis: boolean = true;
    lineShowYAxisLabel: boolean = true;
    lineShowXAxisLabel: boolean = true;
    lineXaxisLabel: string = 'Days Since Last Month';
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
