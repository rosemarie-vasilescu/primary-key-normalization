import mysql.connector
from PyQt5.QtWidgets import QMessageBox


class Normalizare_Existenta:

    def __init__(self, conn):
        self.conn = conn
        self.c = self.conn.cursor()

    # Verifica daca trebuie normalizat
    def verifica_null(self, tabel, tip):
        print('verifica_null')

        nenul = False
        self.c.execute("SELECT table_schema FROM INFORMATION_SCHEMA.tables WHERE table_name='" + tabel + "'")
        sc = self.c.fetchall()
        global bd
        for s in sc:
            bd = s[0]

        print("Aceasta este schmea/bd ", bd, tabel)

        self.c.execute("SELECT COLUMN_NAME, COLUMN_KEY,IS_NULLABLE, DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS"
                       " WHERE table_schema = '"+bd + "' and table_name= '" + tabel + "'")

        content = self.c.fetchall()

        print("CONTENT, ", content)

        for row in content:
            print(row)
            # daca este notNULL si nu este  nici PK atunci este nenul
            if row[2] == 'NO' and row[1] != 'PRI':
                nenul = True
        # o coloana not null
        if nenul == False:
            return self.adauga_null(tabel, tip)
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setWindowTitle("Normalizare existenta")
            msg.setText(" exista o constrangere de existenta NOT NULL")
            msg.exec_()

    #coloane ce pot avea NOT NULL
    def adauga_null(self, tabel, tip):

        # coloane cu valori nenule
        # daca nu exista coloane cu valori nenule utilizatorul trebuie sa umple cel putin o coloana complet cu valori

        self.c.execute("SELECT  COLUMN_NAME, COLUMN_KEY,IS_NULLABLE, DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS"
                       " WHERE table_schema = '" + bd + "' and table_name= '" + tabel + "'")

        content = self.c.fetchall()
        print("CONTENT, ", content)

        coloane = []
        for row in content:

            nenul = True
            c2 = self.conn.cursor()

            print("ROW NULLABLE", row[2])

            # daca e cheie primara continua
            if (row[1]=='PRI'):
                continue

            numeColoana = row[0]
            sql = "SELECT " + numeColoana + " FROM " + tabel

            print("SQL,", sql)
            c2.execute(sql)
            cursor = c2.fetchall()
            print("CURSOR", cursor)


            for item in cursor:

                print("ITEM", item)
                print(item[0])
                # valoare null pe coloana
                if item[0] == None:
                    # nu putem sa o  setam not null
                    nenul = False
                    col=numeColoana
            if nenul:
                print(numeColoana)
                coloane.append(numeColoana)

        if len(coloane) == 0:

            print('Selectati una dintre coloana !')
            msg = QMessageBox()
            msg.setText("Trebuie sa aveti cel putin o coloana compeletata complet!"+numeColoana)
            msg.exec_()

            return False

        if tip == 'popup':
            self.afiseaza_mesaj(coloane)
        else:
            print("coloane")
            return coloane

    #  numele coloanei pe care pot sa pun NOT NULL

    # cauta schema de creare a tabelei
    def afla_create_tabel(self, tabel):

        nou = ''
        cursor = self.c.execute("SHOW CREATE TABLE `" + bd + "`.`" + tabel + "`")
        cursor = self.c.fetchall()
        for row in cursor:
            nou = row[1]
        return nou


    # modifica coloanele din schema

    def modifica_Coloane(self, tabel, coloane):
        print(coloane)

        create_tabel = self.afla_create_tabel(tabel)
        print(create_tabel)

        create_tabel_nou = self.modifica_create_tabel(tabel, create_tabel, coloane)
        print(create_tabel_nou)

        self.recreaza_tabel(tabel, create_tabel_nou)



    # seteaza pe coloanele campuri  NOT NULL
    def modifica_create_tabel(self, tabel, create_tabel, campuri):
        print('SCHEMA MODIFICA')

        print("CAMPURI,", campuri)
        for item in campuri:
             create_tabel = create_tabel.replace("`"+item+"` text", "`"+item+"` text NOT NULL")

        print("create_tabel")
        print(create_tabel)

        return create_tabel

    # recreaza tabel, redenumeste tabelele si il sterge pe cel vechi
    def recreaza_tabel(self, tabel, create_tabel):


        tabel_vechi = tabel+'_vechi'
        print(create_tabel)
        self.c.execute('ALTER TABLE ' + tabel + ' RENAME TO '+tabel_vechi)
        print('ceva orice---')
        self.c.execute(create_tabel)
        print(create_tabel, '++++')

        self.c.execute('INSERT INTO ' + tabel + ' SELECT * FROM ' + tabel_vechi)
        print("INSERT MERGI?")
        print(tabel_vechi)
        self.c.execute('DROP TABLE ' + tabel_vechi)
        print("DROP MERGI??????????")

        print('** CREATE TABLE **')
        print(create_tabel)

        self.conn.commit()



    def afiseaza_mesaj(self, coloane):

        print('selectati pe care dintre urmatoarele coloane vreti sa puneti NOT NULL')
        print("Afiseaza coloanele", coloane)
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)

        lista = ', '.join(coloane)
        msg.setText("Selectati dintre coloanele")
        msg.setInformativeText(lista)
        msg.setWindowTitle("Normalizare existenta")
        msg.setDetailedText("Selectati coloana pe care doriti sa puneti NOT NULL")
        msg.exec_()