import logging
import os

from arcgis.features import FeatureLayer
from arcgis.gis import GIS

# from dotenv import load_dotenv

# load_dotenv()

PORTAL = os.environ["DEVMO_PORTAL"]
PORTAL_USERNAME = os.environ["DEVMO_PORTAL_USERNAME"]
PORTAL_PASSWORD = os.environ["DEVMO_PORTAL_PASSWORD"]


def connectToGIS():
    logging.info("Starting")
    gis = GIS(PORTAL, username=PORTAL_USERNAME, password=PORTAL_PASSWORD)
    logging.info("Successfully logged in as: " + gis.properties.user.username)
    return gis


def queryFields(lyr_url, siteID, fields="GlobalID,SiteID,Region,DevManager"):
    try:
        layer = FeatureLayer(lyr_url)
        feat_set = layer.query(where=f"SiteID='{siteID}'", out_fields=fields)
        feat_list = feat_set.features
        feat = feat_list[0]
        result = feat.attributes
        if not result:
            raise ValueError("No data found for the given SiteID.")
        return result
    except Exception as e:
        print(f"Error occurred: {e}")
        return {"msg": "No Data"}


def addSSlinkToTable():
    pass


# TODO
# Add link to Site Links table SiteGUID/LinkLabel/URL/Source
if __name__ == "__main__":
    print("Starting ...")
    lyr_url = "https://dev-gis.yondrgroup.com/hosting/rest/services/YondrData/YondrSite/MapServer/1"
    fields = "GlobalID,SiteID,Region,DevManager"
    siteID = "TOK01"
    connectToGIS()
    x = queryFields(lyr_url, siteID, fields)
    print(x)
