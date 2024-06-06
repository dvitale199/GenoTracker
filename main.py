from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from enum import Enum

app = FastAPI()

@app.get("/")
async def root():
    return "Welcome to GenoTracker"
