
import mysql.connector
cnx = mysql.connector.connect(host='localhost',
                                     database='sgbd',
                                     user='root',
                                     password='Creative36!')
conn=cnx.cursor()



#drop tabele
#
conn.execute('DROP TABLE ANGAJATI_TO_PK_NENUM');
conn.execute('DROP TABLE ANGAJATI_TO_PK_COMPUS');
conn.execute('DROP TABLE DEPARTAMENTE_FARA_PK');
conn.execute('DROP TABLE DEPARTAMENTE_PK_COMPUS');
conn.execute('DROP TABLE DEPARTAMENTE_PK_NENUMERIC');


# DEPARTAMENTE_FARA_PK - fara cheie primara
conn.execute('''CREATE TABLE DEPARTAMENTE_FARA_PK
         (denumire 		VARCHAR(45)    NOT NULL,
         sal_min 	DECIMAL ,
         nr_locuri 	INT);''')
print ("Table DEPARTAMENTE_FARA_PK created successfully");
#
# DEPARTAMENTE_PK_NENUMERIC - cu cheie primara nenumerica
conn.execute('''CREATE TABLE DEPARTAMENTE_PK_NENUMERIC
         (id 		VARCHAR(2) NOT NULL PRIMARY KEY,
         denumire 		VARCHAR(45)    NOT NULL,
         sal_min 	DECIMAL ,
         nr_locuri 	INT);''')
print ("Table DEPARTAMENTE_PK_NENUMERIC created successfully");
#
# DEPARTAMENTE_PK_COMPUS - cu cheie primara compusa
conn.execute('''CREATE TABLE DEPARTAMENTE_PK_COMPUS
         (id 		VARCHAR(2) NOT NULL,
         denumire 		VARCHAR(45)    NOT NULL,
         sal_min 	DECIMAL ,
         nr_locuri INT,
         PRIMARY KEY (id, denumire)
         );''')
print ("Table DEPARTAMENTE_PK_COMPUS created successfully");
#
# # # ANGAJATI_TO_PK_NENUM - refera cheie primara nenumerica
conn.execute('''CREATE TABLE ANGAJATI_TO_PK_NENUM
         (id 		INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
         nume 		VARCHAR(45)   NOT NULL,
         prenume 	VARCHAR(45) 	NOT NULL,
         id_dep_fk 	VARCHAR(2) NOT NULL,
         CONSTRAINT id_dep_fk
         FOREIGN KEY (id_dep_fk) REFERENCES DEPARTAMENTE_PK_NENUMERIC(id));''')
print ("Table ANGAJATI_TO_PK_NENUM created successfully");
#

conn.execute('''CREATE TABLE ANGAJATI_TO_PK_COMPUS
         (id 		INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
         nume 		VARCHAR(45)   NOT NULL,
         prenume 	VARCHAR(45) 	NOT NULL,
         id_dep_comp_fk 	VARCHAR(2) NOT NULL,
         CONSTRAINT id_dep_comp_fk
         FOREIGN KEY (id_dep_comp_fk) REFERENCES DEPARTAMENTE_PK_COMPUS(id));''')
print ("Table ANGAJATI_TO_PK_COMPUS created successfully");




#insert
conn.execute("INSERT INTO DEPARTAMENTE_FARA_PK (denumire, sal_min, nr_locuri) VALUES ('Shipping', 1200, 30)");
conn.execute("INSERT INTO DEPARTAMENTE_FARA_PK (denumire, sal_min, nr_locuri) VALUES ('Sales', 1400, 35)");




conn.execute("INSERT INTO DEPARTAMENTE_PK_NENUMERIC (id, denumire, sal_min, nr_locuri) VALUES ('SH', 'Shipping', 1200, 30)");
conn.execute("INSERT INTO DEPARTAMENTE_PK_NENUMERIC (id, denumire, sal_min, nr_locuri) VALUES ('SL','Sales', 1400, 35)");


conn.execute("INSERT INTO DEPARTAMENTE_PK_COMPUS (id,denumire,sal_min, nr_locuri ) VALUES ('SH', 'Shipping', 1200, 30)");
conn.execute("INSERT INTO DEPARTAMENTE_PK_COMPUS (id,denumire, sal_min, nr_locuri ) VALUES ('SL','Sales', 1400, 35)");


conn.execute("INSERT INTO ANGAJATI_TO_PK_NENUM (nume, prenume, id_dep_fk) VALUES ('Vasilescu', 'Rosemarie', 'SH')");
conn.execute("INSERT INTO ANGAJATI_TO_PK_NENUM (nume, prenume, id_dep_fk) VALUES ('Stefan', 'Madalina', 'SL')");

conn.execute("INSERT INTO ANGAJATI_TO_PK_COMPUS (nume,prenume,id_dep_comp_fk) VALUES ('Vasilescu', 'Rosemarie', 'SH')");
conn.execute("INSERT INTO ANGAJATI_TO_PK_COMPUS (nume,prenume,id_dep_comp_fk) VALUES ('Stefan', 'Madalina', 'SL')");



cnx.commit()


conn.close()
cnx.close()