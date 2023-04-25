if 1 == 1:
    import sys
    import os

    sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

import gspread_dataframe as gd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
import pandas as pd
from enums.google_enum import GoogleAPI, GoogleSheets
from common.utils import global_log_append
from tenacity import retry, wait_fixed, stop_after_attempt


def get_gspread():
    api_json = GoogleAPI.COCOBLANC_RPA_SHEET_KEY.value
    credentials = ServiceAccountCredentials._from_parsed_json_keyfile(
        api_json, api_json["scopes"], token_uri=api_json["token_uri"], revoke_uri=api_json["revoke_uri"]
    )
    gc = gspread.authorize(credentials)
    return gc


def get_spreadsheet(url):
    gc = get_gspread()
    spreadsheet = gc.open_by_url(url)
    return spreadsheet


def get_worksheet(url, sheet_name):
    spreadsheet = get_spreadsheet(url)
    worksheet = spreadsheet.worksheet(sheet_name)
    return worksheet


@retry(
    wait=wait_fixed(5),  # 5초 대기
    stop=stop_after_attempt(10),  # 5번 재시도
)
def get_gs_data(url, sheet_name):
    worksheet = get_worksheet(url, sheet_name)
    data = worksheet.get_all_values()
    headers = data.pop(0)
    df = pd.DataFrame(data, columns=headers)
    df = df.fillna("")
    return df


if __name__ == "__main__":
    # df_soldout = get_df_soldout()
    # print(df_soldout)
    pass
