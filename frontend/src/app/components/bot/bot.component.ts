import { Component, OnInit } from '@angular/core';
import { DataService } from '../../services/data.service';
import { NgxChartsModule } from '@swimlane/ngx-charts';
import {MatDialog, MatDialogRef, MAT_DIALOG_DATA} from '@angular/material/dialog';
import { AssetModalComponent } from '../asset-modal/asset-modal.component'


@Component({
  selector: 'app-bot',
  templateUrl: './bot.component.html',
  styleUrls: ['./bot.component.css']
})
export class BotComponent implements OnInit {

  constructor(private dataService:DataService, public dialog:MatDialog) {
    this.getData();
   }

  single: any[];
  multi: any[]
  view: any[] = [600, 400];

  colorScheme = {
    domain: ['#5AA454', '#A10A28', '#C7B42C', '#AAAAAA']
  };

  // options
  pieGradient: boolean = true;
  pieShowLegend: boolean = false;
  pieShowLabels: boolean = true;
  pieIsDoughnut: boolean = false;
  pieLegendPosition: string = 'below';
  pieTrimLabels: boolean = false;

  lineLegend: boolean = true;
  lineShowLabels: boolean = true;
  lineAnimations: boolean = true;
  lineLegendPosition: string = "right";
  lineXaxis: boolean = true;
  lineYaxis: boolean = true;
  lineShowYAxisLabel: boolean = true;
  lineShowXAxisLabel: boolean = true;
  lineXaxisLabel: string = 'Days Since Inception';
  lineYaxisLabel: string = '% Allocation';
  lineTimeline: boolean = true;

  ngOnInit() {
  }

  getData(): void{

    this.dataService.getAssetAllocationOverTime().subscribe( result => {
      this.multi = result['data'];
      this.single = result['mostRecent'];
    })
  }

  // INTERACTIVE FUNCTIONS

  // NOTE - THIS FUNCTION ONLY RETURNS "CURRENT" DESRIPTION OF AN ASSET - 
  // eventually, gonna want to have a function that can get the allocation of an asset at different timesteps. To do that, 
  // just need to feed in the day as an argument (which the line graph gives us when we click on it and which for the pie chart 
  // we can just set to the max value of the data coming from the line graph), send that argument as part of the route we call, 
  // and include that in whatever query we use to get the data in the first place.
  openDialog(data): void {
    // call service and get data for that stock
    let assetName:string = data;
    this.dataService.getAssetDescription(assetName.toLowerCase()).subscribe(result => {

      // If it fails for some reason and data is null
      if(!result['data']){
        console.log('found an error, result looks like this', result);
        const dialogRef = this.dialog.open(AssetModalComponent, {
          width: '250px',
          data: {'type': 'ERROR', 'data': []}
        });
        dialogRef.afterClosed().subscribe(closeResult => {
          console.log('The dialog was closed');
        });
      }

      else{
        let constructorArg = {'type': assetName, 'data': result['data']}
        const dialogRef = this.dialog.open(AssetModalComponent, {
          width: '250px',
          data: constructorArg
        });
        dialogRef.afterClosed().subscribe(closeResult => {
          console.log('The dialog was closed');
        });
      }

    })
    
  }

  pieOnSelect(data): void {
    console.log('Item clicked', JSON.parse(JSON.stringify(data)));
    this.openDialog(data['name']);
  }

  pieOnActivate(data): void {
    console.log('Activate', JSON.parse(JSON.stringify(data)));
  }

  pieOnDeactivate(data): void {
    console.log('Deactivate', JSON.parse(JSON.stringify(data)));
  }

  lineOnSelect(data): void {
    console.log('Item clicked', JSON.parse(JSON.stringify(data)));
    this.openDialog(data['series']);
  }

  lineOnActivate(data): void {
    console.log('Activate', JSON.parse(JSON.stringify(data)));
  }

  lineOnDeactivate(data): void {
    console.log('Deactivate', JSON.parse(JSON.stringify(data)));
  }


}
