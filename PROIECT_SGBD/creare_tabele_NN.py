
import mysql
import mysql.connector
cnx = mysql.connector.connect(host='localhost',
                                     database='sgbd1',
                                     user='root',
                                     password='Creative36!')
conn=cnx.cursor()




conn.execute('DROP TABLE STUDENTI_NN_PK')
conn.execute('DROP TABLE STUDENTI_NN_fara_PK')
conn.execute('DROP TABLE STUDENTI_PK_Nenumeric')

conn.execute('''CREATE TABLE STUDENTI_NN_PK
            (id     INTEGER NOT NULL PRIMARY KEY,
            nume    TEXT,
            prenume    TEXT,
            cnp    TEXT,
            email    TEXT
            );''')
print ("Table STUDENTI_NN_PK created successfully")

conn.execute('''CREATE TABLE STUDENTI_NN_fara_PK
            (nume   TEXT,
            prenume    TEXT,
            cnp    TEXT,
            email    TEXT
            );''')
print ("Table STUDENTI_NN_fara_PK created successfully")


conn.execute('''CREATE TABLE STUDENTI_PK_Nenumeric
            (id 	CHAR(2) NOT NULL PRIMARY KEY,
            nume  TEXT,
            prenume  TEXT,
            cnp  TEXT,
            email TEXT
            );''')
print ("Table STUDENTI_PK_Nenumeric created successfully")


conn.execute("INSERT INTO STUDENTI_NN_PK (id,nume,prenume,cnp,email) VALUES (1,'Stefan','Iuliana','6006251324560',null)")
conn.execute("INSERT INTO STUDENTI_NN_PK (id,nume,prenume,cnp,email) VALUES (2,'Vasilescu','Rosemarie',null,'vasilescurosemarie@gmail.com')")
conn.execute("INSERT INTO STUDENTI_NN_PK (id,nume,prenume,cnp,email) VALUES (3,'Stefan',null,'6006251324545','stefaniulianamadalina@gmail.com')")


conn.execute("INSERT INTO STUDENTI_NN_fara_PK (nume,prenume,cnp,email) VALUES ('Stefan','Iuliana','6006251324560',null)")
conn.execute("INSERT INTO STUDENTI_NN_fara_PK (nume,prenume,cnp,email) VALUES ('Vasilescu','Rosemarie',null,'vasilescurosemarie@gmail.com')")
conn.execute("INSERT INTO STUDENTI_NN_fara_PK (nume,prenume,cnp,email) VALUES ('Stefan',null,'6006251324545','stefaniulianamadalina@gmail.com')")


conn.execute("INSERT INTO STUDENTI_PK_Nenumeric (id,nume,prenume,cnp,email) VALUES ('a','Stefan','Iuliana','6006251324560',null)")
conn.execute("INSERT INTO STUDENTI_PK_Nenumeric (id,nume,prenume,cnp,email) VALUES ('b','Vasilescu','Rosemarie',null,'vasilescurosemarie@gmail.com')")
conn.execute("INSERT INTO STUDENTI_PK_Nenumeric (id,nume,prenume,cnp,email) VALUES ('c','Stefan',null,'6006251324545','stefaniulianamadalina@gmail.com')")




print ("succes")

cnx.commit()



conn.close()

cnx.close()