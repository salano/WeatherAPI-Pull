import openmeteo_requests
from openmeteo_sdk.Variable import Variable
import numpy as np
import pandas as pd
from geopy.geocoders import Nominatim

# Create a geolocator object
geolocator = Nominatim(user_agent="WeatherAPIs")

om = openmeteo_requests.Client()
params = {
    "latitude": 51.37,
    "longitude": -0.49,
    "start_date": "2010-09-30",
	  "end_date": "2024-10-14",
    "hourly": ["temperature_2m", "precipitation", "wind_speed_10m"],
    "current": ["temperature_2m", "relative_humidity_2m"]
}

# Forcast load
# responses = om.weather_api("https://api.open-meteo.com/v1/forecast", params=params)
# Historical Load
responses = om.weather_api("https://archive-api.open-meteo.com/v1/archive", params=params)

# Process first location. Add a for-loop for multiple locations or weather models
response = responses[0]
print(f"Coordinates {response.Latitude()}°N {response.Longitude()}°E")
print(f"Elevation {response.Elevation()} m asl")
print(f"Timezone {response.Timezone()} {response.TimezoneAbbreviation()}")
print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")

'''
# Current values
current = response.Current()
current_variables = list(map(lambda i: current.Variables(i), range(0, current.VariablesLength())))
current_temperature_2m = next(filter(lambda x: x.Variable() == Variable.temperature and x.Altitude() == 2, current_variables))
current_relative_humidity_2m = next(filter(lambda x: x.Variable() == Variable.relative_humidity and x.Altitude() == 2, current_variables))

print(f"Current time {current.Time()}")
print(f"Current temperature_2m {current_temperature_2m.Value()}")
print(f"Current relative_humidity_2m {current_relative_humidity_2m.Value()}")


hourly = response.Hourly()
hourly_time = range(hourly.Time(), hourly.TimeEnd(), hourly.Interval())
hourly_variables = list(map(lambda i: hourly.Variables(i), range(0, hourly.VariablesLength())))

hourly_temperature_2m = next(filter(lambda x: x.Variable() == Variable.temperature and x.Altitude() == 2, hourly_variables)).ValuesAsNumpy()
hourly_precipitation = next(filter(lambda x: x.Variable() == Variable.precipitation, hourly_variables)).ValuesAsNumpy()
hourly_wind_speed_10m = next(filter(lambda x: x.Variable() == Variable.wind_speed and x.Altitude() == 10, hourly_variables)).ValuesAsNumpy()

hourly_data = {"date": pd.date_range(
	start = pd.to_datetime(hourly.Time(), unit = "s"),
	end = pd.to_datetime(hourly.TimeEnd(), unit = "s"),
	freq = pd.Timedelta(seconds = hourly.Interval()),
	inclusive = "left"
)}
hourly_data["temperature_2m"] = hourly_temperature_2m
hourly_data["precipitation"] = hourly_precipitation
hourly_data["wind_speed_10m"] = hourly_wind_speed_10m

hourly_dataframe_pd = pd.DataFrame(data = hourly_data)
print(hourly_dataframe_pd)
'''


# Process hourly data. The order of variables needs to be the same as requested.
hourly = response.Hourly()
hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()

hourly_data = {"date": pd.date_range(
	start = pd.to_datetime(hourly.Time(), unit = "s", utc = True),
	end = pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True),
	freq = pd.Timedelta(seconds = hourly.Interval()),
	inclusive = "left"
)}

# Get the location name
location = geolocator.reverse((params['latitude'], params['longitude']), language='en')
address = location.address

hourly_data["Country"] = location.raw['address']['country']
hourly_data["Town"] = location.raw['address']['town']
hourly_data["County"] = location.raw['address']['county']
hourly_data["State"] = location.raw['address']['state']
hourly_data["Zip"] = location.raw['address']['postcode']
hourly_data["temperature_2m"] = hourly_temperature_2m


hourly_dataframe = pd.DataFrame(data = hourly_data)
hourly_dataframe.to_csv(r'D:\Python\data\AddlestoneTemperature.csv', index=False)

print(f"""Country Name: {location.raw['address']['country']}""")
print(f"""Town Name: {location.raw['address']['town']}""")
print(f"""County Name: {location.raw['address']['county']}""")
print(f"""State Name: {location.raw['address']['state']}""")
print(f"""Zip Code: {location.raw['address']['postcode']}""")