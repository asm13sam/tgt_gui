from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QVBoxLayout,
    QWidget,
    QApplication,
    QTabWidget,
    QSplitter,
    QLabel,
    )
from PyQt5.QtGui import QFont

import sys
import qdarktheme


class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.setStyleSheet('padding: 1px; margin: 0px;')
        self.setWindowTitle("Copycenter")
        self.setGeometry(250, 50, 1000, 700)

        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)
        self.main_split = QSplitter(Qt.Orientation.Horizontal)
        self.main_split.setStyleSheet('padding: 1px; margin: 0px;')
        self.main_layout.addWidget(self.main_split, stretch=10)

        self.tabs = QTabWidget()
        self.main_split.addWidget(self.tabs)
        self.tabs.setStyleSheet('padding: 1px; margin: 0px;')

        self.make_gui()

    def make_gui(self):
        self.main_layout.insertWidget(0, QLabel('Controls'), stretch=0)
        self.main_split.insertWidget(0, QLabel('Selector'))
        self.main_split.setStretchFactor(0, 1)
        self.main_split.setStretchFactor(1, 5)
        self.tabs.addTab(QLabel('Tab 0'), 'First tab')
        self.tabs.addTab(QLabel('Tab 1'), 'Second tab')


class MainWindow():
    def __init__(self):
        self.qt_app = QApplication(sys.argv)
        self.window = Window()
        color = "#99BCBC"
        qdarktheme.setup_theme(custom_colors={'primary': color})
        font = QFont()
        font.setPointSize(10)
        QApplication.instance().setFont(font)

    def run(self):
        self.window.show()
        sys.exit(self.qt_app.exec())


if __name__ == '__main__':
    w = MainWindow()
    w.run()
