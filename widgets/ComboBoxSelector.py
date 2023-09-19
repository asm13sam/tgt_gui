from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import (
    QVBoxLayout,
    QComboBox,
    QWidget,
    QLabel,
    )

# values is list of value dict with at least two fields 'name' and 'id' and others that needs
# id starts from 1 (as in SQL tables)
class ComboBoxSelector(QWidget):
    selectionChanged = pyqtSignal(dict)
    def __init__(self, title: str='', values: list=[]):
        super().__init__()
        layout = QVBoxLayout()
        self.setLayout(layout)
        if title:
            layout.addWidget(QLabel(title))
        self.cb = QComboBox()
        layout.addWidget(self.cb)
        self.cb.currentIndexChanged.connect(self.selection_changed)
        if values:
            self.reload(values)
        
    def reload(self, values: list):    
        self.values = [{'name': 'Не обрано', 'id': 0}] + values
        self.cb.clear()
        for v in self.values:
            self.cb.addItem(v['name'], v['id'])
        
    def selection_changed(self, index: int):
        self.selectionChanged.emit(self.values[index])


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication, QPushButton
    
    cb_values = [
        {'name': 'Name A', 'id': 1},
        {'name': 'Name B', 'id': 2},
        {'name': 'Name C', 'id': 3},
        {'name': 'Name D', 'id': 4},
        {'name': 'Name E', 'id': 5}, 
    ]

    new_cb_values = [
        {'name': 'Qwerty', 'id': 11, 'is_active': True},
        {'name': 'Asdfg', 'id': 12, 'is_active': False},
        {'name': 'Zxcvb', 'id': 13, 'is_active': True},
    ]

    qt_app = QApplication(sys.argv)
    window = QWidget()
    layout = QVBoxLayout()
    window.setLayout(layout)
    
    cb = ComboBoxSelector('TestBlock', cb_values)
    layout.addWidget(cb)
    cb.selectionChanged.connect(lambda value: print(value))
    reload_btn = QPushButton('Reload')
    layout.insertWidget(0, reload_btn)
    reload_btn.clicked.connect(lambda: cb.reload(new_cb_values))
    layout.addStretch()
    
    window.show()
    sys.exit(qt_app.exec())
