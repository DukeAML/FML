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

  getAssetDescription(assetType:string){
    let mockData = [
      {'name': 'GS', 'value': 10},
      {'name': 'AAPL', 'value': 20},
      {'name': 'PZZA', 'value': 69},
      {'name': 'FUN', 'value': 1}
    ]
    let mock = {'data': mockData}
    // return of(mock);
    return this.http.get(this.serverURL + '/asset-description/' + assetType);
  }

}
