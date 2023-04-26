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

from dtos.store_detail_dto import StoreDetailDto

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


class SabangnetRegistUploadProcess:
    def __init__(self):
        self.default_wait = 10
        self.driver: webdriver.Chrome = get_chrome_driver_new(is_headless=False, is_secret=True)
        self.driver.implicitly_wait(self.default_wait)
        self.driver.maximize_window()

    def setGuiDto(self, guiDto: GUIDto):
        self.guiDto = guiDto

    def setLogger(self, log_msg):
        self.log_msg = log_msg

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
    def sabangnet_regist_menu(self):
        driver = self.driver
        driver.get("https://sbadmin09.sabangnet.co.kr/#/mall/mall-product-registration")
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//div[./span[contains(text(), "쇼핑몰상품등록")]]'))
        )
        time.sleep(0.5)

    # 11번가, 위메프 작업
    def eleven_shop_regist(self):
        print("11번가, 위메프 작업")

        try:
            shop_name = StoreNameEnum.ElevenStreet.value
            self.shop_regist_upload(shop_name)
        except Exception as e:
            print(e)
            self.log_msg.emit(f"{shop_name} 작업 실패")

        try:
            shop_name = StoreNameEnum.WeMakePrice.value
            self.shop_regist_upload(shop_name)
        except Exception as e:
            print(e)
            self.log_msg.emit(f"{shop_name} 작업 실패")

    # 일반 쇼핑몰 작업
    def shop_regist(self):
        print("일반 쇼핑몰 작업")

        try:
            shop_name = StoreNameEnum.Cafe24.value
            self.shop_regist_upload(shop_name)
        except Exception as e:
            print(e)
            self.log_msg.emit(f"{shop_name} 작업 실패")

        try:
            shop_name = StoreNameEnum.Coupang.value
            self.shop_regist_upload(shop_name)
        except Exception as e:
            print(e)
            self.log_msg.emit(f"{shop_name} 작업 실패")

        try:
            shop_name = StoreNameEnum.Grip.value
            self.shop_regist_upload(shop_name)
        except Exception as e:
            print(e)
            self.log_msg.emit(f"{shop_name} 작업 실패")

        try:
            shop_name = StoreNameEnum.Brandi.value
            self.shop_regist_upload(shop_name)
        except Exception as e:
            print(e)
            self.log_msg.emit(f"{shop_name} 작업 실패")

        try:
            shop_name = StoreNameEnum.KakaoTalkStore.value
            self.shop_regist_upload(shop_name)
        except Exception as e:
            print(e)
            self.log_msg.emit(f"{shop_name} 작업 실패")

    def shop_regist_upload(self, shop_name):
        driver = self.driver

        self.sabangnet_regist_menu()

        # 날짜 검색 기준 설정
        search_date_setting = driver.find_element(By.XPATH, '//li[./span[contains(text(), "상품등록일")]]')
        driver.execute_script("arguments[0].click();", search_date_setting)
        time.sleep(0.2)

        target_date: str = self.target_date
        target_date = target_date.replace("-", "")

        # 시작일
        input_start_date = driver.find_elements(By.XPATH, '//div[contains(@class, "date-editor")]/input')[0]
        input_start_date.clear()
        input_start_date.send_keys(target_date, Keys.ENTER)
        time.sleep(0.2)

        # 종료일
        input_end_date = driver.find_elements(By.XPATH, '//div[contains(@class, "date-editor")]/input')[1]
        input_end_date.clear()
        input_end_date.send_keys(target_date, Keys.ENTER)
        time.sleep(0.2)

        # 검색 버튼 클릭
        search_button = driver.find_element(
            By.XPATH, '//button[contains(@class, "search-btn")][./span[contains(text(), "검색")]]'
        )
        driver.execute_script("arguments[0].click();", search_button)
        time.sleep(0.2)

        # table에 검색 결과가 나오지 않으면 오류로 간주
        # $x('//table[contains(@class, "table__body")]//tr')
        try:
            WebDriverWait(driver, 5).until(
                EC.visibility_of_element_located((By.XPATH, '//table[contains(@class, "table__body")]//tr'))
            )
            time.sleep(0.5)

        except Exception as e:
            self.log_msg.emit(f"[{self.target_date}] 검색 결과를 발견하지 못했습니다.")
            raise Exception(f"[{self.target_date}] 검색 결과를 발견하지 못했습니다.")

        # 쇼핑몰선택
        shop_select = driver.find_element(By.XPATH, f'//li[./span[text()="{shop_name}"]]')
        driver.execute_script("arguments[0].click();", shop_select)
        time.sleep(0.2)

    # 전체작업 시작
    def work_start(self):
        print(f"process: work_start")

        try:
            self.sabangnet_login()

            for target_date in self.guiDto.target_date_list:
                self.target_date = target_date

                try:
                    print(f"[{self.target_date}] 작업 시작")

                    self.sabangnet_main()

                    print(f"11번가, 위메프: {self.guiDto.is_eleven}")

                    if self.guiDto.is_eleven:
                        self.eleven_shop_regist()
                    else:
                        self.shop_regist()

                except Exception as e:
                    print(e)
                    continue

        except Exception as e:
            print(e)

        finally:
            self.driver.close()
            time.sleep(0.2)


if __name__ == "__main__":
    # process = SabangnetAutoUploaderProcess()
    # process.work_start()
    pass
