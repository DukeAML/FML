import { Component, OnInit, Inject } from '@angular/core';
import {MatDialog, MatDialogRef, MAT_DIALOG_DATA} from '@angular/material/dialog';
import { MatDatepicker, MatError, MatTooltip } from '@angular/material'
import { FormControl } from '@angular/forms'



@Component({
  selector: 'app-backtester-dialog',
  templateUrl: './backtester-dialog.component.html',
  styleUrls: ['./backtester-dialog.component.css']
})
export class BacktesterDialogComponent implements OnInit {
  startDate:Date;
  endDate:Date;
  portfolioValue:number;
  models = [
    {'name': 'Model 1', 'parameters':[{'name': 'testParam1', 'value': 69}, {'name': 'testParam2', 'value': 420}]},
    {'name': 'Model 2', 'parameters':[{'name': 'testParam3', 'value': 4}, {'name': 'testParam4', 'value': "ass"}]}
]

  inputError:boolean = false;

  minStartDate:Date;
  maxStartDate:Date;
  minEndDate:Date;
  maxEndDate:Date;
  
  // start date, end date, portfolio values, a trading algorithm (but you'll need to find a nice way to display the 
  // possible trading algorithms i.e. show all the parameters in them so they know) and then what other things you want to plot 
  // (SNP, Oil, a different portfolio)

  constructor(public dialogRef: MatDialogRef<BacktesterDialogComponent>) { }

  ngOnInit() {
    this.getInitialDates();
    this.modelParamsToStrings();
  }
  modelParamsToStrings() {
    this.models.forEach(element => {
      let paramsString = ''
      element['parameters'].forEach(item => {
        paramsString = paramsString + item['name'] + ': ' + item['value'] + ', '
      })
      element['paramsString'] = paramsString.substr(0,paramsString.length-2);
    });
  }

  onCancelClick(): void {
    this.dialogRef.close();
  }

  onSubmit():void{
    this.dialogRef.close('test')
  }

  getInitialDates(){
    // eventually run this through the service to get min start date
    const currentYear = new Date().getFullYear();
    this.minStartDate = new Date(currentYear - 40, 0, 1);
    this.maxStartDate = this.subtractDays(new Date(), 1);
    this.maxEndDate = new Date();
  }

  updateStartDate($event){
    console.log('event in updateMinEndDate', $event['value']);
    this.startDate = new Date($event['value']);
    this.minEndDate = this.subtractDays(new Date(this.startDate), -1);
  }

  updateEndDate($event){
    this.endDate = new Date($event['value']);
  }

  subtractDays(date:Date, days:number){  
    date.setTime(date.getTime() - (days*24*60*60*1000));  
    return date;  
} 

}
