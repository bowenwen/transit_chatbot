#from rasa_core.actions import Action
#from rasa_core.events import SlotSet
from rasa_core_sdk import Action
from rasa_core_sdk.events import SlotSet

import requests
import xml.etree.ElementTree as ET
import pandas as pd
import datetime

class NextbusApiAction(Action):
    def name(self):
        return "action_next_bus"

    def run(self, dispatcher, tracker, domain):
        
        with open('keys/nextbus_api_key.txt', 'r') as myfile:
            nextbus_api_key = myfile.read()
            
        line_number = tracker.get_slot('line_number')
        stop_number = tracker.get_slot('stop_number')
        
        req = 'http://api.translink.ca/rttiapi/v1/stops/'+stop_number+'/estimates?apikey='+nextbus_api_key+'&routeNo='+line_number
        resp = requests.get(req)
        root = ET.fromstring(resp.text)
        
        xmlstr = str(ET.tostring(root, encoding='utf8', method='text'))

        if '200' in str(resp): #valid response code
            nbs = []
            for nb in root:
                r = nb.find('RouteNo').text
                for s in nb.find('Schedules'):
                    t = s.find('ExpectedLeaveTime').text
                    nbs.append((r,t))

            nbs=pd.DataFrame(nbs,columns=('route','lvtime'))
            nbs.sort_values(['route','lvtime'])

            lvtime = nbs.iloc[0].lvtime
            
            dispatcher.utter_message("Your next bus will arrive at: {}".format(lvtime))
        else:
            dispatcher.utter_message('Hmm ... something went wrong :(\nInvalid bus number and/or stop number combination specified. Make sure that this bus number runs at the stop number you specified.\nPlease use a valid bus number is 3 digits, for example 003, 590. For community shuttle or night bus routes, please use "C" or "N" followed by up to 2 digits, i.e. N9, C22')

import json
import urllib.request, urllib.parse, urllib.error
import time
import re
#from IPython.core.display import display, HTML

#define regex to strip postal code from address
postalcode_re = re.compile(r'[A-Z]\d[A-Z] *\d[A-Z]\d')
def remove_postalcode(text):
    return postalcode_re.sub('', text)

#define regex to strip html tags from instructions
htmltags_re = re.compile(r'<[^>]+>')
def remove_htmltags(text):
    return htmltags_re.sub(' ', text)

#base url for api call
url_base = 'https://maps.googleapis.com/maps/api/directions/json?'

#mode of travel
mode = 'transit'

#set departure time as now -- can be changed later to provide directions in the future
departure_time = int(time.time())

class TripApiAction(Action):
    def name(self):
        return "action_trip"

    def run(self, dispatcher, tracker, domain):
        
        with open('keys/googlemaps_api_key.txt', 'r') as myfile:
            googlemaps_api_key = myfile.read()
        
        location_start = tracker.get_slot('location_start')
        location_end = tracker.get_slot('location_end')
        
        try:
            location_start = location_start + ' bc, Canada'
        except:
            pass
        
        try:
            location_end = location_end + ' bc, Canada'
        except:
            pass
        
        def direction(location_start, location_end, departure_time):
            '''
            Function to retreive Google Maps directions based on start and end locations, mode, and departure time.
            Mode is defined as transit and departure time is set to the current time of the request.
            '''
            #define query arguments
            query_args = {
                    'origin':location_start,
                    'destination':location_end,
                    'mode': mode,
                    'departure_time': departure_time
            }

            #encode the arguments
            encoded_args = urllib.parse.urlencode(query_args)

            #create the url with the encoded arguments and api key
            url = url_base + encoded_args
            encoded_url= url+'&key='+googlemaps_api_key

            #make the request and save the json response
            resp=urllib.request.urlopen(encoded_url).read()
            data = json.loads(resp)
            return(data)

        if location_start == '' or location_end == '' or location_start is None or location_end is None or location_start == location_end:
            print("Hmm ... Something went wrong! I can't find the location :(")
        else:
            data = direction(location_start, location_end, departure_time)

            #fallback if the resquest failed
            if data['status'] != 'OK': 
                instructions = 'No route found! Please give me more specific information about the locations of your trip origin and destination.'
                dispatcher.utter_message(instructions)
            else:
                #grab some information form the json response
                start_address = data['routes'][0]['legs'][0]['start_address']
                end_address = data['routes'][0]['legs'][0]['end_address']
                start_address = remove_postalcode(start_address).replace(', BC', '').replace(', Canada', '')
                end_address = remove_postalcode(end_address).replace(', BC', '').replace(', Canada', '')

                #create a map url
                map_url = 'https://www.google.com/maps?'+urllib.parse.urlencode({'saddr': start_address, 'daddr': end_address, 'dirflg': 'r'})

                travel_time = data['routes'][0]['legs'][0]['duration']['text']
                
                if travel_time == 0:
                    arrival_time = departure_time
                else:
                    arrival_time = data['routes'][0]['legs'][0]['arrival_time']['text']

                #grab instructions (step-by-step directions)
                #html_instructions can be found under routes/legs/steps or routes/legs/steps/steps
                #loop through all the steps and save instructions
                instructions = []
                num_iters = max(len(data['routes'][0]['legs'][0]['steps']), len(data['routes'][0]['legs'][0]['steps'][0]['steps']))
                for i in range (0, num_iters):
                    try:
                        instructions.append(remove_postalcode(data['routes'][0]['legs'][0]['steps'][i]['html_instructions'].replace('Subway towards', 'Take SkyTrain')).replace(', BC', '').replace(', Canada', '').replace('U-turn', 'turn'))
                    except:
                        pass
                    for j in range (0, num_iters):
                        try:
                            instructions.append(remove_postalcode(remove_htmltags(data['routes'][0]['legs'][0]['steps'][i]['steps'][j]['html_instructions'])).replace(', BC', '').replace(', Canada', '').replace('U-turn', 'turn'))
                        except:
                            pass
                        
                dispatcher.utter_message("Here are the directions from {} to {}:\n{}\n\nIf you leave now, you should arrive at {} by {}. Your trip should take around {}.\n".format(start_address, end_address, ("\n".join(instructions)), end_address, arrival_time, travel_time))
                dispatcher.utter_message("Click on the following link to view the direction on Google Maps:\n{}".format(map_url))
                #display(HTML("<a href="+map_url+">Google Maps Directions</a>"))
