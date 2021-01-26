try:
    import sys
    import gspread

    from dataclasses import dataclass, field
    from typing import Optional, Union, List

    from secrets.credentials import GoogleCredential

except ModuleNotFoundError as err:
    print('Some modules are missing: {}'.format(err))
    sys.exit()

SA_FILEPATH = GoogleCredential().sheets_account_service_jsonpath
SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
GG_SHEETS = gspread.service_account(filename=SA_FILEPATH, scopes=SCOPES)


class GoogleSheets:
    def __init__(self, spreadsheet_id: str, worksheet_name: str = 'Sheet1'):
        self.spreadsheet_id = spreadsheet_id
        self.worksheet_name = worksheet_name
        self.spreadsheet = GG_SHEETS.open_by_key(spreadsheet_id)
        self.worksheet = self.spreadsheet.worksheet(self.worksheet_name)

    def get_data_by_headers(self, headers: list) -> Union[list, List[dict]]:
        existing_data = self.worksheet.get_all_records()
        if len(headers) == 1:
            single_header = headers[0]
            return [item[single_header] for item in existing_data if single_header in item]

        else:
            ret_data = []
            for item in existing_data:
                temp = dict()
                for key, value in item.items():
                    if key in headers:
                        temp.update({key: value})

                ret_data.append(temp)
            return ret_data

    def get_data_by_column_index(self, **headers_and_indexes):
        existing_data = self.worksheet.get_all_values()
        ret_data = []
        for row in existing_data:
            temp = dict()
            for key, value in headers_and_indexes.items():
                list_index = int(value - 1)
                temp.update({key: row[list_index]})
            ret_data.append(temp)
        return ret_data

    def get_data_by_key_column(self, has_header: bool, key_column: int, **names_and_indexes):
        index_of_keys = key_column - 1
        output_dict = {}
        existing_data = self.worksheet.get_all_values()
        data_iter = iter(existing_data)
        if has_header:
            next(data_iter)
        for row in data_iter:
            output_dict[row[index_of_keys]] = dict()
            for key, value in names_and_indexes.items():
                list_index = int(value - 1)
                output_dict[row[index_of_keys]][key] = row[list_index]

        return output_dict

    def create(self, data_dict_list: list, worksheet_name: str = None, key_header_mapping: dict = None,
               has_sequence: bool = True):

        if worksheet_name:
            self.worksheet_name = worksheet_name
            self.worksheet = self.spreadsheet.worksheet(self.worksheet_name)

        existing_data = self.worksheet.get_all_values()
        if existing_data:
            self.worksheet.clear()

        post_values = []
        if key_header_mapping:
            for row, item in enumerate(data_dict_list, start=1):
                if row == 1:

                    headers = ['SN'] if has_sequence else []

                    for key in item.keys():
                        if key in key_header_mapping:
                            headers.append(key_header_mapping[key])
                    post_values.append(headers)

                entry = [row] if has_sequence else []
                for key, value in item.items():
                    if key in key_header_mapping:
                        entry.append(value)
                post_values.append(entry)
        else:
            for row, item in enumerate(data_dict_list, start=1):
                if row == 1:
                    headers = ['sn'] if has_sequence else []
                    for key in item.keys():
                        headers.append(key)
                    post_values.append(headers)

                entry = [row] if has_sequence else []

                for value in item.values():
                    entry.append(value)
                post_values.append(entry)

        return self.worksheet.update(post_values)

    def append(self, data_dict_list: list, key_header_mapping: dict = None, worksheet_name: str = None,
               has_sequence: bool = False, sequence_col: int = 1):

        last_sn = 0
        sequence_col_index = sequence_col - 1

        if worksheet_name:
            self.worksheet_name = worksheet_name
            self.worksheet = self.spreadsheet.worksheet(self.worksheet_name)

        if has_sequence:
            last_sn = int(self.worksheet.col_values(sequence_col)[-1])
            existing_headers = self.worksheet.row_values(1)
            del existing_headers[sequence_col_index]

        else:
            existing_headers = self.worksheet.row_values(1)

        refined_key_header_mapping = {}
        for key, value in key_header_mapping.items():
            if value not in existing_headers:
                refined_key_header_mapping[key] = value

        put_values = []
        if key_header_mapping:
            for row, item in enumerate(data_dict_list, start=(last_sn + 1)):

                entry = []
                for key, value in item.items():
                    if key in refined_key_header_mapping:
                        entry.append(value)
                if has_sequence:
                    entry.insert(sequence_col_index, row)
                put_values.append(entry)
        else:
            for row, item in enumerate(data_dict_list, start=(last_sn + 1)):

                entry = []

                for value in item.values():
                    entry.append(value)
                if has_sequence:
                    entry.insert(sequence_col_index, row)
                put_values.append(entry)

        return self.spreadsheet.values_append(self.worksheet_name, {'valueInputOption': 'USER_ENTERED'},
                                              {'values': put_values})

    def replace(self, data_dict_list: list, key_header_mapping: dict, worksheet_name: str = None,
                has_sequence: bool = True):

        if worksheet_name:
            self.worksheet_name = worksheet_name
            self.worksheet = self.spreadsheet.worksheet(self.worksheet_name)

        existing_headers = self.worksheet.row_values(1)
        refined_key_header_mapping = {}
        for key, value in key_header_mapping.items():
            if value not in existing_headers:
                refined_key_header_mapping[key] = value

        return self.create(data_dict_list=data_dict_list, key_header_mapping=refined_key_header_mapping,
                           worksheet_name=worksheet_name, has_sequence=has_sequence)


if __name__ == '__main__':
    spreadsheetId = "1iUg_IBkq64BuFBrL0QHSxTo7Ew7tofFCQYGvL8c15LU"  # Please set the Spreadsheet ID.
    sheetName = "Sheet3"  # Please set the sheet name.

    ggs = GoogleSheets(spreadsheetId, sheetName)
    data_dict_list = [{
        "timestamp": "09-04-2019",
        "value": "10.0",
        "company_name": "Xbox",
        "product": "Buy"
    }, {
        "timestamp": "09-03-2019",
        "value": "2.0",
        "company_name": "something",
        "product": "Sell"
    }]

    header_key_mapping = {
        'Date': 'timestamp',
        'Company_Name': 'company_name',
        'Traffic': 'value',
        'Product': 'product'
    }

    key_header_mapping = {
        'timestamp': 'Date',
        'company_name': 'Company_Name',
        'value': 'Traffic',
        'product': 'Product'
    }
    # ggs.create(data_dict_list=data_dict_list, key_header_mapping=None)
    ggs.append(data_dict_list, key_header_mapping, has_sequence=True)
    # existing = ggs.worksheet.col_values(1)
    print(ggs.worksheet.get_all_records())
    # existing = ggs.get_data_by_column_index(sn=0, timestamp=1)
    # existing = ggs.get_data_by_key_column(has_header=True, col_index=3, sn=0, timestamp=1)
    # print(existing)
    # data = [{'sn': 1, 'timestamp': '09-04-2019', 'value': 10.0, 'company_name': 'Xbox', 'product': 'Buy'}, {'sn': 2, 'timestamp': '09-03-2019', 'value': 2.0, 'company_name': 'something', 'product': 'Sell'}]
    # print([item['abc'] for item in data if 'abc' in item])
    # headers = ggs.worksheet.row_values(1)
    # put_values = []
    # for v in data_dict_list:
    #     temp = []
    #     for h in headers:
    #         temp.append(v[header_key_mapping[h]])
    #     put_values.append(temp)
    # ggs.spreadsheet.values_append(ggs.worksheet_name, {'valueInputOption': 'USER_ENTERED'}, {'values': put_values})

'''
# Open a sheet from a spreadsheet in one go
# sheetName =  'Sheet2'
# worksheet = wks.worksheet(sheetName)
# primary_channels = sheet.get_all_records()
# print(primary_channels)
# item = {'SN': 2, 'Channel ID': 'UCie-TaHu03Ka04kkaUiNDkg'}
# primary_channels.append(item)
# print(primary_channels)


spreadsheetId = "1iUg_IBkq64BuFBrL0QHSxTo7Ew7tofFCQYGvL8c15LU"  # Please set the Spreadsheet ID.
sheetName = "Sheet3"  # Please set the sheet name.


sheet_data = [{
    "timestamp": "09-04-2019",
    "value": "10.0",
    "company_name": "Xbox",
    "product": "Buy"
}, {
    "timestamp": "09-03-2019",
    "value": "2.0",
    "company_name": "something",
    "product": "Sell"
}]

header_to_key = {
    'Date': 'timestamp',
    'Company_Name': 'company_name',
    'Traffic': 'value',
    'Product': 'product'
}

spreadsheet = GG_SHEETS.open_by_key(spreadsheetId)
worksheet = spreadsheet.worksheet(sheetName)
existing_data = worksheet.get_all_values()

if existing_data:
    headers = 
    worksheet.clear()

print(worksheet.get_all_records())
put_values = []
for v in sheet_data:
    temp = []
    for h in headers:
        temp.append(v[header_to_key[h]])
    put_values.append(temp)
spreadsheet.values_append(sheetName, {'valueInputOption': 'USER_ENTERED'}, {'values': put_values})

# # Update a range of cells using the top left corner address
# wks.update('A1', [[1, 2], [3, 4]])
#
# # Or update a single cell
# wks.update('B42', "it's down there somewhere, let me take another look.")
#
# # Format the header
# wks.format('A:B1', {'textFormat': {'bold': True}})

'''
