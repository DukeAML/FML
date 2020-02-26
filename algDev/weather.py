
import pyowm

owm = pyowm.OWM('0b5d1aad4776c6f38a88d341233cc6a3')
observation = owm.weather_at_place('London,GB')
w = observation.get_weather()
print(w) 