from PyQt5.QtCore import pyqtSignal, QModelIndex
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import (
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QAbstractItemView,
    QTableView,
    QHeaderView,
    QPushButton,
    )

from widgets.Dialogs import error

ID_ROLE = 110
SORT_ROLE = 111
FULL_VALUE_ROLE = 112
TABLE_BUTTONS = {'reload':'Оновити', 'create':'Створити', 'edit':'Редагувати', 'copy':'Копіювати', 'delete':'Видалити'}

# field_names specified fields of table to be showed,
# if it is empty - all from data model
class TableModel(QStandardItemModel):
    def __init__(self, data_model: dict, field_names: list = []):
        super().__init__()
        self.field_names = field_names if field_names else data_model.keys()
        self.field_names = [name for name in self.field_names if data_model[name]['def'] != []]
        self.headers = [data_model[name]['hum'] for name in self.field_names]
        self.setHorizontalHeaderLabels(self.headers)
        self.setSortRole(SORT_ROLE)

    def reload(self, values):
        self.clear()
        self.setHorizontalHeaderLabels(self.headers)
        for value in values:
            self.append(value)

    def make_item(self, value, name):
        v = value[name]
        if type(v) == float:
            v = round(v, 2)
        item = QStandardItem(str(v))
        item.setData(v, SORT_ROLE)
        item.setEditable(False)
        return item

    def append(self, value):
        row = []
        for name in self.field_names:
            row.append(self.make_item(value, name))
        row[0].setData(value, FULL_VALUE_ROLE)    
        self.appendRow(row)

    def get_row_value(self, index):
        row_value = self.item(index, 0).data(FULL_VALUE_ROLE)
        return row_value

    def values(self):
        values = []
        for i in range(self.rowCount()):
            row = self.get_row_value(i)
            values.append(row)
        return values


# simple table without links to item
# multiselect enabled
# values gets from outer code
# data model example:
# {
#     "id": {"def": 0, "hum": "Номер"},
#     "name": {"def": "", "hum": "Назва"},
#     "full_name": {"def": "", "hum": "Повна назва"},
#     "matherial_group_id": {"def": 0, "hum": "Група"},
#     "measure_id": {"def": 0, "hum": "Од. виміру"},
#     "cost": {"def": 0.0, "hum": "Ціна"},
#     "is_active": {"def": true, "hum": "Діючий"}
# }
class Table(QWidget):
    valueSelected = pyqtSignal(dict)
    valueDoubleCklicked = pyqtSignal(dict)
    tableChanged = pyqtSignal()
    def __init__(self, data_model: dict, table_fields: list=[], values=[]):
        super().__init__()
        self.box = QVBoxLayout()
        self.setLayout(self.box)

        self.table = QTableView()
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.box.addWidget(self.table)

        self._model = TableModel(data_model, table_fields)
        self.table.setModel(self._model)
        self.table.clicked[QModelIndex].connect(self.value_selected)
        self.table.doubleClicked[QModelIndex].connect(self.value_dblclicked)
        self.table.setSortingEnabled(True)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)

        if values:
            self.reload(values)

    def reload(self, values):
        self._model.reload(values)
        for i in range(self._model.columnCount()):
            self.table.resizeColumnToContents(i)
        self.tableChanged.emit()
        
    # def set_values(self, values):
    #     self.reload(values)

    # def add_value(self, value):
    #     self._model.append(value)

    # def delete_values(self):
    #     while True:
    #         selected_rows = self.get_selected_rows()
    #         if not selected_rows:
    #             return
    #         self._model.removeRow(selected_rows[0])

    # def get_selected_ids(self):
    #     indexes = self.table.selectedIndexes()
    #     if not indexes:
    #         return []
    #     ids = (int(self._model.item(index.row()).text()) for index in indexes)
    #     return ids

    # def get_selected_values(self):
    #     selected_ids = list(self.get_selected_ids())
    #     if not selected_ids:
    #         return []
    #     selected_values = (v for v in self.item.values if v['id'] in selected_ids)
    #     return selected_values

    # def get_selected_value(self):
    #     selected_values = list(self.get_selected_values())
    #     if len(selected_values) != 1:
    #         error('Оберіть один елемент')
    #         return
    #     return selected_values[0]

    # def get_selected_rows(self) -> list:
    #     indexes = self.table.selectedIndexes()
    #     if not indexes:
    #         return []
    #     selected_rows = list(set(index.row() for index in indexes))
    #     return selected_rows

    # def get_selected_row(self) -> int:
    #     rows = self.get_selected_rows()
    #     if len(rows) != 1:
    #         error('Оберіть один елемент')
    #         return -1
    #     return rows[0]

    def value_selected(self, index):
        value = self._model.get_row_value(index.row())
        self.valueSelected.emit(value)

    def value_dblclicked(self, index):
        value = self._model.get_row_value(index.row())
        self.valueDoubleCklicked.emit(value)


class TableWControls(Table):
    actionInvoked = pyqtSignal(str)
    def __init__(
            self, 
            data_model: dict, 
            table_fields: list = [], 
            values=[],
            buttons = []):
        super().__init__(data_model, table_fields, values)
        if buttons:
            self.add_buttons(buttons)
            

    def add_buttons(self, buttons):
        controls = QWidget()
        self.box.insertWidget(0, controls)
        hbox = QHBoxLayout()
        controls.setLayout(hbox)
        hbox.addStretch()
        for b in TABLE_BUTTONS:
            if b in buttons:
                btn = QPushButton(TABLE_BUTTONS[b])
                btn.clicked.connect(lambda _,action=b: self.actionInvoked.emit(action))
                hbox.addWidget(btn)

    