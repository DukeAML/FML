from app import app
from flask import render_template, flash, redirect, url_for, session, request
from flask import jsonify
from app.mocks import *


@app.route('/asset-description/<string:type>/<string:day>', methods=['GET'])
def get_asset_description(type, day):

  mock = getDescriptionAtDate(type, day)
  
  return jsonify({'data': mock})


@app.route('/allocation', methods=['GET'])
def get_alloc_info():
    print('got here')
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
  

@app.route('/most-recent-day', methods=['GET'])
def get_most_recent_day():
  return jsonify({'day':60})

@app.route('/performance-stats/<int:day>', methods=['GET'])
def get_performance_stats(day):
  mock = []
  if day > 30:
    mock = [{'name': 'Return', 'value': '10%'}, {'name': 'RandomStat', 'value': '20'}, {'name': 'Volume', 'value': '69'},
    {'name': 'Sharpe Ratio', 'value': '1.420'}, {'name': 'Beta', 'value': '5'}, {'name': 'Alpha', 'value': '7'}]
  else:
    mock = [{'name': 'Return', 'value': '20%'}, {'name': 'RandomStat', 'value': '40'}, {'name': 'Volume', 'value': '420'},
    {'name': 'Sharpe Ratio', 'value': '1.69'}, {'name': 'Beta', 'value': '3'}, {'name': 'Alpha', 'value': '9'}]

  return jsonify({'data':mock})
                