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
  activeModelID:string;
  indicators:string[];
  mostRecentIndicator:string;
  indicatorSelected:boolean = false;
  numParams:any;
  invalidNumParams:boolean = false;
  equities:string[];

  invalidAssetField:boolean = false;
  mostRecentEquity:string;

  readonly separatorKeysCodes: number[] = [ENTER, COMMA];



  ngOnInit() {
    this.populateDropdown();
    this.getAssetData({'value': 'AAPL'})
  }

  populateDropdown(){
    this.dataService.getDropdownInfo().subscribe(result => {
      this.indicators = result['indicators'];
      this.equities = result['equities'];
    })
    
  }

  getIndicatorData($event:any){
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
          formatted = this.mostRecentIndicator + "," + params;
        }
    }
    console.log('most recent equity', this.mostRecentEquity);
    this.dataService.getCustomIndicatorsInfo(formatted, this.mostRecentEquity).subscribe(result => {
      console.log('indicator data from backend looks like', result);
      this.handleNewGraphData(result, formatted + ' ' + this.mostRecentEquity, 'indicator');
    })
  }

  getAssetData($event:any){
    let input = $event.input;
    let value = $event.value.toUpperCase();
    if(!value){
      return
    }
    this.mostRecentEquity = value;

    this.dataService.getAssetValueOverTime(value).subscribe(result => {
      this.handleNewGraphData(result, value, 'asset');
      if(input){ input.value = ''; }
    })
    
  }

  handleNewGraphData(result:any, value:string, dataType:string){
    console.log('data before was ', this.assetData);
    if(result['data']){
      this.invalidAssetField = false;
      let tempObjArr = result['data']

      for(let tempObj of tempObjArr){
        tempObj['type'] = dataType;
        console.log('tempObj to be added', tempObj);
        let assetDataCopy = [...this.assetData];
        assetDataCopy.push(tempObj);
        this.assetData = assetDataCopy;
        console.log('data after is ', this.assetData);

      }
      // handle updating equity for indicators performance

    }
    else{
      this.invalidAssetField = true;
      // handle invalid asset
    }
  }

  remove(ticker){
    this.invalidAssetField = false;

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
    this.indicatorSelected = false;
    if(!$event['value']){
      return;
    }
    this.mostRecentIndicator = $event['value'];
    this.dataService.getNumberOfParameters(this.mostRecentIndicator).subscribe(result => {
      let number = result['data']
      this.numParams = number;

      if(number == 0){
        this.getIndicatorData({})
        return;

      }
      this.indicatorSelected = true;


    })
  }

  getModelData($event){
    console.log('get model data event is ', $event);

    this.activeModelID = $event['value']['id'];

    // subscribe to data call, set render thing to true, input the model id into the indicators service to fetch the data
  
  }

  getModelsForEquity($event){
    let ticker = $event['value'];
    console.log('event value is', $event['value']);

    this.dataService.getModelsForEquity(ticker).subscribe(result => {
      console.log('models collections stuff returned from service is', result['data']);
      this.models = result['data'];

    })

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
      domain: ['#5AA454', '#A10A28', '#C7B42C', '#EF6F6C', '#7FC6B8', '#AAAAAA']
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
