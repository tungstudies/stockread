from __future__ import print_function

from googleapiclient.discovery import build
from google.oauth2 import service_account
from xlsxwriter import utility

# If modifying these scopes, delete the file token.pickle.
from secrets.credentials import GOOGLE_SHEET_SERVICE_ACCOUNT_FILE

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

credentials = service_account.Credentials.from_service_account_file(
    GOOGLE_SHEET_SERVIxCE_ACCOUNT_FILE, scopes=SCOPES)


class GoogleSheets1:
    range = ''

    def __init__(self, spreadsheet_id: str):
        self.spreadsheet_id = spreadsheet_id
        self.service = build('sheets', 'v4', credentials=credentials)
        self.sheet = self.service.spreadsheets()

    def get_headers(self, tab_name: str):
        header_range = '{}!1:1'.format(tab_name)
        result = self.sheet.values().get(spreadsheetId=self.spreadsheet_id,
                                         range=header_range).execute()

        global headers
        values = result.get('values', [])

        if not values:
            print('No news found.')
        else:
            headers = values[0]
        return headers

    def get_column_data(self, column_index, tab_name: str):
        column_letter = utility.xl_col_to_name(column_index - 1)
        data_range = '{}!{}:{}'.format(tab_name, column_letter, column_letter)

        result = self.sheet.values().get(spreadsheetId=self.spreadsheet_id,
                                         range=data_range).execute()

        values = result.get('values', [])

        if not values:
            print('No news found.')
        else:
            elements = [value for value in values][1:]
            return elements

    def post_data_range(self, list_of_data_list, tab_name: str, start_cell='A1'):
        data_range = f'{tab_name}!{start_cell}'
        clear_values_request_body = {
            # TODO: Add desired entries to the request body.
        }

        clear_request = self.sheet.values().clear(spreadsheetId=self.spreadsheet_id, range=tab_name,
                                       body=clear_values_request_body)
        clear_response = clear_request.execute()
        print(clear_response)

        body = {
            'values': list_of_data_list
        }

        update_request = self.sheet.values().update(
            spreadsheetId=self.spreadsheet_id, range=data_range,
            valueInputOption="RAW", body=body)

        update_response = update_request.execute()
        print(update_response)


# Call the Sheets API


'''
aoa = [["Tung", 4000], ["Nam", 2000], ["Benson", 5000]]

body = {
    'values': aoa
}

request = sheet.values().update(
    spreadsheetId=SPREADSHEET_ID, range='HelloPython!A3',
    valueInputOption="RAW", body=body).execute()
'''
