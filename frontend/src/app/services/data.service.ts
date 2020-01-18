import { Injectable } from '@angular/core';
import { HttpClientModule } from '@angular/common/http';
import { Observable, of } from 'rxjs';



@Injectable({
  providedIn: 'root'
})
export class DataService {

  constructor() { }

  private serverURL = "localhost:5000"

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
    let mock = [
      {
        "name": "Stocks",
        "series": [
          {
            "name": 10,
            "value": 10
          },
          {
            "name": 20,
            "value": 20
          },
          {
            "name": 30,
            "value": 30
          },
          {
              "name": 40,
              "value": 40
            },
            {
              "name": 50,
              "value": 50
            },
            {
              "name": 60,
              "value": 40
            }
        ]
      },
    
      {
        "name": "Bonds",
        "series": [
          {
            "name": 10,
            "value": 60
          },
          {
            "name": 20,
            "value": 40
          },
          {
            "name": 30,
            "value": 20
          },
          {
              "name": 40,
              "value": 5
            },
            {
              "name": 50,
              "value": 10
            },
            {
              "name": 60,
              "value": 15
            }
        ]
      },
    
      {
        "name": "Latvian Brothels",
        "series": [
          {
            "name": 10,
            "value": 20
          },
          {
            "name": 20,
            "value": 10
          },
          {
            "name": 30,
            "value": 40
          },
          {
              "name": 40,
              "value": 27
            },
            {
              "name": 50,
              "value": 25
            },
            {
              "name": 60,
              "value": 25
            }
        ]
      },
  
      {
          "name": "Other",
          "series": [
              {
                "name": 10,
                "value": 10
              },
              {
                "name": 20,
                "value": 30
              },
              {
                "name": 30,
                "value": 10
              },
              {
                  "name": 40,
                  "value": 28
                },
                {
                  "name": 50,
                  "value": 15
                },
                {
                  "name": 60,
                  "value": 20
                }
            ]
        }
  
    ];
    
    return of(mock);
  }

}
