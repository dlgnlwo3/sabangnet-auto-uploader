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

from common.google_sheet import get_worksheet


class SabangnetModifyUploadProcess:
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
        driver.refresh()
        time.sleep(0.5)
        driver.get("https://sbadmin09.sabangnet.co.kr/#/dashboard")
        time.sleep(0.5)
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//a[contains(@href, "dashboard")]'))
        )
        time.sleep(0.5)

    # 쇼핑몰상품수정 화면 이동
    def sabangnet_store_upload_menu(self):
        driver = self.driver
        driver.refresh()
        time.sleep(0.5)
        driver.get("https://sbadmin09.sabangnet.co.kr/#/mall/mall-product-update")
        time.sleep(0.5)
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, '//div[./span[contains(text(), "쇼핑몰상품수정")]][not(contains(@class, "scroll"))]')
            )
        )
        time.sleep(1)

    def modify_upload(self, product_code: str, product_name: str, detail_modify: str, html_modify: str):
        driver = self.driver

        self.sabangnet_store_upload_menu()

        print(product_code, product_name, detail_modify, html_modify)

        # 날짜 검색 기준 -> 송신일 (기본설정됨)
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

        # 쇼핑몰(중복선택)
        # 상세이미지 수정 송신 -> 11번가,그립,브랜디,카카오톡스토어
        # HTML 수정 송신 -> 그립,브랜디,카카오톡스토어
        # $x('//div[contains(text(), "쇼핑몰(중복선택)")]/following-sibling::div//ul/li[./span[text()="11번가"]]')
        if detail_modify == "O" or detail_modify == "o":
            modify_type = "detail"
            target_store_list = [
                StoreNameEnum.Grip.value,
                StoreNameEnum.KakaoTalkStore.value,
                StoreNameEnum.Coupang.value,
            ]

        elif html_modify == "O" or html_modify == "o":
            modify_type = "html"
            target_store_list = [
                StoreNameEnum.ElevenStreet.value,
                StoreNameEnum.Grip.value,
                StoreNameEnum.KakaoTalkStore.value,
                StoreNameEnum.Brandi.value,
                StoreNameEnum.Coupang.value,
                StoreNameEnum.WeMakePrice.value,
            ]

        for target_store in target_store_list:
            target_store_select = driver.find_element(
                By.XPATH,
                f'//div[contains(text(), "쇼핑몰(중복선택)")]/following-sibling::div//ul/li[./span[text()="{target_store}"]]',
            )
            driver.execute_script("arguments[0].click();", target_store_select)
            time.sleep(0.2)

        print()

        # 자체상품코드 입력 후 엔터 (검색버튼의 셀렉터가 약간 다름)
        # $x('//div[contains(text(), "검색항목")]/following-sibling::div//input[not(contains(@readonly, "readonly"))]')
        input_product_code = driver.find_element(
            By.XPATH,
            '//div[contains(text(), "검색항목")]/following-sibling::div//input[not(contains(@readonly, "readonly"))]',
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

        # 상품 전체 선택
        select_all_checkbox = driver.find_element(By.XPATH, '//thead//th//input[contains(@class, "checkbox")]')
        driver.execute_script("arguments[0].click();", select_all_checkbox)
        time.sleep(0.2)

        # html 수정 송신의 경우 '위메프 -> 쇼핑몰별 상세설명 적용 부분 체크'
        # 위메프는 'shop0287'로 검색됨
        # $x('//tr[.//img[@title="shop0287"]]/td[contains(@class, "column_29")]//input[@type="checkbox"]')
        if modify_type == "html":
            store_detail_note_checkbox = driver.find_element(
                By.XPATH, '//tr[.//img[@title="shop0287"]]/td[contains(@class, "column_29")]//input[@type="checkbox"]'
            )
            driver.execute_script("arguments[0].click();", store_detail_note_checkbox)
            time.sleep(0.2)

        # 상품수정송신 -> 새 창이 열림
        regist_upload_button = driver.find_element(By.XPATH, '//button[./span[contains(text(), "상품수정송신")]]')
        driver.execute_script("arguments[0].click();", regist_upload_button)
        time.sleep(0.2)

        tabs = driver.window_handles
        print(tabs)
        try:
            driver.switch_to.window(tabs[1])
            self.upload_modify()

        except Exception as e:
            print(e)
            self.log_msg.emit(f"작업 실패 {e}")

        finally:
            # 원래 탭으로 돌아오기
            driver.close()
            driver.switch_to.window(tabs[0])
            time.sleep(0.5)

        print()

    # 상품수정송신
    def upload_modify(self):
        driver = self.driver
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//div[./span[contains(text(), "상품수정 송신")]]'))
        )
        time.sleep(0.5)

        # 일반항목
        product_state_change_radio_button = driver.find_element(
            By.XPATH, '//tr[./td[.//strong[contains(text(), "판매상태와 옵션재고수량을 제외한 항목을 수정합니다.")]]]//input[@type="radio"]'
        )
        driver.execute_script("arguments[0].click();", product_state_change_radio_button)
        time.sleep(0.2)

        # 즉시송신 버튼 클릭
        submit_button = driver.find_element(By.XPATH, '//button[./span[contains(text(), "즉시송신")]]')
        driver.execute_script("arguments[0].click();", submit_button)
        time.sleep(0.2)

        # $x('//div[contains(text(), "상세설명")]')
        WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, '//div[contains(text(), "상세설명")]')))
        time.sleep(0.5)

        # $x('//div[contains(text(), "상세설명")]/following-sibling::div//label[.//span[text()="수정함"]]//input')
        detail_state_radio_button = driver.find_element(
            By.XPATH, '//div[contains(text(), "상세설명")]/following-sibling::div//label[.//span[text()="수정함"]]//input'
        )
        driver.execute_script("arguments[0].click();", detail_state_radio_button)
        time.sleep(0.2)

        print(f"즉시송신 클릭 시점")

    def get_gs_data(self, url, sheet_name):
        self.worksheet = get_worksheet(url, sheet_name)
        data = self.worksheet.get_all_values()
        headers = data.pop(0)
        df = pd.DataFrame(data, columns=headers)
        df = df.fillna("")
        return df

    # 전체작업 시작
    def work_start(self):
        self.df_googlesheet = self.get_gs_data(self.guiDto.google_sheet_url, self.guiDto.selected_sheet_name)

        self.get_df_product_code()
        print(f"{len(self.df_googlesheet)}개의 데이터 중 {len(self.df_product_code)}개의 자체상품코드를 발견했습니다.")
        self.log_msg.emit(f"{len(self.df_googlesheet)}개의 데이터 중 {len(self.df_product_code)}개의 자체상품코드를 발견했습니다.")

        try:
            self.sabangnet_login()

            for i, row in self.df_product_code[:].iterrows():
                try:
                    product_code = str(row[ModifySheetEnum.ProductCode.value])
                    product_name = str(row[ModifySheetEnum.ProductName.value])
                    detail_modify = str(row[ModifySheetEnum.DetailModify.value])
                    html_modify = str(row[ModifySheetEnum.HTMLModify.value])

                    if detail_modify != "":
                        pass
                    else:
                        detail_modify = "X"

                    if html_modify != "":
                        pass
                    else:
                        html_modify = "X"

                    print(f"{i}, {product_code}, {product_name}, {detail_modify}, {html_modify} 작업 시작")
                    self.log_msg.emit(f"{i}, {product_code}, {product_name}, {detail_modify}, {html_modify} 작업 시작")

                    self.sabangnet_main()

                    self.modify_upload(product_code, product_name, detail_modify, html_modify)

                    print(f"작업 완료")

                    self.log_msg.emit(f"{i}, {product_code}, {product_name}, {detail_modify}, {html_modify} 작업 완료")

                except Exception as e:
                    print(e)
                    self.log_msg.emit(f"{i}, {product_code}, {product_name}, {detail_modify}, {html_modify} 작업 실패")
                    continue

                finally:
                    pass

        except Exception as e:
            print(e)

        finally:
            self.driver.quit()
            time.sleep(0.2)


if __name__ == "__main__":
    # process = SabangnetModifyUploadProcess()
    # process.work_start()
    pass
