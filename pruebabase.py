# Clave pública
public_key = (43931, 12637)

# Clave privada
private_key = (43931, 32869)

# Función para cifrar un mensaje
def encrypt(message, public_key):
    n, e = public_key
    encrypted_message = [pow(ord(char), e, n) for char in message]
    return encrypted_message

# Función para descifrar un mensaje
def decrypt(encrypted_message, private_key):
    n, d = private_key
    decrypted_message = ''.join([chr(pow(char, d, n)) for char in encrypted_message])
    return decrypted_message
message = "Hola, mundo!"

# Cifrar el mensaje con la clave pública
encrypted_message = encrypt(message, public_key)
print(type(encrypted_message))
print("Mensaje cifrado:", encrypted_message)

# Descifrar el mensaje con la clave privada
decrypted_message = decrypt([19872, 10269, 22675, 60, 10469, 32237, 14784, 20056, 5881, 10269, 60, 32237, 28121, 14546, 3620, 5881], private_key)
print("Mensaje descifrado:", decrypted_message)
a=[19872, 10269, 22675, 60, 10469, 32237, 14784, 20056, 5881, 10269, 60, 32237, 28121, 14546, 3620, 5881]
for i in a:
    print(type(i),i)