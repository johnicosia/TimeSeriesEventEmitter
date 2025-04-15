from fastapi import FastAPI
from sse_starlette.sse import EventSourceResponse
from datetime import datetime
import asyncio
import json
import random
import uvicorn

app = FastAPI()

async def generate_tempature_events():
    interval = 1
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
        yield {"data": json.dumps(data)}
        # wait an interval before repeating the loop
        await asyncio.sleep(interval)

@app.get("/stream")
async def get_timeseries_data():
    return EventSourceResponse(generate_tempature_events())

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000, reload=False)
