class Usuario:
    def __init__(self, nombre, edad, correo, ip, contrasena):
        self.nombre = nombre
        self.edad = edad
        self.correo = correo
        self.ip = ip
        self.contrasena = contrasena

    def __str__(self):
        return f"Nombre: {self.nombre}, Edad: {self.edad}, Correo: {self.correo}, IP: {self.ip}, Contraseña: {self.contrasena}"
