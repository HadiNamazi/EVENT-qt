from PyQt5 import QtCore, QtGui, QtWidgets
from . import state_report
from . import common_functions as cf
import jdatetime
import xlsxwriter, sqlite3

s = None

class StateReportForm(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.ui = state_report.Ui_Form()
        self.ui.setupUi(self)

class Ui_Form(object):

    stateReportForm = None

    # to connect to sqlite and have a cursor
    con = sqlite3.connect("db.db", check_same_thread=False)
    cur = con.cursor()


    def search_btn_click(self):
        state_report.state = self.state_combo.currentText()
        if not self.stateReportForm:
            self.stateReportForm = StateReportForm()
        state_report.Ui_Form.fill_data(state_report.s)
        self.stateReportForm.show()

    def excel_name(self):
        date = jdatetime.datetime.now().strftime('%Y-%m-%d')

        if self.state_combo.currentText() == "بسته بندی نشده":
            name = 'Unpacked report '
        elif self.state_combo.currentText() == "بسته بندی شده":
            name = 'Packed report '
        elif self.state_combo.currentText() == "فروخته شده":
            name = 'Sold report '
        elif self.state_combo.currentText() == "معیوب":
            name == 'Defective report '

        name += date + '.xlsx'
        return name

    def excel_export(self):
        try:
            workbook = xlsxwriter.Workbook(cf.resource_path('خروجی های اکسل/' + self.excel_name()))
            worksheet = workbook.add_worksheet()
            worksheet.write(0, 0, 'اسم کالا')
            worksheet.write(0, 1, 'تعداد')

            res = self.cur.execute("SELECT name, unpacked_count, packed_count, sold_count, defective_count FROM t1").fetchall()
            # sorting by name
            res = sorted(res, key=lambda x: x[0])
            state = self.state_combo.currentText()
            dic = {}
            for i in res:
                if state == 'بسته بندی نشده' and i[1] != '0':
                    dic[i[0]] = i[1]
                elif state == 'بسته بندی شده' and i[2] != '0':
                    dic[i[0]] = i[2]
                elif state == 'فروخته شده' and i[3] != '0':
                    dic[i[0]] = i[3]
                elif i[4] != '0': #معیوب
                    dic[i[0]] = i[4]

            # for i, row in enumerate(dic):
            #     for j, value in enumerate(row):
            #         worksheet.write(i+1, j, value)

            for i in range(0, len(dic)):
                worksheet.write(i+1, 0, list(dic.keys())[i])
                worksheet.write(i+1, 1, dic[list(dic.keys())[i]])

            workbook.close()
        except:
            cf.warning_dialog('ابتدا فایل اکسل قبلی را ببندید')
            return
        cf.warning_dialog("فایل اکسل در پوشه 'خروجی های اکسل' در پوشه برنامه ایجاد شد.", 'Done')


    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.setFixedSize(313, 133)
        self.state_combo = QtWidgets.QComboBox(Form)
        self.state_combo.setEnabled(True)
        self.state_combo.setGeometry(QtCore.QRect(40, 30, 231, 31))
        self.state_combo.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.state_combo.setObjectName("state_combo")
        self.state_combo.addItem("")
        self.state_combo.addItem("")
        self.state_combo.addItem("")
        self.state_combo.addItem("")
        self.search_btn = QtWidgets.QPushButton(Form)
        self.search_btn.setGeometry(QtCore.QRect(40, 70, 111, 31))
        self.search_btn.clicked.connect(self.search_btn_click)
        self.excel_btn = QtWidgets.QPushButton(Form)
        self.excel_btn.setGeometry(QtCore.QRect(160, 70, 111, 31))
        self.excel_btn.clicked.connect(self.excel_export)
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
        self.excel_btn.setText(_translate("Form", "خروجی اکسل"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
