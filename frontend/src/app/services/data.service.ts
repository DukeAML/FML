import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, of } from 'rxjs';



@Injectable({
  providedIn: 'root'
})
export class DataService {

  constructor( private http:HttpClient ) { }

  private serverURL = "http://localhost:5000"

  getAssetTypeAllocation(){
    let mock = [
      { name: 'Stocks', value: 40 },
      { name: 'Bonds', value: 15 },
      { name: 'Latvian Brothels', value: 25 },
      { name: 'Other', value: 20 }
  ]

    return of(mock);
  }


  getAssetAllocationOverTime(){
    this.http.get(this.serverURL + '/allocation').subscribe(result => {
      console.log('result', result);
    })
    
    return this.http.get(this.serverURL + '/allocation')
  }

}
