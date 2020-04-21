import { Component, OnInit, Inject } from '@angular/core';
import {MatDialog, MatDialogRef, MAT_DIALOG_DATA} from '@angular/material/dialog';
import { MatDatepicker, MatError, MatTooltip } from '@angular/material'
import { FormControl } from '@angular/forms'

import { DataService } from '../../services/data.service';



@Component({
  selector: 'app-backtester-dialog',
  templateUrl: './backtester-dialog.component.html',
  styleUrls: ['./backtester-dialog.component.css']
})
export class BacktesterDialogComponent implements OnInit {
  startDate:Date;
  endDate:Date;
  portfolioValue:number;

  models:any[];

  selectedModel:string;

  inputError:boolean = false;

  minStartDate:Date;
  maxStartDate:Date;
  minEndDate:Date;
  maxEndDate:Date;
  
  // start date, end date, portfolio values, a trading algorithm (but you'll need to find a nice way to display the 
  // possible trading algorithms i.e. show all the parameters in them so they know) and then what other things you want to plot 
  // (SNP, Oil, a different portfolio)

  constructor(private dataService:DataService, public dialogRef: MatDialogRef<BacktesterDialogComponent>, @Inject(MAT_DIALOG_DATA) private data) { }

  ngOnInit() {
    this.minStartDate = new Date(this.data['firstDate'])
    this.maxEndDate = new Date(this.data['endDate']);
    this.models = this.data['models']
    this.maxStartDate = this.subtractDays(this.maxEndDate, 1);

    // eventually move this to backend
    this.modelParamsToStrings();
  }
  modelParamsToStrings() {
    let paramsStrings = [];
    this.models.forEach(element => {
      
      let paramsString = ''
      element['parameters'].forEach(item => {
        paramsString = paramsString + item['name'] + ': ' + item['value']  + '    |    '
      })
      element['paramsString'] = paramsString.substr(0,paramsString.length-2);
    });
  }

  onCancelClick(): void {
    this.dialogRef.close();
  }

  onSubmit():void{
    // validate data, throw error if necessary, otherwise return to other component

    if(this.startDate == null || this.endDate == null || 
      this.startDate.getTime() >= this.endDate.getTime() || isNaN(Number(this.portfolioValue)) || this.selectedModel == null){
      this.inputError = true;
      return;
    }
    let modelId = "";
    
    this.models.forEach( model => {
      if(model['name'] == this.selectedModel){
        modelId = model['id'];
      }
    });

    this.dialogRef.close({'startDate': this.startDate, 'endDate': this.endDate, 'portfolioValue': this.portfolioValue, 'model': modelId});
  }

  updateStartDate($event){
    this.inputError = false;
    this.startDate = new Date($event['value']);
    this.minEndDate = this.subtractDays(new Date(this.startDate), -1);
  }

  updateEndDate($event){
    this.inputError = false;
    this.endDate = new Date($event['value']);
  }

  updateModel($event){
    this.inputError = false;
    this.selectedModel = $event['value'];
  }

  subtractDays(date:Date, days:number){ 
    let tempDate = new Date(); 
    tempDate.setTime(date.getTime() - (days*24*60*60*1000));  
    return tempDate;  
} 

}
