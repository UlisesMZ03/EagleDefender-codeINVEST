import sqlite3
import hashlib

# Llave pública proporcionada
public_key = (19303, 13595)

class Usuario:
    db_path = "usuarios.db"

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

        # Crea la tabla si no existe
        cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, username TEXT, age INTEGER, email TEXT, password TEXT, uid TEXT)''')
        conn.commit()

        # Obtiene el último ID asignado, o 0 si no hay usuarios en la base de datos
        cursor.execute('''SELECT MAX(id) FROM usuarios''')
        last_id = cursor.fetchone()[0]
        conn.close()

        return last_id + 1 if last_id else 1

    def _encrypt_data(self, data):
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
        elif existing_email:
            print("No se pudo crear el usuario. El email ya está en uso.")
        elif existing_uid:
            print("No se pudo crear el usuario. El UID ya está en uso.")
        else:
            # Inserta el usuario en la base de datos
            cursor.execute('''INSERT INTO usuarios (id, name, username, age, email, password, uid) VALUES (?, ?, ?, ?, ?, ?, ?)''',
                           (self.id, str(self.name), str(self.username), self.age, str(self.email), str(self.password), str(self.uid)))
            conn.commit()
            print("Usuario creado con éxito.")

        conn.close()


