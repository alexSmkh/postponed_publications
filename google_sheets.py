from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from urllib.parse import urlparse
from urlextract import URLExtract
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive


def get_id(formula):
    extractor = URLExtract()
    url = extractor.find_urls(formula)
    parse_result = urlparse(url[0])
    file_id = parse_result.query
    return file_id[3:]


def auth_in_google_sheets():
    scopes = ['https://www.googleapis.com/auth/spreadsheets']
    credentials = None

    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            credentials = pickle.load(token)
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', scopes)
            credentials = flow.run_local_server()
        with open('token.pickle', 'wb') as token:
            pickle.dump(credentials, token)
    service = build('sheets', 'v4', credentials=credentials)
    return service


def auth_in_google_drive():
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    drive = GoogleDrive(gauth)
    return drive


def fetch_sheet_rows(sheet_id, service):
    # scopes = ['https://www.googleapis.com/auth/spreadsheets']
    # credentials = None
    #
    # if os.path.exists('token.pickle'):
    #     with open('token.pickle', 'rb') as token:
    #         credentials = pickle.load(token)
    # if not credentials or not credentials.valid:
    #     if credentials and credentials.expired and credentials.refresh_token:
    #         credentials.refresh(Request())
    #     else:
    #         flow = InstalledAppFlow.from_client_secrets_file(
    #             'credentials.json', scopes)
    #         credentials = flow.run_local_server()
    #     with open('token.pickle', 'wb') as token:
    #         pickle.dump(credentials, token)
    # service = build('sheets', 'v4', credentials=credentials)
    range_ = 'Лист1!A3:H'
    value_render_option = 'FORMULA'
    date_time_render_option = 'FORMATTED_STRING'
    request = service.spreadsheets().values().get(
        spreadsheetId=sheet_id,
        range=range_,
        valueRenderOption=value_render_option,
        dateTimeRenderOption=date_time_render_option)
    response = request.execute()
    row_number_in_sheet = 3
    rows_with_articles = list(enumerate(response['values'], row_number_in_sheet))
    return rows_with_articles



def fetch_image_file(image_id, drive):
    picture_metadate = drive.CreateFile({'id': image_id})
    picture_metadate.FetchMetadata(fetch_all=True)
    filename = picture_metadate['title']
    picture = drive.CreateFile({'id': image_id})
    picture.GetContentFile(filename)
    return filename


def fetch_text_file(text_id, drive):
    article_metadata = drive.CreateFile({'id': text_id})
    article_metadata.FetchMetadata(fetch_all=True)
    article_title = article_metadata['title']
    article_text = drive.CreateFile({'id': text_id})
    article_text.GetContentFile(
        filename='{}.txt'.format(article_title),
        mimetype='text/plain')
    return '{}.txt'.format(article_title)


def update_sheet_row(sheet_id, row_number, service):
    range_for_update = 'H{}'.format(row_number)
    value_input_option = 'USER_ENTERED'

    body = {
        'values': [
            ['да']
        ],
    }
    service.spreadsheets().values().update(
        spreadsheetId=sheet_id,
        range=range_for_update,
        valueInputOption=value_input_option,
        body=body).execute()
