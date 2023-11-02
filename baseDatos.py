import sqlite3

#creacion de la base de datos 
class database():
    def __init__(self):
        self.db_path = "database.db"
        self.con=sqlite3.connect(self.db_path)
        self.cursor=self.con.cursor()
        self.cursor.executescript(
                '''CREATE TABLE IF NOT EXISTS usuarios (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, username TEXT, age INTEGER, email TEXT, password TEXT, uid TEXT);
                    CREATE TABLE IF NOT EXISTS musica (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,id_user Integer, name TEXT, artista TEXT, url TEXT,
                    FOREIGN KEY (id_user) REFERENCES usuarios(id)
                    );
                
                '''

        )
    
      
        #guarda los cambios en la base de datos
        self.con.commit()
        self.con.close()




