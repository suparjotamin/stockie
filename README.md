# Stockie

a stock screener to help the stock trader in making a trading decision. 

# Features in Stockie 1.0 
* **Multiple stock input** <br>
This version allows multiple inputs for stock to be analyzed or displayed later.  
* **Tabular of candlestick detector** <br>
you can show the table that shows whether a specific candlestick pattern has formed or not, with a total of more than 50 patterns.
* **Interactive Candlestick stock screener** <br>
an interactive HTML display of stock in candlestick.
* **Happening Pattern** <br>
a table that shows the currently happening pattern in the last 10 days with its accuracy based on the past and number their occurrence. 

# Setup
### Install the package
```python
!pip install stockie
```
### Import
```python
from Stockie.stockie import stockie
```

# Utilization
### Load in stock name
To load in the data, We use [yfinance](https://pypi.org/project/yfinance/) package which is included inside. So, the input just need to be the ticker of the stock which is registered.
```python
a = stockie(['UNVR.JK','AAPL','C6L.SI'])
```
### Display tabular data
```python
df = a.find_pattern()['AAPL']
```
<img alt="Notebook Widgets" src="https://github.com/suparjotamin/stockie/blob/master/Asset/sample%20tab%20gif.gif" width="600" />

### Stock screener
```python
a.get_candlestick_report()
```

<img alt="Notebook Widgets" src="https://github.com/suparjotamin/stockie/blob/master/Asset/screener.gif" width="600" />

# Bug
We found that some platforms can't display the interactive. You can download the HTML file instead until we fix this bug ( Google Colab, Jupyter Notebook, and Kaggle Notebook can do well)
```python
a.get_candlestick_report(create_HTML_file=True, location = 'your_directory/file.html')
```
