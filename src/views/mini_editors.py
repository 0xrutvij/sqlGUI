from PyQt5 import QtGui
from PyQt5.QtCore import QDate
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QDialog, QShortcut

from src.generated_views.addressEdit import Ui_addressEditor
from src.generated_views.phoneEdit import Ui_phoneEditor
from src.generated_views.dateEdit import Ui_dateEditor


class DateEditor(QDialog):

    def __init__(self, date_pair):
        super().__init__()
        self.date_pair = date_pair
        self.ui = Ui_dateEditor()
        self.ui.setupUi(self)

        dtype, dval = self.date_pair
        date = QDate(*[int(x) for x in dval.split("-")])
        self.ui.dateField.setDate(date)
        self.ui.typeField.setText(dtype)

        self.ui.saveButton.clicked.connect(lambda: self.accept())
        self.ui.cancelButton.clicked.connect(lambda: self.reject())
        self.quitSc = QShortcut(QKeySequence("Ctrl+W"), self)
        self.quitSc.activated.connect(lambda: self.reject())

        self.ui.dateField.dateChanged.connect(self.update_pair)
        self.ui.typeField.textChanged.connect(self.update_pair)

    def update_pair(self):

        self.date_pair = (self.ui.typeField.text(), "-".join(map(str, self.ui.dateField.date().getDate())))

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.reject()


class PhoneEditor(QDialog):

    def __init__(self, phone_pair):
        super().__init__()
        self.ui = Ui_phoneEditor()
        self.ui.setupUi(self)
        self.phone_pair = phone_pair

        ptype, pval = self.phone_pair
        area_code, number = "", ""
        if pval:
            area_code, number = pval.split("-", 1)

        self.ui.typeField.setText(ptype)
        self.ui.areaField.setText(area_code)
        self.ui.numberField.setText(number)

        self.ui.saveButton.clicked.connect(lambda: self.accept())
        self.ui.cancelButton.clicked.connect(lambda: self.reject())
        self.quitSc = QShortcut(QKeySequence('Ctrl+W'), self)
        self.quitSc.activated.connect(lambda: self.reject())

        self.ui.typeField.textChanged.connect(self.update_pair)
        self.ui.areaField.textChanged.connect(self.update_pair)
        self.ui.numberField.textChanged.connect(self.update_pair)

    def update_pair(self):
        ptype = self.ui.typeField.text()
        area_code = self.ui.areaField.text()
        number = self.ui.numberField.text()
        self.phone_pair = (ptype, f"{area_code}-{number}")

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.reject()


class AddressEditor(QDialog):

    def __init__(self, address_type_dict_pair):
        super().__init__()
        self.ui = Ui_addressEditor()
        self.ui.setupUi(self)
        self.address_type_dict_pair = address_type_dict_pair

        atype, avals = self.address_type_dict_pair
        self.ui.typeField.setText(atype)
        self.ui.addressField.setText(avals[f"{atype}_address"])
        self.ui.cityField.setText(avals[f"{atype}_city"])
        self.ui.stateField.setText(avals[f"{atype}_state"])
        self.ui.zipField.setText(avals[f"{atype}_zip"])
        self.update_address()

        self.ui.typeField.textChanged.connect(self.update_address)
        self.ui.addressField.textChanged.connect(self.update_address)
        self.ui.cityField.textChanged.connect(self.update_address)
        self.ui.stateField.textChanged.connect(self.update_address)
        self.ui.zipField.textChanged.connect(self.update_address)

        self.quitSc = QShortcut(QKeySequence('Ctrl+W'), self)
        self.quitSc.activated.connect(lambda: self.reject())

        self.ui.buttonBox.accepted.connect(lambda: self.accept())
        self.ui.buttonBox.rejected.connect(lambda: self.reject())

    def update_address(self):
        avals = {}
        atype = self.ui.typeField.text()
        avals["address"] = self.ui.addressField.text()
        avals["city"] = self.ui.cityField.text()
        avals["state"] = self.ui.stateField.text()
        avals["zip"] = self.ui.zipField.text()

        self.address_type_dict_pair = (atype, avals)
