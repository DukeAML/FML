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

  pieOnSelect(data): void {
    console.log('Item clicked', JSON.parse(JSON.stringify(data)));
    this.openDialog(data['name'], 'recent');
  }

  pieOnActivate(data): void {
    console.log('Activate', JSON.parse(JSON.stringify(data)));
  }

  pieOnDeactivate(data): void {
    console.log('Deactivate', JSON.parse(JSON.stringify(data)));
  }

  lineOnSelect(data): void {
    console.log('Item clicked', JSON.parse(JSON.stringify(data)));
    this.openDialog(data['series'], data['name']);
  }

  lineOnActivate(data): void {
    console.log('Activate', JSON.parse(JSON.stringify(data)));
  }

  lineOnDeactivate(data): void {
    console.log('Deactivate', JSON.parse(JSON.stringify(data)));
  }

  openDialog(assetName:string, day:string): void {
    // call service and get data for that stock
    this.dataService.getAssetDescription(assetName.toLowerCase(), day).subscribe(result => {

      // If it fails for some reason and data is null
      if(!result['data']){
        console.log('found an error, result looks like this', result);
        // const dialogRef = this.dialog.open(AssetModalComponent, {
        //   width: '250px',
        //   data: {'type': 'ERROR', 'data': []}
        // });
        // dialogRef.afterClosed().subscribe(closeResult => {
        //   console.log('The dialog was closed');
        // });
      }

      else{
        // get position of asset in color scheme array, use that for pie chart
        let colorIndex = 0;
        for(let i=0; i<this.single.length; i++){

          if(this.single[i]['name'] == assetName){
            colorIndex = i;
            break;
          }

        }

        let numberOfSlices = result['data'].length;
        let colors = this.makeColorScheme(this.colorScheme['domain'][colorIndex], numberOfSlices);

        this.single = result['data'];
        this.colorScheme = {domain: colors};

        // let constructorArg = {'type': assetName, 'data': result['data']}
        // const dialogRef = this.dialog.open(AssetModalComponent, {
        //   width: '250px',
        //   data: constructorArg
        // });
        // dialogRef.afterClosed().subscribe(closeResult => {
        //   console.log('The dialog was closed');
        // });

      }

    })
    
  }

  makeColorScheme(hex:string, numberOfAssets:number) {
    let result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
    let rgb = {
      r: parseInt(result[1], 16),
      g: parseInt(result[2], 16),
      b: parseInt(result[3], 16)
    };

    let maxColor = Math.max(rgb['r'], rgb['g'], rgb['b']);
    let totalRange = (255 - maxColor) * 2;
    let increment = totalRange/numberOfAssets;
    let baseValues = {r: rgb['r'] - totalRange/2, g: rgb['g'] - totalRange/2, b: rgb['b'] - totalRange/2}
    console.log('baseValues', baseValues);

    let colors:any[] = [];

    let i = 0;
    for(i=0; i<numberOfAssets; i++){
      let tempObj = {r: baseValues['r'] + increment*i, g: baseValues['r'] + increment*i, b: baseValues['r'] + increment*i};
      colors.push(tempObj);
    }

    colors.map(x => this.rgbToHex(x));
    console.log('colors', colors)
    return colors;

  }

  componentToHex(c) {
    var hex = c.toString(16);
    return hex.length == 1 ? "0" + hex : hex;
  }
  
  rgbToHex(obj:any) {
    return "#" + this.componentToHex(obj['r']) + this.componentToHex(obj['g']) + this.componentToHex(obj['b']);
  }

}
