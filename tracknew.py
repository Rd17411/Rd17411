# track location and time zone using the phone number
import phonenumbers
from phonenumbers import timezone
from phonenumbers import geocoder
from phonenumbers import carrier

import folium

from opencage.geocoder import OpenCageGeocode

number = input("Enter the phone number with country code : ")

phoneNumber = ""
Key = "edef9646a00b4465a0a03718f3374328"

# Using the geocoder module of phonenumbers to print the Location in console
yourLocation = geocoder.description_for_number(phoneNumber, "en")
print("location : " + yourLocation)

# Parsing String to the Phone number
phoneNumber = phonenumbers.parse(number)

# printing the timezone using the timezone module
timeZone = timezone.time_zones_for_number(phoneNumber)
print("timezone : " + str(timeZone))

# printing the geolocation of the given number using the geocoder module
geolocation = geocoder.description_for_number(phoneNumber, "en")
print("location : " + geolocation)

geocoder = OpenCageGeocode(Key)
query = str(yourLocation)

results = geocoder.geocode(query)
lat = results[0]['geometry']['lat']
lng = results[0]['geometry']['lng']
#
# Getting the map for the given latitude and longitude
myMap = folium.Map(loction=[lat, lng], zoom_start=9)

# Adding a Marker on the map to show the location name
folium.Marker([lat, lng], popup=yourLocation).add_to(myMap)

# printing the service provider name using the carrier module
service = carrier.name_for_number(phoneNumber, "en")
print("service provider : " + service)