from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import (
    QVBoxLayout,
    QWidget,
    QLabel,
    QPushButton,
    )

# values is list of value dict with at least one field 'name' and others that needs
class ButtonsBlock(QWidget):
    buttonClicked = pyqtSignal(dict)
    def __init__(self, title: str = '', values: list = []):
        super().__init__()
        self.buttons = []
        self.box = QVBoxLayout()
        self.setLayout(self.box)
        if title:
            self.box.addWidget(QLabel(title))
        self.selected = QLabel('Не обрано')
        self.box.addWidget(self.selected)
        if values:
            self.reload(values)

    def reload(self, values):
        for btn in self.buttons:
            self.box.removeWidget(btn)
        self.buttons = []
        for v in values:
            self.buttons.append(QPushButton(v['name']))
            self.buttons[-1].clicked.connect(lambda _, value=v: self.act(value))
            self.box.addWidget(self.buttons[-1])

    def act(self, value):
        self.selected.setText(value['name'])
        self.buttonClicked.emit(value)


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    
    bb_values = [
        {'name': 'Name A', 'id': 1},
        {'name': 'Name B', 'id': 2},
        {'name': 'Name C', 'id': 3},
        {'name': 'Name D', 'id': 4},
        {'name': 'Name E', 'id': 5}, 
    ]

    new_bb_values = [
        {'name': 'Qwerty', 'id': 11, 'is_active': True},
        {'name': 'Asdfg', 'id': 12, 'is_active': False},
        {'name': 'Zxcvb', 'id': 13, 'is_active': True},
    ]

    qt_app = QApplication(sys.argv)
    window = QWidget()
    layout = QVBoxLayout()
    window.setLayout(layout)
    
    bb = ButtonsBlock('TestBlock', bb_values)
    layout.addWidget(bb)
    bb.buttonClicked.connect(lambda value: print(value))
    reload_btn = QPushButton('Reload')
    layout.insertWidget(0, reload_btn)
    reload_btn.clicked.connect(lambda: bb.reload(new_bb_values))
    layout.addStretch()
    
    window.show()
    sys.exit(qt_app.exec())

