if 1 == 1:
    import sys
    import warnings
    import os

    sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
    warnings.simplefilter("ignore", UserWarning)
    sys.coinit_flags = 2

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from common.chrome import *
from dtos.gui_dto import *
from common.utils import global_log_append
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest

from configs.program_config import ProgramConfig as Config

from tabs.sabangnet_regist_upload_tab import SabangnetRegistUploadTab
from tabs.sabangnet_stock_setting_tab import SabangnetStockSettingTab
from tabs.sabangnet_modify_upload_tab import SabangnetModifyUploadTab
from tabs.user_setting_tab import UserSettingTab


# 오류 발생 시 프로그램 강제종료 방지
def my_exception_hook(exctype, value, traceback):
    print(exctype, value, traceback)
    global_log_append(str(value))
    sys._excepthook(exctype, value, traceback)


sys.excepthook = my_exception_hook

# pyinstaller -n "sabangnet v0.0.6" -w --onefile --clean "main.py" --icon "assets\sb_brand_logo.ico"


class MainUI(QWidget):
    # 초기화
    def __init__(self):
        self.config = Config()

        print(f"exe_path: {self.config.exe_path}")
        print(f"log_folder_path: {self.config.log_folder_path}")

        # UI
        super().__init__()
        self.initUI()

    # 가운데 정렬
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    # 프로그램 닫기 클릭 시
    def closeEvent(self, event):
        quit_msg = "프로그램을 종료하시겠습니까?"
        reply = QMessageBox.question(self, "프로그램 종료", quit_msg, QMessageBox.Yes, QMessageBox.No)

        if reply == QMessageBox.Yes:
            print(f"프로그램을 종료합니다.")
            event.accept()
        else:
            print(f"종료 취소")
            event.ignore()

    # 아이콘 설정
    def set_window_icon_from_response(self, http_response):
        pixmap = QPixmap()
        pixmap.loadFromData(http_response.readAll())
        icon = QIcon(pixmap)
        self.setWindowIcon(icon)

    # 메인 UI
    def initUI(self):
        # 이미지 주소를 복사해야 함
        ICON_IMAGE_URL = "https://i.imgur.com/oZSmG3V.png"
        self.icon = QNetworkAccessManager()
        self.icon.finished.connect(self.set_window_icon_from_response)
        self.icon.get(QNetworkRequest(QUrl(ICON_IMAGE_URL)))

        # 탭 초기화
        self.sabangnet_regist_upload_tab = SabangnetRegistUploadTab()
        self.sabangnet_stock_setting_tab = SabangnetStockSettingTab()
        self.sabangnet_modify_upload_tab = SabangnetModifyUploadTab()
        self.user_setting_tab = UserSettingTab()

        # 탭 추가
        tabs = QTabWidget()
        tabs.addTab(self.sabangnet_regist_upload_tab, "등록송신")
        tabs.addTab(self.sabangnet_stock_setting_tab, "품절설정")
        tabs.addTab(self.sabangnet_modify_upload_tab, "수정송신")
        tabs.addTab(self.user_setting_tab, "사용자 설정")

        vbox = QVBoxLayout()

        vbox.addWidget(tabs)
        self.setLayout(vbox)

        # 앱 기본 설정
        self.setWindowTitle(f"sabangnet v0.0.6")
        self.resize(600, 600)
        self.center()
        self.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = MainUI()
    sys.exit(app.exec_())
