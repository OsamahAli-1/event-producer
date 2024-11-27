from fastapi import FastAPI
from pydantic import BaseModel
import faust
import logging

app = FastAPI()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("event-producer")

class Event(BaseModel):
    event_name: str
    event_payload: dict


faustApp = faust.App('event-producer', broker='kafka://kafka:9092')

@app.post("/produce-event")
async def produce_event(event: Event):
    try:
        await produce_to_topic(event.event_name,event.event_payload)
    except Exception:
        logger.info(f"kafka producer failed")



async def produce_to_topic(topic_name,event_data):
    try:
        topic = faustApp.topic(topic_name)
        await topic.send(value=event_data)
        logger.info(f"event produced with payload {event_data} ")
    except Exception:
        logger.info(f"kafka producer failed")
