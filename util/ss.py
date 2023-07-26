import logging
import os

import smartsheet
from dotenv import load_dotenv

load_dotenv()


# Set the API token in the environment variable "SMARTSHEET_ACCESS_TOKEN"
if "SMARTSHEET_ACCESS_TOKEN" not in os.environ:
    print("SMARTSHEET_ACCESS_TOKEN environment variable not set.")
    exit()

ACCESS_TOKEN = os.environ["SMARTSHEET_ACCESS_TOKEN"]
WORKBOOK_ID = int(os.environ["DEV_MANAGER_WORKBOOK_ID"])
DEV_MANAGER_WORKSPACE = int(os.environ["DEV_MANAGER_WORKSPACE"])


def checkIfSheetExits(workspace, sheetName):
    result = any(item.name in sheetName for item in workspace.sheets.to_list())
    return bool(result)


if __name__ == "__main__":
    print("Starting ...")

    # Initialize client. Uses the API token in the environment variable "SMARTSHEET_ACCESS_TOKEN"
    smart = smartsheet.Smartsheet(ACCESS_TOKEN)
    # Make sure we don't miss any error
    smart.errors_as_exceptions(True)
    sheet = smart.Sheets.get_sheet(WORKBOOK_ID)

    workspace = smart.Workspaces.get_workspace(DEV_MANAGER_WORKSPACE)

    # Destination = smartsheet.models.ContainerDestination(
    #     {
    #         "destination_type": "home",  # folder, workspace, or home
    #         #  "destination_id": 5984333325461380,  # folder_id
    #         "new_name": "TESTTESTES",
    #     }
    # )
    new_sheet_name = "fdsaasdfasdf"
    ExistingSite = checkIfSheetExits(workspace, new_sheet_name)
    if ExistingSite is False:
        sht = smart.Sheets.copy_sheet(
            WORKBOOK_ID,
            smart.models.ContainerDestination(
                {"destination_type": "workspace", "destination_id": DEV_MANAGER_WORKSPACE, "new_name": new_sheet_name}
            ),
            include=["data"],
        )
    else:
        sheet = smart.Sheets.get_sheet_by_name(new_sheet_name)
        print(f'Sheet Already Exists: {sheet.permalink}')

    # Log all calls
    logging.basicConfig(filename="rwsheet.log", level=logging.INFO)

    print("Done")
