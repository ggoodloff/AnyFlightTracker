#####################################    CREDITS    #########################################################
#This is an UNATTACHED fork from the shbisson/OverPutney (https://github.com/shbisson/OverPutney) repository#
#modified with the amazing help of Scott Ladewig (https://github.com/ladewig)                               #
#############################################################################################################
# Using the api.joshdouch.me calls to get data from ICAO hex

import requests

def regis(hex):
        """
        Gets registration from hex
        """
        if hex == None:
                 return None
        regis = requests.get(f"https://hexdb.io/hex-reg?hex={hex}")
        if regis.text == "n/a":
                regis.text=" "
        return regis.text

def plane(hex):
        """
        Gets plane from hex
        """
        if hex == None:
                 return None
        plane = requests.get(f"https://hexdb.io/hex-type?hex={hex}")
        if plane.text == "n/a":
                plane.text=""
        return plane.text

def oper(hex):
        """
        Gets plane from hex
        """
        if hex == None:
                 return None
        oper = requests.get(f"https://hexdb.io/hex-airline?hex={hex}")
        if oper.text == "n/a":
                oper.text = ""
        return oper.text

def route(flight):
        """
        Gets route from callsign
        """
        if flight == None:
                         return None
        # ICAOroute = requests.get(f"https://api.joshdouch.me/callsign-route.php?callsign={flight}")
        origin = requests.get(f"https://hexdb.io/callsign-origin_icao?callsign={flight}")
        destination = requests.get(f"https://hexdb.io/callsign-des_icao?callsign={flight}")
        origin_IATA = requests.get(f"https://hexdb.io/callsign-origin_iata?callsign={flight}")
        destination_IATA = requests.get(f"https://hexdb.io/callsign-des_iata?callsign={flight}")
        origin_name = requests.get(f"https://hexdb.io/iata-airport?iata={origin.text}")
        destination_name = requests.get(f"https://hexdb.io/iata-airport?iata={destination.text}")
        route = requests.get(f"https://hexdb.io/callsign-origin_icao?callsign={flight}")
        if route == "n/a-n/a n/a to n/a":
                route = ""
        return route
        droute = origin_name.text + " to " + destination_name.text
        if droute == "n/a-n/a n/a to n/a":
                droute = ""
        return droute

def droute(flight):
        """
        Gets route from callsign
        """
        if flight == None:
                         return None
        # ICAOroute = requests.get(f"https://api.joshdouch.me/callsign-route.php?callsign={flight}")
        origin = requests.get(f"https://hexdb.io/callsign-origin_icao?callsign={flight}")
        destination = requests.get(f"https://hexdb.io/callsign-des_icao?callsign={flight}")
        origin_IATA = requests.get(f"https://hexdb.io/callsign-origin_iata?callsign={flight}")
        destination_IATA = requests.get(f"https://hexdb.io/callsign-des_iata?callsign={flight}")
        origin_name = requests.get(f"https://hexdb.io/iata-airport?iata={origin.text}")
        destination_name = requests.get(f"https://hexdb.io/iata-airport?iata={destination.text}")
        droute = origin_name.text + " to " + destination_name.text
        if droute == "n/a-n/a n/a to n/a":
                droute = ""
        return droute
