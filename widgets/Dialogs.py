from PyQt5.QtWidgets import (
    QVBoxLayout,
    QWidget,
    QLabel,
    QDialogButtonBox as DBB,
    QMessageBox as MB,
    QDialog,
    QLineEdit,
    )

def error(text):
    MB(MB.Icon.Critical, "Помилка", text).exec()


def messbox(text, title="Повідомлення"):
    MB(MB.Icon.Information, title, text).exec()


def askdlg(question: str):
    dlg = AskDialog(question)
    res = dlg.exec()
    if not res:
        return ''
    return dlg.entry.text()


def ok_cansel_dlg(question: str, title: str='Запитання'):
    dlg = CustomDialog(QLabel(question), title)
    return dlg.exec()


# widget - widget to show on dialog
class CustomDialog(QDialog):
    def __init__(self, widget: QWidget, title: str):
        super().__init__()

        self.setWindowTitle(title)
        self.widget = widget

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        QBtn = DBB.StandardButton.Ok | DBB.StandardButton.Cancel
        self.buttonBox = DBB(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout.addWidget(self.widget)
        self.layout.addWidget(self.buttonBox)


# Dialog with QLineEdit widget
class AskDialog(CustomDialog):
    def __init__(self, question: str):
        question_label = QLabel(question)
        self.entry = QLineEdit()
        w = QWidget()
        wl = QVBoxLayout()
        wl.addWidget(question_label)
        wl.addWidget(self.entry)
        w.setLayout(wl)
        super().__init__(w, 'Запитання')