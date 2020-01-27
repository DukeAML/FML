from app import app
from flask import render_template, flash, redirect, url_for, session, request
from flask import jsonify
import random

@app.route('/allocation', methods=['GET'])
def get_alloc_info():
    print('got here')
    multiseriesData = [
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
    ]


    # get most recent day's values across all asset categories
    testSeries = multiseriesData[0]['series']
    maxDay = testSeries[0]['name']
    for entry in testSeries:
      if entry['name'] > maxDay:
        maxDay = entry['name']
    

    mostRecentAllocation = []

    for assetType in multiseriesData:
      tempDict = {}
      assetName = assetType['name']
      currentSeries = assetType['series']

      for dayValuePair in currentSeries:
        if dayValuePair['name'] == maxDay:
          tempDict['name'] = assetName
          tempDict['value'] = dayValuePair['value']
          break
      
      mostRecentAllocation.append(tempDict)
    print(mostRecentAllocation)

    return jsonify({'data':multiseriesData, 'mostRecent':mostRecentAllocation})

    #  now, want to add to mock a separate "single" form that the current allocation chart can access