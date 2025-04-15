from fastapi import FastAPI
from sse_starlette.sse import EventSourceResponse
from datetime import datetime
import asyncio
import json
import random
import uvicorn

app = FastAPI()

events = []

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
        events.append(data)
        yield {"data": json.dumps(data)}
        # wait an interval before repeating the loop
        await asyncio.sleep(interval)

@app.get("/stream")
async def get_timeseries_data(interval: int = 1):
    return EventSourceResponse(generate_tempature_events(interval))

@app.get("/history")
async def get_history(last: int = 10):
    return events[-last:][::-1]

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000, reload=False)
