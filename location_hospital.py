# from googleplaces import GooglePlaces, types, lang
# import requests
# import json
#
# # send_url = 'http://freegeoip.net/json'
# # r = requests.get(send_url)
# # j = json.loads(r.text)
# # print(j)
# # lat = j['latitude']
# # lon = j['longitude']
# def get_location():
# 	API_KEY = 'AIzaSyBPNgFZT6ZUIN2Wsrk3GOSgo67NAKseTIA'
#
# 	google_places = GooglePlaces(API_KEY)
#
# 	query_result = google_places.nearby_search(
# 			# lat_lng ={'lat': 46.1667, 'lng': -1.15},
# 			lat_lng ={'lat': 28.4089, 'lng': 77.3178},
# 			radius = 5000,
# 			# types =[types.TYPE_HOSPITAL] or
# 			# [types.TYPE_CAFE] or [type.TYPE_BAR]
# 			# or [type.TYPE_CASINO])
# 			types =[types.TYPE_HOSPITAL])
#
# 	if query_result.has_attributions:
# 		print (query_result.html_attributions)
#
#
#
# 	for place in query_result.places:
# 		print(place)
# 		# place.get_details()
# 		print (place.name)
# 		print("Latitude", place.geo_location['lat'])
# 		print("Longitude", place.geo_location['lng'])
# 		print()

import googlemaps
import pandas as pd
# get_location()

# def miles_to_meters():
# 	try:
# 		return miles*1
