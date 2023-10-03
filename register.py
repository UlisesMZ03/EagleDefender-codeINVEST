import customtkinter as ctk
import tkinter.messagebox as tkmb
from usuarios import Usuario
import serial
import re
import json
import os
import threading
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.geometry("800x800")
app.title("Eagle Defender")




# Función para validar el correo electrónico
def is_valid_email(email):
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(email_regex, email) is not None

# Función para validar la contraseña
def is_valid_password(password):
    password_regex = r'^(?=.*[A-Z])(?=.*[!@#$%^&*()_+{}\[\]:;<>,.?~\\-]).{8,}$'
    return re.match(password_regex, password) is not None

# Función para validar el nombre de usuario
def is_valid_username(username):
    # Aquí puedes agregar tu propia lista de palabras soeces
    banned_words = ['badword1', 'badword2', 'badword3']
    return all(word not in username.lower() for word in banned_words)

# Función para validar la edad
def is_valid_age(age):
    return age.isdigit()

# Función para el botón de registro
def register():
    name = name_entry.get()
    email = email_entry.get()
    age = age_entry.get()
    username = user_entry.get()
    password = user_pass.get()
    confirm_password = confirm_pass_entry.get()

    if username != "" and password == confirm_password and is_valid_email(email) and is_valid_password(password) and is_valid_username(username) and is_valid_age(age):
        
        user = Usuario(name,username,age,email,ip_device,password)
        print(user)

        # Convertir el objeto de usuario a un diccionario
        user_dict = {
            "Name": name,
            "Username": username,
            "Email": email,
            "Age": age,
            "Ip": ip_device,
            "Password": password
        }
        
                # Verificar si el archivo usuarios.json existe
        if not os.path.exists("usuarios.json"):
            # Si no existe, crear un nuevo archivo y escribir el primer usuario
            with open("usuarios.json", "w") as json_file:
                json.dump([user_dict], json_file, indent=4)
        else:
            # Si el archivo existe, abrirlo y agregar el nuevo usuario al final
            with open("usuarios.json", "r") as json_file:
                
                # Cargar datos existentes del archivo
                users = json.load(json_file)
            # Agregar el nuevo usuario a la lista existente
            users.append(user_dict)
            # Escribir la lista actualizada al archivo
            with open("usuarios.json", "w") as json_file:
                json.dump(users, json_file, indent=4)

    elif password != confirm_password:
        tkmb.showwarning(title='Password Mismatch', message='Password and confirm password do not match')
    elif not is_valid_email(email):
        tkmb.showwarning(title='Invalid Email', message='Please enter a valid email address')
    elif not is_valid_password(password):
        tkmb.showwarning(title='Invalid Password', message='Password must be at least 8 characters long with at least one uppercase letter and one special symbol')
    elif not is_valid_username(username):
        tkmb.showwarning(title='Invalid Username', message='Username contains prohibited words')
    elif not is_valid_age(age):
        tkmb.showwarning(title='Invalid Age', message='Age must be a number')
    else:
        tkmb.showerror(title="Register Failed", message="Invalid Username and password")


server_socket = None



# Variable de bandera para controlar la ejecución del hilo
hilo_en_ejecucion = True

def receive_data_from_uart():
    def uart_thread_function():
        SERIAL_PORT = '/dev/ttyACM0'  # Reemplaza esto con el puerto serial al que está conectada la Raspberry Pi Pico en tu PC
        BAUD_RATE = 9600
        tkmb.showinfo("Registrar dispositivo", "Por favor, conéctese a la red WiFi llamada EagleDefender desde su celular o dispositivo electrónico, seguidamente abra la siguiente dirección: http://192.168.4.1.")
       
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE)
        global hilo_en_ejecucion
        while hilo_en_ejecucion:
            data_received = ser.readline().decode().strip()
            print("Datos recibidos desde Raspberry Pi Pico:", data_received)

            global ip_device
            ip_device = data_received
            break
        # El hilo se detendrá cuando salga del bucle while
        
    # Creamos un hilo para ejecutar uart_thread_function()
    uart_thread = threading.Thread(target=uart_thread_function)
    
    # Iniciamos el hilo
    uart_thread.start()
 
        





font_size = 25

font = "Roboto"

label = ctk.CTkLabel(app, text="Register", font=("Arial", font_size))
label.pack(pady=0)

frame = ctk.CTkFrame(master=app)
frame.pack(pady=10, padx=10, fill='both', expand=True)
email_entry = ctk.CTkEntry(master=frame, placeholder_text="Email", font=(font, font_size))
email_entry.pack(pady=12, padx=10)

age_entry = ctk.CTkEntry(master=frame, placeholder_text="Age", font=(font, font_size))
age_entry.pack(pady=12, padx=10)

user_entry = ctk.CTkEntry(master=frame, placeholder_text="Username", font=(font, font_size))
user_entry.pack(pady=12, padx=10)

user_pass = ctk.CTkEntry(master=frame, placeholder_text="Password", show="*", font=(font, font_size))
user_pass.pack(pady=12, padx=10)

confirm_pass_entry = ctk.CTkEntry(master=frame, placeholder_text="Confirm Password", show="*", font=(font, font_size))
confirm_pass_entry.pack(pady=12, padx=10)

ip_label = ctk.CTkLabel(app, text="", font=("Arial", font_size))
ip_label.pack(pady=10)


connect_button = ctk.CTkButton(master=frame, text='Registrar celular', command=receive_data_from_uart, font=(font, font_size))
name_entry = ctk.CTkEntry(master=frame, placeholder_text="Name", font=(font, font_size))
name_entry.pack(pady=12, padx=10)
connect_button.pack(pady=12, padx=10)

button = ctk.CTkButton(master=frame, text='Register', command=register, font=(font, font_size))
button.pack(pady=12, padx=10)

checkbox = ctk.CTkCheckBox(master=frame, text='Remember Me', font=(font, font_size))
checkbox.pack(pady=12, padx=10)

app.mainloop()
