import os

from arcgis.features import FeatureLayer
from arcgis.gis import GIS
from dotenv import load_dotenv

load_dotenv()

PORTAL = os.environ["PORTAL"]
PORTAL_USERNAME = os.environ["PORTAL_USERNAME"]
PORTAL_PASSWORD = os.environ["PORTAL_PASSWORD"]


def connectToGIS():
    gis = GIS(PORTAL, username=PORTAL_USERNAME, password=PORTAL_PASSWORD)
    print("Successfully logged in as: " + gis.properties.user.username)


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
