if 1 == 1:
    import sys
    import os

    sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))


from selenium import webdriver
from dtos.gui_dto import GUIDto

from common.utils import global_log_append
from common.chrome import open_browser, get_chrome_driver, get_chrome_driver_new
from common.selenium_activities import close_new_tabs, alert_ok_try
from common.account_file import AccountFile


from enums.store_name_enum import StoreNameEnum

from features.convert_store_name import StoreNameConverter


from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import ActionChains
from selenium.webdriver.support.select import Select

import time

import pandas as pd
from openpyxl import load_workbook

from common.google_sheet import get_gs_data


class SabangnetStockSettingProcess:
    def __init__(self):
        self.default_wait = 10
        self.driver: webdriver.Chrome = get_chrome_driver_new(is_headless=True, is_secret=False)
        self.driver.implicitly_wait(self.default_wait)
        self.driver.maximize_window()

    def setGuiDto(self, guiDto: GUIDto):
        self.guiDto = guiDto

    def setLogger(self, log_msg):
        self.log_msg = log_msg

    # 전체작업 시작
    def work_start(self):
        print(f"process: work_start")

        df_soldout = get_gs_data(self.guiDto.google_sheet_url, self.guiDto.selected_sheet_name)
        self.log_msg.emit(f"{len(df_soldout)}개의 데이터를 발견했습니다.")
        print(df_soldout)


if __name__ == "__main__":
    # process = SabangnetAutoUploaderProcess()
    # process.work_start()
    pass
