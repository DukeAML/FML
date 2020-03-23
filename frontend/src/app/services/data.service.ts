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

  getAssetValueOverTime(assetName:string){
    return this.http.get(this.serverURL + '/asset-value-over-time/' + assetName);

  }

  getModelPerformanceOverTime(assetName:string){
    return this.http.get(this.serverURL + '/model-performance-over-time/' + assetName);

  }

  getPerformanceStats(day:number) {
    return this.http.get(this.serverURL + '/performance-stats/' + day);
  }

  getIndicatorValue(name:string){
    this.http.get(this.serverURL + '/indicators/' + name).subscribe(result => {
      console.log('indicator result', result);
    })
    
    return this.http.get(this.serverURL + '/indicators/' + name);
  }


}
