import customtkinter as ctk
import tkinter.messagebox as tkmb

import re
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
        new_window = ctk.CTkToplevel(app)
        new_window.title("Register Info")
        new_window.geometry("400x300")
        ctk.CTkLabel(new_window, text=f"Name: {name}").pack()
        ctk.CTkLabel(new_window, text=f"Email: {email}").pack()
        ctk.CTkLabel(new_window, text=f"Age: {age}").pack()
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

# Resto del código permanece igual

font_size = 25
font = "Roboto"

label = ctk.CTkLabel(app, text="Register", font=("Arial", font_size))
label.pack(pady=0)

frame = ctk.CTkFrame(master=app)
frame.pack(pady=10, padx=10, fill='both', expand=True)

name_entry = ctk.CTkEntry(master=frame, placeholder_text="Name", font=(font, font_size))
name_entry.pack(pady=12, padx=10)

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

button = ctk.CTkButton(master=frame, text='Register', command=register, font=(font, font_size))
button.pack(pady=12, padx=10)

checkbox = ctk.CTkCheckBox(master=frame, text='Remember Me', font=(font, font_size))
checkbox.pack(pady=12, padx=10)

app.mainloop()
