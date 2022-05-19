import copy
import re
from PyQt5.QtWidgets import QMessageBox


class NormalizarePK:

    def __init__(self, conn):
        self.conn = conn
        self.c = self.conn.cursor()

    def cauta_cheie(self, tabel):
        print('cauta_cheie')
        # pkcompus are pk pe mai multe coloane, pkexist exista pk, pknenum pk nenumeric
        PKcompusa = False
        PKexist = False
        PKnenum = False
        # aflu baza de date
        self.c.execute("SELECT table_schema FROM INFORMATION_schema.tables WHERE table_name='" + tabel + "'")
        sc = self.c.fetchall()
        for s in sc:
            bd = s[0]
        # aflu nr pk
        pk = self.c.execute(
            "SELECT COUNT(COLUMN_NAME) FROM  INFORMATION_schema.COLUMNS WHERE TABLE_schema = '" + bd + "' AND  TABLE_NAME = '" + tabel + "'  AND COLUMN_KEY = 'PRI';")
        pk = self.c.fetchall()
        for p in pk:
            nr_pk = p[0]
        type = self.c.execute(
            "SELECT DATA_TYPE FROM  INFORMATION_schema.COLUMNS WHERE TABLE_schema = '" + bd + "' AND  TABLE_NAME = '" + tabel + "'  AND COLUMN_KEY = 'PRI';")
        type = self.c.fetchall()
        print(nr_pk)
        for t in type:
            t_pk = t[0]
        # tip pk

        if nr_pk > 1:
            PKcompusa = True
        if nr_pk == 1:
            PKexist = True
        if nr_pk == 1 and (t_pk != 'int'):
            PKnenum = True
            print(PKnenum)
        if PKcompusa == True:
            self.reparaPK(tabel, bd)

        elif PKnenum == True:
            self.reparaPK(tabel, bd)

        elif PKexist == False:
            create_table = self.afla_create_table(tabel, bd)
            create_table_noua = self.cheieNoua(create_table)
            self.tabel_nou(tabel, create_table_noua, bd)

        else:

            msg = QMessageBox()
            msg.setText("Nu exista modificari de facut")
            msg.exec_()

    def afla_create_table(self, tabel, bd):
        print('sunt in afla create table')
        self.c.execute("SHOW CREATE TABLE " + bd + "." + tabel)
        cursor = self.c.fetchall()

        for row in cursor:
            create_table = row[1]
            print(create_table + " statement in afla")
        create_table = create_table.replace(tabel, bd + "." + tabel, 1)
        return create_table

    def reparaPK(self, tabel, bd):
        print('reparaPK ')

        create_table = self.afla_create_table(tabel, bd)
        create_table_faraPK = self.stergeCheie(create_table, tabel, bd)
        create_table_noua = self.cheieNoua(create_table_faraPK)
        self.tabel_nou(tabel, create_table_noua, bd)

    def stergeCheie(self, create_table, tabel, bd):
        print('sterge cheie')

        stm = re.split('[ \n\t]', create_table)
        # fac stm lista sa pot sa gasesc primary si sa elimin
        stm_split = []
        for i in stm:

            if i != '':
                stm_split.append(i)

        stm = ' '.join(stm_split)
        stm = re.split('[ ]', stm)

        for i in range(len(stm)):
            eliminat = False
            if (stm[i][-1] == ',' and stm[i + 1].lower() == 'primary'):
                eliminat = True
                stm2 = stm[i].split(',')  # scapam de virgula
                stm[i] = copy.deepcopy(stm2[0])
                sterge = 1
                j = i + 1
                while stm[j].count(')') == 0:
                    stm[j] = ''
                    j += 1

                stm[j] = ''
            if eliminat == True:
                break

        stm = ' '.join(stm)

        # PK nonnumeric
        stm2 = stm.split('PRIMARY KEY')
        stm = ''.join(stm2)

        # print(nou)
        return stm

    # adauga PK surogat
    def cheieNoua(self, create_table):
        print('cheieNoua')

        create_table = create_table.split('(')
        create_table[1] = ' id_nou INT NOT NULL PRIMARY KEY, ' + create_table[1]
        create_table = ' ( '.join(create_table)

        print(create_table)

        return create_table

    # AM RAMAS AICI

    def gasesteFK(self, tabel, bd, tabel_nou, vechi):
        print('gasesteFK')

        # selecteaza toate tabelele din baza de date
        c2 = self.conn.cursor()
        c1 = self.conn.cursor()
        stm_split_tabele_interzis = []
        stm_splitPKs = []
        stm_splitFKs = []
        stm_split_tabeleFK_vechi = []
        stm_split_scheme_noi = []

        sql = "Select table_name from INFORMATION_schema.tables where table_schema='" + bd + "'"
        print(sql)
        c2.execute(sql)
        cursor = c2.fetchall()
        print('show tables')

        for row in cursor:

            ok = 0

            stm_splitPKs.clear()
            stm_splitFKs.clear()

            numeTabelFK = str(row[0])
            print(numeTabelFK)
            if numeTabelFK in stm_split_tabele_interzis:
                print('incerci sa repari acelasi tablou')
            else:

                rows = c1.execute(
                    "SELECT referenced_table_name,column_name,referenced_column_name  FROM  INFORMATION_schema.KEY_COLUMN_USAGE  WHERE TABLE_NAME = '" + numeTabelFK + "' and referenced_table_name is not null")
                rows = c1.fetchall()
                for r in rows:

                    if r[0] == tabel:
                        print("are fk = " + numeTabelFK + "\n")
                        ok = 1
                        pk = r[2]
                        fk = r[1]
                        stm_splitPKs.append(pk)
                        stm_splitFKs.append(fk)

            if ok == 1:
                tabelFK_vechi, create_table_noua = self.stergeFK(tabel_nou, numeTabelFK, stm_splitPKs, stm_splitFKs, bd,
                                                                 tabel, vechi)  # tabelaPK, tabelaFK, pk, fk

                stm_split_tabeleFK_vechi.append(tabelFK_vechi)
                stm_split_scheme_noi.append(create_table_noua)
                # tabelFK_vechi = ''
                stm_split_tabele_interzis.append(numeTabelFK)

                print('stm_split tabele')
                print(stm_split_tabele_interzis)

        # try:
        print('reface')
        for i in range(len(stm_split_scheme_noi)):
            print('tabel nou')
            print(stm_split_tabeleFK_vechi[i])
            print(self.afla_create_table(stm_split_tabeleFK_vechi[i], bd))

            # try:
            self.FK_nou(stm_split_scheme_noi[i], stm_split_tabeleFK_vechi[i], bd, vechi)
            # except:
            #     continue

    def tabel_nou(self, tabel, create_table, bd):
        print(' in tabel nou')

        create_table = create_table.replace("" + bd + "." + tabel + "", bd + "`.`" + tabel, 1)

        create_table_noua = "" + create_table

        create_table_noua = create_table_noua.replace("" + bd + "`.`" + tabel + "", bd + "`.`nou_" + tabel,
                                                      1)  # create table nou_nume
        tabel_nou = bd + ".nou_" + tabel
        print(create_table_noua + "tabel noua")

        self.c.execute(create_table_noua)

        print('create_table noua')
        print(create_table_noua)

        contor = 1
        c2 = self.conn.cursor()

        lselect = []  # pentru valorile returnate de select
        # copierea continutului vechii tabele
        self.c.execute('SELECT * FROM ' + bd + "." + tabel)
        cursor = self.c.fetchall()

        for r in cursor:
            print(r[0])
            lselect.clear()
            for i in range(len(r)):
                if r[i] is not None:
                    val = str(r[i])
                    if val.isnumeric():
                        lselect.append(val)
                    else:
                        lselect.append("'" + val + "'")  # daca e string sa imi puna ghilimelele
                else:
                    lselect.append('null')

            values = ', '.join(lselect)
            print(values)

            # umplem tabela NOUA cu valorile coloanei noii chei primare plus ce era in tabela veche
            insert = 'INSERT INTO ' + tabel_nou + ' VALUES ( ' + str(contor) + ' , ' + values + ' )'
            print(insert)
            c2.execute(insert)
            contor += 1

        print('create_table ')
        print(create_table)

        sql = 'DROP TABLE ' + bd + "." + tabel
        print(sql)
        self.c.execute("SET foreign_key_checks = 0")
        self.gasesteFK(tabel, bd, tabel_nou, True)
        self.c.execute(sql)
        print("drop tabel")
        print("create_table inainte de execute" + create_table)
        self.c.execute(create_table)
        print("execute create_table")
        # nu face insert
        print(tabel_nou + "tabel")
        sql1 = 'INSERT INTO ' + bd + "." + tabel + ' SELECT * FROM ' + tabel_nou
        print(sql1)
        self.c.execute(sql1)
        print("insert")
        print("cauta fk" + tabel_nou + "  " + tabel)
        self.gasesteFK(tabel_nou, bd, tabel, False)
        print("a cautat")
        self.c.execute('DROP TABLE ' + tabel_nou + "")
        print('a dat drop')
        # pus inapoi in caz ca nu merge
        print('executat key check')
        self.conn.commit()
        print(tabel_nou + "tabel nou in reface tabel")

    def stergeFK(self, tabelPK, tabelFK, pk, fk, bd, tabel_vechi, vechi):
        print('refaceFK')

        print(pk)
        print(fk)

        c1 = self.conn.cursor()
        c2 = self.conn.cursor()
        if vechi:
            fknou = 'fk_' + tabelFK
            adauga = 'ALTER TABLE ' + tabelFK + ' ADD COLUMN ' + fknou + ' INTEGER'

            print(adauga)
            c1.execute(adauga)
        else:
            fknou = 'fk1_' + tabelFK

        print(self.afla_create_table(tabelFK, bd))

        #
        getid_nou = "SELECT tpk.id_nou, tfk." + fk[
            0] + " FROM " + tabelPK + " tpk INNER JOIN " + bd + "." + tabelFK + " tfk ON tpk." + pk[0] + " = tfk." + fk[
                        0]
        print(getid_nou)
        rows = c1.execute(getid_nou)
        rows = c1.fetchall()
        print('ok')
        print(rows)
        for row in rows:
            print(row[0])
            update = "UPDATE " + bd + "." + tabelFK + " SET " + fknou + " = " + str(row[0]) + " WHERE " + fk[
                0] + " = '" + str(row[1]) + "'"
            print(update)
            c2.execute(update)
        print("update ok" + tabelFK)

        create_table = self.afla_create_table(tabelFK, bd)
        print('create_table dupa update fk_nou')

        print(create_table)

        stm = re.split('[ \n\t]', create_table)
        print('create_table fara spatii si tabburi')
        print(stm)

        # scapam de spatiile goale din urma split-ului
        stm_split = []
        for i in stm:

            if i != '' and i != ' ':
                stm_split.append(i)

        stm = ' '.join(stm_split)

        stm = stm.split(' ( ')
        stm = '('.join(stm)
        print('join ' + stm)

        stm = stm.split('(', 1)
        stm = ' ('.join(stm)
        print('reparare spatiu= ' + stm)

        create_table_noua = stm
        for i in range(len(fk)):

            create_table_noua = create_table_noua.replace(fk[i], fknou)
            create_table_noua = create_table_noua.replace(tabel_vechi, tabelPK)
            create_table_noua = create_table_noua.replace(pk[i], "id_nou")
            if vechi:
                create_table_noua = create_table_noua.replace("id_nou", "id", 2)
                create_table_noua = create_table_noua.replace(fknou, fk[i], 1)

        print('tabel nou stergefk')
        print(create_table_noua)

        create_table_noua = create_table_noua.replace("`", "", 2)
        print('tabel cu ghilimele ' + create_table_noua)

        return tabelFK, create_table_noua

    def FK_nou(self, create_table, tabelFK, bd, vechi):

        print('create_table initial')
        print(create_table)
        create_table_noua = create_table.replace(bd + "." + tabelFK, bd + ".nou_" + tabelFK, 1)
        print(create_table_noua)

        create_table_noua = create_table_noua.split()
        tabel_nou = create_table_noua[2]
        create_table_noua = ' '.join(create_table_noua)
        if vechi == False:
            create_table_noua = create_table_noua.replace("fk1_" + tabelFK, "fk_" + tabelFK)

        print('create_table_NOUA')
        print(create_table_noua)
        self.c.execute(create_table_noua)
        print('INSERT INTO ' + tabel_nou + ' SELECT * FROM ' + tabelFK)
        self.c.execute('INSERT INTO ' + tabel_nou + ' SELECT * FROM ' + tabelFK)

        print('final')
        print(create_table)

        print(tabelFK + " tabelfk " + tabel_nou + "  tabel nou")
        self.c.execute('DROP TABLE ' + tabelFK)
        print("drop tabel fk")

        create_table = create_table.replace("`", "", 2)
        create_table = create_table.replace("fk_" + tabelFK, "fk1_" + tabelFK)
        print("fk_nou " + tabelFK)

        print(create_table + " in refac fk")
        self.c.execute(create_table)
        print("execute create_table")
        self.c.execute('INSERT INTO ' + tabelFK + ' SELECT * FROM ' + tabel_nou)
        print("insert into tabelfk")
        self.c.execute('DROP TABLE ' + tabel_nou)
        print("drop tabel nou " + tabel_nou)

        self.conn.commit()


