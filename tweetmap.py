import tweetstream
import settings
import json
import requests
from flask import Flask
from flask import Response
from flask import send_file
from flask import render_template

MAX_POINTS = 1000
app = Flask(__name__)
# Ireland longtitude, latitude from south west to north east
locations = ['-10, 51', '-6, 54']

def tweet_stream():
	with tweetstream.FilterStream(settings.twitterUsername, settings.twitterPassword, locations=locations) as stream:
		for tweet in stream:
			# Why is it like this? O_o
			if tweet['coordinates'] != None:
				text = tweet['text']
				coordinates = tweet['coordinates']['coordinates']
				yield 'data: %s\n\n' % json.dumps({'text': text, 'coordinates': coordinates})
			else:
				# figured out why, see http://stackoverflow.com/questions/3836304/why-are-some-geo-tagged-tweets-null-twitter-streaming-api
				# The Streaming API matches against geo, coordinates, and place
				# Sample place parameter
				# Do it later
				# {
				#     "geo": null,
				#     "coordinates": null,
				#     "place": {
				#         "country_code": "US",
				#         "bounding_box": {
				#             "type": "Polygon",
				#             "coordinates": [[[ - 77.119759, 38.791645], [ - 76.909393, 38.791645], [ - 76.909393, 38.995548], [ - 77.119759, 38.995548]]]
				#             },
				#         "place_type": "city",
				#         "country": "United States",
				#         "attributes": {},
				#         "full_name": "Washington, DC",
				#         "name": "Washington",
				#         "url": "http:\/\/api.twitter.com\/1\/geo\/id\/01fbe706f872cb32.json",
				#         "id": "01fbe706f872cb32"
				#     },
				#     "user": {
				#     },
				#     "id": 73218362645282816
				# }
				pass

@app.route('/tweets')
def tweets():
    return Response(tweet_stream(), headers={'Content-Type':'text/event-stream'})

@app.route('/static/<filename>')
def serve_static(filename):
	return send_file('static/' + filename)


def get_previous_tweets():
	geocode = '52,-9,260km'
	rpp = 100
	url = 'http://search.twitter.com/search.json?q=&geocode=%s&rpp=%s&result_type=recent' % (geocode, rpp)

	# FIXME
	# This should go the other way! 
	# First page is latest tweets, so they should be hotest
	# Meaning they should be added last
	page = 1
	counter = 0;
	json_data = requests.get(url + '&page=%s' % page).json()
	data = []
	tweets = []
	while 'results' in json_data and counter <= 1000:
		for result in json_data['results']:
			if result['geo'] != None:
				counter += 1
				# FIXME
				# should be getting LATEST 15 tweets
				# i guess fixing the overarching problem would fix this as well
				if len(tweets) < 15:
					tweets.append(result['text'])
				lat = result['geo']['coordinates'][0]
				lng = result['geo']['coordinates'][1]
				# cooldown previous points
				for point in data:
					point['count'] -= 1
				data.append({'lat': lat, 'lng': lng, 'count': MAX_POINTS})
		page += 1
		json_data = requests.get(url + '&page=%s' % page).json()
	print 'counter: %s' % counter
	return data, tweets

@app.route('/')
def index():
	data, tweets = get_previous_tweets()
	return render_template('map.html', max_points=MAX_POINTS, data=data, tweets=json.dumps(tweets))

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')