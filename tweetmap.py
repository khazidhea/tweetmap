import tweetstream
import settings
import json
from flask import Flask
from flask import Response
from flask import send_file

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

@app.route('/')
def index():
	return send_file('static/map.html')



if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')