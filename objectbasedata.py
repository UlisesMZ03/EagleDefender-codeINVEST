import sqlite3
import hashlib
# Llave pública proporcionada
public_key = (43931, 12637)
private_key = (43931,32869)

class Usuario:
    db_path = "database.db"
    def __init__(self, name, username, age, email, password, uid):
        self.name = self._encrypt_data(name)
        self.username = self._encrypt_data(username)
        self.age = age

        self.email = self._encrypt_data(email)
        # Encripta la contraseña al crear una instancia de Usuario
        self.password = self._encrypt_data(password)
        self.uid = uid
        self.id = self._get_next_id()
    @staticmethod
    def _encrypt_data(message):
        n, e = public_key
        encrypted_message = [pow(ord(char), e, n) for char in message]
        return encrypted_message
    @staticmethod
    def _decrypt_data(encrypted_message):
        n, d = private_key
        cleaned_message = encrypted_message.replace("[", "").replace("]", "").replace("'", "")
        decrypted_message = ''.join([chr(pow(int(char), d, n)) for char in cleaned_message.split(',')])
        return decrypted_message

    @staticmethod
    def decrypt(encrypted_message):
        n, d = private_key
        decrypted_message = ''.join([chr(pow(char, d, n)) for char in encrypted_message])
        return decrypted_message
    def _get_next_id(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Obtiene el último ID asignado, o 0 si no hay usuarios en la base de datos
        cursor.execute('''SELECT MAX(id) FROM usuarios''')
        last_id = cursor.fetchone()[0]
        conn.close()

        return last_id + 1 if last_id else 1

    @staticmethod
    def getID(username):
        conn = sqlite3.connect(Usuario.db_path)
        cursor = conn.cursor()
        encrypt_username = Usuario._encrypt_data(username)
        cursor.execute("SELECT id FROM usuarios WHERE username=?", (str(encrypt_username),))
        
        # Obtén el resultado de la consultausername
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
        encrypted_username = Usuario._encrypt_data(username)
        encrypted_password = Usuario._encrypt_data(password)

        conn = sqlite3.connect(Usuario.db_path)
        cursor = conn.cursor()

        cursor.execute('''SELECT username, password FROM usuarios WHERE username = ?''', (str(encrypted_username),))
        user_data = cursor.fetchone()
        conn.close()

        if user_data is not None and user_data[1] == str(encrypted_password):
            return True
        else:
            return False

    @staticmethod
    def get_user_by_uid(uid):
        user_id = Usuario.get_user_id_by_uid(uid)  # Obtiene el ID del usuario por su UID

        if user_id is not None:
            conn = sqlite3.connect(Usuario.db_path)
            cursor = conn.cursor()

            # Realiza una consulta para obtener los datos del usuario con el ID obtenido
            cursor.execute('''SELECT * FROM usuarios WHERE id = ?''', (user_id,))
            user_data = cursor.fetchone()
            conn.close()

            if user_data is not None:
                print(user_data)
                # Desencripta los datos antes de devolverlos
                decrypted_user_data = {
                    'id': user_data[0],
                    'name': Usuario._decrypt_data(user_data[1]),
                    'username': Usuario._decrypt_data(user_data[2]),
                    'age': user_data[3],
                    'email': Usuario._decrypt_data(user_data[4]),
                    'password': Usuario._decrypt_data(user_data[5]),
                    'uid': user_data[6]
                }
                return decrypted_user_data
        return None  # Si no se encuent
    @staticmethod
    def get_user_id_by_uid(uid):
        conn = sqlite3.connect(Usuario.db_path)
        cursor = conn.cursor()

        cursor.execute('''SELECT id FROM usuarios WHERE uid = ?''', (str(uid),))
        user_id = cursor.fetchone()

        conn.close()
        
        if user_id is not None:
            return (user_id[0])  # Devuelve el ID del usuario
        else:
            return None  # Si no se encuentra ningún usuario con el UID dado, devuelve None
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
            return 1
        elif existing_email:
            return 2
        elif existing_uid and self.uid!="":
            return 3
        else:
            
            # Inserta el usuario en la base de datos
            cursor.execute('''INSERT INTO usuarios (id, name, username, age, email, password, uid) VALUES (?, ?, ?, ?, ?, ?, ?)''',
                           (self.id, str(self.name), str(self.username), self.age, str(self.email), str(self.password), str(self.uid)))
            conn.commit()
            print("Usuario creado con éxito.")
            
        
        conn.close()

    @staticmethod
    def getName(id):
        conn=sqlite3.connect(Usuario.db_path)
        cursor=conn.cursor()
        cursor.execute('select name from usuarios where id=?',(id,))
        result = cursor.fetchall() 
        result=eval(result[0][0])
        result=Usuario.decrypt(result)
        conn.close()
        return result
    @staticmethod
    def getAge(id):
        conn=sqlite3.connect(Usuario.db_path)
        cursor=conn.cursor()
        cursor.execute('select age from usuarios where id=?',(id,))
        result = cursor.fetchall()
        result=result[0][0]
        conn.close()
        return result
    @staticmethod
    def getUsername(id):
        conn=sqlite3.connect(Usuario.db_path)
        cursor=conn.cursor()
        cursor.execute('select username from usuarios where id=?',(id,))
        result = cursor.fetchall()
        result=eval(result[0][0])
        result=Usuario.decrypt(result)
        conn.close()
        return result
    @staticmethod
    def getEmail(id):
        conn=sqlite3.connect(Usuario.db_path)
        cursor=conn.cursor()
        cursor.execute('select email from usuarios where usuarios.id=?',(id,))
        result = cursor.fetchall()
        result=eval(result[0][0])
        result=Usuario.decrypt(result)
        conn.close()
        return result
    @staticmethod
    def getPassword(id):
        conn=sqlite3.connect(Usuario.db_path)
        cursor=conn.cursor()
        cursor.execute('select password from usuarios where usuarios.id=?',(id,))
        result = cursor.fetchall()
        result=eval(result[0][0])
        result=Usuario.decrypt(result)
        conn.close()
        return result
    def updateEmail(id,newValue):
        conn=sqlite3.connect(Usuario.db_path)
        cursor=conn.cursor()
        cursor.execute('upadate usuarios set email=? where usuarios.id=?',(newValue,id))
        conn.commit()
        conn.close()
        return True
    def updateName(id,newValue):
        conn=sqlite3.connect(Usuario.db_path)
        cursor=conn.cursor()
        cursor.execute('upadate usuarios set email=? where usuarios.id=?',(newValue,id))
        conn.commit()
        conn.close()
        return True
    def updateUsername(id,newValue):
        conn=sqlite3.connect(Usuario.db_path)
        cursor=conn.cursor()
        cursor.execute('upadate usuarios set username=? where usuarios.id=?',(newValue,id))
        conn.commit()
        conn.close()
        return True
    def updatePassword(id,newValue):
        conn=sqlite3.connect(Usuario.db_path)
        cursor=conn.cursor()
        cursor.execute('upadate usuarios set password=? where usuarios.id=?',(newValue,id))
        conn.commit()
        conn.close()
        return True
    def updateEge(id,newValue):
        conn=sqlite3.connect(Usuario.db_path)
        cursor=conn.cursor()
        cursor.execute('upadate usuarios set ege=? where usuarios.id=?',(newValue,id))
        conn.commit()
        conn.close()
        return True
 
class Musica():
    db_path = "database.db"
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
    @staticmethod
    def NameArtist(id):
        conn=sqlite3.connect(Usuario.db_path)
        cursor=conn.cursor()
        cursor.execute('select musica.name, artista from usuarios inner join musica on usuarios.id=musica.id_user where usuarios.id=?',(id,))
        result = cursor.fetchall()
        conn.close()
        return result
        




class Score():
    db_path = "database.db"
    def __init__(self,id_user,puntaje) -> None:
        self.id_user=id_user
        self.puntaje=puntaje
        self.id=self._get_next_id()


    def _get_next_id(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Obtiene el último ID asignado, o 0 si no hay usuarios en la base de datos
        cursor.execute('''SELECT MAX(id) FROM puntajes''')
        last_id = cursor.fetchone()[0]
        conn.close()

        return last_id + 1 if last_id else 1
    def save_data(self):
        self.con=sqlite3.connect(self.db_path)
        self.cursor=self.con.cursor()
        #guardando datos en la base de datos
        
        self.cursor.execute('INSERT INTO puntajes VALUES (?, ?, ?)', (self.id,self.id_user, self.puntaje))
      
        self.con.commit()
        self.con.close()
        return True
    @staticmethod
    def get_top_scores():
        conn = sqlite3.connect(Score.db_path)
        cursor = conn.cursor()

        # Obtiene los 10 mejores puntajes ordenados de mayor a menor
        cursor.execute('''SELECT id_user, puntos FROM puntajes ORDER BY puntos DESC LIMIT 10''')
        top_scores = cursor.fetchall()

        conn.close()
        return top_scores
    

