if 1 == 1:
    import sys
    import warnings
    import os

    sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
    warnings.simplefilter("ignore", UserWarning)
    sys.coinit_flags = 2
from tkinter import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from dtos.gui_dto import *
from datetime import timedelta
from timeit import default_timer as timer

from process.sabangnet_modify_upload_process import SabangnetModifyUploadProcess

import debugpy


class SabangnetModifyUploadThread(QThread):
    log_msg = pyqtSignal(str)
    modify_upload_finished = pyqtSignal()

    # 호출 시점
    def __init__(self):
        super().__init__()

    # guiDto세팅
    def setGuiDto(self, guiDto: GUIDto):
        self.guiDto = guiDto

    def run(self):
        try:
            debugpy.debug_this_thread()

            self.log_msg.emit(f"시작")

            start_time = timer()

            process = SabangnetModifyUploadProcess()

            process.setGuiDto(self.guiDto)

            process.setLogger(self.log_msg)

            process.work_start()

            end_time = timer()

            progress_time = timedelta(seconds=end_time - start_time).seconds

            self.log_msg.emit(f"총 {str(progress_time)}초 소요되었습니다.")

        except Exception as e:
            print(f"작업 중 오류가 발생했습니다. {str(e)}")
            self.log_msg.emit(f"작업 중 오류가 발생했습니다. {str(e)}")

        self.modify_upload_finished.emit()

    def stop(self):
        try:
            self.terminate()
        except Exception as e:
            print(e)
