# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Yonet\Desktop\exceltoexcelınvoiceui\gelir.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Gelir(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1007, 673)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(0, 10, 1001, 611))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.tableWidgetFaturalar_1 = QtWidgets.QTableWidget(self.frame)
        self.tableWidgetFaturalar_1.setGeometry(QtCore.QRect(10, 10, 991, 240))
        self.tableWidgetFaturalar_1.setMaximumSize(QtCore.QSize(16777215, 245))
        self.tableWidgetFaturalar_1.setSizeIncrement(QtCore.QSize(0, 0))
        self.tableWidgetFaturalar_1.setRowCount(10)
        self.tableWidgetFaturalar_1.setColumnCount(33)
        self.tableWidgetFaturalar_1.setObjectName("tableWidgetFaturalar_1")
        self.tableWidgetFaturalar_2 = QtWidgets.QTableWidget(self.frame)
        self.tableWidgetFaturalar_2.setGeometry(QtCore.QRect(10, 300, 991, 240))
        self.tableWidgetFaturalar_2.setMaximumSize(QtCore.QSize(16777215, 245))
        self.tableWidgetFaturalar_2.setSizeIncrement(QtCore.QSize(0, 0))
        self.tableWidgetFaturalar_2.setRowCount(10)
        self.tableWidgetFaturalar_2.setColumnCount(33)
        self.tableWidgetFaturalar_2.setObjectName("tableWidgetFaturalar_2")
        self.pushButton_select_folder = QtWidgets.QPushButton(self.frame)
        self.pushButton_select_folder.setGeometry(QtCore.QRect(950, 260, 51, 30))
        self.pushButton_select_folder.setObjectName("pushButton_select_folder")
        self.pushButton = QtWidgets.QPushButton(self.frame)
        self.pushButton.setGeometry(QtCore.QRect(910, 550, 93, 28))
        self.pushButton.setObjectName("pushButton")
        self.lineEdit_path_excel = QtWidgets.QLineEdit(self.frame)
        self.lineEdit_path_excel.setGeometry(QtCore.QRect(540, 260, 391, 30))
        self.lineEdit_path_excel.setObjectName("lineEdit_path_excel")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1007, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton_select_folder.setText(_translate("MainWindow", "..."))
        self.pushButton.setText(_translate("MainWindow", "Create Excel"))



