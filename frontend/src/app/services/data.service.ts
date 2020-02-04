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

  getAssetDescription(assetType:string, day:string){
    return this.http.get(this.serverURL + '/asset-description/' + assetType + '/' + day);
  }

  getMostRecentDay(){
    return this.http.get(this.serverURL + '/most-recent-day');
  }

  getPerformanceStats(day:number) {
    return this.http.get(this.serverURL + '/performance-stats/' + day);
  }

}
