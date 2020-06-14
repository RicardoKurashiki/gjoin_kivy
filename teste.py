import sqlite3

conn = sqlite3.connect('BANCO.db')
cursor = conn.cursor()

cursor.execute('''
INSERT INTO groupsdb(idUser)
VALUES (?) 
WHERE idGrupo = {}
'''.format(29), ('666')
)
conn.commit()
conn.close()