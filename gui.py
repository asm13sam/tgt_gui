from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QVBoxLayout,
    QWidget,
    QApplication,
    QTabWidget,
    QSplitter,
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

        layout = QVBoxLayout()
        self.setLayout(layout)
        main_split = QSplitter(Qt.Orientation.Horizontal)
        main_split.setStyleSheet('padding: 1px; margin: 0px;')
        layout.addWidget(main_split)

        self.tabs = QTabWidget()
        main_split.addWidget(self.tabs)
        self.tabs.setStyleSheet('padding: 1px; margin: 0px;')


        


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
