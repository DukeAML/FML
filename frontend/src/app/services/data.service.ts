import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { Observable, of } from 'rxjs';




@Injectable({
  providedIn: 'root'
})
export class DataService {

  constructor( private http:HttpClient ) { }

  private serverURL = "http://localhost:5000"

  getAssetAllocationOverTime(){
    this.http.get(this.serverURL + '/allocation').subscribe(result => {
      console.log('result', result);
    })
    
    return this.http.get(this.serverURL + '/allocation')
  }

  getAssetCategoryDescription(assetType:string, day:string){
    return this.http.get(this.serverURL + '/asset-category-description/' + assetType + '/' + day);
  }

  getMostRecentDay(){
    return this.http.get(this.serverURL + '/most-recent-day');
  }

  getDropdownInfo(){
    return this.http.get(this.serverURL + '/dashboard-dropdown')
  }

  getAssetValueOverTime(assetName:string, time:string="1mo"){
    return this.http.get(this.serverURL + '/asset-value-over-time/' + assetName + '/' + time);

  }

  getPerformanceStats(day:number) {
    return this.http.get(this.serverURL + '/performance-stats/' + day);
  }

  getModelInformation(model:string, equity:string){
    console.log('getting indicator information for model: ', model);
    return this.http.get(this.serverURL + '/modelPerformance/' + model + '/' + equity);
  }

  getNumberOfParameters(indicator:string){
    return this.http.get(this.serverURL + '/indicators/' + indicator + '/params');
  }

  getCustomIndicatorsInfo(formatted:string, ticker:string){
    return this.http.get(this.serverURL + '/indicators/' + formatted + '/' + ticker);
  }

  getTopIndicators(){
    return this.http.get(this.serverURL + '/assets/top');
  }

  getBacktesterDropdownData(){
    console.log('called service');
    return this.http.get(this.serverURL + '/backtester/dropdown');
  }

  runBacktester(params:any){
    // return this.http.get(this.serverURL + '/backtester/run',
    // )
    let positions = [{'ticker': 'GS', 'values':[50,60,40], 'trades': [{'datePurchased': new Date('2020-04-03'), 'numShares': 50, 'sold': true, 'dateSold': new Date('2020-01-12')}]},
                    {'ticker': 'AAPL', 'values':[70,80,90], 'trades': [{'datePurchased': new Date('2020-04-06'), 'numShares': 50, 'sold': false, 'dateSold': null}]}
                    ]
    
    let stats = [{'name': 'Total Returns', 'value': '5%'},{'name': 'Market Returns', 'value': '2%'},{'name': 'Beta', 'value': '69'},
    {'name': 'Average Free Cash', 'value': 2000}, {'name': 'Log Returns', 'value': 1.5}, {'name': 'Average Free Cash', 'value': 2000}, {'name': 'Standard Deviation', 'value': 25}]
    
    let portfolioValues = [{'name': 'Portfolio Value', 'series': [{'name': 0, 'value': 10}, {'name': 30, 'value': 100}]}]

    let testObj = {'positions': positions, 'stats': stats, 'portfolioValues': portfolioValues};

    return of(testObj);
  }

}
