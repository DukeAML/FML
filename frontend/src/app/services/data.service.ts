import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
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


}
