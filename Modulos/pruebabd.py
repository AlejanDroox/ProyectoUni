import mariadb 
def consulta(query):
    try:
        conect = mariadb.connect(
            user="root",
            password="root",
            host="localhost",
            port=3309,
            database="ferreteria"
        )
    except mariadb.Error as e:
        print(e)
    cur = conect.cursor()
    cur.execute(query)
    conect.commit()
    return cur
cur = consulta('INSERT INTO productos (Nombre) VALUES ("newnew");')
print(cur)
cur = consulta('SELECT `Nombre` FROM `ferreteria`.`productos`; ')
for i in cur:
    print(i)