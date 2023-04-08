# AnyFlightTracker Aircraft Tracker v2.5

April 2023: This has capability to post to: Twitter,Facebook,Mastodon,Discord
----------------------------------------------------------------
#################################################################
This is a heavily modified UNATTACHED fork from the
shbisson/OverPutney (https://github.com/shbisson/OverPutney)
repository modified with the amazing help of Scott Ladewig
(https://github.com/ladewig)
#################################################################

An ADSB trackingbot which can be utilized anywhere with or without with or without equipment. 
Code is configured so that the use of a local or global JSON file will allows it to monitor
aircraft anywhere there is coverage. This code will also post to Facebook, Twitter and 
Mastodon (Multiple Servers) and is  written in Python for use with the tar1090 aircraft mapping 
tool.

Originally based on the twitterbot OverPutney by @shbisson 
(https://github.com/shbisson/OverPutney) and updated and modified with the assistance of 
Scott Ladewig (https://github.com/ladewig)

For aircraft images of aircraft are downloaded from planespotters.net api and images are credited 
on the fly using PILLOW and included Arial.ttf font.

Does not pre-load webpage. Screenshot taken only when environment is triggered.

Read the INSTALL.txt file for a very detailed, step by step guide to installing this bot on your system. 
There is also a install.sh file included that will step through all the steps needed to install this bot.

SUDO access is needed to install all the needed components. Bot will run as a user and not as root. 

The instructions were created step by step after moving my operational system from a clean install of Ubuntu 
on a x64 machine as well as a clean install on a Raspberry Pi 4B.

Configurations are mainly controlled by the config.ini file.

Advanced use: ability to track anywhere using latitude/longitude and access to global map and data/aircraft.json file. 

The installation and operation is very straightforward and works amazingly well. The hardest part was navigating the Facebook developer site to create the correct application and obtain the correct keys that allowed for posting to a Facebook Page of a profile.

See my operational setup at:

### Physical Equipment ###
  https://adsb.pro/@overbellevue (Mastodon)  <- Mastodon Server
  https://twitter.com/sarpy_spotter  <- Twitter
  https://www.facebook.com/RadarOverBellevue/  <- Facebook
  https://discord.gg/sA4RFkMh4V <- Discord Server

### Virtual Bot with no equipment ####
  https://adsb.pro/@riadsb  (Mastodon) <- Rhode Island & Boston Logan Airport
  https://adsb.pro/@hawaii  (Mastodon) <- Honolulu Hawaii

ACCESS TO GLOBAL DATA JSON IS AVAILABLE FOR $3/month per IP address - email info@adsb.pro for more information. This allows for bots to be setup without any equipment
at designated coordinates. Example:  https://adsb.pro/@riadsb is a bot used in this method that posts to Mastodon and has absolutly no physical
presense in that location. http://pawtucket.rtmladsb.com is the map used for screen captures (not data).

ACCESS TO PRIVATELY MAINTAINED AIRCRAFT DATABASE IS AVAILABLE FOR $2/month per IP address. This will bypass the included API interface that relies on a 3rd party.
