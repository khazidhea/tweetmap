import requests

geocode = '53,-8,250km'
rpp = 100
url = 'http://search.twitter.com/search.json?q=&geocode=%s&rpp=%s&result_type=recent' % (geocode, rpp)

page = 1
counter = 0;
json_data = requests.get(url + '&page=%s' % page).json()
while 'results' in json_data and counter <= 1000:
	for result in json_data['results']:
		if result['geo'] != None:
			counter += 1
			print result['geo']
	page += 1
	json_data = requests.get(url + '&page=%s' % page).json()

print 'counter: %s' % counter