from app import app
from flask import render_template, flash, redirect, url_for, session, request
from flask import jsonify
from app.mocks import *


@app.route('/dashboard-dropdown', methods=['GET'])
def getModelsAndAssets():
  mockModels = getAllModels()
  mockAssets = getAllAssetNames()
  return jsonify({'models': mockModels, 'assets': mockAssets})


@app.route('/asset-value-over-time/<string:name>', methods=['GET'])
def get_description_over_time(name):
  mock = getAssetValueOverTime(name)
  return jsonify({'data':mock})

@app.route('/model-performance-over-time/<string:modelName>', methods=['GET'])
def get_model_performance_over_time(modelName):
  mock = getModelPerformanceOverTime(modelName)
  return jsonify({'data':mock})

@app.route('/asset-category-description/<string:assetType>/<string:day>', methods=['GET'])
def get_asset_description(assetType, day):

  mock = getCategoryDescriptionAtDate(assetType, day)
  
  return jsonify({'data': mock})


# THIS MOCK IS MADE POORLY ESPECIALLY CAUSE I ENDED UP MOCKING THIS EXACT DATA LATER ON...
# GONNA LEAVE IT THOUGH BECAUSE EVENTUALLY IT'S JUST GONNA GET REPLACED BY DB STUFF
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
                