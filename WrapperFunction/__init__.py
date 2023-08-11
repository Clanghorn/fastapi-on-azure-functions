import logging

import azure.functions as func
import fastapi
from fastapi.middleware.cors import CORSMiddleware

import util.gismo as gismo
import util.ss as ss

app = fastapi.FastAPI()

origins = [
    "https://gismoappsdev.yondrgroup.com",
    "https://localhost:3001",
]

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
    lyr_url = "https://dev-gis.yondrgroup.com/hosting/rest/services/YondrData/YondrSite/MapServer/1"
    return gismo.queryFields(lyr_url, siteID)


@app.get("/createSmartSheet/{siteID}")
async def createSmartSheet(siteID: str):
    gismo.connectToGIS()
    lyr_url = "https://dev-gis.yondrgroup.com/hosting/rest/services/YondrData/YondrSite/MapServer/1"
    data = gismo.queryFields(lyr_url, siteID)
    return ss.createSmartSheet(data["Region"], siteID)
