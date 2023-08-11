import os

import smartsheet

# from dotenv import load_dotenv

# load_dotenv()


# Set the API token in the environment variable "SMARTSHEET_ACCESS_TOKEN"
if "SMARTSHEET_ACCESS_TOKEN" not in os.environ:
    print("SMARTSHEET_ACCESS_TOKEN environment variable not set.")
    exit()

ACCESS_TOKEN = os.environ["SMARTSHEET_ACCESS_TOKEN"]
WORKBOOK_ID = int(os.environ["DEV_MANAGER_WORKBOOK_ID"])
DEV_MANAGER_WORKSPACE = int(os.environ["DEV_MANAGER_WORKSPACE"])

# The API identifies columns by Id, but it's more convenient to refer to column names. Store a map here
column_map = {}


def checkIfSheetExits(workspace, sheetName):
    result = False
    for sheet in workspace.sheets.to_list():
        if sheet.name == sheetName:
            return True
    return result


# Helper function to find cell in a row
def get_cell_by_column_name(row, column_name):
    column_id = column_map[column_name]
    return row.get_column(column_id)


def setupSheet(smart, result, region, siteID):
    # Build column map for later reference - translates column names to column id
    sheet = smart.Sheets.get_sheet(result.id)
    for column in sheet.columns:
        column_map[column.title] = column.id
    new_row = []

    new_cell = smart.models.Cell()
    new_cell.column_id = column_map["Task"]
    # Set Region
    new_cell.value = region
    new_row = smart.models.Row()
    new_row.id = sheet.rows[0].id
    new_row.cells.append(new_cell)
    smart.Sheets.update_rows(sheet.id, new_row)
    # Set Site Code
    new_cell.value = siteID
    new_row = smart.models.Row()
    new_row.id = sheet.rows[1].id
    new_row.cells.append(new_cell)
    smart.Sheets.update_rows(sheet.id, new_row)


def createSmartSheet(region, siteID):
    # Initialize client. Uses the API token in the environment variable "SMARTSHEET_ACCESS_TOKEN"
    smart = smartsheet.Smartsheet(ACCESS_TOKEN)
    # Make sure we don't miss any error
    smart.errors_as_exceptions(True)
    sheet = smart.Sheets.get_sheet(WORKBOOK_ID)
    workspace = smart.Workspaces.get_workspace(DEV_MANAGER_WORKSPACE)

    ExistingSite = checkIfSheetExits(workspace, siteID)
    msg = ""
    if ExistingSite is False:
        sheet = smart.Sheets.copy_sheet(
            WORKBOOK_ID,
            smart.models.ContainerDestination(
                {"destination_type": "workspace", "destination_id": DEV_MANAGER_WORKSPACE, "new_name": siteID}
            ),
            include=["data"],
        )
        setupSheet(smart, sheet.result, region, siteID)
        msg = {"url": sheet.result.permalink}
    else:
        sheet = smart.Sheets.get_sheet_by_name(siteID)
        msg = {"url": sheet.permalink}

    return msg


if __name__ == "__main__":
    print("Starting ...")
    result = createSmartSheet("APAC", "TOK12345")
    print(result)
    print("Done")
