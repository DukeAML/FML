import { Component, OnInit } from '@angular/core';
import { MatChip, MatChipInputEvent, MatChipList, MatError, MatFormField, MatInputModule, MatOption, MatPlaceholder, MatSelect } from '@angular/material';
import {COMMA, ENTER} from '@angular/cdk/keycodes';
import { NgxChartsModule } from '@swimlane/ngx-charts';
import { DataService } from '../../services/data.service';


@Component({
  selector: 'app-dashboard-graphs',
  templateUrl: './dashboard-graphs.component.html',
  styleUrls: ['./dashboard-graphs.component.css'],
})
export class DashboardGraphsComponent implements OnInit {

  constructor(private dataService:DataService) { }

  assets:string[];
  models:string[];
  assetData:any[] = [];
  modelData:any[] = [];
  activeModel:string = '';
  indicators:string[];
  mostRecentIndicator:string;
  indicatorSelected:boolean = false;
  numParams:any;
  invalidNumParams:boolean = false;

  invalidAssetField:boolean = false;
  mostRecentEquity:string;

  readonly separatorKeysCodes: number[] = [ENTER, COMMA];



  ngOnInit() {
    this.populateDropdown();
    this.getAssetData({'value': 'AAPL'})
  }

  populateDropdown(){
    this.dataService.getDropdownInfo().subscribe(result => {
      console.log('dropdown finished populating');
      this.models = result['models'];
      this.indicators = result['indicators'];
    })
    
  }

  getIndicatorData($event:any){
    console.log('getIndicatorData event', $event);
    let formatted = this.mostRecentIndicator;

    if(this.numParams != 0){
        this.invalidNumParams = false;
        let params:string = event['target']['value'];
    
        if(this.numParams != 'n' && params.split(",").length != this.numParams){
          this.invalidNumParams = true;
          return;
        }
    
        // make the textbox blank after parameters have been confirmed
        event['target']['value'] = '';
    
        if(this.mostRecentIndicator){
          let formatted = this.mostRecentIndicator + "," + params;
          this.mostRecentIndicator = null;
        }
    }
    this.dataService.getCustomIndicatorsInfo(formatted, this.mostRecentEquity).subscribe(result => {
      this.handleNewGraphData(result, formatted + ' ' + this.mostRecentEquity, 'indicator');
    })
  }

  getAssetData($event:any){
    let input = $event.input;
    let value = $event.value.toUpperCase();
    this.mostRecentEquity = value;
    if(!value){
      return
    }

    this.dataService.getAssetValueOverTime(value).subscribe(result => {
      console.log('result was', result);
      this.handleNewGraphData(result, value, 'asset');
      if(input){ input.value = ''; }
    })
    
  }

  handleNewGraphData(result:any, value:string, dataType:string){
    console.log('result', result);
    if(result['data']){
      this.invalidAssetField = false;
      let data = result['data']
      let tempObj = {'name': value, 'series': data, 'type': dataType}

      console.log('tempObj', tempObj)
      let assetDataCopy = [...this.assetData];
      assetDataCopy.push(tempObj);
      this.assetData = assetDataCopy;
      
      // handle updating equity for indicators performance

    }
    else{
      this.invalidAssetField = true;
      // handle invalid asset
    }
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
    assetDataCopy.splice(tickerIndex, 1);
    this.assetData = assetDataCopy;
  }

  loadParameterFields($event){
    console.log('loadParamterFields called with event', $event);
    this.mostRecentIndicator = $event['value'];
    this.dataService.getNumberOfParameters(this.mostRecentIndicator).subscribe(result => {
      let number = result['data']
      this.numParams = number;

      if(number != 0){
        this.indicatorSelected = true;
      }
      this.getIndicatorData({})

    })
  }

  getModelData($event){
    this.activeModel = '';

    let modelName = $event['value'];
    this.activeModel = modelName;    
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
