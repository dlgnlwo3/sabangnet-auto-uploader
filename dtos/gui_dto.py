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

    def to_print(self):
        print("google_sheet_url: ", self.google_sheet_url)
        print("sabangnet_id: ", self.sabangnet_id)
        print("sabangnet_pw: ", self.sabangnet_pw)
