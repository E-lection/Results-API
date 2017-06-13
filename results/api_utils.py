import urllib2
import urllib
import json

PIN_VERIFICATION_URL = 'http://pins.eelection.co.uk/verify_pin_code_and_make_ineligible/'

def verify_pin_and_make_ineligible(station_id, pin_code):
    url = PIN_VERIFICATION_URL + '/station_id/' + urllib.quote(str(station_id)) + '/pin_code/' + urllib.quote(str(pin_code))
    response = urllib2.urlopen(url)
    return json.loads(response.read())['success']
