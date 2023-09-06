from PyQt5 import QtCore, QtGui, QtWidgets
from . import  edit_history as eh
from . import common_functions as cf
import sqlite3

s = None

class Ui_Form(object):

    # to connect to sqlite and have a cursor
    con = sqlite3.connect("db.db", check_same_thread=False)
    cur = con.cursor()

    def default(self):
        action = self.cur.execute("SELECT action FROM t2 WHERE ROWID=?", (eh.rowId_to_edit_history,)).fetchone()[0]
        
        if action == '01':
            dbState = 0
        elif action == '12':
            dbState = 1
        elif action == '23':
            dbState = 2
        elif action == '112':
            dbState = 3
        elif action == '113':
            dbState = 4
        elif action == '334':
            dbState = 5
        elif action == '110':
            dbState = 6
        elif action == '220':
            dbState = 7
        elif action == '111':
            dbState = 8
        elif action == '221':
            dbState = 9

        self.state_combo.setCurrentIndex(dbState)

    def edit_btn_clicked(self):
        comboState = self.state_combo.currentText()
        dbState = ''
        ex_name = eh.ex_name_to_edit_history
        rowId = eh.rowId_to_edit_history

        if comboState == 'ورود کالای بسته بندی نشده':
            dbState = '01'
        elif comboState == 'انجام بسته بندی':
            dbState = '12'
        elif comboState == 'فروش':
            dbState = '23'
        elif comboState == 'معیوب':
            dbState = '112'
        elif comboState == 'مرجوع خرید':
            dbState = '113'
        elif comboState == 'مرجوع فروش':
            dbState = '334'
        elif comboState == 'کسری بسته بندی نشده':
            dbState = '110'
        elif comboState == 'کسری بسته بندی شده':
            dbState = '220'
        elif comboState == 'مازاد بسته بندی نشده':
            dbState = '111'
        elif comboState == 'مازاد بسته بندی شده':
            dbState = '221'

        self.cur.execute("UPDATE t2 SET action=? WHERE ROWID=?", (dbState, rowId,))
        reslist = self.cur.execute("SELECT * FROM t2 ORDER BY date")
        if cf.check_conflict(reslist, ex_name):
            self.con.commit()
            cf.update_t1(ex_name)
            eh.s.fill_table()
        else:
            cf.warning_dialog('با تغییر این عملیات، در تاریخچه مشکل ایجاد خواهد شد.\nشما قادر به تغییر این عملیات نیستید.')
            self.con.rollback()
            eh.s.fill_table()
        self.default()

    def setupUi(self, Form):
        global s
        s = self
        Form.setObjectName("Form")
        Form.setFixedSize(315, 96)
        self.state_combo = QtWidgets.QComboBox(Form)
        self.state_combo.setEnabled(True)
        self.state_combo.setGeometry(QtCore.QRect(120, 30, 161, 31))
        self.state_combo.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.state_combo.setObjectName("state_combo")
        self.state_combo.addItem("")
        self.state_combo.addItem("")
        self.state_combo.addItem("")
        self.state_combo.addItem("")
        self.state_combo.addItem("")
        self.state_combo.addItem("")
        self.state_combo.addItem("")
        self.state_combo.addItem("")
        self.state_combo.addItem("")
        self.state_combo.addItem("")
        self.edit_btn = QtWidgets.QPushButton(Form)
        self.edit_btn.clicked.connect(self.edit_btn_clicked)
        self.edit_btn.setGeometry(QtCore.QRect(40, 30, 71, 31))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.edit_btn.setFont(font)
        self.edit_btn.setObjectName("edit_btn")

        QtWidgets.QWidget.setTabOrder(self.state_combo, self.edit_btn)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "ویرایش وضعیت کالا"))
        self.state_combo.setItemText(0, _translate("Form", "ورود کالای بسته بندی نشده"))
        self.state_combo.setItemText(1, _translate("Form", "انجام بسته بندی"))
        self.state_combo.setItemText(2, _translate("Form", "فروش"))
        self.state_combo.setItemText(3, _translate("Form", "معیوب"))
        self.state_combo.setItemText(4, _translate("Form", "مرجوع خرید"))
        self.state_combo.setItemText(5, _translate("Form", "مرجوع فروش"))
        self.state_combo.setItemText(6, _translate("Form", "کسری بسته بندی نشده"))
        self.state_combo.setItemText(7, _translate("Form", "کسری بسته بندی شده"))
        self.state_combo.setItemText(8, _translate("Form", "مازاد بسته بندی نشده"))
        self.state_combo.setItemText(9, _translate("Form", "مازاد بسته بندی شده"))
        self.edit_btn.setText(_translate("Form", "ثبت ویرایش"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
