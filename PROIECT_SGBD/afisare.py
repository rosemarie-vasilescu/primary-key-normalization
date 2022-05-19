# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'afisare.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1064, 550)
        MainWindow.setStyleSheet("QPushButton{background-color: rgb(219, 237, 243);\n"
"border-radius: 10px;\n"
"color: rgb(255, 255, 255);\n"
"}\n"
"QPushButton::hover{\n"
"background-color: rgb(0, 143, 105);\n"
"}")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setStyleSheet("background-color: rgb(244, 247, 255);")
        self.centralwidget.setObjectName("centralwidget")
        self.tableView = QtWidgets.QTableWidget(self.centralwidget)
        self.tableView.setGeometry(QtCore.QRect(30, 150, 741, 221))
        self.tableView.setStyleSheet("")
        self.tableView.setRowCount(5)
        self.tableView.setColumnCount(7)
        self.tableView.setObjectName("tableView")
        self.btnInsert = QtWidgets.QPushButton(self.centralwidget)
        self.btnInsert.setGeometry(QtCore.QRect(790, 200, 101, 31))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.btnInsert.setFont(font)
        self.btnInsert.setStyleSheet("QPushButton{background-color: rgb(110, 203, 238);\n"
"border-radius: 0px;\n"
"color: rgb(255, 255, 255);\n"
"}\n"
"QPushButton::hover{\n"
"background-color: rgb(19, 184, 245);\n"
"}")
        self.btnInsert.setObjectName("btnInsert")
        self.cmbTable = QtWidgets.QComboBox(self.centralwidget)
        self.cmbTable.setGeometry(QtCore.QRect(240, 80, 401, 31))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.cmbTable.setFont(font)
        self.cmbTable.setObjectName("cmbTable")
        self.cmbDatabase = QtWidgets.QComboBox(self.centralwidget)
        self.cmbDatabase.setGeometry(QtCore.QRect(240, 30, 401, 31))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.cmbDatabase.setFont(font)
        self.cmbDatabase.setStyleSheet("")
        self.cmbDatabase.setObjectName("cmbDatabase")
        self.lblDatabase = QtWidgets.QLabel(self.centralwidget)
        self.lblDatabase.setGeometry(QtCore.QRect(40, 30, 181, 20))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.lblDatabase.setFont(font)
        self.lblDatabase.setObjectName("lblDatabase")
        self.lblTable = QtWidgets.QLabel(self.centralwidget)
        self.lblTable.setGeometry(QtCore.QRect(40, 80, 171, 21))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.lblTable.setFont(font)
        self.lblTable.setObjectName("lblTable")
        self.btnUpdate = QtWidgets.QPushButton(self.centralwidget)
        self.btnUpdate.setGeometry(QtCore.QRect(790, 260, 111, 31))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.btnUpdate.setFont(font)
        self.btnUpdate.setStyleSheet("QPushButton{background-color: rgb(110, 203, 238);\n"
"border-radius: 0px;\n"
"color: rgb(255, 255, 255);\n"
"}\n"
"QPushButton::hover{\n"
"background-color: rgb(19, 184, 245);\n"
"}")
        self.btnUpdate.setObjectName("btnUpdate")
        self.btnDelete = QtWidgets.QPushButton(self.centralwidget)
        self.btnDelete.setGeometry(QtCore.QRect(790, 310, 111, 31))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.btnDelete.setFont(font)
        self.btnDelete.setStyleSheet("QPushButton{background-color: rgb(110, 203, 238);\n"
"border-radius: 0px;\n"
"color: rgb(255, 255, 255);\n"
"}\n"
"QPushButton::hover{\n"
"background-color: rgb(19, 184, 245);\n"
"}")
        self.btnDelete.setObjectName("btnDelete")
        self.btnRefresh = QtWidgets.QPushButton(self.centralwidget)
        self.btnRefresh.setGeometry(QtCore.QRect(790, 150, 91, 31))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.btnRefresh.setFont(font)
        self.btnRefresh.setStyleSheet("QPushButton{background-color: rgb(110, 203, 238);\n"
"border-radius: 0px;\n"
"color: rgb(255, 255, 255);\n"
"}\n"
"QPushButton::hover{\n"
"background-color: rgb(19, 184, 245);\n"
"}")
        self.btnRefresh.setObjectName("btnRefresh")
        self.btnExistenta = QtWidgets.QPushButton(self.centralwidget)
        self.btnExistenta.setGeometry(QtCore.QRect(780, 420, 261, 31))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.btnExistenta.setFont(font)
        self.btnExistenta.setStyleSheet("QPushButton{background-color: rgb(110, 203, 238);\n"
"border-radius: 0px;\n"
"color: rgb(255, 255, 255);\n"
"}\n"
"QPushButton::hover{\n"
"background-color: rgb(19, 184, 245);\n"
"}")
        self.btnExistenta.setObjectName("btnExistenta")
        self.btnPK = QtWidgets.QPushButton(self.centralwidget)
        self.btnPK.setGeometry(QtCore.QRect(780, 370, 261, 31))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.btnPK.setFont(font)
        self.btnPK.setStyleSheet("QPushButton{background-color: rgb(110, 203, 238);\n"
"border-radius: 0px;\n"
"color: rgb(255, 255, 255);\n"
"}\n"
"QPushButton::hover{\n"
"background-color: rgb(19, 184, 245);\n"
"}")
        self.btnPK.setObjectName("btnPK")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.btnInsert.setText(_translate("MainWindow", "Insereaza"))
        self.lblDatabase.setText(_translate("MainWindow", "Alegeti o baza de date"))
        self.lblTable.setText(_translate("MainWindow", "Alegeti un tabel"))
        self.btnUpdate.setText(_translate("MainWindow", "Modifica"))
        self.btnDelete.setText(_translate("MainWindow", "Sterge"))
        self.btnRefresh.setText(_translate("MainWindow", "Refresh"))
        self.btnExistenta.setText(_translate("MainWindow", "Normalizare existenta"))
        self.btnPK.setText(_translate("MainWindow", "Normalizare Cheie Primara"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
