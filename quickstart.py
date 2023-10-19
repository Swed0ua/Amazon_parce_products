from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import codecs
import json



file_path = os.path.abspath(__file__)
file_name = file_path.split('\\')[-1]
dir_path = file_path.replace(f'\\{file_name}', '')

def get_data_product():
    with codecs.open(f'{dir_path}\\DATA\\products.json', 'r', encoding='utf-8-sig') as f:
        data_products = json.load(f)
    return data_products

def get_config ():
    with codecs.open(f'{dir_path}\\SETT\\config.json', 'r', encoding='utf-8-sig') as f:
        data_config = json.load(f)
    return data_config

def set_config (ids):
    data = get_data_product()
    data["links"] = ids
    with codecs.open(f'{dir_path}\\SETT\\config.json', 'w', encoding='utf-8-sig') as f:
        json.dump(data, f,ensure_ascii=False, indent=4)


SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

SAMPLE_SPREADSHEET_ID = '1rYyyUpq6VQdmEWxH80tUSQuJByETyDYP0N1ErJTHa3A'
SAMPLE_RANGE_NAME = 'A:F'
SAMPLE_PRODUCT_ID = 'G2:G'

def auth():
    creds = None

    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

def get_values():
    creds = auth()

    try:
        service = build('sheets', 'v4', credentials=creds)

        result = service.spreadsheets().values().get(
            spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_PRODUCT_ID).execute()
        rows = result.get('values', [])
        print(f"{len(rows)} rows retrieved")
        print(rows)
        return rows
    except HttpError as error:
        print(f"An error occurred: {error}")
        return error


def main(config_links):
    creds = auth()

    try:
        service = build('sheets', 'v4', credentials=creds)

        # Call the Sheets API
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                    range=SAMPLE_RANGE_NAME).execute()
        values = result.get('values', [])
        data = get_data_product()
        values = [
            ['Назва', 'Ціна', 'Категорія', 'Підкатегорія', 'Наявність', 'Силка']
        ]
        for item in config_links:
            res = data[item[0]]
            values.append([res['title'], res['price'], res['category'], res['subcategory'], res['stock'][0], res['link']])

        
        body = {
            'values': values
        }
        result = service.spreadsheets().values().update(
            spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME,
            valueInputOption="USER_ENTERED", body=body).execute()
        print(f"{result.get('updatedCells')} cells updated.")


        if not values:
            print('No data found.')
            return

        print('Name, Major:')
        for row in values:
            # Print columns A and E, which correspond to indices 0 and 4.
            print(row)
    except HttpError as err:
        print(err)