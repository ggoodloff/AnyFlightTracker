# AircraftTracker Facebook & Twitter Bot v2
Multi Images to Facebook
----------------------------------------------------------------------------------------------
#############################################################################################################
#This is a heavily modified UNATTACHED fork from the shbisson/OverPutney (https://github.com/shbisson/OverPutney) repository#
#modified with the amazing help of Scott Ladewig (https://github.com/ladewig)                               #
#############################################################################################################

An ADSB trackingbot that will post to Facebook and/or Twitter written in Python for use with the tar1090 aircraft mapping tool.

Based on the twitterbot OverPutney by @shbisson (https://github.com/shbisson/OverPutney) and updated and modified with the assistance of Scott Ladewig (https://github.com/ladewig)

For facebook - images of aircraft are downloaded from planespotters.net api and images are credited on the fly using PILLOW and included Arial.ttf font.
Does not pre-load webpage. Screenshot taken only when environment is triggered.

Read the INSTALL.txt file for a very detailed, step by step guide to installing this twitterbot/facebook-pages-bot on your system. 
The instructions were created step by step after moving my operational system from my Raspberry Pi to a clean install of Ubuntu on a x64 machine.

Configurations are mainly controlled by the config.ini file.

Advanced use: ability to track anywhere using latitude/longitude and access to global map and data/aircraft.json file. 

The installation and operation is very straightforward and works amazingly well. The hardest part was navigating the Facebook developer site to create the correct application and obtain the correct keys that allowed for posting to a Facebook Page of a profile.

See my operational setup at:
  http://facebook.com/RadarOverBellevue
  http://twitter.com/sarpy_spotter

