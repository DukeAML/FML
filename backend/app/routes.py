from app import app
from flask import render_template, flash, redirect, url_for, session, request
from flask import jsonify
import app.mocks as mocks


@app.route('/dashboard-dropdown', methods=['GET'])
def getModelsAndAssets():
  tickers = mocks.getAllAssetNames()
  return jsonify({'indicators': sorted([*mocks.indicatorDict]), 'equities': tickers})


@app.route('/dashboard-dropdown/<string:ticker>', methods=['GET'])
def getModelsForEquity(ticker):
  modelCollections = mocks.getModelsForEquity(ticker)
  return jsonify({'data': modelCollections})

@app.route('/asset-value-over-time/<string:name>/<string:period>', methods=['GET'])
def get_description_over_time(name, period):
  assetData = mocks.getAssetValueOverTime(name, period)
  if(assetData == "ERROR"):
    return jsonify({'ERROR': 'Invalid ticker used'})
  else:
    return jsonify({'data':assetData})


@app.route('/asset-category-description/<string:assetType>/<string:day>', methods=['GET'])
def get_asset_description(assetType, day):

  mock = mocks.getCategoryDescriptionAtDate(assetType, day)
  
  return jsonify({'data': mock})


# THIS MOCK IS MADE POORLY ESPECIALLY CAUSE I ENDED UP MOCKING THIS EXACT DATA LATER ON...
# GONNA LEAVE IT THOUGH BECAUSE EVENTUALLY IT'S JUST GONNA GET REPLACED BY DB STUFF
@app.route('/allocation', methods=['GET'])
def get_alloc_info():
    print('got here')
    # get most recent day's values across all asset categories
    testSeries = mocks.multiseriesData[0]['series']
    maxDay = testSeries[0]['name']
    for entry in testSeries:
      if entry['name'] > maxDay:
        maxDay = entry['name']
    

    mostRecentAllocation = []

    for assetType in mocks.multiseriesData:
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

    return jsonify({'data': mocks.multiseriesData, 'mostRecent':mostRecentAllocation})

  
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


@app.route('/modelPerformance/<string:modelID>', methods=['GET'])
def get_indicators_for_model(modelID):
  result = mocks.getModelGraphsData(modelID)
  return jsonify({'data': result})

@app.route('/indicators/<string:indicator>/params', methods=['GET'])
def getNumParams(indicator):
  test = mocks.indicatorDict
  return jsonify({'data':test[indicator]})

@app.route('/indicators/<string:formatted>/<string:equity>', methods=['GET'])
def getIndicatorData(formatted, equity):
  test = mocks.getIndicatorData(formatted, equity)
  return jsonify({'data': test})

@app.route('/assets/top', methods=['GET'])
def getTopAssets():
  result = mocks.getTopAssets()
  return jsonify({'data': result})

@app.route('/backtester/dropdown', methods=['GET'])
def getDates():
  tradingAlgs = mocks.getTradingAlgorithms()
  result = mocks.getBacktesterDates()
  result['models'] = tradingAlgs
  return jsonify(result)

@app.route('/backtester/run', methods=['POST'])
def runBacktester():
  json = request.get_json()
  result = mocks.runBacktester(json['startDate'], json['endDate'], int(json['portfolioValue']), json['model'])
  return jsonify(result)


