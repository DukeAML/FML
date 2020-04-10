import sys
# gives backend app access to modules in algDev by adding directory to pythonpath
sys.path.insert(1, '../')
import numpy as np
# gonna have to rewrite this once DB structure in place
import algDev.API.dataGatherer as dataGatherer
import algDev.API.indicators as indicators
import algDev.db.wrapper as wrapper


def getCategoryDescriptionAtDate(asset, date):
    
    assetData = []
    
    if date=='recent':

        if asset == 'stocks':
            assetData = stocksData
        else:
            assetData = bondsData
        
        return getMostRecentAllocation(assetData)
    
        # find most recent date and return distribution across stocks
    
    else:
        
        if asset == 'stocks':
            assetData = stocksData
        else:
            assetData = bondsData
        
        return getAllocationOnDay(assetData, int(date))
        

def getMostRecentAllocation(assetData):
	testSeries = assetData[0]['series']
	maxDay = testSeries[0]['name']
	for entry in testSeries:
		if entry['name'] > maxDay:
			maxDay = entry['name']
	
	return getAllocationOnDay(assetData, maxDay)
        

def getAllocationOnDay(assetData, day):
	allocationOnDay = []

	for asset in assetData:
		tempDict = {}
		assetName = asset['name']
		currentSeries = asset['series']

		for dayValuePair in currentSeries:
			if dayValuePair['name'] == day:
				tempDict['name'] = assetName
				tempDict['value'] = dayValuePair['value']
				break
		allocationOnDay.append(tempDict)

	return allocationOnDay

bondsData = [
    {
        "name": "US Government Bonds",
        "series": [
          {
            "name": 10,
            "value": 40
          },
          {
            "name": 20,
            "value": 30
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
              "value": 60
            }
        ]
      },
    
      {
        "name": "Idk other bonds",
        "series": [
          {
            "name": 10,
            "value": 60
          },
          {
            "name": 20,
            "value": 70
          },
          {
            "name": 30,
            "value": 70
          },
          {
              "name": 40,
              "value": 60
            },
            {
              "name": 50,
              "value": 10
            },
            {
              "name": 60,
              "value": 40
            }
        ]
      }
]

stocksData = [
    {
        "name": "GS",
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
        "name": "APPL",
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
        "name": "FUN",
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
          "name": "PZZA",
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

usGovtBondsData = [
          {
            "name": 10,
            "value": 10
          },
          {
            "name": 20,
            "value": 11
          },
          {
            "name": 30,
            "value": 12
          },
          {
              "name": 40,
              "value": 13
            },
            {
              "name": 50,
              "value": 14
            },
            {
              "name": 60,
              "value": 15
            }
        ]

idkOtherBondsData = [
          {
            "name": 10,
            "value": 20
          },
          {
            "name": 20,
            "value": 21
          },
          {
            "name": 30,
            "value": 22
          },
          {
              "name": 40,
              "value": 23
            },
            {
              "name": 50,
              "value": 24
            },
            {
              "name": 60,
              "value": 25
            }
        ]

gsData = [{
            "name": 10,
            "value": 237.75
          },
          {
            "name": 20,
            "value": 239.01
          },
          {
            "name": 30,
            "value": 241.94
          },
          {
              "name": 40,
              "value": 244.30
            },
            {
              "name": 50,
              "value": 241.82
            },
            {
              "name": 60,
              "value": 238
            }]

applData = [
          {
            "name": 10,
            "value": 308.66
          },
          {
            "name": 20,
            "value": 318.85
          },
          {
            "name": 30,
            "value": 321.45
          },
          {
              "name": 40,
              "value": 325.21
            },
            {
              "name": 50,
              "value": 320.03
            },
            {
              "name": 60,
              "value": 321.55
            }
        ]
pzzaData = [
              {
                "name": 10,
                "value": 64.22
              },
              {
                "name": 20,
                "value": 64.74
              },
              {
                "name": 30,
                "value": 64.55
              },
              {
                  "name": 40,
                  "value": 65.75
                },
                {
                  "name": 50,
                  "value": 64.64
                },
                {
                  "name": 60,
                  "value": 64.79
                }
            ]
funData = [
          {
            "name": 10,
            "value": 53.2
          },
          {
            "name": 20,
            "value": 55.21
          },
          {
            "name": 30,
            "value": 53.91
          },
          {
              "name": 40,
              "value": 54.44
            },
            {
              "name": 50,
              "value": 54.52
            },
            {
              "name": 60,
              "value": 54.75
            }
        ]


def getAssetValueOverTime(name, period):
  pricesData = dataGatherer.getPrices(name, period)
  if(len(pricesData) > 0):
    return [{'name': name, 'series': pricesData}]
  else:
    return "ERROR"


def getAllAssetNames():
  # THIS IS GONNA NEED TO BE SORTED
  return dataGatherer.getTickers()

def getAllModels():
  # THIS IS GONNA NEED TO BE SORTED
  return ['Model 1', 'Model 2', 'Model 3', 'Model 4', 'Model 5']

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


indicatorValues = {
  "name": "data", 
  "series": [
      {
        "name": 10,
        "value": 40
      },
      {
        "name": 20,
        "value": 30
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
          "value": 60
        }
    ]}

indicatorDict = {
"SMA": 1,
"EMA": 1,
"Wilder MA": 1,
"MACD": 2,
"MACDSig": 2,
"KST": 0,
"TRIX": 0,
"KSTTrix": 0,
"RSI": 0,
"Prings": 0,
"OLHC": 0,
"Rainbow": "n",
"Oil": 0,
"SNP": 0,
"Reit": 0,
"GOP": 1,
"BOP": 0,
"Volumes": 0,
"Closes": 0,
"UpperBol": 0,
"LowerBol": 0,
"AccumSwing": 0,
"ATR": 1}

modelData = [{'indicator': indicatorName, 'data':[indicatorValues]} for indicatorName in sorted(indicatorDict.keys())]

mockIndicatorData = [
          {
            "name": 0,
            "value": 40
          },
          {
            "name": 4,
            "value": 10
          },
          {
            "name": 8,
            "value": 20
          },
          {
            "name": 12,
            "value": 30
          },
          {
              "name": 16,
              "value": 40
            },
            {
              "name": 20,
              "value": 50
            }
        ]

def getIndicatorData(formatted, equity):
  data = []
  
  underscored = formatted.replace(",", "_")
  print('underscored is', underscored)

  # FOR NOW - JUST USING LENGTH OF HISTORICAL PRICES DATA TO GET LAST X VALUES
  numDays = len(dataGatherer.getPrices('AAPL'))
  indicatorData = indicators.get_indicator_value(equity, underscored)

  samples = indicatorData[:numDays]
  samples = np.flipud(samples) 

  if len(samples[0]) == 1:
    series = []
    samples = [item[0] for item in samples] #unpack it

    for i in range(len(samples)):
      series.append({'name': i, 'value': samples[i]}) # reverse the days
        
    singleSeriesData = {'name': formatted, 'series': series}
    data.append(singleSeriesData)
  
  else:
    # big brain data processing
    paramSplit = formatted.split(",")
    for i in range(1, len(paramSplit)):
      tempDict = {'name': paramSplit[0] + ',' + paramSplit[i], 'series': []}
      data.append(tempDict)
    
    for i in range(len(samples)):
      for j in range(len(samples[i])):
        currentEntry = samples[i][j]
        tempDict = {'name': i, 'value': currentEntry}
        data[j]['series'].append(tempDict)
  
  return data


def getTopAssets():
  print('getTopAssets called')
  allAssets = wrapper.getTickers()
  
  changes = []

  for asset in allAssets:
    print('current asset', asset)
    data = dataGatherer.getPrices(asset, "5d")

    print('data in top assets is', data)

    firstObj = data[0]
    lastObj = data[len(data)-1]

    totalChange = lastObj['value'] - firstObj['value']
    percentChange = (totalChange/firstObj['value']) * 100
    print('percentChange is', percentChange)
    changes.append((percentChange, asset))

  changes.sort()

  finalResult = []

  for item in changes[-3:]:
    tempDict = {'percentChange': item[0], 'asset': item[1], 'type': 'top'} 
    finalResult.append(tempDict)

  for item in changes[:3]:
    tempDict = {'percentChange': item[0], 'asset': item[1], 'type': 'bottom'} 
    finalResult.append(tempDict)

  return finalResult


  

