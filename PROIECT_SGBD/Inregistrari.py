from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QMainWindow, QApplication


from afisare import Ui_MainWindow as viewTables
from adaugare import Ui_MainWindow as addRecords

from PyQt5.QtGui import QImage, QMouseEvent


import traceback

import mysql.connector




class Inregistrari(QMainWindow):



    def __init__(self, tip, table_optiune, nume_db, nameCols, conn):
        super().__init__()
        self.tip = tip
        self.table_optiune = table_optiune
        self.nume_db = nume_db
        self.nameCols = nameCols

        self.conn = conn
        self.c = self.conn.cursor()

        self.ui1 = addRecords()
        self.ui1.setupUi(self)

        print('TIPUL= '+tip)

        if tip == 'update':
            self.ui1.btnNewLine.setVisible(False)
            self.ui1.btnDelete.setVisible(False)

        self.ui1.btnNewLine.clicked.connect(self.adauga_randuri)
        self.ui1.btnSend.clicked.connect(self.trimite_date)
        self.ui1.btnDelete.clicked.connect(self.sterge_randuri)




    def seteaza_nume_coloane(self):
        self.ui1.tableWidget.setRowCount(1)
        self.ui1.tableWidget.setColumnCount(len(self.nameCols))
        self.ui1.tableWidget.setHorizontalHeaderLabels(self.nameCols)


    def adauga_randuri(self):
        countRow = self.ui1.tableWidget.rowCount()
        self.ui1.tableWidget.setRowCount(countRow+1)

    def sterge_randuri(self):
        try:
            rows = self.ui1.tableWidget.selectionModel().selectedRows()
            rows.sort(key=lambda x: x.row(), reverse=True)
            print(str(rows))
            lista_drop = []
            for r in rows:
                print(r)
                print(r.row())

                lista_drop.clear()
                for i in range (self.ui1.tableWidget.columnCount()):
                    val = self.ui1.tableWidget.item(r.row(), i)
                    if val is not None:
                        lista_drop.append(val.text())
                    else:
                        lista_drop.append('')
                self.ui1.tableWidget.removeRow(r.row())
                print(lista_drop)
        except:
            traceback.print_exc()

    def trimite_date(self):
        line = []
        for row in range(self.ui1.tableWidget.rowCount()):
            line.clear()
            for col in range (self.ui1.tableWidget.columnCount()):
                val = self.ui1.tableWidget.item(row, col)
                if val is not None:
                    val = val.text()
                    if val.isnumeric():
                        line.append(val)
                    else:
                        line.append("'" + val + "'")
                else:
                    line.append('null')

            if self.tip == 'insert':

                values = ', '.join(line)

                numeColoane = ', '.join(self.nameCols)
                Cmd = 'INSERT INTO ' + self.table_optiune + ' (' + numeColoane + ') VALUES (' + values + ')'
                print(Cmd)
                try:
                    self.c.execute(Cmd)
                except mysql.connector.IntegrityError:
                    msg = QMessageBox()

                    msg.setText("exista deja!")
                    msg.exec_()
            else:
                lista_update = [0] * len(self.nameCols)
                print('e UPDATE')
                for i in range(len(self.nameCols)):
                    lista_update[i] = self.nameCols[i] + ' = ' + line[i]
                lista_update = ', '.join(lista_update)
                print('indici element')
                print(row)
                print(self.index_cheie)
                Cmd = 'UPDATE ' + self.table_optiune + ' SET ' + lista_update + ' WHERE ' + self.nume_cheie + ' = ' + self.chei_val_init[row].text()
                print(Cmd)
                try:
                    self.c.execute(Cmd)
                except mysql.connector.IntegrityError:

                    msg = QMessageBox()

                    msg.setText("exista deja!")
                    msg.exec_()

        self.conn.commit()


    def completeazaContinut(self, rows):
        self.ui1.tableWidget.removeRow(0)
        for row_number, row_data in enumerate(rows):
            self.ui1.tableWidget.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.ui1.tableWidget.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))


    def detaliiCheie(self, nume_cheie, index_cheie, chei_val_init):

        self.nume_cheie = nume_cheie
        self.index_cheie = index_cheie
        self.chei_val_init = chei_val_init

