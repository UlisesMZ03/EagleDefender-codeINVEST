def encrypt(message, public_key):
    n, e = public_key
    encrypted_message = [pow(ord(char), e, n) for char in message]
    return encrypted_message

def decrypt(encrypted_message, private_key):
    n, d = private_key
    decrypted_message = ''.join([chr(pow(char, d, n)) for char in encrypted_message])
    return decrypted_message

public_key = (43931, 12637)
private_key = (43931, 32869)

# Mensaje que deseas encriptar
mensaje_original = ""

# Encriptar el mensaje usando la clave pública
mensaje_encriptado = encrypt(mensaje_original, public_key)
# Convertir el mensaje cifrado a una cadena sin comas
mensaje_encriptado_string = ''.join(map(str, mensaje_encriptado))

print("Mensaje encriptado:", mensaje_encriptado)

# Desencriptar el mensaje usando la clave privada
mensaje_desencriptado = decrypt([10181, 767, 19872, 28717, 20056, 40760, 13935, 3309, 32237, 34239, 21083], private_key)
print("Mensaje desencriptado:", mensaje_desencriptado)
