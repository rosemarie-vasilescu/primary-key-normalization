
import os

from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QMainWindow, QApplication
from Normalizare_Existenta import Normalizare_Existenta
from Normalizare_PK import NormalizarePK
from Inregistrari import Inregistrari

import copy
import numpy as np

from afisare import Ui_MainWindow as viewTables
from adaugare import Ui_MainWindow as addRecords

from PyQt5.QtGui import QImage, QMouseEvent


import traceback

import mysql.connector

# fereastra principala
# implementeaza vizualizareTabele.py
class StartWindow(QMainWindow):
    # incarca tableView (datagrid-ul) cu inregistrarile din tabela
    def incarca_date(self):

        # nume tabela selectata din combo box
        self.tabel_optiune = str(self.ui.cmbTable.currentText())

        print(self.tabel_optiune)

        cursor = self.conn.cursor()
        # obtine denumirele la coloane si cate sunt
        self.nameCols = []
        rows = cursor.execute('DESCRIBE ' + self.dbName +"." + self.tabel_optiune)
        rows = cursor.fetchall()
        for row in rows:  # contine detalii despre coloanele unei tabele
            print(row[0])
            self.nameCols.append(row[0])  # contine numele coloanei
        print(len(self.nameCols))

        # count cate coloane sunt in tabela respectiva
        self.ui.tableView.setColumnCount(len(self.nameCols))

        # seteaza numele la coloane cu numele din tabela
        self.ui.tableView.setHorizontalHeaderLabels(self.nameCols)

        # 0 linii/inregistrari
        self.ui.tableView.setRowCount(0)

        query = "SELECT * FROM " + self.tabel_optiune + ""
        print(query)
        result = self.c.execute(query)
        result = self.c.fetchall()
        # umple tableView cu datele din tabela
        for row_number, row_data in enumerate(result):
            self.ui.tableView.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.ui.tableView.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))

    # citeste din fisier text denumirea la database-uri
    # si umple combobox-ul cu acele denumiri
    def completaza_combo_bd(self):
        file = open('databases.txt', 'r')
        Lines = file.readlines()
        for line in Lines:
            print(line)
            self.ui.cmbDatabase.addItem(line.strip())
        file.close()


    def completeaza_combo_tabel(self):

        # get denumire database selectat
        self.dbName = str(self.ui.cmbDatabase.currentText())
        print(self.dbName)
        import mysql.connector
        self.conn = mysql.connector.connect(host='localhost',
                                      database=self.dbName,
                                      user='root',
                                      password='Creative36!')
        #conn = cnx.cursor()

        self.c = self.conn.cursor(buffered=True)

        print("Opened database successfully");
        # clear combobox tabele (ca sa nu faca append)
        self.ui.cmbTable.clear()
        # selecteaza toate tabelele din baza de date nume_db
        self.c.execute("SELECT table_name FROM INFORMATION_SCHEMA.tables WHERE table_schema='"+ self.dbName+"'")
        cursor = self.c.fetchall()
        print(cursor)
        for row in cursor:
            print ("nume = ", row[0], "\n")
            self.ui.cmbTable.addItem(row[0])

        self.incarca_date()

    # pentru insert
    def adaugare(self):
        print('')
        self.ai = Inregistrari('insert', self.tabel_optiune, self.dbName, self.nameCols, self.conn)
        self.ai.seteaza_nume_coloane()
        self.ai.show()

    # pentru update
    def modificare(self):
        if self.contineCheiaPk() == True:
            PK_nume = self.whoPK()  # denumirea coloanei pe care este setata PK
            print(PK_nume)
            try:
                for col in range(self.ui.tableView.columnCount()):
                    sir = self.ui.tableView.horizontalHeaderItem(col).text()
                    if sir == PK_nume:
                        PK_index = col # nr coloanei pe care se afla PK
            except:
                traceback.print_exc()

            rows = self.ui.tableView.selectionModel().selectedRows()
            print(len(rows))
            rows_count, cols_count = (len(rows), self.ui.tableView.columnCount())
            arr = [[0] * cols_count] * rows_count

            toBeUpdated = []  # in caz de eroare, de verificat constrangerea de cheie straina pana sa dau delete
            contor = 0
            PKs_val_init = []
            for r in rows:
                toBeUpdated.clear()
                for i in range(self.ui.tableView.columnCount()):
                    val = self.ui.tableView.item(r.row(), i)
                    if i == PK_index: # e cheia primara sa tin minte valoare initiala
                        PKs_val_init.append(val)
                    if val is not None:
                        toBeUpdated.append(val.text())
                    else:
                        toBeUpdated.append('')
                # print(toBeUpdated)
                arr[contor] = copy.deepcopy(toBeUpdated)
                contor += 1
            print(arr)
            self.ai = Inregistrari('update', self.tabel_optiune, self.dbName, self.nameCols, self.conn)
            self.ai.detaliiCheie(PK_nume, PK_index, PKs_val_init)
            self.ai.seteaza_nume_coloane()
            self.ai.completeazaContinut(arr)
            self.ai.show()
            # return self.ai
            # self.hide() #daca vreau sa o ascund pe cea curenta
        else:
            print('Trebuie sa puneti o cheie primara!')
            msg = QMessageBox()

            msg.setText("Trebuie sa puneti o cheie primara!")
            msg.exec_()

    # sterge randuri din tabela
    def stergere(self):
        if self.contineCheiaPk() == True:
            PK_nume = self.whoPK() # denumirea coloanei pe care este setata cheia priamara
            try:
                for col in range (self.ui.tableView.columnCount()):
                    sir = self.ui.tableView.horizontalHeaderItem(col).text()
                    if sir == PK_nume:
                        PK_index = col
            except:
                traceback.print_exc()
            try:
                rows = self.ui.tableView.selectionModel().selectedRows()
                rows.sort(key=lambda x: x.row(), reverse=True)
                print(str(rows))
                toBeDeleted = []  # in caz de eroare, de verificat constrangerea de cheie straina pana sa dau delete
                for r in rows:
                    print(r)
                    print(r.row())

                    toBeDeleted.clear()
                    for i in range(self.ui.tableView.columnCount()):
                        val = self.ui.tableView.item(r.row(), i)
                        if val is not None:
                            toBeDeleted.append(val.text())
                        else:
                            toBeDeleted.append('')

                    self.c.execute('DELETE FROM ' + self.tabel_optiune + ' WHERE ' + PK_nume + ' = ' + self.ui.tableView.item(r.row(), PK_index).text())
                    self.ui.tableView.removeRow(r.row())
                    self.conn.commit()
                    print(toBeDeleted)
            except:
                traceback.print_exc()
        else:
            print('Trebuie sa puneti o cheie primara, numerica, simpla')
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Trebuie sa puneti o cheie primara, numerica, simpla")
            msg.exec_()

    def contineCheiaPk(self):
        print('verifica daca e bine pusa cheia primara')
        permis = True
        arePk = False
        pk = self.c.execute("SELECT COUNT(COLUMN_NAME) FROM  INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = '" + self.dbName +"' AND  TABLE_NAME = '" + self.tabel_optiune + "'  AND COLUMN_KEY = 'PRI';")
        pk = self.c.fetchall()
        for p in pk:
            nr_pk=p[0]
        rows = self.c.execute("SELECT DATA_TYPE FROM  INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = '" + self.dbName +"' AND  TABLE_NAME = '" + self.tabel_optiune + "'  AND COLUMN_KEY = 'PRI';")
        rows = self.c.fetchall()
        print(nr_pk)


        for row in rows:
            print(row[0])
            if nr_pk > 1:  #
                arePk = True
                permis = False
            if nr_pk == 1 and (row[0] != 'int'):  # daca e una singura si nu e numerica
                arePk = True
                permis = False
                print('int')
            if nr_pk == 1:  # gaseste PK
                arePk = True
                print('true')
        if arePk == True and permis == True:
            return True
        return False

    def whoPK(self):
        print('whopk')
        rows = self.c.execute('DESCRIBE ' + self.dbName + "." + self.tabel_optiune)
        rows = self.c.fetchall()
        for row in rows:
            if row[3] == 'PRI': # gaseste PK
                print(row[3])
                return row[0]

    def normalizeazaExistenta(self):
        cols = self.ui.tableView.selectionModel().selectedColumns()
        lista_coloane = []
        for c in cols:
            print('c='+self.nameCols[c.column()])
            # print(c.column())
            lista_coloane.append(self.nameCols[c.column()]) #numele coloanelor selectate

        print(len(cols))

        normalizator = Normalizare_Existenta(self.conn)
        if len(cols) == 0: #daca nu am selectat nicio coloana
            # conn.commit()
            normalizator.verifica_null(self.tabel_optiune, 'popup') # imi spune ce am voie sa selectez
        else:
            rez = normalizator.verifica_null(self.tabel_optiune, 'ok')
            if rez is not None: #in caz ca e deja bine proiectat si eu selectez coloane imi da return None

                print(rez)
                # coloanele selectate trebuie sa fie dintre coloanele valide
                result = all(elem in rez for elem in lista_coloane)
                if result:
                    normalizator.modifica_Coloane(self.tabel_optiune, lista_coloane)
                else:
                    print('Selectati dintre coloanele specificate va rog')
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Critical)
                    msg.setText("Selectati dintre coloanele specificate")
                    msg.exec_()

    def normalizeazaPK(self):
        normalizator = NormalizarePK(self.conn)
        normalizator.cauta_cheie(self.tabel_optiune)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ui = viewTables()
        self.ui.setupUi(self)


        self.completaza_combo_bd() #incarca combobox-ul cu baze de date
        self.completeaza_combo_tabel()
        self.incarca_date()
        self.ui.cmbDatabase.activated.connect(self.completeaza_combo_tabel) #incarca combobox-ul cu tabele
        self.ui.cmbTable.activated.connect(self.incarca_date) #  tabel  selectata
        self.ui.btnRefresh.clicked.connect(self.incarca_date)  #  tabel  selectata

        self.ui.btnInsert.clicked.connect(self.adaugare) # adaugare
        self.ui.btnDelete.clicked.connect(self.stergere)  # stergere
        self.ui.btnUpdate.clicked.connect(self.modificare)  # modificare

        self.ui.btnExistenta.clicked.connect(self.normalizeazaExistenta)  # normalizare existenta
        self.ui.btnPK.clicked.connect(self.normalizeazaPK)  # normalizeaza cheie primar

if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    widget = StartWindow()
    widget.show()

    app.exec_()
