import sys

from PyQt5.QtWidgets import QMainWindow, QApplication, QAbstractItemView, QDialog

from src.database.sql_queries import Queries
from src.database.sql_edit_ops import TableChanges
from src.generated_views.contactDisplayHome import Ui_MainWindow
from src.model.contacts_default_table_model import ContactsDefaultTable
from src.views.contact_form import ContactForm


class HomePage(QMainWindow):

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.sql_crud_model = TableChanges()

        self.sql_query_model = Queries()
        contact_list = self.sql_query_model.get_combined_contact_info()
        contact_list_dict = self.sql_query_model.get_contacts_json()
        self._defalt_table_model_list = [[k]+v for k, v in contact_list.items()]
        self._defalt_table_model_dict = contact_list_dict

        table_model = ContactsDefaultTable(self._defalt_table_model_list)

        self.ui.contactsDefaultTable.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.ui.contactsDefaultTable.setModel(table_model)
        self.ui.contactsDefaultTable.setSortingEnabled(True)
        self.ui.contactsDefaultTable.resizeColumnsToContents()

        self.ui.editEntry.clicked.connect(self.edit_default_table_entry)
        self.ui.addEntry.clicked.connect(self.add_default_table_entry)
        self.ui.deleteEntry.clicked.connect(self.delete_default_table_entry)

    def edit_default_table_entry(self):
        selection_model = self.ui.contactsDefaultTable.selectionModel()
        selected_indices = selection_model.selectedIndexes()
        if len(selected_indices) > 0:
            cid = selected_indices[0].data()
            obj_to_edit = self._defalt_table_model_dict[cid]
            fname, mname, lname = (obj_to_edit["name"].values())
            dlg = ContactForm(obj_to_edit.copy(), cid)
            result = dlg.exec()
            if result == QDialog.Accepted:
                modified_dict = dlg.model
                nfname, nmname, nlname = (modified_dict["name"].values())
                if fname != nfname or mname != nmname or nlname != lname:
                    self.sql_crud_model.update_contact_name(
                        modified_dict["name"],
                        cid
                    )
                    self.refresh_view()
                    row_num = 0
                    for r_num, entry in enumerate(self._defalt_table_model_list):
                        if int(entry[0]) == int(cid):
                            row_num = r_num
                            break

                    self.ui.contactsDefaultTable.selectRow(row_num)
                else:
                    print("No Change detected")

    def add_default_table_entry(self):
        new_person_dict = {
            "name": {
                "first_name": "",
                "middle_name": "",
                "last_name": ""
            },
            "addresses": {},
            "phones": {},
            "dates": {}
        }
        dlg = ContactForm(new_person_dict.copy(), -1)
        result = dlg.exec()
        if result == QDialog.Accepted:
            modified_dict = dlg.model
            if any(modified_dict["name"].values()):
                print("Minimal Contact Creation Possible")
                cid = self.sql_crud_model.add_contact(modified_dict)
                self.refresh_view()
                row_num = 0
                for r_num, entry in enumerate(self._defalt_table_model_list):
                    if int(entry[0]) == int(cid):
                        row_num = r_num
                        break

                self.ui.contactsDefaultTable.selectRow(row_num)
            else:
                print("No Change detected, delete new row")

    def delete_default_table_entry(self):
        selection_model = self.ui.contactsDefaultTable.selectionModel()
        selected_indices = selection_model.selectedIndexes()
        if len(selected_indices) > 0:
            cid = selected_indices[0].data()
            self.sql_crud_model.delete_contact(cid)
            self.refresh_view()

    def refresh_view(self):
        contact_list = self.sql_query_model.get_combined_contact_info()
        contact_list_dict = self.sql_query_model.get_contacts_json()
        self._defalt_table_model_list = [[k] + v for k, v in contact_list.items()]
        self._defalt_table_model_dict = contact_list_dict
        table_model = ContactsDefaultTable(self._defalt_table_model_list)
        self.ui.contactsDefaultTable.setModel(table_model)
        self.ui.contactsDefaultTable.resizeColumnsToContents()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = HomePage()
    win.show()
    sys.exit(app.exec_())
