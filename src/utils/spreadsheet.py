import gspread
from oauth2client.service_account import ServiceAccountCredentials


def update_rouge_score_drive(dataset_dir, cells_range, values):
    # use creds to create a client to interact with the Google Drive API
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('/home/sajad/2extsum/src/utils/client_secret.json', scope)
    client = gspread.authorize(creds)

    # determine the sheet number
    if "longsumm" in dataset_dir.lower():
        sheet_num = 1
    elif "arxivl" in dataset_dir.lower():
        sheet_num = 2
    elif "pubmedl" in dataset_dir.lower():
        sheet_num = 3

    # round values
    values = [round(v,4) for v in values]
    worksheets = eval("client.open(\"Model Results\").worksheets()")
    sheet = worksheets[sheet_num - 1]
    sheet.batch_update([{
        'range': cells_range,
        'values': [values],
    }])


def update_recall_drive(dataset_dir, cell, value):
    # use creds to create a client to interact with the Google Drive API
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('/home/sajad/2extsum/src/utils/client_secret.json', scope)
    client = gspread.authorize(creds)

    # determine the sheet number
    if "longsumm" in dataset_dir.lower():
        sheet_num = 1
    elif "arxivl" in dataset_dir.lower():
        sheet_num = 2
    elif "pubmedl" in dataset_dir.lower():
        sheet_num = 3

    worksheets = eval("client.open(\"Model Results\").worksheets()")
    sheet = worksheets[sheet_num - 1]

    sheet.update(cell, value)

def update_step(dataset_dir, cell, value):
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('/home/sajad/2extsum/src/utils/client_secret.json', scope)
    client = gspread.authorize(creds)

    # determine the sheet number
    if "longsumm" in dataset_dir.lower():
        sheet_num = 1
    elif "arxivl" in dataset_dir.lower():
        sheet_num = 2
    elif "pubmedl" in dataset_dir.lower():
        sheet_num = 3

    worksheets = eval("client.open(\"Model Results\").worksheets()")
    sheet = worksheets[sheet_num - 1]

    sheet.update(cell, value)
