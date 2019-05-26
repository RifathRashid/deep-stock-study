from iexfinance.stocks import Stock
from iexfinance.refdata import get_symbols


from datetime import datetime
from iexfinance.stocks import get_historical_data

class IEXData: 

	def __init__(self):
		self.data = []

	def get_symbols(self):

		symbols = get_symbols(output_format='pandas')
		return symbols

	def get_stock_price_for_ticker(self, company_ticker):
		start = datetime(2018, 1, 1)
		end = datetime(2019, 1, 1)

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
			#change = high_price
			results.append((processed_date, change))

		return sorted(results)


