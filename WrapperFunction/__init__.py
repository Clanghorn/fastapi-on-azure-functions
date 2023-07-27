import azure.functions as func
import fastapi

import util.gismo as gismo
import util.ss as ss

app = fastapi.FastAPI()


@app.get("/sample")
async def index():
    return {
        "info": "Try /hello/Shivani for parameterized route.",
    }


@app.get("/getSiteInfo/{siteID}")
async def getSiteInfo(siteID: str):
    gismo.connectToGIS()
    lyr_url = "https://dev-gis.yondrgroup.com/hosting/rest/services/YondrData/YondrSite/MapServer/1"
    return gismo.queryFields(lyr_url, siteID)


@app.get("/createSmartSheet/{siteID}")
async def createSmartSheet(siteID: str):
    return ss.createSmartSheet(siteID)
