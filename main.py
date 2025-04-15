from fastapi import FastAPI
from sse_starlette.sse import EventSourceResponse
from datetime import datetime
import asyncio
import json
import random
import uvicorn
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS

# TODO externalize influxdb configuration
bucket = "test"
org = "test"
token = "HLA5J8IhE_TAQjAoXX8buquu49a6tpofyXNs26RfWNtTNJXpnfox2zwgBSEeKTP7ggb6G55xJrZaupDVKGBkSg=="
# Store the URL of your InfluxDB instance
url="http://localhost:8086"

events = []

app = FastAPI()

client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)

def store_data(data):
    write_api = client.write_api(write_options=SYNCHRONOUS)
    point = influxdb_client.Point("metrics").tag("metric", data["metric"]).tag("timestamp", data["timestamp"]).field("value", data["value"])
    write_api.write(bucket=bucket, org=org, record=point)

async def generate_tempature_events(interval):
    temperature = 70
    while True:
        data = {}
        # Get the current date and time
        data["timestamp"] = datetime.now().isoformat()
        data["metric"] = "temperature"
        # Randomly choose if tempature goes up
        tempature_goes_up = random.choice([True, False])
        tempature_difference = random.random() if tempature_goes_up else (random.random() * -1)
        temperature = round(temperature + tempature_difference, 2)
        data["value"] = temperature
        store_data(data)
        yield {"data": json.dumps(data)}
        # wait an interval before repeating the loop
        await asyncio.sleep(interval)

@app.get("/stream")
async def get_timeseries_data(interval: int = 1):
    return EventSourceResponse(generate_tempature_events(interval))

@app.get("/history")
async def get_history(last: int = 10):
    query_api = client.query_api()
    query = f'from(bucket: \"{bucket}\") |> range(start: -99y) |> group() |> sort(columns: ["_time"], desc: true) |> limit(n: {last})'
    result = query_api.query(org=org, query=query)
    results = []
    for table in result:
        for record in table.records:
            data = {}
            data["timestamp"] = record.values.get("timestamp")
            data["metric"] = record.values.get("metric")
            data["value"] = record.get_value()
            results.append(data)
    return results

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000, reload=False)
