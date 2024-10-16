from fastapi import Request, FastAPI, Depends
from contextlib import asynccontextmanager
from httpx import AsyncClient
import os
import requests 

app = FastAPI()


async def get_client():
    async with AsyncClient() as client:
        yield client


@app.get("/weather-data")
async def get_weather_data(client: AsyncClient = Depends(get_client)):
    W_KEY = os.environ.get("WEATHERSTACK_KEY")
    url = "http://api.weatherstack.com/current?access_key=ee70feab84a6f07858fc116c8e391e17" # + W_KEY
    querystring = {"query": "London"}
    response = await client.get(url, params=querystring)
    response.json()


@app.get("/weather-data-basic")
async def get_weather_data_basic():
    url = "http://api.weatherstack.com/current?access_key=ee70feab84a6f07858fc116c8e391e17" # + W_KEY
    querystring = {"query":"New Delhi"}
    response = requests.get(url, params=querystring)
    response.json()


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.requests_client = AsyncClient()
    yield
    await app.requests_client.aclose()

app = FastAPI(lifespan=lifespan)

@app.get("/weather")
async def get_location_weather(request: Request):
    requests_client = request.app.requests_client
    url = "http://api.weatherstack.com/current?access_key=ee70feab84a6f07858fc116c8e391e17" # + W_KEY
    url = "http://api.weatherstack.com/current?access_key=ee70feab84a6f07858fc116c8e391e17&query=London" # + W_KEY
    response = await requests_client.post(url, data={"query": "New Delhi"})
    return response.json()