from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QDialog, QTableWidgetItem, QShortcut, QAbstractItemView

from src.database.sql_edit_ops import TableChanges
from src.generated_views.contactForm import Ui_ContactForm
from src.views.mini_editors import DateEditor, PhoneEditor, AddressEditor


class ContactForm(QDialog):

    def __init__(self, contact_entry, cid):
        super().__init__()
        self._ui = Ui_ContactForm()
        self._ui.setupUi(self)
        self.model = contact_entry
        self.cid = cid
        self.sql_crud_model = TableChanges()

        self.setup_name_fields()
        self.setup_addresses()
        self.setup_phones()
        self.setup_dates()

        self._ui.saveButton.clicked.connect(lambda: self.accept())
        self._ui.cancelButton.clicked.connect(lambda: self.reject())
        self.quitSc = QShortcut(QKeySequence('Ctrl+W'), self)
        self.quitSc.activated.connect(lambda: self.reject())

        self._ui.fnameField.textChanged.connect(self.name_change_tracker)
        self._ui.mnameField.textChanged.connect(self.name_change_tracker)
        self._ui.lnameField.textChanged.connect(self.name_change_tracker)

        # addresses
        self._ui.addAddress.clicked.connect(self.add_address)
        self._ui.editAddress.clicked.connect(self.edit_address)
        self._ui.removeAddress.clicked.connect(self.delete_address)

        # phones
        self._ui.addPhone.clicked.connect(self.add_phone)
        self._ui.editPhone.clicked.connect(self.edit_phone)
        self._ui.removePhone.clicked.connect(self.delete_phone)

        # dates
        self._ui.addDate.clicked.connect(self.add_date)
        self._ui.editDate.clicked.connect(self.edit_date)
        self._ui.removeDate.clicked.connect(self.delete_date)

    def setup_name_fields(self):
        contact_entry = self.model
        self._ui.fnameField.setText(contact_entry["name"]["first_name"])
        self._ui.mnameField.setText(contact_entry["name"]["middle_name"])
        self._ui.lnameField.setText(contact_entry["name"]["last_name"])

    def setup_addresses(self):
        addresses = self.model["addresses"]
        self._ui.addressTable.setSortingEnabled(False)
        self._ui.addressTable.clear()
        self._ui.addressTable.setRowCount(0)
        row_num = self._ui.addressTable.rowCount()

        if addresses:
            for type_a, address in addresses.items():
                self._ui.addressTable.insertRow(row_num)
                for i, header_name in enumerate(["type_a", "address", "city", "state", "zip"]):
                    if header_name == "type_a":
                        txt = type_a
                    else:
                        txt = address.get(f"{type_a}_{header_name}", address.get(header_name))
                    item = QTableWidgetItem(txt)
                    self._ui.addressTable.setItem(row_num, i, item)
                row_num += 1

        self._ui.addressTable.setSortingEnabled(True)
        self._ui.addressTable.resizeColumnsToContents()
        self._ui.addressTable.setSelectionBehavior(QAbstractItemView.SelectRows)

    def setup_phones(self):
        phones = self.model["phones"]
        self._ui.phoneTable.clear()
        self._ui.phoneTable.setRowCount(0)
        row_num = self._ui.phoneTable.rowCount()
        self._ui.phoneTable.setSortingEnabled(False)

        if phones:
            for ptype, pval in phones.items():
                self._ui.phoneTable.insertRow(row_num)
                area_code, number = pval.split("-", 1)
                self._ui.phoneTable.setItem(row_num, 0, QTableWidgetItem(ptype))
                self._ui.phoneTable.setItem(row_num, 1, QTableWidgetItem(area_code))
                self._ui.phoneTable.setItem(row_num, 2, QTableWidgetItem(number))
                row_num += 1

        self._ui.phoneTable.setSortingEnabled(True)
        self._ui.phoneTable.resizeColumnsToContents()
        self._ui.phoneTable.setSelectionBehavior(QAbstractItemView.SelectRows)

    def setup_dates(self):
        dates = self.model["dates"]
        self._ui.dateTable.clear()
        self._ui.dateTable.setRowCount(0)
        row_num = self._ui.dateTable.rowCount()
        self._ui.dateTable.setSortingEnabled(False)

        if dates:
            for dtype, dval in dates.items():
                self._ui.dateTable.insertRow(row_num)
                self._ui.dateTable.setItem(row_num, 0, QTableWidgetItem(dtype))
                self._ui.dateTable.setItem(row_num, 1, QTableWidgetItem(dval))
                row_num += 1

        self._ui.dateTable.setSortingEnabled(True)
        self._ui.dateTable.resizeColumnsToContents()
        self._ui.dateTable.setSelectionBehavior(QAbstractItemView.SelectRows)

    def name_change_tracker(self):

        name_dict = {
            "first_name": self._ui.fnameField.text(),
            "middle_name": self._ui.mnameField.text(),
            "last_name": self._ui.lnameField.text()
        }

        if self.cid != -1:
            self.sql_crud_model.update_contact_name(name_dict, self.cid)

        self.model["name"] = name_dict

    def add_address(self):
        dlg = AddressEditor(("", {
                "_address": "",
                "_city": "",
                "_state": "",
                "_zip": ""
            }))
        if dlg.exec() == QDialog.Accepted:
            atype, avals = dlg.address_type_dict_pair
            if atype:
                self.model["addresses"][atype] = avals
                if self.cid != -1:
                    self.sql_crud_model.add_address_for_cid(avals, atype, self.cid)
                self.setup_addresses()

    def edit_address(self):
        selection_model = self._ui.addressTable.selectionModel()
        selections = selection_model.selectedRows()
        if len(selections) > 0:
            row_num = selections[0].row()
            otype, oadd = None, None
            for i, add in enumerate(self.model["addresses"].items()):
                if row_num == i:
                    otype = add[0]
                    oadd = add[1]

            dlg = AddressEditor((otype, oadd))
            if dlg.exec() == QDialog.Accepted:
                atype, avals = dlg.address_type_dict_pair
                if atype:
                    oadd = {k.split("_", 1)[-1]: v for k, v in oadd.items()}
                    if self.cid != -1:
                        self.sql_crud_model.update_address_for_cid(
                            oadd,
                            otype,
                            avals,
                            atype,
                            self.cid
                        )
                    self.model["addresses"].pop(otype, None)
                    self.model["addresses"][atype] = avals
                    self.setup_addresses()

    def delete_address(self):
        selection_model = self._ui.addressTable.selectionModel()
        selections = selection_model.selectedRows()
        if len(selections) > 0:
            row_num = selections[0].row()
            otype, oadd = None, None
            for i, add in enumerate(self.model["addresses"].items()):
                if row_num == i:
                    otype = add[0]
                    oadd = add[1]
            oadd = {k.split("_", 1)[-1]: v for k, v in oadd.items()}
            if self.cid != -1:
                self.sql_crud_model.delete_address_for_cid(
                    oadd,
                    otype,
                    self.cid
                )
            self.model["addresses"].pop(otype, None)
            self.setup_addresses()

    def add_phone(self):
        dlg = PhoneEditor(("", "123-1231231"))
        if dlg.exec() == QDialog.Accepted:
            if self.cid != -1:
                self.sql_crud_model.add_phone_for_cid(
                    dlg.phone_pair,
                    self.cid
                )
            self.model["phones"][dlg.phone_pair[0]] = dlg.phone_pair[1]
            self.setup_phones()

    def edit_phone(self):
        selection_model = self._ui.phoneTable.selectionModel()
        selections = selection_model.selectedRows()
        if len(selections) > 0:
            row_num = selections[0].row()
            optype = self._ui.phoneTable.item(row_num, 0).text()
            oarc = self._ui.phoneTable.item(row_num, 1).text()
            onum = self._ui.phoneTable.item(row_num, 2).text()
            dlg = PhoneEditor((optype, f"{oarc}-{onum}"))
            if dlg.exec() == QDialog.Accepted:
                if self.cid != -1:
                    self.sql_crud_model.update_phone_for_cid(
                        (optype, f"{oarc}-{onum}"),
                        dlg.phone_pair,
                        self.cid
                    )
                self.model["phones"].pop(optype, None)
                self.model["phones"][dlg.phone_pair[0]] = dlg.phone_pair[1]
                self.setup_phones()

    def delete_phone(self):
        selection_model = self._ui.phoneTable.selectionModel()
        selections = selection_model.selectedRows()
        if len(selections) > 0:
            row_num = selections[0].row()
            optype = self._ui.phoneTable.item(row_num, 0).text()
            oarc = self._ui.phoneTable.item(row_num, 1).text()
            onum = self._ui.phoneTable.item(row_num, 2).text()
            if self.cid != -1:
                self.sql_crud_model.delete_phone_for_cid(
                    (optype, f"{oarc}-{onum}"),
                    self.cid
                )
            self.model["phones"].pop(optype, None)
            self.setup_phones()

    def add_date(self):
        dlg = DateEditor(("", "0-0-0"))
        if dlg.exec() == QDialog.Accepted:
            if self.cid != -1:
                self.sql_crud_model.add_date_for_cid(
                    dlg.date_pair,
                    self.cid
                )
            self.model["dates"][dlg.date_pair[0]] = dlg.date_pair[1]
            self.setup_dates()

    def edit_date(self):
        selection_model = self._ui.dateTable.selectionModel()
        selections = selection_model.selectedRows()
        if len(selections) > 0:
            row_num = selections[0].row()
            odtype = self._ui.dateTable.item(row_num, 0).text()
            odval = self._ui.dateTable.item(row_num, 1).text()
            dlg = DateEditor((odtype, odval))
            if dlg.exec() == QDialog.Accepted:
                if self.cid != -1:
                    self.sql_crud_model.update_date_for_cid(
                        (odtype, odval),
                        dlg.date_pair,
                        self.cid
                    )
                self.model["dates"].pop(odtype, None)
                self.model["dates"][dlg.date_pair[0]] = dlg.date_pair[1]
                self.setup_dates()

    def delete_date(self):
        selection_model = self._ui.dateTable.selectionModel()
        selections = selection_model.selectedRows()
        if len(selections) > 0:
            row_num = selections[0].row()
            odtype = self._ui.dateTable.item(row_num, 0).text()
            odval = self._ui.dateTable.item(row_num, 1).text()

            if self.cid != -1:
                self.sql_crud_model.delete_date_for_cid((odtype, odval), self.cid)

            self.model["dates"].pop(odtype, None)
            self.setup_dates()
