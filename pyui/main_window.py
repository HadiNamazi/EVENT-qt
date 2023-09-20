# -*- coding: utf-8 -*-
import os.path
from time import sleep
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox, QMainWindow
from . import add_unpacked, add_packed, alarm, add_product_name, add_sold_items, delete_product_name, edit_name_serial_search, inventory_modification, simple_report_search, add_password, change_password, search_advance_report, state_report_search, edit_history, returned
from . import common_functions as cf
import sqlite3
import threading
import jdatetime
import xlsxwriter

s = None

report_name = ''

class UnpackedForm(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.ui = add_unpacked.Ui_Form()
        self.ui.setupUi(self)
class PackedForm(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.ui = add_packed.Ui_Form()
        self.ui.setupUi(self)
class AlarmForm(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.ui = alarm.Ui_Form()
        self.ui.setupUi(self)
class ProductNameForm(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.ui = add_product_name.Ui_Form()
        self.ui.setupUi(self)
class SoldForm(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.ui = add_sold_items.Ui_Form()
        self.ui.setupUi(self)
class SearchAdvanceReportForm(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.ui = search_advance_report.Ui_Form()
        self.ui.setupUi(self)
class DeleteProductNameForm(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.ui = delete_product_name.Ui_Form()
        self.ui.setupUi(self)
class EditNameSerialSearchForm(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.ui = edit_name_serial_search.Ui_Form()
        self.ui.setupUi(self)
class InventoryModificationForm(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.ui = inventory_modification.Ui_Form()
        self.ui.setupUi(self)
class SimpleReportSearchForm(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.ui = simple_report_search.Ui_Form()
        self.ui.setupUi(self)
class StateReportSearchForm(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.ui = state_report_search.Ui_Form()
        self.ui.setupUi(self)
class AddPasswordForm(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.ui = add_password.Ui_Form()
        self.ui.setupUi(self)
class ChangePasswordForm(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.ui = change_password.Ui_Form()
        self.ui.setupUi(self)
class EditHistoryForm(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.ui = edit_history.Ui_Form()
        self.ui.setupUi(self)
class ReturnedForm(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.ui = returned.Ui_Form()
        self.ui.setupUi(self)


class Ui_MainWindow(QMainWindow):

    # to connect to sqlite and have a cursor
    con = sqlite3.connect("db.db", check_same_thread=False)
    cur = con.cursor()

    unpackedForm = None
    packedForm = None
    soldForm = None
    searchAdvanceReportForm = None
    productNameForm = None
    alarmForm = None
    deleteProductNameForm = None
    deleteWarningForm = None
    editNameSerialSearchForm = None
    editWarningForm = None
    inventoryModificationForm = None
    simpleReportSearchForm = None
    addPasswordForm = None
    changePasswordForm = None
    stateReportSearchForm = None
    editHistoryForm = None
    returnedForm = None

    def unpacked_click(self):
        if not self.unpackedForm:
            self.unpackedForm = UnpackedForm()
        add_unpacked.Ui_Form.default(add_unpacked.s)
        add_unpacked.Ui_Form.search_recommendation(add_unpacked.s)
        self.unpackedForm.show()

    def packed_click(self):
        if not self.packedForm:
            self.packedForm = PackedForm()
        add_packed.Ui_Form.default(add_packed.s)
        add_packed.Ui_Form.search_recommendation(add_packed.s)
        self.packedForm.show()

    def sold_click(self):
        if not self.soldForm:
            self.soldForm = SoldForm()
        add_sold_items.Ui_Form.default(add_sold_items.s)
        add_sold_items.Ui_Form.search_recommendation(add_sold_items.s)
        self.soldForm.show()

    def search_advance_report_click(self):
        if not self.searchAdvanceReportForm:
            self.searchAdvanceReportForm = SearchAdvanceReportForm()
        search_advance_report.Ui_Form.default(search_advance_report.s)
        search_advance_report.Ui_Form.search_recommendation(search_advance_report.s)
        self.searchAdvanceReportForm.show()

    def product_name_click(self):
        if not self.productNameForm:
            self.productNameForm = ProductNameForm()
        add_product_name.Ui_Form.default(add_product_name.s)
        self.productNameForm.show()

    def alarm_click(self):
        if not self.alarmForm:
            self.alarmForm = AlarmForm()
        alarm.Ui_Form.default(alarm.s)
        alarm.Ui_Form.search_recommendation(alarm.s)
        self.alarmForm.show()

    def delete_product_name_click(self):
        if not self.deleteProductNameForm:
            self.deleteProductNameForm = DeleteProductNameForm()
        delete_product_name.Ui_Form.default(delete_product_name.s)
        delete_product_name.Ui_Form.search_recommendation(delete_product_name.s)
        self.deleteProductNameForm.show()

    def edit_name_serial_search_click(self):
        if not self.editNameSerialSearchForm:
            self.editNameSerialSearchForm = EditNameSerialSearchForm()
        edit_name_serial_search.Ui_Form.default(edit_name_serial_search.s)
        edit_name_serial_search.Ui_Form.search_recommendation(edit_name_serial_search.s)
        self.editNameSerialSearchForm.show()

    def inventory_modification_click(self):
        if not self.inventoryModificationForm:
            self.inventoryModificationForm = InventoryModificationForm()
        inventory_modification.Ui_Form.default(inventory_modification.s)
        inventory_modification.Ui_Form.search_recommendation(inventory_modification.s)
        self.inventoryModificationForm.show()

    def simple_report_search_click(self):
        if not self.simpleReportSearchForm:
            self.simpleReportSearchForm = SimpleReportSearchForm()
        global report_name
        simple_report_search.Ui_Form.default(simple_report_search.ss)
        simple_report_search.Ui_Form.search_recommendation(simple_report_search.ss)
        self.simpleReportSearchForm.show()

    def state_report_search_click(self):
        if not self.stateReportSearchForm:
            self.stateReportSearchForm = StateReportSearchForm()
        self.stateReportSearchForm.show()

    def add_password_click(self):
        if not self.addPasswordForm:
            self.addPasswordForm = AddPasswordForm()
        add_password.Ui_Form.default(add_password.ss)
        add_password.s = self.addPasswordForm
        self.addPasswordForm.show()

    def change_password_click(self):
        if not self.changePasswordForm:
            self.changePasswordForm = ChangePasswordForm()
        change_password.Ui_Form.default(change_password.ss)
        change_password.s = self.changePasswordForm
        self.changePasswordForm.show()

    def password_click(self):
        self.cur.execute('SELECT password FROM t3')
        if self.cur.fetchone():
            self.change_password_click()
        else:
            self.add_password_click()

    def edit_history_click(self):
        if not self.editHistoryForm:
            self.editHistoryForm = EditHistoryForm()
        edit_history.Ui_Form.ex_names_list_generator(edit_history.s)
        edit_history.Ui_Form.fill_table(edit_history.s)
        self.editHistoryForm.show()

    def returned_click(self):
        if not self.returnedForm:
            self.returnedForm = ReturnedForm()
        returned.Ui_Form.default(returned.s)
        returned.Ui_Form.search_recommendation(returned.s)
        self.returnedForm.show()

    def live_datetime(self):
        while True:
            datetime = jdatetime.datetime.now().strftime('%Y/%m/%d - %H:%M:%S')
            self.datetime_lbl.setText(datetime)
            sleep(1)

    def status_lbl(self):
        self.cur.execute('SELECT unpacked_count, packed_count FROM t1')
        res = self.cur.fetchall()
        if not res:
            self.unpacked_lbl.setText('0')
            self.packed_lbl.setText('0')
            return
        unpacked_count = 0
        packed_count = 0
        for i in res:
            unpacked_count += int(i[0])
            packed_count += int(i[1])
        self.unpacked_lbl.setText(str(unpacked_count))
        self.packed_lbl.setText(str(packed_count))

    def alarm(self):
        self.cur.execute('SELECT name, unpacked_count, min FROM t1')
        res = self.cur.fetchall()
        txt = ''
        count = 0
        for i in res:
            if i[2] != '' and i[2] is not None:
                if int(i[1]) < int(i[2]):
                    txt += '{} و '.format(i[0])
                    count += 1
        if len(txt) != 0:
            txt = txt[:len(txt)-3]
            txt += ' به کمتر از حداقل موجودی رسیده'
            if count > 1:
                txt += ' اند.'
            else:
                txt += ' است.'
            dialog = QMessageBox()
            dialog.setText(txt)
            dialog.setWindowTitle('هشدار حداقل موجودی')
            dialog.setIcon(QMessageBox.Information)
            dialog.setStandardButtons(QMessageBox.Ok)
            dialog.exec_()

    # @QtCore.pyqtSlot()
    def closeEvent(self, event):
        print('closeevent')
        event.accept()
        # for window in QApplication.topLevelWidgets():
        #     window.close()
        # app = QtGui.QApplication.instance()
        # app.closeAllWindows()

    def export_click(self):
        try:
            date = jdatetime.datetime.now().strftime('%Y-%m-%d')
            name = 'All history ' + date + '.xlsx'
            workbook = xlsxwriter.Workbook(cf.resource_path('خروجی های اکسل/' + name))
            worksheet = workbook.add_worksheet()
            mysel = self.cur.execute("SELECT * FROM t2 ORDER BY date").fetchall()

            worksheet.write(0, 0, 'اسم کالا')
            worksheet.write(0, 1, 'تعداد')
            worksheet.write(0, 2, 'تاریخ')
            worksheet.write(0, 3, 'عملیات')
            worksheet.write(0, 4, 'قیمت')
            worksheet.write(0, 5, 'شماره فاکتور')

            for i, row in enumerate(mysel):
                for j, value in enumerate(row):
                    if j == 3:
                        worksheet.write(i+1, j, cf.action_code_to_text(value))
                    else:
                        worksheet.write(i+1, j, value)
            workbook.close()
        except:
            cf.warning_dialog('ابتدا فایل اکسل قبلی را ببندید')
            return
        cf.warning_dialog("فایل اکسل در پوشه 'خروجی های اکسل' در پوشه برنامه ایجاد شد.", 'Done')

    def setupUi(self, MainWindow):
        global s
        s = self
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(600, 506)
        icon = QtGui.QIcon()
        CURRENT_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
        filename = os.path.join(CURRENT_DIRECTORY, cf.resource_path('logo/removed_babr.png'))
        icon.addPixmap(QtGui.QPixmap(filename), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setStyleSheet("")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(340, 290, 151, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(230, 30, 131, 141))
        self.label_4.setText("")
        filename = os.path.join(CURRENT_DIRECTORY, cf.resource_path('logo/babr.png'))
        self.label_4.setPixmap(QtGui.QPixmap(filename))
        self.label_4.setScaledContents(True)
        self.label_4.setObjectName("label_4")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(90, 290, 151, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(520, 440, 61, 16))
        self.label_6.setStyleSheet("color:#444444")
        self.label_6.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label_6.setObjectName("label_6")
        self.packed_lbl = QtWidgets.QLabel(self.centralwidget)
        self.packed_lbl.setGeometry(QtCore.QRect(130, 330, 81, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.packed_lbl.setFont(font)
        self.packed_lbl.setStyleSheet("color:#00aa00")
        self.packed_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.packed_lbl.setObjectName("packed_lbl")
        self.unpacked_lbl = QtWidgets.QLabel(self.centralwidget)
        self.unpacked_lbl.setGeometry(QtCore.QRect(380, 330, 81, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.unpacked_lbl.setFont(font)
        self.unpacked_lbl.setStyleSheet("color:#c80000")
        self.unpacked_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.unpacked_lbl.setObjectName("unpacked_lbl")
        self.datetime_lbl = QtWidgets.QLabel(self.centralwidget)
        self.datetime_lbl.setGeometry(QtCore.QRect(20, 10, 211, 21))
        self.datetime_lbl.setText("")
        self.datetime_lbl.setAlignment(Qt.AlignLeft)
        self.datetime_lbl.setObjectName("datetime_lbl")
        thread = threading.Thread(target=self.live_datetime)
        thread.start()
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(10, 440, 191, 16))
        self.label_3.setStyleSheet("color:#444444")
        self.label_3.setTextFormat(QtCore.Qt.RichText)
        self.label_3.setOpenExternalLinks(True)
        self.label_3.setObjectName("label_3")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(230, 150, 131, 61))
        self.label_5.setText("")
        filename = os.path.join(CURRENT_DIRECTORY, "../logo/event text.png")
        self.label_5.setPixmap(QtGui.QPixmap(filename))
        self.label_5.setScaledContents(True)
        self.label_5.setObjectName("label_5")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setLayoutDirection(Qt.RightToLeft)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 600, 21))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        self.menu_2 = QtWidgets.QMenu(self.menubar)
        self.menu_2.setObjectName("menu_2")
        self.menu_3 = QtWidgets.QMenu(self.menubar)
        self.menu_3.setObjectName("menu_3")
        self.setting = QtWidgets.QMenu(self.menubar)
        self.setting.setObjectName("setting")
        self.menu_history = QtWidgets.QMenu(self.menubar)
        self.menu_history.setObjectName("menu_history")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.unpacked_act = QtWidgets.QAction(MainWindow)
        self.unpacked_act.triggered.connect(self.unpacked_click)
        self.unpacked_act.setObjectName("unpacked_act")
        self.edit_history_act = QtWidgets.QAction(MainWindow)
        self.edit_history_act.triggered.connect(self.edit_history_click)
        self.edit_history_act.setObjectName("edit_history_act")
        self.packed_act = QtWidgets.QAction(MainWindow)
        self.packed_act.triggered.connect(self.packed_click)
        self.packed_act.setObjectName("packed_act")
        self.sold_act = QtWidgets.QAction(MainWindow)
        self.sold_act.triggered.connect(self.sold_click)
        self.sold_act.setObjectName("sold_act")
        self.simple_report_act = QtWidgets.QAction(MainWindow)
        self.simple_report_act.triggered.connect(self.simple_report_search_click)
        self.simple_report_act.setObjectName("simple_report_act")
        self.state_report_act = QtWidgets.QAction(MainWindow)
        self.state_report_act.triggered.connect(self.state_report_search_click)
        self.state_report_act.setObjectName("state_report_act")
        self.advanced_report_act = QtWidgets.QAction(MainWindow)
        self.advanced_report_act.triggered.connect(self.search_advance_report_click)
        self.advanced_report_act.setObjectName("advanced_report_act")
        self.export_act = QtWidgets.QAction(MainWindow)
        self.export_act.triggered.connect(self.export_click)
        self.export_act.setObjectName("export_act")
        self.add_name_act = QtWidgets.QAction(MainWindow)
        self.add_name_act.triggered.connect(self.product_name_click)
        self.add_name_act.setObjectName("add_name_act")
        self.password_act = QtWidgets.QAction(MainWindow)
        self.password_act.triggered.connect(self.password_click)
        self.password_act.setObjectName("add_name_act")
        self.delete_name_act = QtWidgets.QAction(MainWindow)
        self.delete_name_act.triggered.connect(self.delete_product_name_click)
        self.delete_name_act.setObjectName("delete_name_act")
        self.edit_name_serial_act = QtWidgets.QAction(MainWindow)
        self.edit_name_serial_act.triggered.connect(self.edit_name_serial_search_click)
        self.edit_name_serial_act.setObjectName("edit_name_serial_act")
        self.alarm_act = QtWidgets.QAction(MainWindow)
        self.alarm_act.triggered.connect(self.alarm_click)
        self.alarm_act.setObjectName("alarm_act")
        self.returned_act = QtWidgets.QAction(MainWindow)
        self.returned_act.triggered.connect(self.returned_click)
        self.returned_act.setObjectName("returned_act")
        self.inventory_modification_act = QtWidgets.QAction(MainWindow)
        self.inventory_modification_act.setObjectName("inventory_modification_act")
        self.inventory_modification_act.triggered.connect(self.inventory_modification_click)
        self.menu.addAction(self.unpacked_act)
        self.menu.addAction(self.packed_act)
        self.menu.addAction(self.sold_act)
        self.menu.addSeparator()
        self.menu.addAction(self.inventory_modification_act)
        self.menu.addAction(self.returned_act)
        self.menu_2.addAction(self.add_name_act)
        self.menu_2.addAction(self.delete_name_act)
        self.menu_2.addAction(self.edit_name_serial_act)
        self.menu_2.addSeparator()
        self.menu_3.addAction(self.simple_report_act)
        self.menu_3.addAction(self.state_report_act)
        # self.menu_3.addAction(self.advanced_report_act)
        self.setting.addAction(self.alarm_act)
        self.setting.addAction(self.password_act)
        self.menu_history.addAction(self.advanced_report_act)
        self.menu_history.addAction(self.edit_history_act)
        self.menu_history.addAction(self.export_act)
        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menu_2.menuAction())
        self.menubar.addAction(self.menu_3.menuAction())
        self.menubar.addAction(self.menu_history.menuAction())
        self.menubar.addAction(self.setting.menuAction())
        self.lbl = QtWidgets.QLabel(self.centralwidget)
        self.lbl.setAlignment(Qt.AlignRight)

        res = self.cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='t1'")
        if res.fetchone() is not None:
            self.status_lbl()
            self.alarm()
        else:
            self.unpacked_lbl.setText('0')
            self.packed_lbl.setText('0')

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "ایونت - صفحه اصلی"))
        self.label.setText(_translate("MainWindow", "کالاهای بسته بندی نشده"))
        self.label_2.setText(_translate("MainWindow", "کالاهای بسته بندی شده"))
        self.label_6.setText(_translate("MainWindow", "V1.6"))
        self.label_3.setText(_translate("MainWindow", "<html><head/><body><p><a href=\"https://github.com/HadiNamazi\"><span style=\" text-decoration: underline; color:#444444;\">Design &amp; Development by HadiNmz</span></a></p></body></html>"))
        self.menu.setTitle(_translate("MainWindow", "مدیریت کالاها"))
        self.menu_2.setTitle(_translate("MainWindow", "اطلاعات اولیه"))
        self.menu_3.setTitle(_translate("MainWindow", "گزارشات"))
        self.menu_history.setTitle(_translate("MainWindow", "تاریخچه"))
        self.setting.setTitle(_translate("MainWindow", "تنظیمات"))
        self.unpacked_act.setText(_translate("MainWindow", "ثبت ورود کالای بسته بندی نشده"))
        self.packed_act.setText(_translate("MainWindow", "ثبت بسته بندی کالا"))
        self.sold_act.setText(_translate("MainWindow", "ثبت فروش کالای بسته بندی شده"))
        self.add_name_act.setText(_translate("MainWindow", "افزودن اسم و کد کالا"))
        self.delete_name_act.setText(_translate("MainWindow", "حذف کردن کالا"))
        self.edit_name_serial_act.setText(_translate("MainWindow", "ویرایش اسم و کد کالا"))
        self.alarm_act.setText(_translate("MainWindow", "تنظیم هشدار"))
        self.password_act.setText(_translate("MainWindow", "رمز عبور"))
        self.simple_report_act.setText(_translate("MainWindow", "گزارش بر اساس نام کالا"))
        self.state_report_act.setText(_translate("MainWindow", "گزارش بر اساس وضعیت کالا"))
        self.advanced_report_act.setText(_translate("MainWindow", "مشاهده تاریخچه"))
        self.inventory_modification_act.setText(_translate("MainWindow", "اصلاح موجودی"))
        self.returned_act.setText(_translate("MainWindow", "ثبت مرجوعی"))
        self.edit_history_act.setText(_translate("MainWindow", "ویرایش تاریخچه"))
        self.export_act.setText(_translate("MainWindow", "خروجی اکسل تاریخچه"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
