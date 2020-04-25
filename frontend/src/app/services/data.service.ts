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

  getModelsForEquity(equity:string){
    return this.http.get(this.serverURL + '/dashboard-dropdown/' + equity);
  }

  getAssetValueOverTime(assetName:string, time:string="1mo"){
    return this.http.get(this.serverURL + '/asset-value-over-time/' + assetName + '/' + time);

  }

  getPerformanceStats(day:number) {
    return this.http.get(this.serverURL + '/performance-stats/' + day);
  }

  getModelInformation(modelID:string){
    console.log('getting indicator information for model: ', modelID);
    return this.http.get(this.serverURL + '/modelPerformance/' + modelID);
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
    console.log('params in service', params);

    return this.http.post(this.serverURL + '/backtester/run', params)
  }

}
