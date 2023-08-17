import os

import azure.functions as func
import fastapi
from fastapi.middleware.cors import CORSMiddleware

import util.gismo as gismo
import util.ss as ss

app = fastapi.FastAPI()

origins = [
    "https://gismoapps.yondrgroup.com",
    "https://gismoappsdev.yondrgroup.com",
    "https://localhost:3001",
]
SITE_URL = os.environ["SITE_URL"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)


@app.get("/")
async def main():
    return {"message": "Hello World"}


@app.get("/sample")
async def index():
    return {
        "info": "Try /hello/Shivani for parameterized route.",
    }


@app.get("/getGIS")
async def getGIS():
    gis = gismo.connectToGIS()
    return {"Successfully logged in as": gis.properties.user.username}


@app.get("/getSiteInfo/{siteID}")
async def getSiteInfo(siteID: str):
    gismo.connectToGIS()
    return gismo.queryFields(SITE_URL, siteID)


@app.get("/createSmartSheet/{siteID}")
async def createSmartSheet(siteID: str):
    gismo.connectToGIS()
    data = gismo.queryFields(SITE_URL, siteID)
    return ss.createSmartSheet(data["Region"], data["GlobalID"], siteID)
