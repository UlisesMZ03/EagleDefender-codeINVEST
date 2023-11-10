import re


def validate_UID_device(UID_device):
    if not UID_device:
        return False
    
    # Verificar si la dirección UID consiste en grupos de enteros separados por puntos
    UID_parts = UID_device.split('.')
    if len(UID_parts) != 4:
        return False
    
    for part in UID_parts:
        if not part.isdigit() or not 0 <= int(part) <= 255:
            return False
    
    return True

def validate_email(email):
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(email_regex, email)

def validate_password(password):
    password_regex = r'^(?=.*[A-Z])(?=.*[!@#$%^&*()_+{}\[\]:;<>,.?~\\-]).{8,}$'
    return re.match(password_regex, password)

def validate_username(username):
    banned_words = ['badword1', 'badword2', 'badword3']

    # Verificar si el nombre de usuario contiene espacios
    if ' ' in username:
        return 2
    # Verificar si el nombre de usuario contiene palabras prohibidas
    if any(word in username.lower() for word in banned_words):
        return 1
    # Si no hay espacios y no contiene palabras prohibidas, el nombre de usuario es válido
    return True

def validate_age(age):
    return age.isdigit()
