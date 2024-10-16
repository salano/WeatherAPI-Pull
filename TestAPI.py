import requests
import os
from pprint import pprint

W_KEY = os.environ.get("WEATHERSTACK_KEY")
print(W_KEY)
pprint(os.environ)
exit()
url = "https://api.weatherstack.com/current?access_key=" + W_KEY

querystring = {"query":"New Delhi"}

response = requests.get(url, params=querystring)

print(response.json())