import { Component, OnInit } from '@angular/core';
import {FormControl} from '@angular/forms';

import { BacktesterDialogComponent } from '../backtester-dialog/backtester-dialog.component'
import { DataService } from '../../services/data.service';
import { MatButton, MatAccordion, MatExpansionPanel, MatProgressSpinner, MatTable } from '@angular/material'
import {MatDialog, MatDialogRef, MAT_DIALOG_DATA} from '@angular/material/dialog';


@Component({
  selector: 'app-backtester',
  templateUrl: './backtester.component.html',
  styleUrls: ['./backtester.component.css']
})
export class BacktesterComponent implements OnInit {

  params:any[];

  startDate:Date;
  endDate:Date;
  minEndDate:Date;
  maxStartDate:Date;

  showButton:boolean;
  isLoading:boolean;
  testerComplete:boolean;
  positions:any[];
  predictions:any[];
  performanceStats:any[];

  selectedPositions:any[];
  minVizDate:Date = new Date('2018-01-01');
  maxVizDate:Date = new Date();

  earlyDate:Date = new Date('1970-01-01');
  graphData:any[];

  renderedTrades:any[] = [];
  renderedPredictions:any[] = [];

  displayedColumns: string[] = ['datePurchased', 'numShares', 'dateSold'];
  predColumns: string[] = ['date', 'prediction', 'confidence'];


  constructor(private dataService:DataService, public dialog:MatDialog) { }

  ngOnInit() {
    this.showButton = true;
    this.isLoading = false;
    this.testerComplete = false;
  }

  openDialog(): void {
    this.showButton = false;
    this.isLoading = true
    this.dataService.getBacktesterDropdownData().subscribe(result => {
      this.isLoading = false;
      console.log('opened');
      const dialogRef = this.dialog.open(BacktesterDialogComponent, {
        width: '250px',
        hasBackdrop:false,
        data: result
      });

      dialogRef.afterClosed().subscribe(params => {
        if(params){
          this.startDate = params['startDate'];
          this.endDate = params['endDate'];
          this.maxStartDate = new Date(this.endDate.getTime() - 24*60*60*1000);
          this.showButton = false;
          this.isLoading = true;

          this.dataService.runBacktester(params).subscribe(result => {
            this.isLoading = false;
            this.testerComplete = true;

            this.positions = this.formatPositions(result['positions']);
            // this.predictions = this.formatPredictions(result['predictions']);
            this.performanceStats =  result['stats'];
            this.graphData = result['graphData'];
          })
        }
        else{
          this.showButton = true;
        }

      });

    });

  }
  formatPositions(positions){
    let betterPoss = [];
    positions.forEach(pos => {
      let formattedPos = {'ticker': pos['ticker'], 'trades': this.formatTrades(pos['trades'])};
      betterPoss.push(formattedPos);
    });
    return betterPoss;
}

  formatTrades(trades) {
    let betterTrades = []
    trades.forEach(trade => {
      console.log(trade);
      let formattedTrade = {'datePurchased': new Date(trade['datePurchased']), 'dateSold': new Date(trade['dateSold']), 'numShares': trade['numShares']}
      betterTrades.push(formattedTrade)
    })
    return betterTrades
  }

  formatPredictions(predictions){
    let betterPreds = [];
    predictions.forEach(pos => {
      let formattedPred = {'ticker': pos['ticker'], 'predictions': this.formatPreds(pos['predictions'])};
      betterPreds.push(formattedPred);
    });
    return betterPreds;
}

  formatPreds(preds) {
    let betterPreds = [];
    preds.forEach(pred => {
      let formattedPred = {'date': new Date(pred['date']), 'prediction': pred['prediction'], 'confidence': pred['confidence']};
      betterPreds.push(formattedPred);
    })
    return betterPreds
  }
  onPositionsChange($event){
    console.log('positionsChangeEvent', $event);
    this.selectedPositions = $event['value'];
    this.updateRendered();
    // for the selected positions, go through trades and render ones that are between minVizDate and maxVisDate
  }

  updateStartDate($event){
    // update rendered trades here too
    console.log('update start date event', $event)
    this.minVizDate = new Date($event['value']);
    this.minEndDate = new Date(this.minVizDate.getTime() + (24*60*60*1000));
    this.updateRendered();

  }

  updateEndDate($event){
    // update rendered trades here too ==> add the date to compare it to as a parameter in function
    // that can be used to update renderedtrades from both start end end
    this.maxVizDate = new Date($event['value']);
    this.updateRendered();
  }

  updateRendered(){
    this.renderedTrades = [];
    this.renderedPredictions = [];
    this.positions.forEach(position => {
      console.log('current position is', position);
      if(this.selectedPositions.indexOf(position['ticker']) > -1){
        console.log(position);
        let tempObj = {'name': position['ticker'], 'trades': position['trades'].filter(trade => (trade['datePurchased'] >= this.minVizDate && trade['datePurchased'] <= this.maxVizDate))}
        this.renderedTrades.push(tempObj);
      }
    });
    // this.predictions.forEach(prediction => {
    //   if(this.selectedPositions.indexOf(prediction['ticker']) > -1){
    //     console.log(prediction);
    //     let tempObj = {'name': prediction['ticker'], 'predictions': prediction['predictions'].filter(pred => (pred['date'] >= this.minVizDate && pred['date'] <= this.maxVizDate))};
    //     this.renderedPredictions.push(tempObj);
    //   }
    // });
    console.log(this.renderedTrades);
    console.log(this.renderedPredictions);
  }

    // GRAPH FORMAT OPTIONS
    lineShowLabels: boolean = false;
    lineAnimations: boolean = false;
    lineLegendPosition: string = "right";
    lineXaxis: boolean = true;
    lineYaxis: boolean = true;
    lineShowYAxisLabel: boolean = false;
    lineShowXAxisLabel: boolean = false;
    lineXaxisLabel: string = 'Days Since Last Month';
    lineYaxisLabel: string = 'Value';
    lineTimeline: boolean = false;


    view: any[] = [450, 300];

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


}
