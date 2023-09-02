from PyQt5 import QtCore, QtGui, QtWidgets
import sqlite3

from PyQt5.QtWidgets import QTableWidgetItem

state = ''
s = None

class Ui_Form(object):

    # to connect to sqlite and have a cursor
    con = sqlite3.connect("db.db")
    cur = con.cursor()

    def fill_data(self):
        res = self.cur.execute("SELECT name, unpacked_count, packed_count, sold_count, defective_count FROM t1").fetchall()
        dict = {}
        for i in res:
            if state == 'بسته بندی نشده' and i[1] != '0':
                dict[i[0]] = i[1]
            elif state == 'بسته بندی شده' and i[2] != '0':
                dict[i[0]] = i[2]
            elif state == 'فروخته شده' and i[3] != '0':
                dict[i[0]] = i[3]
            elif i[4] != '0': #معیوب
                dict[i[0]] = i[4]
        self.tableWidget.setRowCount(len(dict))
        for i in range(0, len(dict)):
            self.tableWidget.setItem(i, 0, QTableWidgetItem(list(dict.keys())[i]))
            self.tableWidget.setItem(i, 1, QTableWidgetItem(dict[list(dict.keys())[i]]))

    def setupUi(self, Form):
        global s
        s = self
        Form.setObjectName("Form")
        Form.setFixedSize(600, 506)
        self.tableWidget = QtWidgets.QTableWidget(Form)
        self.tableWidget.setGeometry(QtCore.QRect(0, 0, 601, 511))
        self.tableWidget.setAlternatingRowColors(False)
        self.tableWidget.setWordWrap(True)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setRowCount(0)
        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        self.tableWidget.horizontalHeader().setVisible(True)
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(95)
        self.tableWidget.horizontalHeader().setHighlightSections(True)
        self.tableWidget.horizontalHeader().setSortIndicatorShown(False)
        self.tableWidget.verticalHeader().setCascadingSectionResizes(False)
        self.tableWidget.verticalHeader().setHighlightSections(True)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "گزارش بر اساس وضعیت کالا"))
        self.tableWidget.setHorizontalHeaderLabels(['اسم کالا', 'تعداد'])


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
