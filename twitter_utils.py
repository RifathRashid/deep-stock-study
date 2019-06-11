import os
import json 
import numpy
from datetime import datetime 

class TwitterApiData:

	def __init__(self):
		self.data = []


	def get_data_file(self, year):
		dir_name = 'trump_tweet_data_archive'
		base_file = 'condensed_' + str(year) + '.json'
		result = os.path.join(dir_name, base_file)
		return result 

	def get_posts(self, year, additional_features):

		data_file = self.get_data_file(year)
		with open(data_file) as json_file:
			data = json.load(json_file)

		tweets = []
		for raw_tweet in data: 
			raw_date = raw_tweet['created_at']
			processed_date = None
			if year == 2019:
				processed_date = datetime.strptime(raw_date, '%Y-%m-%d %H:%M:%S')
			else:
				processed_date = datetime.strptime(raw_date, '%a %b %d %H:%M:%S %z %Y')
			processed_date = datetime(processed_date.year, processed_date.month, processed_date.day)

			raw_text = raw_tweet['text']
			if year == 2019: 
				raw_text = str((raw_text[1:])[1:-1])

			tweet = [processed_date, raw_text]

			for f in additional_features:
				value = raw_tweet[f]
				if f == 'retweet_count':
					value = int(value)

				tweet.append(value)
			tweet = tuple(tweet)
			tweets.append(tweet)

		tweets = sorted(tweets)
		return tweets






		