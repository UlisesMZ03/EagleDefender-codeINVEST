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
def login():
    # Obtiene los datos ingresados por el usuario
    username = user_entry.get()
    password = user_pass.get()
    
    # Abre el archivo JSON y carga los datos en una lista de diccionarios
    with open("usuarios.json", "r") as json_file:
        data = json.load(json_file)
        
    # Busca el usuario en la lista de usuarios registrados
    for usuario_data in data:
        if usuario_data["Username"] == username and usuario_data["Password"] == password:
            tkmb.showinfo("Login Exitoso", "¡Bienvenido, {}!".format(username))
            # Aquí puedes agregar código para redirigir a la siguiente pantalla o realizar otras acciones
            break
    else:
        tkmb.showerror("Error de Login", "Nombre de usuario o contraseña incorrectos")

    







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
            verificar_ip()

            break
        # El hilo se detendrá cuando salga del bucle while
        
    # Creamos un hilo para ejecutar uart_thread_function()
    uart_thread = threading.Thread(target=uart_thread_function)
    
    # Iniciamos el hilo
    uart_thread.start()
 
        
def verificar_ip():
    # Asegúrate de que ip_device tenga un valor
    if not ip_device:
        tkmb.showerror("Error", "No se pudo obtener la dirección IP del dispositivo")
        return
    
    # Abre el archivo JSON y carga los datos en una lista de diccionarios
    with open("usuarios.json", "r") as json_file:
        data = json.load(json_file)
        
    # Busca la dirección IP en la lista de usuarios registrados
    for usuario_data in data:
        if usuario_data["Ip"] == ip_device:
            tkmb.showinfo("Dispositivo Encontrado", "La dirección IP está asociada al usuario: {}".format(usuario_data["Name"]))
            # Llena automáticamente el campo de texto con el nombre de usuario
            user_entry.insert(0, usuario_data["Username"])
            user_pass.insert(0, usuario_data["Password"])
            login()
            return
        
    tkmb.showerror("Error", "La dirección IP no está asociada a ningún usuario registrado")





font_size = 25

font = "Roboto"

label = ctk.CTkLabel(app, text="login", font=("Arial", font_size))
label.pack(pady=0)

frame = ctk.CTkFrame(master=app)
frame.pack(pady=10, padx=10, fill='both', expand=True)



user_entry = ctk.CTkEntry(master=frame, placeholder_text="Username", font=(font, font_size))
user_entry.pack(pady=12, padx=10)

user_pass = ctk.CTkEntry(master=frame, placeholder_text="Password", show="*", font=(font, font_size))
user_pass.pack(pady=12, padx=10)




checkbox = ctk.CTkCheckBox(master=frame, text='Remember Me', font=(font, font_size))
checkbox.pack(pady=12, padx=10)


connect_button = ctk.CTkButton(master=frame, text='Phone login', command=receive_data_from_uart, font=(font, font_size))
connect_button.pack(pady=12, padx=10)
button = ctk.CTkButton(master=frame, text='login', command=login, font=(font, font_size))
button.pack(pady=12, padx=10)

app.mainloop()
