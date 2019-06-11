from iexfinance.stocks import Stock
from iexfinance.refdata import get_symbols
import pandas as pd


from datetime import datetime
from iexfinance.stocks import get_historical_data

class IEXData: 

	def __init__(self):
		self.data = []

	def get_symbols(self):

		symbols = get_symbols(output_format='pandas')
		return symbols
	'''

	def get_stock_price_for_ticker(self, company_ticker, start, end):
		df = get_historical_data(company_ticker, start, end)

		results = []
		for d in df:
			raw_date = d 
			processed_date = datetime.strptime(raw_date, '%Y-%m-%d')
			processed_date = (processed_date.year, processed_date.month, processed_date.day)

			open_price = df[d]['open']
			close_price = df[d]['close']
			high_price = df[d]['high']

			change = ((close_price - open_price)/(open_price))*100 
			#change = close_price
			#change = high_price
			#change = 1 if change > 0 else 0
			results.append((processed_date, change))

		return sorted(results)
	'''

	def get_stock_price_for_ticker(self, company_ticker, start, end):
		file_name = 'EOD-' + str(company_ticker) + '.csv'
		data = pd.read_csv(file_name)
		results = []
		for index, row in data.iterrows(): 
			raw_date = row['Date']
			processed_date = datetime.strptime(raw_date, '%Y-%m-%d')
			if (processed_date < start) or (processed_date > end):
				continue
			#processed_date = (processed_date.year, processed_date.month, processed_date.day)
			open_price = row['Open']
			close_price = row['Close']
			high_price = row['High']

			change = ((close_price - open_price)/(open_price))*100 

			results.append((processed_date, change))

		return sorted(results)


