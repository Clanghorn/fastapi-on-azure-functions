from arcgis.features import FeatureLayer
from arcgis.gis import GIS

gis = GIS("https://dev-gis.yondrgroup.com/portal/", username="portaladmin", password="textiles.Busy.drift6")
print("Successfully logged in as: " + gis.properties.user.username)


lyr_url = "https://dev-gis.yondrgroup.com/hosting/rest/services/YondrData/YondrSite/MapServer/1"

layer = FeatureLayer(lyr_url)
siteID = "TOK01"
result = layer.query(where=f"SiteID='{siteID}'", out_fields="SiteID,Region,DevManager")
print(result.features)


# TODO
# Add link to Site Links table SiteGUID/LinkLabel/URL/Source
