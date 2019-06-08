import twitter_utils as tu
import weather_utils as wu 
import iex_utils as iu 

from textblob import TextBlob
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression 

import post_to_bert as pb

def plot_polarity_histogram(polarity_scores, year, plot_color):
	polarity_scores = [p[3] for p in polarity_scores]
	values, base = np.histogram(polarity_scores, bins=40)


	plt.plot(base[:-1], values, c=plot_color, label=str(year))

	plt.xlabel("TextBlob Subjectivity Score")
	plt.ylabel("Number of Tweets")
	plt.title("Subjectivity Scores of Trump Tweets")
	#plt.show()

def get_polarity_from_tweets(tweet_data):
	polarity_results = []
	for tweet in tweet_data:
		date = tweet[0]
		formatted_date = (date.year, date.month, date.day)
		text = tweet[1]
		opinion = TextBlob(text)

		to_add = [formatted_date, text, opinion.sentiment.polarity, opinion.sentiment.subjectivity]
		for f in tweet[2:]:
			to_add.append(f)
		t_add = tuple(to_add)
		polarity_results.append(to_add)

	polarity_results = sorted(polarity_results)
	return polarity_results

def get_date_to_price_mapping(stock_data):
	result = {}
	for data_point in stock_data:
		date = data_point[0]
		price = data_point[1]

		if date not in result: 
			result[date] = price 
	return result 

def get_input_data(date_to_price, polarity_results):
	x = []
	y = []

	for pr in polarity_results: 
		tweet_date = pr[0]
		if tweet_date not in date_to_price:
			continue 
		x_to_add = pr[2:]
		x.append(x_to_add)
		y.append(date_to_price[tweet_date])

	return np.array(x), np.array(y)


def compare_stocks_to_tweets(symbols, polarity_results):
	results = []

	max_company_so_far = None
	number_of_companies = len(symbols)
	processed_so_far = 0

	for company_ticker in symbols:
		processed_so_far += 1 
		try: 

			iexstock_data = iexstock_data_api.get_stock_price_for_ticker(company_ticker)
			if len(iexstock_data) < 50:
				continue 
			date_to_price = get_date_to_price_mapping(iexstock_data)

			x, y = get_input_data(date_to_price, polarity_results)
			y = y.reshape(-1, 1)

			reg = LinearRegression().fit(x, y)
			score = reg.score(x, y)

			to_add = (score, company_ticker)
			if not max_company_so_far:
				max_company_so_far = to_add
			else: 
				if score > max_company_so_far[0]:
					max_company_so_far = to_add

			print(number_of_companies - processed_so_far)

			#print("Current evaluation: ", to_add, "         Max Company so far: ", max_company_so_far, "    Num Remaining: ", number_of_companies - processed_so_far)

			results.append(to_add)
		except:
			print(company_ticker, " attempt failed.")

	return results


def print_top_results(results):
	results = sorted(results, reverse=True)
	top_results = results[0:100]

	for tr in top_results:
		print(tr[1], tr[0])

'''

twitter_data_api = tu.TwitterApiData()
weather_data_api = wu.WeatherData()
iexstock_data_api = iu.IEXData()


year = 2018

additional_features = ['retweet_count']
trump_data = twitter_data_api.get_posts(year, additional_features)
polarity_results = get_polarity_from_tweets(trump_data)




color = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
years = [2016, 2017, 2018]
for i in range(len(years)):
	year = years[i]
	plot_color = color[i]
	trump_data = twitter_data_api.get_posts(year, additional_features)
	polarity_results = get_polarity_from_tweets(trump_data)
	plot_polarity_histogram(polarity_results, year, plot_color)


plt.legend()
plt.show()



symbols = iexstock_data_api.get_symbols()['symbol']

#symbols = ['AAPL', 'GOOGL']


results = compare_stocks_to_tweets(symbols, polarity_results)
print_top_results(results)
'''
year = 2018
twitter_data_api = tu.TwitterApiData()
additional_features = ['retweet_count']
trump_data = twitter_data_api.get_posts(year, additional_features)
be = pb.BertEncoder()

for post in trump_data:
	text = post[1]
	post_result = be.get_bert_embedding(text)
	print(post_result)















