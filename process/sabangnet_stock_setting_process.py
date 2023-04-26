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
from enums.google_sheet_enum import StockSettingSheetEnum, ModifySheetEnum


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
        self.driver: webdriver.Chrome = get_chrome_driver_new(is_headless=False, is_secret=True)
        self.driver.implicitly_wait(self.default_wait)
        self.driver.maximize_window()

    def setGuiDto(self, guiDto: GUIDto):
        self.guiDto = guiDto

    def setLogger(self, log_msg):
        self.log_msg = log_msg

    # 자체상품코드가 있는 데이터만 필터링합니다.
    def get_df_product_code(self):
        self.df_product_code = self.df_googlesheet.loc[
            self.df_googlesheet[StockSettingSheetEnum.ProductCode.value] != ""
        ]
        print(self.df_product_code)

    def sabangnet_login(self):
        driver = self.driver
        driver.get(f"https://www.sabangnet.co.kr/")
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '//a[contains(@href, "index.html")]'))
        )
        time.sleep(0.2)

        login_id = self.guiDto.sabangnet_id
        login_pw = self.guiDto.sabangnet_pw

        # 로그인 시도
        try:
            driver.implicitly_wait(2)

            input_id = driver.find_element(By.XPATH, '//input[@id="txtID"]')
            input_id.clear()
            input_id.send_keys(login_id)
            time.sleep(0.2)

            input_pwd = driver.find_element(By.XPATH, '//input[@id="txtPWD"]')
            input_pwd.clear()
            input_pwd.send_keys(login_pw)
            time.sleep(0.2)

            login_button = driver.find_element(
                By.XPATH, '//button[contains(@onclick, "chk") and contains(text(), "로그인")]'
            )
            login_button.click()

            # 사방넷 접속 버튼 대기
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "사방넷 접속")]'))
            )
            time.sleep(0.2)

            driver.find_element(By.XPATH, '//button[contains(text(), "사방넷 접속")]').click()

            # 대시보드 로딩 대기
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '//a[contains(@href, "dashboard")]'))
            )
            time.sleep(0.2)

        except Exception as e:
            print(e)
            raise Exception(f"사방넷 로그인 실패")

        finally:
            driver.implicitly_wait(self.default_wait)

    # 메인화면으로 이동 (반복 작업 시 필요)
    def sabangnet_main(self):
        driver = self.driver
        driver.get("https://sbadmin09.sabangnet.co.kr/#/dashboard")
        time.sleep(0.5)
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//a[contains(@href, "dashboard")]'))
        )
        time.sleep(0.5)

    # 쇼핑몰상품등록 화면 이동
    def sabangnet_stock_setting_menu(self):
        driver = self.driver
        driver.get("https://sbadmin09.sabangnet.co.kr/#/product/product-inquiry")
        time.sleep(0.5)
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//a[contains(@href, "dashboard")]'))
        )
        time.sleep(0.5)

    def stock_setting(self, product_code: str, soldout_type: str):
        driver = self.driver

        self.sabangnet_stock_setting_menu()

        # 날짜 검색 기준 설정
        search_date_setting = driver.find_element(By.XPATH, '//li[./span[contains(text(), "상품등록일")]]')
        driver.execute_script("arguments[0].click();", search_date_setting)
        time.sleep(0.2)

        # 시작일
        input_start_date = driver.find_elements(By.XPATH, '//div[contains(@class, "date-editor")]/input')[0]
        input_start_date.clear()
        input_start_date.send_keys("18991130", Keys.ENTER)
        time.sleep(0.2)

        # 자체상품코드 검색 설정
        search_type_select_list = driver.find_elements(By.XPATH, '//li[./span[contains(text(), "자체상품코드")]]')
        for search_type_select in search_type_select_list:
            driver.execute_script("arguments[0].click();", search_type_select)
            time.sleep(0.2)

        # 자체상품코드 입력 후 엔터 (검색버튼의 셀렉터가 약간 다름)
        # $x('//div[./span[contains(text(), "검색항목")]]/following-sibling::div//input[not(contains(@readonly, "readonly"))]')
        input_product_code = driver.find_element(
            By.XPATH,
            '//div[./span[contains(text(), "검색항목")]]/following-sibling::div//input[not(contains(@readonly, "readonly"))]',
        )
        input_product_code.clear()
        input_product_code.send_keys(product_code, Keys.ENTER)
        time.sleep(0.2)

        # table에 검색 결과가 나오지 않으면 오류로 간주
        # $x('//table[contains(@class, "table__body")]//tr')
        try:
            WebDriverWait(driver, 5).until(
                EC.visibility_of_element_located((By.XPATH, '//table[contains(@class, "table__body")]//tr'))
            )
            time.sleep(0.5)

        except Exception as e:
            self.log_msg.emit(f"[{product_code}] 검색 결과를 발견하지 못했습니다.")
            raise Exception(f"[{product_code}] 검색 결과를 발견하지 못했습니다.")

        print(f"작업타입: {soldout_type}")

        if soldout_type == "옵션품절":
            # 옵션품절 작업
            pass
        elif soldout_type == "전체품절":
            # 전체품절 작업
            pass
        else:
            self.log_msg.emit(f"[{soldout_type}] 품절여부 형식이 다릅니다.")
            raise Exception(f"[{soldout_type}] 품절여부 형식이 다릅니다.")

        print()

    # 전체작업 시작
    def work_start(self):
        self.df_googlesheet = get_gs_data(self.guiDto.google_sheet_url, self.guiDto.selected_sheet_name)

        self.get_df_product_code()
        print(f"{len(self.df_googlesheet)}개의 데이터 중 {len(self.df_product_code)}개의 자체상품코드를 발견했습니다.")
        self.log_msg.emit(f"{len(self.df_googlesheet)}개의 데이터 중 {len(self.df_product_code)}개의 자체상품코드를 발견했습니다.")

        try:
            self.sabangnet_login()

            for i, row in self.df_product_code[:].iterrows():
                try:
                    product_code = str(row[StockSettingSheetEnum.ProductCode.value])
                    product_name = str(row[StockSettingSheetEnum.ProductName.value])
                    soldout_type = str(row[StockSettingSheetEnum.SoldOutType.value])
                    sabangnet_check = str(row[StockSettingSheetEnum.Sabangnet.value])

                    if sabangnet_check.find("품절처리완료") > -1 or sabangnet_check.find("처리 완료") > -1:
                        print(f"{i}, {product_code}, {product_name}, {soldout_type} 이미 {sabangnet_check}된 행입니다.")
                        self.log_msg.emit(
                            f"{i}, {product_code}, {product_name}, {soldout_type} 이미 {sabangnet_check}된 행입니다."
                        )
                        continue

                    print(f"{i}, {product_code}, {product_name}, {soldout_type} 작업 시작")
                    self.log_msg.emit(f"{i}, {product_code}, {product_name}, {soldout_type} 작업 시작")

                    self.sabangnet_main()

                    self.stock_setting(product_code, soldout_type)

                except Exception as e:
                    print(e)
                    self.log_msg.emit(f"{i}, {product_code}, {product_name}, {soldout_type} 작업 실패")
                    continue

                finally:
                    pass

        except Exception as e:
            print(e)

        finally:
            self.driver.quit()
            time.sleep(0.2)


if __name__ == "__main__":
    # process = SabangnetAutoUploaderProcess()
    # process.work_start()
    pass
