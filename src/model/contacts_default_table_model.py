from typing import Any, List

from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QModelIndex


class ContactsDefaultTable(QtCore.QAbstractTableModel):

    def __init__(self, data):
        super(ContactsDefaultTable, self).__init__()
        self._data = data
        self._header = ["Contact ID", "First Name", "Middle Name",
                        "Last Name", "Address List", "Phone List", "Date List"]

    def data(self, index, role):
        if role == Qt.DisplayRole and index:
            return self._data[index.row()][index.column()]

    def headerData(self, section, orientation, role) -> Any:
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._header[section]
        return None

    def rowCount(self, index):
        # The length of the outer list.
        return len(self._data)

    def columnCount(self, index):
        # The following takes the first sub-list, and returns
        # the length (only works if all rows are an equal length)
        return len(self._data[0])

    def sort(self, column, order):
        try:
            # noinspection PyUnresolvedReferences
            self.layoutAboutToBeChanged.emit()
            self._data.sort(key=lambda k: k[column] or "", reverse=not order)
            self.layoutChanged.emit()
        except Exception as e:
            print(e)

    def insertRows(self, row: int, count: int, parent: QModelIndex) -> bool:

        self.beginInsertRows(QModelIndex(), row, row+count-1)

        for _ in range(count):
            self._data += [[""] * 7]

        self.endInsertRows()
        return True

