#####################################    CREDITS    #########################################################
#This is an UNATTACHED fork from the shbisson/OverPutney (https://github.com/shbisson/OverPutney) repository#
#modified with the amazing help of Scott Ladewig (https://github.com/ladewig)                               #
#############################################################################################################
import requests
import json

def get_aircraft_photo(hex):
	api_url = "https://api.planespotters.net/pub/photos/hex/{}".format(hex)
	session = requests.Session()
	session.headers.update({'User-Agent':'Mozilla/5.0 (Linux; Android 13; SM-S908U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Mobile Safari/537.36'})
	photo_json = session.get(api_url).text
	photo_data = json.loads(photo_json)['photos']
	try:
		photo_url = photo_data[0]['thumbnail_large']['src']
		photo_credit = photo_data[0]['photographer']
	except IndexError as err: 
		photo_url = "https://skynetaero.com/wp-content/uploads/2020/08/Commercial-ASD-B-1024x536.jpg"
		photo_credit = " "


	return (photo_url, photo_credit)

