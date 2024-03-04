from app.lambda_handler import regression_handler
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Payload(BaseModel):
    type: str
    params: List[float]
    results: List[float]
    aprox: int = None
    expr: str = None

@app.post("/")
async def regression_api(payload: Payload):
    event = {
        'body-json': {
            'type': payload.type,
            'params': payload.params,
            'results': payload.results,
        }
    }

    if payload.aprox:
        event['body-json']['aprox'] = payload.aprox

    if payload.expr:
        event['body-json']['expr'] = payload.expr

    return regression_handler(event, None)
