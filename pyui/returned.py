from PyQt5 import QtCore, QtGui, QtWidgets
import sqlite3
import jdatetime
from . import common_functions as cf
from . import main_window as mw

s = None

class Ui_Form(object):

    # to connect to sqlite and have a cursor
    con = sqlite3.connect("db.db")
    cur = con.cursor()

    item_text = ''

    def default(self):
        # self.search_list.clear()
        self.name_inpt.clear()
        self.date_inpt.setText(jdatetime.datetime.now().strftime('%Y/%m/%d'))
        self.count_inpt.setValue(1)
        self.price_inpt.clear()
        self.factor_inpt.clear()

    def search_recommendation(self):
        self.search_list.clear()

        if self.name_inpt.text() == '':
            self.cur.execute("SELECT name, serial FROM t1")
            res = self.cur.fetchall()
            rec = []
            for i in res:
                data = i[1] + ' - ' + i[0]
                rec.append(data)
            self.search_list.addItems(rec)
            self.item_text = ''
        else:
            name = self.name_inpt.text()
            splitted_name = name.split()
            rec = []

            self.cur.execute("SELECT name, serial FROM t1")
            res = self.cur.fetchall()

            count = 0
            for i in res:
                data = i[1] + ' - ' + i[0]
                # if one of the items was clicked
                if self.name_inpt.text() == data:
                    rec = [data]
                    break
                for j in splitted_name:
                    if len(splitted_name) == 1 and j in i[1] and not data in rec:
                        rec.append(data)
                        break
                    if j != '-' and j in i[0] and not data in rec:
                        count += 1
                if count == len(splitted_name):
                    rec.append(data)
                count = 0

            self.search_list.addItems(rec)


    def item_clicked(self, item):
        self.item_text = item.text()
        self.name_inpt.setText(item.text())

    def btn_clicked(self):
        self.date_inpt.setText(cf.date_format_reviser(self.date_inpt.text()))
        if self.item_text != '' and self.count_inpt.text() != '' and cf.date_validator(self.date_inpt.text()):
            text_array = self.item_text.split()[2:]
            text = ''
            for t in text_array:
                text += t + ' '
            text = text[0:len(text) - 1]

            if self.combo.currentText() == 'مرجوع فروش':
                price = cf.separateor(self.price_inpt.text(), -1)
                if price != '' and self.factor_inpt.text() != '' and price.isnumeric() and self.factor_inpt.text().isnumeric():
                    data = (text, self.count_inpt.text(), self.date_inpt.text(), '334', price, self.factor_inpt.text())
                    self.cur.execute("INSERT INTO t2 VALUES(?, ?, ?, ?, ?, ?)", data)
                    history = self.cur.execute("SELECT * FROM t2 ORDER BY date").fetchall()

                    if cf.check_conflict(history, text):
                        self.con.commit()
                        cf.update_t1(text)
                        mw.Ui_MainWindow.status_lbl(mw.s)
                        self.search_recommendation()
                    else:
                        self.con.rollback()
                        cf.warning_dialog('تعداد کالاهای فروخته شده این محصول کافی نیست.')
                else:
                    cf.warning_dialog('اطلاعات وارد شده معتبر نیست.')
            elif self.combo.currentText() == 'مرجوع خرید':
                data = (text, self.count_inpt.text(), self.date_inpt.text(), '113', None, None)
                self.cur.execute("INSERT INTO t2 VALUES(?, ?, ?, ?, ?, ?)", data)
                history = self.cur.execute("SELECT * FROM t2 ORDER BY date").fetchall()

                if cf.check_conflict(history, text):
                    self.con.commit()
                    cf.update_t1(text)
                    self.search_recommendation()
                else:
                    self.con.rollback()
                    cf.warning_dialog('تعداد کالاهای معیوب این محصول کافی نیست.')

            self.item_text = ''
        else:
            cf.warning_dialog('اطلاعات وارد شده معتبر نیست.')
        self.default()

    def combo_changed(self, value):
        if value == 'مرجوع خرید':
            self.factor_inpt.clear()
            self.price_inpt.clear()
            self.factor_inpt.setEnabled(False)
            self.price_inpt.setEnabled(False)
        elif value == 'مرجوع فروش':
            self.factor_inpt.setEnabled(True)
            self.price_inpt.setEnabled(True)

    def separator(self):
        self.price_inpt.setText(cf.separateor(self.price_inpt.text()))

    def setupUi(self, Form):
        global s
        s = self
        Form.setObjectName("Form")
        Form.setFixedSize(600, 506)
        self.count_inpt = QtWidgets.QSpinBox(Form)
        self.count_inpt.setGeometry(QtCore.QRect(460, 70, 101, 31))
        self.count_inpt.setMinimum(1)
        self.count_inpt.setMaximum(1000000)
        self.count_inpt.setProperty("value", 1)
        self.count_inpt.setObjectName("count_inpt")
        self.add_btn = QtWidgets.QPushButton(Form)
        self.add_btn.clicked.connect(self.btn_clicked)
        self.add_btn.setGeometry(QtCore.QRect(40, 450, 521, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.add_btn.setFont(font)
        self.add_btn.setObjectName("add_btn")
        self.name_inpt = QtWidgets.QLineEdit(Form)
        self.name_inpt.textChanged.connect(self.search_recommendation)
        self.name_inpt.setGeometry(QtCore.QRect(40, 30, 411, 31))
        self.name_inpt.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.name_inpt.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.name_inpt.setClearButtonEnabled(True)
        self.name_inpt.setObjectName("name_inpt")
        self.date_inpt = QtWidgets.QLineEdit(Form)
        self.date_inpt.setGeometry(QtCore.QRect(350, 70, 101, 31))
        self.date_inpt.setObjectName("date_inpt")
        self.combo = QtWidgets.QComboBox(Form)
        self.combo.setGeometry(QtCore.QRect(460, 30, 101, 31))
        self.combo.setObjectName("combo")
        self.combo.addItem("")
        self.combo.addItem("")
        self.combo.currentTextChanged.connect(self.combo_changed)
        self.search_list = QtWidgets.QListWidget(Form)
        self.search_list.itemClicked.connect(self.item_clicked)
        self.search_list.setGeometry(QtCore.QRect(40, 110, 521, 321))
        self.search_list.setViewMode(QtWidgets.QListView.ListMode)
        self.search_list.setObjectName("search_list")
        self.price_inpt = QtWidgets.QLineEdit(Form)
        self.price_inpt.textChanged.connect(self.separator)
        self.price_inpt.setGeometry(QtCore.QRect(40, 70, 191, 31))
        self.price_inpt.setObjectName("price_inpt")
        self.factor_inpt = QtWidgets.QLineEdit(Form)
        self.factor_inpt.setGeometry(QtCore.QRect(240, 70, 101, 31))
        self.factor_inpt.setObjectName("factor_inpt")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "ثبت مرجوعی"))
        self.add_btn.setText(_translate("Form", "ثبت"))
        self.name_inpt.setPlaceholderText(_translate("Form", "اسم یا کد کالا"))
        self.date_inpt.setPlaceholderText(_translate("Form", "تاریخ"))
        self.combo.setItemText(0, _translate("Form", "مرجوع خرید"))
        self.combo.setItemText(1, _translate("Form", "مرجوع فروش"))
        self.price_inpt.setPlaceholderText(_translate("Form", "قیمت"))
        self.factor_inpt.setPlaceholderText(_translate("Form", "شماره فاکتور"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
