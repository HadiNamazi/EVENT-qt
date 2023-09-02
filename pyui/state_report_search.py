from PyQt5 import QtCore, QtGui, QtWidgets
from . import state_report

s = None

class StateReportForm(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.ui = state_report.Ui_Form()
        self.ui.setupUi(self)

class Ui_Form(object):

    stateReportForm = None

    def search_btn_click(self):
        state_report.state = self.state_combo.currentText()
        if not self.stateReportForm:
            self.stateReportForm = StateReportForm()
        state_report.Ui_Form.fill_data(state_report.s)
        self.stateReportForm.show()

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.setFixedSize(360, 103)
        self.state_combo = QtWidgets.QComboBox(Form)
        self.state_combo.setEnabled(True)
        self.state_combo.setGeometry(QtCore.QRect(150, 30, 171, 31))
        self.state_combo.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.state_combo.setObjectName("state_combo")
        self.state_combo.addItem("")
        self.state_combo.addItem("")
        self.state_combo.addItem("")
        self.state_combo.addItem("")
        self.search_btn = QtWidgets.QPushButton(Form)
        self.search_btn.setGeometry(QtCore.QRect(40, 30, 101, 31))
        self.search_btn.clicked.connect(self.search_btn_click)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.search_btn.setFont(font)
        self.search_btn.setObjectName("search_btn")

        QtWidgets.QWidget.setTabOrder(self.state_combo, self.search_btn)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "جستجو"))
        self.state_combo.setItemText(0, _translate("Form", "بسته بندی نشده"))
        self.state_combo.setItemText(1, _translate("Form", "بسته بندی شده"))
        self.state_combo.setItemText(2, _translate("Form", "فروخته شده"))
        self.state_combo.setItemText(3, _translate("Form", "معیوب"))
        self.search_btn.setText(_translate("Form", "مشاهده گزارش"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
