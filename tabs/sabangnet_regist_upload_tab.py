import sys
import warnings

warnings.simplefilter("ignore", UserWarning)
sys.coinit_flags = 2
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from datetime import *

from threads.sabangnet_regist_upload_thread import SabangnetRegistUploadThread
from dtos.gui_dto import GUIDto
from common.utils import *

from common.account_file import AccountFile
import pandas as pd

from configs.sabangnet_auto_uploader_config import SabangnetAutoUploaderConfig as Config
from configs.sabangnet_auto_uploader_config import SabangnetAutoUploaderData as ConfigData

from common.chrome import open_browser, get_chrome_driver
from selenium import webdriver

from common.google_sheet import get_spreadsheet
import gspread


class SabangnetRegistUploadTab(QWidget):
    # 초기화
    def __init__(self):
        self.config = Config()
        __saved_data = self.config.get_data()
        self.saved_data = self.config.dict_to_data(__saved_data)

        super().__init__()
        self.initUI()

    # 로그 작성
    @pyqtSlot(str)
    def log_append(self, text):
        today = str(datetime.now())[0:10]
        now = str(datetime.now())[0:-7]
        self.browser.append(f"[{now}] {str(text)}")
        global_log_append(text)

    # 크롬 브라우저
    def open_chrome_browser(self):
        open_browser()

    # 시작 클릭
    def regist_upload_start_button_clicked(self):
        # sender()를 이용하여 어떤 버튼이 호출했는지 확인
        button = self.sender()

        if button == self.eleven_regist_upload_start_button:
            print("11번가, 위메프")
            is_eleven = True
        elif button == self.regist_upload_start_button:
            print("일반 쇼핑몰")
            is_eleven = False

        self.config = Config()
        __saved_data = self.config.get_data()
        self.saved_data = self.config.dict_to_data(__saved_data)

        selected_date_list = []
        self.date_listwidget.selectAll()
        if len(self.date_listwidget.selectedItems()) <= 0:
            print(f"선택된 날짜가 없습니다.")
            QMessageBox.information(self, "날짜 선택", f"선택된 날짜가 없습니다.")
            return

        else:
            date_list_items = self.date_listwidget.selectedItems()
            for date_item in date_list_items:
                selected_date_list.append(date_item.text())

        if self.saved_data.sabangnet_id == "":
            QMessageBox.information(self, "작업 시작", f"아이디를 입력해주세요.")
            return

        if self.saved_data.sabangnet_pw == "":
            QMessageBox.information(self, "작업 시작", f"비밀번호를 입력해주세요.")
            return

        guiDto = GUIDto()
        guiDto.google_sheet_url = self.saved_data.google_sheet_url
        guiDto.sabangnet_id = self.saved_data.sabangnet_id
        guiDto.sabangnet_pw = self.saved_data.sabangnet_pw
        guiDto.target_date_list = selected_date_list
        guiDto.is_eleven = is_eleven

        self.regist_upload_thread = SabangnetRegistUploadThread()
        self.regist_upload_thread.log_msg.connect(self.log_append)
        self.regist_upload_thread.regist_upload_finished.connect(self.regist_upload_finished)
        self.regist_upload_thread.setGuiDto(guiDto)

        self.regist_upload_start_button.setDisabled(True)
        self.regist_upload_stop_button.setDisabled(False)
        self.eleven_regist_upload_start_button.setDisabled(True)
        self.eleven_regist_upload_stop_button.setDisabled(False)
        self.regist_upload_thread.start()

    # 중지 클릭
    @pyqtSlot()
    def regist_upload_stop_button_clicked(self):
        print(f"search stop clicked")
        self.log_append(f"중지 클릭")
        self.regist_upload_finished()

    # 작업 종료
    @pyqtSlot()
    def regist_upload_finished(self):
        print(f"search thread finished")
        self.log_append(f"작업 종료")
        self.regist_upload_thread.stop()
        self.regist_upload_start_button.setDisabled(False)
        self.regist_upload_stop_button.setDisabled(True)
        self.eleven_regist_upload_start_button.setDisabled(False)
        self.eleven_regist_upload_stop_button.setDisabled(True)
        print(f"thread_is_running: {self.regist_upload_thread.isRunning()}")

    def add_date_button_clicked(self):
        target_date = self.date_edit.text()
        print(target_date)
        self.date_listwidget.addItem(target_date)

    def remove_date_button_clicked(self):
        print("click")
        selected_items = self.date_listwidget.selectedItems()
        if not selected_items:
            return
        for item in selected_items:
            self.date_listwidget.takeItem(self.date_listwidget.row(item))

    # 메인 UI
    def initUI(self):
        # 작업 날짜 선택
        date_edit_groupbox = QGroupBox("날짜 선택")
        self.date_edit = QDateEdit(QDate.currentDate().addDays(-1))
        self.date_edit.setGeometry(100, 100, 150, 40)

        date_edit_inner_layout = QHBoxLayout()
        date_edit_inner_layout.addWidget(self.date_edit)
        date_edit_groupbox.setLayout(date_edit_inner_layout)

        # 날짜 버튼
        date_button_groupbox = QGroupBox("작업 날짜 추가")
        self.add_date_button = QPushButton("날짜 추가")
        self.remove_date_button = QPushButton("날짜 제거")

        self.add_date_button.clicked.connect(self.add_date_button_clicked)
        self.remove_date_button.clicked.connect(self.remove_date_button_clicked)

        date_button_inner_layout = QHBoxLayout()
        date_button_inner_layout.addWidget(self.add_date_button)
        date_button_inner_layout.addWidget(self.remove_date_button)
        date_button_groupbox.setLayout(date_button_inner_layout)

        # 날짜 리스트
        date_list_groupbox = QGroupBox("날짜 목록")
        self.date_listwidget = QListWidget()
        self.date_listwidget.setSelectionMode(QAbstractItemView.MultiSelection)

        date_list_inner_layout = QVBoxLayout()
        date_list_inner_layout.addWidget(self.date_listwidget)
        date_list_groupbox.setLayout(date_list_inner_layout)

        # 사전 작업용 브라우저
        chrome_browser_groupbox = QGroupBox("브라우저 사전 작업")
        self.chrome_browser_button = QPushButton("브라우저 열기")

        self.chrome_browser_button.clicked.connect(self.open_chrome_browser)

        browser_inner_layout = QVBoxLayout()
        browser_inner_layout.addWidget(self.chrome_browser_button)
        chrome_browser_groupbox.setLayout(browser_inner_layout)

        # 11번가, 위메프
        eleven_start_stop_groupbox = QGroupBox("11번가, 위메프")
        self.eleven_regist_upload_start_button = QPushButton("시작")
        self.eleven_regist_upload_stop_button = QPushButton("중지")
        self.eleven_regist_upload_stop_button.setDisabled(True)

        self.eleven_regist_upload_start_button.clicked.connect(self.regist_upload_start_button_clicked)
        self.eleven_regist_upload_stop_button.clicked.connect(self.regist_upload_stop_button_clicked)

        eleven_start_stop_inner_layout = QHBoxLayout()
        eleven_start_stop_inner_layout.addWidget(self.eleven_regist_upload_start_button)
        eleven_start_stop_inner_layout.addWidget(self.eleven_regist_upload_stop_button)
        eleven_start_stop_groupbox.setLayout(eleven_start_stop_inner_layout)

        # 일반 쇼핑몰
        start_stop_groupbox = QGroupBox("일반 쇼핑몰")
        self.regist_upload_start_button = QPushButton("시작")
        self.regist_upload_stop_button = QPushButton("중지")
        self.regist_upload_stop_button.setDisabled(True)

        self.regist_upload_start_button.clicked.connect(self.regist_upload_start_button_clicked)
        self.regist_upload_stop_button.clicked.connect(self.regist_upload_stop_button_clicked)

        start_stop_inner_layout = QHBoxLayout()
        start_stop_inner_layout.addWidget(self.regist_upload_start_button)
        start_stop_inner_layout.addWidget(self.regist_upload_stop_button)
        start_stop_groupbox.setLayout(start_stop_inner_layout)

        # 로그 그룹박스
        log_groupbox = QGroupBox("로그")
        self.browser = QTextBrowser()

        log_inner_layout = QHBoxLayout()
        log_inner_layout.addWidget(self.browser)
        log_groupbox.setLayout(log_inner_layout)

        # 레이아웃 배치
        top_layout = QVBoxLayout()

        mid_layout = QHBoxLayout()
        mid_layout.addWidget(date_edit_groupbox, 7)
        mid_layout.addWidget(date_button_groupbox, 3)

        date_button_layout = QHBoxLayout()

        date_list_layout = QHBoxLayout()
        date_list_layout.addStretch(6)
        date_list_layout.addWidget(date_list_groupbox, 4)

        bottom_layout = QHBoxLayout()
        bottom_layout.addStretch(5)
        # bottom_layout.addWidget(chrome_browser_groupbox, 2)
        bottom_layout.addWidget(eleven_start_stop_groupbox, 3)
        bottom_layout.addWidget(start_stop_groupbox, 3)

        log_layout = QVBoxLayout()
        log_layout.addWidget(log_groupbox)

        layout = QVBoxLayout()
        layout.addLayout(mid_layout, 1)
        layout.addLayout(date_list_layout, 4)
        layout.addLayout(bottom_layout, 1)
        layout.addLayout(log_layout, 8)

        self.setLayout(layout)
