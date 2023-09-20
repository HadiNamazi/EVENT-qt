import threading
from time import sleep
from PyQt5 import QtCore, QtGui, QtWidgets
import sqlite3
from . import edit_history_state
from . import common_functions as cf
from PyQt5.QtWidgets import QTableWidgetItem, QTableWidget, QMessageBox

s = None
rowId_to_edit_history = None
ex_name_to_edit_history = None

class EditHistoryStateForm(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.ui = edit_history_state.Ui_Form()
        self.ui.setupUi(self)

class Ui_Form(object):

    # to connect to sqlite and have a cursor
    con = sqlite3.connect("db.db")
    cur = con.cursor()
    ex_names_list = []

    editHistoryStateForm = None

    def edit_history_click(self):
        if not self.editHistoryStateForm:
            self.editHistoryStateForm = EditHistoryStateForm()
        edit_history_state.Ui_Form.default(edit_history_state.s)
        self.editHistoryStateForm.show()

    def ex_names_list_generator(self):
        self.ex_names_list = self.cur.execute('SELECT name FROM t2 ORDER BY date').fetchall()

    def fill_table(self):
        try:
            self.tableWidget.itemChanged.disconnect()
            self.tableWidget.itemSelectionChanged.disconnect()
        except:
            pass

        # to clear tableWidget
        self.tableWidget.setRowCount(0)

        self.cur.execute('SELECT * FROM t2 ORDER BY date')
        res = self.cur.fetchall()
        self.tableWidget.setRowCount(len(res))
        for i in range(0, len(res)):
            if res[i][3] == '01':
                self.tableWidget.setItem(i, 0, QTableWidgetItem('ورود کالای بسته بندی نشده'))
            elif res[i][3] == '12':
                self.tableWidget.setItem(i, 0, QTableWidgetItem('انجام بسته بندی'))
            elif res[i][3] == '23':
                self.tableWidget.setItem(i, 0, QTableWidgetItem('فروش'))
            elif len(res[i][3]) == 3 and res[i][3] == '110':
                self.tableWidget.setItem(i, 0, QTableWidgetItem('کسری بسته بندی نشده'))
            elif len(res[i][3]) == 3 and res[i][3] == '220':
                self.tableWidget.setItem(i, 0, QTableWidgetItem('کسری بسته بندی شده'))
            elif len(res[i][3]) == 3 and res[i][3] == '111':
                self.tableWidget.setItem(i, 0, QTableWidgetItem('مازاد بسته بندی نشده'))
            elif len(res[i][3]) == 3 and res[i][3] == '221':
                self.tableWidget.setItem(i, 0, QTableWidgetItem('مازاد بسته بندی شده'))
            elif len(res[i][3]) == 3 and res[i][3][2] == '2':
                self.tableWidget.setItem(i, 0, QTableWidgetItem('معیوب'))
            elif len(res[i][3]) == 3 and res[i][3][2] == '3':
                self.tableWidget.setItem(i, 0, QTableWidgetItem('مرجوع خرید'))
            elif len(res[i][3]) == 3 and res[i][3][2] == '4':
                self.tableWidget.setItem(i, 0, QTableWidgetItem('مرجوع فروش'))
            self.tableWidget.setItem(i, 1, QTableWidgetItem(res[i][0]))
            self.tableWidget.setItem(i, 2, QTableWidgetItem(res[i][1]))
            self.tableWidget.setItem(i, 3, QTableWidgetItem(res[i][2]))
            self.tableWidget.setItem(i, 4, QTableWidgetItem(res[i][5]))
            self.tableWidget.setItem(i, 5, QTableWidgetItem(cf.separateor(res[i][4])))
        self.tableWidget.itemChanged.connect(self.item_edited)
        self.tableWidget.itemSelectionChanged.connect(self.selection_changed)

    def delete_dialog_clicked(self, dbutton):
        if dbutton.text() == 'OK':
            row = self.tableWidget.currentRow()
            ex_name = self.ex_names_list[row][0]
            res = self.cur.execute("SELECT ROWID, name, count, date, action FROM t2 ORDER BY date").fetchall()
            rowIds = self.cur.execute("SELECT ROWID FROM t2 ORDER BY date").fetchall()
            rowId = rowIds[row][0]

            self.cur.execute("DELETE FROM t2 WHERE ROWID=?", (rowId,))
            reslist = self.cur.execute("SELECT * FROM t2 ORDER BY date")
            if cf.check_conflict(reslist, ex_name):
                self.con.commit()
                cf.update_t1(ex_name)
                self.fill_table()
            else:
                self.con.rollback()
                cf.warning_dialog('با حذف این سطر از تاریخچه، در تاریخچه مشکل ایجاد خواهد شد.\nشما قادر به حذف کردن این سطر نیستید.')

    def delete_clicked(self):
        row_count = int(len(self.tableWidget.selectedIndexes())/6)
        if row_count == 1:
            dialog = QMessageBox()
            dialog.setText('از حذف کردن سطر انتخاب شده مطمئن هستید؟')
            dialog.setWindowTitle('Delete warning')
            dialog.setIcon(QMessageBox.Warning)
            dialog.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            dialog.buttonClicked.connect(self.delete_dialog_clicked)
            dialog.exec_()
        elif row_count > 1:
            cf.warning_dialog('در هر نوبت فقط میتوانید یک سطر را حذف کنید.')
        else:
            cf.warning_dialog('ابتدا سطری که میخواهید حذف کنید را انتخاب کنید.')

    def selection_changed(self):
        row = self.tableWidget.currentRow()
        column = self.tableWidget.currentColumn()

        if column == 0: # state
            rowIds = self.cur.execute("SELECT ROWID FROM t2 ORDER BY date").fetchall()
            rowId = rowIds[row][0]
            ex_name = self.ex_names_list[row][0]
            global rowId_to_edit_history, ex_name_to_edit_history
            rowId_to_edit_history = rowId
            ex_name_to_edit_history = ex_name
            self.edit_history_click()

    
    def item_edited(self, item):
        self.ex_names_list_generator()
        row = item.row()
        column = item.column()
        ex_name = self.ex_names_list[row][0]
        rowIds = self.cur.execute("SELECT ROWID FROM t2 ORDER BY date").fetchall()
        rowId = rowIds[row][0]

        if column == 1:
            self.cur.execute("UPDATE t2 SET name=? WHERE ROWID=?", (item.text(), rowId,))
            reslist = self.cur.execute("SELECT * FROM t2 ORDER BY date").fetchall()
            if cf.check_conflict(reslist, item.text()) and cf.check_conflict(reslist, ex_name):
                self.con.commit()
                cf.update_t1(item.text())
                cf.update_t1(ex_name)
                self.fill_table()
            else:
                cf.warning_dialog('با تغییر نام کالا، در تاریخچه مشکل ایجاد خواهد شد.\nشما قادر به تغییر نام کالا نیستید.')
                self.con.rollback()
                self.fill_table()
        elif column == 2:
            self.cur.execute("UPDATE t2 SET count=? WHERE ROWID=?", (item.text(), rowId,))
            reslist = self.cur.execute("SELECT * FROM t2 ORDER BY date")
            if item.text().isnumeric() and cf.check_conflict(reslist, ex_name):
                self.con.commit()
                cf.update_t1(ex_name)
                self.fill_table()
            else:
                cf.warning_dialog('با تغییر تعداد کالا، در تاریخچه مشکل ایجاد خواهد شد.\nشما قادر به تغییر تعداد کالا نیستید.')
                self.con.rollback()
                self.fill_table()
        elif column == 3:
            revised_date = cf.date_format_reviser(item.text())
            self.cur.execute("UPDATE t2 SET date=? WHERE ROWID=?", (revised_date, rowId,))
            reslist = self.cur.execute("SELECT * FROM t2 ORDER BY date")
            if cf.date_validator(revised_date) and cf.check_conflict(reslist, ex_name):
                self.con.commit()
                self.fill_table()
            else:
                cf.warning_dialog('با تغییر این تاریخ، در تاریخچه مشکل ایجاد خواهد شد.\nشما قادر به تغییر این تاریخ نیستید.')
                self.con.rollback()
                self.fill_table()
        elif column == 4:
            if item.text().isnumeric():
                self.cur.execute("UPDATE t2 SET factor=? WHERE ROWID=?", (item.text(), rowId,))
                self.con.commit()
                self.fill_table()
            else:
                cf.warning_dialog('شماره فاکتور باید متشکل از اعداد باشد.\nدوباره تلاش کنید.')
                self.fill_table()
        else:
            if item.text().isnumeric():
                price = cf.separateor(item.text(), -1)
                self.cur.execute("UPDATE t2 SET price=? WHERE ROWID=?", (price, rowId,))
                self.con.commit()
                self.fill_table()
            else:
                cf.warning_dialog('قیمت باید متشکل از اعداد باشد.\nدوباره تلاش کنید.')
                self.fill_table()


    def setupUi(self, Form):
        global s
        s = self
        Form.setObjectName("Form")
        Form.setFixedSize(600, 506)
        self.tableWidget = QtWidgets.QTableWidget(Form)
        self.tableWidget.setGeometry(QtCore.QRect(0, 0, 601, 471))
        self.tableWidget.setAlternatingRowColors(False)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(6)
        self.tableWidget.setRowCount(0)
        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(5, QtWidgets.QHeaderView.ResizeToContents)
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(95)
        self.tableWidget.verticalHeader().setCascadingSectionResizes(False)
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(0, 470, 602, 37))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.delete_clicked)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "ویرایش تاریخچه"))
        self.tableWidget.setHorizontalHeaderLabels(['عملیات', 'اسم کالا', 'تعداد', 'تاریخ', 'شماره فاکتور', 'قیمت'])
        self.pushButton.setText(_translate("Form", "حذف"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
