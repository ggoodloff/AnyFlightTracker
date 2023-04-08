#####################################    CREDITS    #########################################################
#This is an UNATTACHED fork from the shbisson/OverPutney (https://github.com/shbisson/OverPutney) repository#
#modified with the amazing help of Scott Ladewig (https://github.com/ladewig)                               #
#############################################################################################################
#
# tracker.py
#
# kevinabrandon@gmail.com
#
# modified by
#
# simon@sandm.co.uk
#

import sys
import traceback
import time
import psutil
import shutil
import tweepy #added
import os
from time import sleep
from configparser import ConfigParser
from string import Template
import requests
import json
from mastodon import Mastodon  # added
from discord_webhook import DiscordWebhook, DiscordEmbed


import datasource
import fa_api
import flightdata
import geomath
import screenshot
import aircraftdata
import planespotters
import ac_query_tr

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont


# Read the configuration file for this application.
parser = ConfigParser()
parser.read('config.ini')

# Assign Database Variables
hexdb_enable = parser.getboolean('database', 'hexdb_enable')
mysql_enable = parser.getboolean('database', 'mysql_enable')

# Assign AboveTustin variables.
abovetustin_distance_alarm = float(parser.get('abovetustin', 'distance_alarm'))	# The alarm distance in miles.
abovetustin_elevation_alarm = float(parser.get('abovetustin', 'elevation_alarm'))	# The angle in degrees that indicates if the airplane is overhead or not.
abovetustin_wait_x_updates = int(parser.get('abovetustin', 'wait_x_updates'))	# Number of updates to wait after the airplane has left the alarm zone before tweeting.
abovetustin_sleep_time = float(parser.get('abovetustin', 'sleep_time'))		# Time between each loop.

# Assign FlightAware variables.
fa_enable = parser.getboolean('flightaware', 'fa_enable')
fa_username = parser.get('flightaware', 'fa_username')
fa_api_key = parser.get('flightaware', 'fa_api_key')

# Assign Twitter variables.
twitter_consumer_key = parser.get('twitter', 'consumer_key')
twitter_consumer_secret = parser.get('twitter', 'consumer_secret')
twitter_access_token = parser.get('twitter', 'access_token')
twitter_access_token_secret = parser.get('twitter', 'access_token_secret')

# Enable Socials
twitter_enable = parser.getboolean('twitter','twitter_enable')
fb_enable = parser.getboolean('facebook','fb_enable')
mastodon_enable = parser.getboolean('mastodon','mastodon_enable')
discord_enable = parser.getboolean('discord','discord_enable')


# Facebook variables and function
auth_token = parser.get('facebook','facebook_access_token_1') #facebook multipicture post
page_id = parser.get('facebook', 'page_id_1') #facebook multipicture post

# Mastodon variables
mastodon_token = parser.get('mastodon','token')
mastodon_server = parser.get('mastodon','server')
#mastodon_token2 = parser.get('mastodon','token2')
#mastodon_server2 = parser.get('mastodon','server2')

#Discord Variables
discord_webhook = parser.get('discord', 'webhook')
post_username = parser.get('discord', 'post_username')
post_title = parser.get('discord', 'post_title')
post_footer = parser.get('discord', 'post_footer')
post_color = parser.get('discord', 'post_color')


#Image variables
img_path_1 = parser.get('images','img_path_1') # FB Post Image - Duplicated from Image_3 in CORE section
img_path_2 = parser.get('images','img_path_2') # Image downloaded from planespotters.net
img_path_3 = parser.get('images','img_path_3') # Set in screenshot.py - screenshot of tar1090 screen when alarm is triggered


########################  Build Facebook / Twitter Structure  ####################################
def FB(a):
	# compile the template arguments
	templateArgs = dict()
	flight = a.flight or a.hex
	flight = flight.replace(" ", "")
	templateArgs['flight'] = flight
	templateArgs['icao'] = a.hex
	templateArgs['icao'] = templateArgs['icao'].replace(" ", "")
	if mysql_enable:
		templateArgs['model'] = ac_query_tr.model(a.hex)
		templateArgs['typecode'] = ac_query_tr.typecode(a.hex)
		templateArgs['owner'] = ac_query_tr.owner(a.hex)
		templateArgs['myoper'] = ac_query_tr.myoper(a.hex)
	if hexdb_enable:
		templateArgs['regis'] = aircraftdata.regis(a.hex)
		templateArgs['plane'] = aircraftdata.plane(a.hex)
		templateArgs['oper'] = aircraftdata.oper(a.hex)
		templateArgs['route'] = aircraftdata.route(flight)
	templateArgs['dist_mi'] = "%.1f" % a.distance
	templateArgs['dist_km'] = "%.1f" % geomath.mi2km(a.distance)
	templateArgs['dist_nm'] = "%.1f" % geomath.mi2nm(a.distance)
	templateArgs['alt_ft'] = a.altitude
	templateArgs['alt_m'] = "%.1f" % geomath.ft2m(a.altitude)
	templateArgs['el'] = "%.1f" % a.el
	templateArgs['az'] = "%.1f" % a.az
	templateArgs['heading'] = geomath.HeadingStr(a.track)
	templateArgs['speed_mph'] = "%.1f" % a.speed
	templateArgs['speed_kmph'] = "%.1f" % geomath.mi2km(a.speed)
	templateArgs['speed_kts'] = "%.1f" % geomath.mi2nm(a.speed)
	templateArgs['time'] = a.time.strftime('%H:%M:%S')
	templateArgs['squawk'] = a.squawk
	templateArgs['vert_rate_ftpm'] = a.vert_rate
	templateArgs['vert_rate_mpm'] = "%.1f" % geomath.ft2m(a.vert_rate)
	templateArgs['rssi'] = a.rssi
	if fa_enable and faInfo:
		templateArgs['orig_name'] = faInfo['orig_name']
		templateArgs['dest_name'] = faInfo['dest_name']
		if faInfo['orig_alt']:
			templateArgs['orig_alt'] = faInfo['orig_alt']
		else:
			templateArgs['orig_alt'] = faInfo['orig_code']
		if faInfo['dest_alt']:
			templateArgs['dest_alt'] = faInfo['dest_alt']
		else:
			templateArgs['dest_alt'] = faInfo['dest_code']
		if faInfo['dest_city']:
			templateArgs['dest_city'] = faInfo['dest_city']
		if faInfo['orig_city']:
			templateArgs['orig_city'] = faInfo['orig_city']
		if templateArgs['orig_alt'] and templateArgs['dest_alt']:
			tweet = Template(parser.get('tweet', 'fa_tweet_template')).substitute(templateArgs)
		else:
			tweet = Template(parser.get('tweet', 'tweet_template')).substitute(templateArgs)
	else:
		tweet = Template(parser.get('tweet', 'tweet_template')).substitute(templateArgs)
	#conditional hashtags:
	hashtags = []
	if a.time.hour < 6 or a.time.hour >= 22 or (a.time.weekday() == 7 and a.time.hour < 8):
		hashtags.append(" #AfterHours")
	if a.altitude < 1000:
		hashtags.append(" #LowFlier")
	if a.altitude >= 1000 and a.altitude < 2500 and (templateArgs['heading'] == "S" or templateArgs['heading'] == "SW"):
		hashtags.append(" #ProbablyLanding")
	if a.altitude > 20000 and a.altitude < 35000:
		hashtags.append(" #UpInTheClouds")
	if a.altitude >= 35000:
		hashtags.append(" #WayTheHeckUpThere")
	if a.speed > 300 and a.speed < 500:
		hashtags.append(" #MovingQuickly")
	if a.speed >= 500 and a.speed < 770:
		hashtags.append(" #FlyingFast")
	if a.speed >= 700:
		hashtags.append(" #SpeedDemon")

	# add the conditional hashtags as long as there is room in 140 chars
	for hash in hashtags: 
		if len(tweet) + len(hash) <= 300:
			tweet += hash

	# add the default hashtags as long as there is room
	for hash in parser.get('tweet', 'default_hashtags').split(' '):
		if len(tweet) + len(hash) <= 1000:
			tweet += " " + hash


###########  Call Planespotters function and download aircraft image  ##########################

	hex = templateArgs['icao']

	ps_photo = planespotters.get_aircraft_photo(hex)
	photo_url = ps_photo[0]
	photo_credit = ps_photo[1]

#	print(photo_url)
#	print(photo_credit)


	img_data = requests.get(photo_url).content
	with open(img_path_2, 'wb') as handler: ##
		handler.write(img_data)

	photo_file = img_path_2 # var of saved file used for manipulation

#########   Modify © photo overlay for planespotter photos  ########## 

	if not photo_credit == ' ':
		img = Image.open(photo_file) # Call draw Method to add 2D graphics in an image
		I1 = ImageDraw.Draw(img) # Add Text to an image
		I1.font = ImageFont.truetype("./font/arial.ttf", size=18)
		I1.text((10, 10), "Credit: "+ (photo_credit)+" - Planespotters.net", fill=(255, 255, 255)) # Display edited image
#		img.show() # Save the edited image
		img.save(photo_file)


#######################################################################

	return (tweet,photo_credit,photo_url) # <- allows variables to be carries out of function with return ()


############## Discord Server #########################################

def discordpost():

	fb_prep = FB(a[0])  #run FB function to downloads photo from planespotters.net and sets fb_tweet_msg variable
	discord_msg = (fb_prep[0])+" Photo by: "+(fb_prep[1])+" @ Planespotters.net"

	webhook = DiscordWebhook(
		url=discord_webhook,
		username = post_username
		)


	embed = DiscordEmbed(
    	title=post_title,
    	color=post_color
    	)

	embed.set_author(name='AnyFlightTracker', url='https://github.com/ggoodloff/AnyFlightTracker')


# Set `inline=False` for the embed field to occupy the whole line
	embed.add_embed_field(name="Details",
		value=discord_msg, 
		inline=False
		)

##embed.add_embed_field(name='Field 1', value='Details:')

# send two images
	with open(img_path_3, "rb") as f:
		webhook.add_file(file=f.read(), filename='screenshot.png')
	with open(img_path_2, "rb") as f:
		webhook.add_file(file=f.read(), filename='aircraft.jpg')


	embed.set_footer(text=post_footer)
	embed.set_timestamp()

	webhook.add_embed(embed)
	webhook.execute()

#######################################################################

############## Facebook multi_image post ##############################

def postImage(page_id, img):
	url = f"https://graph.facebook.com/{page_id}/photos?access_token=" + auth_token
	files = {
			'file': open(img, 'rb'),
			}
	data = {
		"published" : False
	}
	r = requests.post(url, files=files, data=data).json()
	return r

def multiPostImage(page_id):

	fb_prep = FB(a[0])  #run FB function to downloads photo from planespotters.net and sets fb_tweet_msg variable
	fb_tweet_msg = (fb_prep[0])+" Photo by: "+(fb_prep[1])+" @ Planespotters.net"

	imgs_id = []
	img_list = [img_path_3, img_path_2] #  <- modify this to reflect paths set in facebook section at line 64 above and [facebook] section of config file
	for img in img_list:
		post_id = postImage(page_id ,img)
		imgs_id.append(post_id['id'])

	args=dict()
	args["message"]=fb_tweet_msg
	for img_id in imgs_id:
		key="attached_media["+str(imgs_id.index(img_id))+"]"
		args[key]="{'media_fbid': '"+img_id+"'}"
	url = f"https://graph.facebook.com/{page_id}/feed?access_token=" + auth_token
	requests.post(url, data=args)


###########################  Mastodon Post  ####################################

def mastadonpost():

	fb_prep = FB(a[0])  #run FB function to downloads photo from planespotters.net and sets mastodon_msg variable
	mastodon_msg = (fb_prep[0])+" Photo by: "+(fb_prep[1])+" @ Planespotters.net"


	#   Set up Mastodon
	mastodon1 = Mastodon(
		access_token = mastodon_token,
		api_base_url = mastodon_server
	)
#	mastodon2 = Mastodon(
#		access_token = mastodon_token2,
#		api_base_url = mastodon_server2
#	)


########## Server 1 ##########
#uncomment image files used from [images] in config.ini - Mastadon can upload 4 images max per post
#	media1x1 = mastodon1.media_post(img_path_1, description="Github AnyFlightTracker by @rtmladsb:mastadon.social")
	media1x2 = mastodon1.media_post(img_path_2, description="Github AnyFlightTracker by @rtmladsb:mastadon.social")
	media1x3 = mastodon1.media_post(img_path_3, description="Github AnyFlightTracker by @rtmladsb:mastadon.social")
#	media1x4 = mastodon1.media_post(img_path_4, description="Github AnyFlightTracker by @rtmladsb:mastadon.social")
	mastodon1.status_post(mastodon_msg, media_ids=[media1x3,media1x2]) # Set order of image upload

########## Server 2 ##########
#uncomment image files used from [images] in config.ini - Mastadon can upload 4 images max per post
#	media2x1 = mastodon2.media_post(img_path_1, description="Github AnyFlightTracker by @rtmladsb:mastadon.social")
#	media2x2 = mastodon2.media_post(img_path_2, description="Github AnyFlightTracker by @rtmladsb:mastadon.social")
#	media2x3 = mastodon2.media_post(img_path_3, description="Github AnyFlightTracker by @rtmladsb:mastadon.social")
#	media2x4 = mastodon2.media_post(img_path_4, description="Github AnyFlightTracker by @rtmladsb:mastadon.social")
#	mastodon2.status_post(mastodon_msg, media_ids=[media2x3,media2x2]) # Set order of image upload


########################   TWITTER POST  ##################################

def twitterpost():
	fb_prep = FB(a[0])  #run FB function to downloads photo from planespotters.net and sets fb_tweet_msg variable
	twitter_auth_keys = {


#variables for accessing twitter API
		"consumer_key"          : (twitter_consumer_key),
		"consumer_secret_key"   : (twitter_consumer_secret),
		"access_token"          : (twitter_access_token),
		"access_token_secret"   : (twitter_access_token_secret)
	}

	auth = tweepy.OAuthHandler(
		twitter_auth_keys['consumer_key'],
		twitter_auth_keys['consumer_secret_key']
			)
	auth.set_access_token(
		twitter_auth_keys['access_token'],
		twitter_auth_keys['access_token_secret']
			)
	api = tweepy.API(auth)

	twittermsg = fb_prep[0]
	screenshot = img_path_3

# Upload image
	media = api.media_upload(screenshot)

# Post tweet with image
	post_result = api.update_status(status=twittermsg, media_ids=[media.media_id])

#######################################################################


##################  Core  #############################################


if __name__ == "__main__":

	lastReloadTime = time.time()
	display = datasource.get_map_source()
	# dictonary of all aircraft that have triggered the alarm
	# Indexed by it's hex code, each entry contains a tuple of
	# the aircraft data at the closest position so far, and a
	# counter.  Once the airplane is out of the alarm zone,
	# the counter is incremented until we hit [abovetustin_wait_x_updates]
	# (defined above), at which point we then Tweet
	alarms = dict()

	fd = datasource.get_data_source()
	lastTime = fd.time

	while True:
#		if time.time() > lastReloadTime + 3600 and len(alarms) == 0:
		if time.time() > lastReloadTime + 540 and len(alarms) == 0:	# Adjust this time (in seconds) if chromium cannot keep up based on server resources <- prevents zombie process
#			display.reload()
			lastReloadTime = time.time()

		sleep(abovetustin_sleep_time)
		fd.refresh()
		if fd.time == lastTime:
			continue
		lastTime = fd.time

#		print("Now: {}".format(fd.time))

		current = dict() # current aircraft inside alarm zone

		# loop on all the aircarft in the receiver
		for a in fd.aircraft:
			# if they don't have lat/lon or a heading skip them
			if a.lat == None or a.lon == None or a.track == None:
				continue
			# check to see if it's in the alarm zone:
			if a.distance < abovetustin_distance_alarm or a.el > abovetustin_elevation_alarm:
				# add it to the current dictionary
				current[a.hex] = a 
				if a.hex in alarms:
					#if it's already in the alarms dict, check to see if we're closer
					if a.distance < alarms[a.hex][0].distance:
						#if we're closer than the one already there, then overwrite it
						alarms[a.hex] = (a, 0)
				else:
					#add it to the alarms
					alarms[a.hex] = (a, 0)

		finishedalarms = []
		# loop on all the aircraft in the alarms dict
		for h, a in alarms.items():
			found = False
			# check to see if it's in the current set of aircraft
			for h2, a2 in current.items():
				if h2 == h:
					found = True
					break
			# if it wasn't in the current set of aircraft, that means it's time to tweet!
			if not found:
				if a[1] < abovetustin_wait_x_updates:
					alarms[h] = (a[0], a[1]+1)
				else:
					havescreenshot = False
					if display != None:
						print("time to create screenshot of {}:".format(a[0]))
						hexcode = a[0].hex
						hexcode = hexcode.replace(" ", "")
						hexcode = hexcode.replace("~", "")
						havescreenshot = display.clickOnAirplane(hexcode) # call screenshot.py to grab image for post

					if fa_enable:
						print("Getting FlightAware flight details")
						faInfo = fa_api.FlightInfo(a[0].flight, fa_username, fa_api_key)
					else:
						faInfo = False
					try:
						if twitter_enable:
							print("Post to Twitter!!!!!")
							twitterpost()
							print("Done....")
						if fb_enable:
#							shutil.copyfile(img_path_3, img_path_1)
							print("Post to Facebook!!!!!")
							multiPostImage(page_id)
							print("Done....")
							print("#################################################################")
							print("")
						if mastodon_enable:
							print("Post to Masodon!!!!!")
							mastadonpost()
							print("Done....")
							print("#################################################################")
							print("")
						if discord_enable:
							print("Post to Discord Channel!!!!!")
							discordpost()
							print("Done....")
							print("#################################################################")
							print("")

						#remove generated image files so not duplicated in next post
#						os.remove(img_path_1) #removes facebook file 
#						os.remove(img_path_2) #removes planespotters.net file
#						os.remove(img_path_3) #removes screenshot file
					except Exception:
							print("Problems with FB or Twitter post:")
							traceback.print_exc()
					finishedalarms.append(a[0].hex)

		# for each alarm that is finished, delete it from the dictionary
		for h in finishedalarms:
			del(alarms[h])

		# flush output for following in log file
		sys.stdout.flush()
