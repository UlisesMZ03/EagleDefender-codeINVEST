import sqlite3
import hashlib
# Llave pública proporcionada
public_key = (19303, 13595)
class Usuario:
    db_path = "prueba.db"
    def __init__(self, name, username, age, email, password, uid):
        self.name = self._encrypt_data(name)
        self.username = self._encrypt_data(username)
        self.age = age

        self.email = self._encrypt_data(email)
        # Encripta la contraseña al crear una instancia de Usuario
        self.password = self._encrypt_data(password)
        self.uid = self._encrypt_data(uid)
        self.id = self._get_next_id()
       

    def _get_next_id(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Obtiene el último ID asignado, o 0 si no hay usuarios en la base de datos
        cursor.execute('''SELECT MAX(id) FROM usuarios''')
        last_id = cursor.fetchone()[0]
        conn.close()

        return last_id + 1 if last_id else 1

    def _encrypt_data(self,data):
        if data == int:
            hashed_data = hashlib.sha256(data.encode()).hexdigest()
            data_int = int(hashed_data, 16) % public_key[0]
            encrypted_data = pow(data_int, public_key[1], public_key[0])
        else:

            hashed_data = hashlib.sha256(data.encode()).hexdigest()
            data_int = int(hashed_data, 16) % public_key[0]
            encrypted_data = pow(data_int, public_key[1], public_key[0])
        return encrypted_data
  
    @staticmethod
    def getID(username):
        conn = sqlite3.connect(Usuario.db_path)
        cursor = conn.cursor()
       
        cursor.execute("SELECT id FROM usuarios WHERE username=?", (username,))
        
        # Obtén el resultado de la consulta
        result = cursor.fetchone()
        
        conn.close()
        
        # Verifica si se encontró un resultado
        if result is not None:
            # result es una tupla, por lo que puedes acceder al ID como result[0]
            return result[0]
        else:
            # Retorna un valor indicando que no se encontró el email en la base de datos
            return None
    @staticmethod
    def encripta(data):
        if data == int:
            hashed_data = hashlib.sha256(data.encode()).hexdigest()
            data_int = int(hashed_data, 16) % public_key[0]
            encrypted_data = pow(data_int, public_key[1], public_key[0])
        else:

            hashed_data = hashlib.sha256(data.encode()).hexdigest()
            data_int = int(hashed_data, 16) % public_key[0]
            encrypted_data = pow(data_int, public_key[1], public_key[0])
        return encrypted_data
        

    @staticmethod
    def check_credentials(username, password):
        encrypted_username = Usuario._encrypt_data(Usuario,username)
        encrypted_password = Usuario._encrypt_data(Usuario,password)

        conn = sqlite3.connect(Usuario.db_path)
        cursor = conn.cursor()

        cursor.execute('''SELECT username, password FROM usuarios WHERE username = ?''', (str(encrypted_username),))
        user_data = cursor.fetchone()
        conn.close()

        if user_data is not None and user_data[1] == str(encrypted_password):
            return True
        else:
            return False

    def save_to_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        # Verifica si ya existe un usuario con el mismo username
        cursor.execute('''SELECT * FROM usuarios WHERE username = ?''', (str(self.username),))
        existing_username = cursor.fetchone()
        # Verifica si ya existe un usuario con el mismo email
        cursor.execute('''SELECT * FROM usuarios WHERE email = ?''', (str(self.email),))
        existing_email = cursor.fetchone()
        # Verifica si ya existe un usuario con el mismo uid
        cursor.execute('''SELECT * FROM usuarios WHERE uid = ?''', (str(self.uid),))
        existing_uid = cursor.fetchone()

        if existing_username:
            print("No se pudo crear el usuario. El username ya está en uso.")
            return -1
        elif existing_email:
            print("No se pudo crear el usuario. El email ya está en uso.")
            return -1
        elif existing_uid and self.uid!=16188:
            print(self.uid)
        else:
            # Inserta el usuario en la base de datos
            cursor.execute('''INSERT INTO usuarios (id, name, username, age, email, password, uid) VALUES (?, ?, ?, ?, ?, ?, ?)''',
                           (self.id, str(self.name), str(self.username), self.age, str(self.email), str(self.password), str(self.uid)))
            conn.commit()
            print("Usuario creado con éxito.")
            return 1
            
            

        conn.close()
class Musica():
    db_path = "prueba.db"
    def __init__(self,id_usuario,name,artista,url):
        self.name=name
        self.artista=artista
        self.url=url
        self.id_usuario=id_usuario
        self.id=self._get_next_id()
    def _get_next_id(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Obtiene el último ID asignado, o 0 si no hay usuarios en la base de datos
        cursor.execute('''SELECT MAX(id) FROM musica''')
        last_id = cursor.fetchone()[0]
        conn.close()

        return last_id + 1 if last_id else 1
    def save_data(self):
        self.con=sqlite3.connect(self.db_path)
        self.cursor=self.con.cursor()
        #guardando datos en la base de datos
        
        self.cursor.execute('INSERT INTO musica VALUES (?, ?, ?, ?,?)', (self.id,self.id_usuario, self.name, self.artista, self.url))
      
        self.con.commit()
        self.con.close()
        return True
    @staticmethod
    def getMusic(id):
        conn=sqlite3.connect(Usuario.db_path)
        cursor=conn.cursor()
        cursor.execute('select url from usuarios inner join musica on usuarios.id=musica.id_user where usuarios.id=?',(id,))
        result = cursor.fetchall()
        conn.close()
        return result
        




