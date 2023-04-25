import sys
import warnings

warnings.simplefilter("ignore", UserWarning)
sys.coinit_flags = 2
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from datetime import *


from configs.sabangnet_auto_uploader_config import SabangnetAutoUploaderConfig as Config
from configs.sabangnet_auto_uploader_config import SabangnetAutoUploaderData as ConfigData


class UserSettingTab(QWidget):
    # 초기화
    def __init__(self):
        self.config = Config()
        __saved_data = self.config.get_data()
        self.saved_data = self.config.dict_to_data(__saved_data)

        super().__init__()
        self.initUI()

    # 상태 저장
    def google_sheet_url_save_button_clicked(self):
        dict_save = {
            "google_sheet_url": self.google_sheet_url.text(),
            "sabangnet_id": self.saved_data.sabangnet_id,
            "sabangnet_pw": self.saved_data.sabangnet_pw,
        }

        question_msg = "현재 상태를 저장하시겠습니까?"
        reply = QMessageBox.question(self, "상태 저장", question_msg, QMessageBox.Yes, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.config.write_data(dict_save)
            print(f"저장")
            QMessageBox.information(self, "상태 저장", f"구글 시트 주소를 저장했습니다.")

        else:
            print(f"저장 취소")

    def sabangnet_account_save_button_clicked(self):
        dict_save = {
            "google_sheet_url": self.saved_data.google_sheet_url,
            "sabangnet_id": self.sabangnet_id.text(),
            "sabangnet_pw": self.sabangnet_pw.text(),
        }

        question_msg = "현재 상태를 저장하시겠습니까?"
        reply = QMessageBox.question(self, "상태 저장", question_msg, QMessageBox.Yes, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.config.write_data(dict_save)
            print(f"저장")
            QMessageBox.information(self, "상태 저장", f"계정 정보를 저장했습니다.")

    # 메인 UI
    def initUI(self):
        # 구글 시트 주소
        google_sheet_url_groupbox = QGroupBox("구글 시트 주소")
        self.google_sheet_url = QLineEdit(f"{self.saved_data.google_sheet_url}")
        self.google_sheet_url_save_button = QPushButton("저장")

        self.google_sheet_url_save_button.clicked.connect(self.google_sheet_url_save_button_clicked)

        google_sheet_url_inner_layout = QHBoxLayout()
        google_sheet_url_inner_layout.addWidget(self.google_sheet_url)
        google_sheet_url_inner_layout.addWidget(self.google_sheet_url_save_button)
        google_sheet_url_groupbox.setLayout(google_sheet_url_inner_layout)

        # 사방넷 계정 정보
        sabangnet_account_groupbox = QGroupBox("사방넷 계정 정보")
        self.sabangnet_id_label = QLabel("아이디")
        self.sabangnet_id = QLineEdit(f"{self.saved_data.sabangnet_id}")
        self.sabangnet_pw_label = QLabel("비밀번호")
        self.sabangnet_pw = QLineEdit(f"{self.saved_data.sabangnet_pw}")
        self.sabangnet_account_save_button = QPushButton("저장")

        self.sabangnet_account_save_button.clicked.connect(self.sabangnet_account_save_button_clicked)

        sabangnet_account_inner_layout = QHBoxLayout()
        sabangnet_account_inner_layout.addWidget(self.sabangnet_id_label)
        sabangnet_account_inner_layout.addWidget(self.sabangnet_id)
        sabangnet_account_inner_layout.addWidget(self.sabangnet_pw_label)
        sabangnet_account_inner_layout.addWidget(self.sabangnet_pw)
        sabangnet_account_inner_layout.addWidget(self.sabangnet_account_save_button)
        sabangnet_account_groupbox.setLayout(sabangnet_account_inner_layout)

        # 레이아웃 배치
        top_layout = QHBoxLayout()
        top_layout.addWidget(google_sheet_url_groupbox)

        mid_layout = QHBoxLayout()
        mid_layout.addWidget(sabangnet_account_groupbox)

        bottom_layout = QHBoxLayout()
        bottom_layout.addStretch(1)
        bottom_layout.addStretch(1)

        layout = QVBoxLayout()
        layout.addLayout(top_layout, 1)
        layout.addLayout(mid_layout, 1)
        layout.addLayout(bottom_layout, 1)
        layout.addStretch(8)

        self.setLayout(layout)
