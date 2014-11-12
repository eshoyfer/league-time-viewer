import urllib2
import json
import time
from datetime import datetime
import plotly.plotly as py
from plotly.graph_objs import *
from collections import Counter

## API STUFF ##

# League of Legends
API_KEY = "d55fcba1-9126-4003-9180-b4765301f452"

# Plotly
PLOTLY_USERNAME = "swagacc"
PLOTLY_API_KEY = "80pu77z5iy"

API_KEY_QUERY = "?api_key=" + API_KEY
BASE_URL = "https://na.api.pvp.net"
SUMMONER_SEARCH = "/api/lol/na/v1.4/summoner/by-name/%s"
MATCH_HISTORY = "/api/lol/na/v2.2/matchhistory/%s"
SUMMONER_BY_ID = "/api/lol/na/v1.4/summoner/%s"

# Sign in to plotly
py.sign_in(PLOTLY_USERNAME, PLOTLY_API_KEY)

# Don't forget to insert the parameter into the string when you're actually working with it.
# Note: request must refer to one of the request types represented by a variable above.
def get_URL(request):
	return BASE_URL + request + API_KEY_QUERY

def get_dict(request, parameter):
	url = get_URL(request) % parameter
	request = urllib2.urlopen(url)
	json_result = request.read()
	data_dict = json.loads(json_result)
	return data_dict

def search_user(username):
	search_result = get_dict(SUMMONER_SEARCH, username)
	return search_result

def get_match_history(str_id):
	match_history = get_dict(MATCH_HISTORY, str_id)
	return match_history

def get_user_by_id(str_id):
	results = get_dict(SUMMONER_BY_ID, str_id)
	return results[str_id]['name']

def get_match_times(str_id):
	history = get_match_history(str_id)['matches']
	times = []
	for game in history:
		print game
		start_time = game['matchCreation']
		times.append(start_time)
	return times

def get_times_plot(username):
	match_times = get_match_times(username)

	time_now = str(time.time())[:-3]

	# Times need to be meaningful.
	# The League API returns stuff in terms of seconds passed
	# since the Unix Epoch.
	rounded_times = []

	for this_time in match_times:
		print this_time, "YO"
		print int(this_time), "doubleyo"
		formatted_tuple = time.localtime(int(this_time)/1000) # Uses local time, 24-hour based
		hour = formatted_tuple[3]
		minute = formatted_tuple[4]

		# Rounding

		if minute >= 30:
			hour += 1
			hour = hour % 24 # Accounting for the rollover case

		rounded_times.append(hour)

		counted = Counter(rounded_times)

		hours_formatted = []
		for hour in counted.keys():
			formatted = str(hour) + ":00"
			hours_formatted.append(formatted)

		trace1 = Scatter(
			x=hours_formatted, # Times
			y=counted.values(), # Number of game occurrences at that time
			mode='markers'
		)

		data = Data([trace1])

		layout = Layout(
			title='Games Played by Hour',
			xaxis=XAxis(
				title='Time (24H)'
			),
			yaxis=YAxis(
				title='Number of Games'
			)
		)

		fig = Figure(data=data, layout=layout)

		# Saves image as time now

		filename = time_now + ".png"
		py.image.save_as(fig, "static/" + filename)

	return filename







