# Location Finder Device with Full Stack WebApp to reduce COVID-19 spread

A pocket size device, in which if a person come under 2 meter distance with someone, presses a button on this device , which will send the location coordinates of the person with date-time in to the person's own unique database. To access and create database person has to register on this website : https://findloc.herokuapp.com..

The aim of this project is to reduce COVID-19 spread. If in future any COVID-19 patient's location matches with the location database of the person, then person aware about it because he has gone through that address and try to stay healthy as possible and take care of the health.

If everyone has this device especially in containment zone so everyone will be aware to keep minimum 2 meter distance.



#introduction 

When location information is needed in an electronic project, we normally think about a GPS module. But we know that mobile phones can get approximate location listening WiFi signals, when GPS is disabled or not usable because we are inside a building.

If your project needs approximate location or you are indoors, and it is connected to the Internet, you can use same mechanism to get latitude and longitude. So, you don't need additional hardware.

This code uses access to Google Maps GeoLocation API. Please check Google Policies.

Description
This is a library that sends Google Maps GeoLocaion API a request with a list of all WiFi AP's BSSID that your microcontroller listens to. Google, then answer with location and accuracy in JSON format.

Request body has this form:

{
	"wifiAccessPoints": [
		{"macAddress":"XX:XX:XX:XX:XX:XX","signalStrength":-58,"channel":11},
		{"macAddress":"XX:XX:XX:XX:XX:XX","signalStrength":-85,"channel":11},
		{"macAddress":"XX:XX:XX:XX:XX:XX","signalStrength":-82,"channel":1},
		{"macAddress":"XX:XX:XX:XX:XX:XX","signalStrength":-89,"channel":6},
		{"macAddress":"XX:XX:XX:XX:XX:XX","signalStrength":-86,"channel":13},
		{"macAddress":"XX:XX:XX:XX:XX:XX","signalStrength":-89,"channel":4},
		{"macAddress":"XX:XX:XX:XX:XX:XX","signalStrength":-42,"channel":5}
   ]
}

If information is correct, Google GeoLocation API response will be like this:

{
 "location": {
  "lat": 37.3689919,
  "lng": -122.1054095
 },
 "accuracy": 39.0
}

You need a google API key to validate with Google API. Navigate to Google Developers Console to enable GeoLocation API. Without this API key you will get an error as response.

Go to https://developers.google.com/maps/documentation/geolocation/intro to learn how to create an API key.

That API key has to be provided to WifiLocation class constructor like a String.

Once WifiLocation object is created, you can get location calling getGeoFromWiFi().

Google requires using secure TLS connection in order to use GeoLocation API. WifiLocation.cpp includes GoogleCA certificate to check server chain. This certificate may expire.

##################################
Using this code on ESP8266 or ESP32 platform does not require any external library.

In order to compile this on MRK1000, WiFi101 library is needed.


Limitations:

Notice that in order to get location this library has to scan for all surrounding Wi-Fi networks and make the request to Google API. Don't expect to get this immediately. All needed steps may take up to 20 seconds.

So, if your project is powered with batteries, you need to drastically limit the frequency of position updates or use a GPS instead.

Current version uses synchronous programming. This means that main code will be blocked while location is being resolved. As this can be quite long you need to take it into account while programming your project.

In future versions, I'll try to add non blocking options. I think I can keep back compatibility so that anyone can get updated versions without using new features.
