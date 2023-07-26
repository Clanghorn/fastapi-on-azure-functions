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
WORKBOOK_ID = os.environ["DEV_MANAGER_WORKBOOK_ID"]

_dir = os.path.dirname(os.path.abspath(__file__))

# The API identifies columns by Id, but it's more convenient to refer to column names. Store a map here
column_map = {}


# Helper function to find cell in a row
def get_cell_by_column_name(row, column_name):
    column_id = column_map[column_name]
    return row.get_column(column_id)


# TODO: Replace the body of this function with your code
# This *example* looks for rows with a "Status" column marked "Complete" and sets the "Remaining" column to zero
#
# Return a new Row with updated cell values, else None to leave unchanged
def evaluate_row_and_build_updates(source_row):
    # Find the cell and value we want to evaluate
    status_cell = get_cell_by_column_name(source_row, "Status")
    status_value = status_cell.display_value
    if status_value == "Complete":
        remaining_cell = get_cell_by_column_name(source_row, "Remaining")
        if remaining_cell.display_value != "0":  # Skip if already 0
            print("Need to update row #" + str(source_row.row_number))

            # Build new cell value
            new_cell = smart.models.Cell()
            new_cell.column_id = column_map["Remaining"]
            new_cell.value = 0

            # Build the row to update
            new_row = smart.models.Row()
            new_row.id = source_row.id
            new_row.cells.append(new_cell)

            return new_row

    return None


def sample(smart):
    # Import the sheet
    result = smart.Sheets.import_xlsx_sheet(_dir + "/Sample Sheet.xlsx", header_row_index=0)

    # Load entire sheet
    sheet = smart.Sheets.get_sheet(result.data.id)

    print("Loaded " + str(len(sheet.rows)) + " rows from sheet: " + sheet.name)

    # Build column map for later reference - translates column names to column id
    for column in sheet.columns:
        column_map[column.title] = column.id

    # Accumulate rows needing update here
    rowsToUpdate = []

    for row in sheet.rows:
        rowToUpdate = evaluate_row_and_build_updates(row)
        if rowToUpdate is not None:
            rowsToUpdate.append(rowToUpdate)

    # Finally, write updated cells back to Smartsheet
    if rowsToUpdate:
        print("Writing " + str(len(rowsToUpdate)) + " rows back to sheet id " + str(sheet.id))
        result = smart.Sheets.update_rows(result.data.id, rowsToUpdate)
    else:
        print("No updates required")


if __name__ == "__main__":
    print("Starting ...")

    # Initialize client. Uses the API token in the environment variable "SMARTSHEET_ACCESS_TOKEN"
    smart = smartsheet.Smartsheet(ACCESS_TOKEN)
    # Make sure we don't miss any error
    smart.errors_as_exceptions(True)

    sheet = smart.Sheets.get_sheet(WORKBOOK_ID)

    # Destination = smartsheet.models.ContainerDestination(
    #     {
    #         "destination_type": "home",  # folder, workspace, or home
    #         #  "destination_id": 5984333325461380,  # folder_id
    #         "new_name": "TESTTESTES",
    #     }
    # )
    new_sheet_name = "BLBLALA"
    inc_list = ["data"]
    sht = smart.Sheets.copy_sheet(
        WORKBOOK_ID,
        smart.models.ContainerDestination(
            {"destination_type": "workspace", "destination_id": 5984333325461380, "new_name": new_sheet_name}
        ),
        include=inc_list,
    )

    print(sht)

    # Log all calls
    logging.basicConfig(filename="rwsheet.log", level=logging.INFO)

    print("Done")
