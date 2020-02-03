# FML
FML - Arizona Zervas (10/10 would recommend)

## Running Instructions
Two terminals are required to run this program.
To run the frontend, first, in frontend/src/environments, rename the file `environment.prod.ts` to `environment.ts`. Next, cd into the "frontend" directory and run `ng serve`
To run the backend, cd into the backend and run the script `./flask-restart-on-file-change.sh` after installing the necessary dependencies
through `pip`. 

## ML

### Creating Data for LSTM
```
from gen_lstm_data import gen_data

eq = 'VSLR' ## Ticker of the stock you want to look at, be sure you have added this to the data/equities folder

train_split = 0.8 ## Percent of data to use for training data, rest to test data

days = 500 ## How many days you want to be using of the data. As of now, there is no check on size, so if you put too large of a number, you may get index OB

look_back = 19 ## How many days you want to use to predict the next one. This will be the second dimension of your X data

label_range = 5 ## How many days you want to look at price change over. This will determine how the labels are calculated

verbose = False ## Prints out some shapes and other relevant things if you are curious.

X_train, y_train, X_test, y_test = gen_data(eq, train_split, days, look_back, label_range, verbose)

## X_train.shape = (days * train_split - (look_back + 1), look_back, 25)

## y_test.shape = (days * train_split - (look_back + 1), 10)

## X_test.shape = (days * (1 - train_split) - (look_back + 1), look_back, 25)

## y_test.shape = (days * (1 - train_split) - (look_back + 1), 10)
```

### Features

|Vector|Description|
|------|-----------|
|Vector 0|Volumes                 |
|Vector 1|Prices                  |
|Vector 2|SMA                     |
|Vector 3|EMA                     |
|Vector 4|Wilder MA               |
|Vector 5|Upper Bolinger Band     |
|Vector 6|Lower Bolinger Band     |
|Vector 7|Accumulative Swing Index|
|Vector 8|Average True Range      |
|Vector 9|Balance of Power        |
|Vector 10|Gopalakrishnan Range Index|
|Vector 11|Price - Pivot Point    |
|Vector 12|Pring's Know Sure Thing - SMA(Pring's Know Sure Thing)|
|Vector 13|MACD - SMA(MACD)       |
|Vector 14|d KST * d TRIX         |
|Vector 15|TRIX - MA(TRIX)        |
|Vector 16|RSI                    |
|Vector 17|MA(OHLC/4, 1)          |
|Vector 18|MA(OHLC/4, 3)          |
|Vector 19|MA(OHLC/4, 5)          |
|Vector 20|MA(OHLC/4, 7)          |
|Vector 21|MA(OHLC/4, 9)          |
|Vector 22|West Texas             |
|Vector 23|Wilshire US Real Estate|
|Vector 24|SNP                    |

|Label|
|-----|
| -10% <= (p_1 - p_0)/p_0 < - 7% |
| - 7% <= (p_1 - p_0)/p_0 < - 5% |
| - 5% <= (p_1 - p_0)/p_0 < - 3% |
| - 3% <= (p_1 - p_0)/p_0 < - 1% |
| - 1% <= (p_1 - p_0)/p_0 <   1% |
|   1% <= (p_1 - p_0)/p_0 <   3% |
|   3% <= (p_1 - p_0)/p_0 <   5% |
|   5% <= (p_1 - p_0)/p_0 <   7% |
|   7% <= (p_1 - p_0)/p_0 <   9% |
|   9% <= (p_1 - p_0)/p_0 < 100% |

Where p_1 is the price at the predicted day and p_0 is the price at ```predicted day - label_range```