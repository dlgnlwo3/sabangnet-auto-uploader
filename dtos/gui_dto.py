if 1 == 1:
    import sys
    import os

    sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))


class GUIDto:
    def __init__(self):
        self.__google_sheet_url = ""
        self.__selected_sheet_name = ""
        self.__sabangnet_id = ""
        self.__sabangnet_pw = ""
        self.__target_date_list = []

        # 등록송신 시 [11번가, 위메프], [일반 쇼핑몰]인지 확인하는 부분
        self.__is_eleven = bool

    @property
    def google_sheet_url(self):  # getter
        return self.__google_sheet_url

    @google_sheet_url.setter
    def google_sheet_url(self, value):  # setter
        self.__google_sheet_url = value

    @property
    def selected_sheet_name(self):  # getter
        return self.__selected_sheet_name

    @selected_sheet_name.setter
    def selected_sheet_name(self, value):  # setter
        self.__selected_sheet_name = value

    @property
    def sabangnet_id(self):  # getter
        return self.__sabangnet_id

    @sabangnet_id.setter
    def sabangnet_id(self, value):  # setter
        self.__sabangnet_id = value

    @property
    def sabangnet_pw(self):  # getter
        return self.__sabangnet_pw

    @sabangnet_pw.setter
    def sabangnet_pw(self, value):  # setter
        self.__sabangnet_pw = value

    @property
    def target_date_list(self):  # getter
        return self.__target_date_list

    @target_date_list.setter
    def target_date_list(self, value):  # setter
        self.__target_date_list = value

    @property
    def is_eleven(self):  # getter
        return self.__is_eleven

    @is_eleven.setter
    def is_eleven(self, value):  # setter
        self.__is_eleven = value

    def to_print(self):
        print("google_sheet_url: ", self.google_sheet_url)
        print("sabangnet_id: ", self.sabangnet_id)
        print("sabangnet_pw: ", self.sabangnet_pw)
