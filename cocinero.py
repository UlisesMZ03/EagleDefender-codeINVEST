import numpy as np

def cocinero(tempo, tonos, valencia, energia, bailabilidad, instrumentalidad, acustica, duracion):
    if valencia > 0.7:
        nValencia = 2
    else:
        nValencia = 1
    
    if bailabilidad > 0.7:
        nBailabilidad = np.random.poisson(bailabilidad)
    else:
        nBailabilidad = np.random.exponential(bailabilidad)
    
    valor = (tempo + tonos + valencia * nValencia + energia + bailabilidad * nBailabilidad + (1 - instrumentalidad) + acustica) * (duracion / 1000)
    
    return valor

# Ejemplo de uso
print(1/cocinero(120, 8, 0.8, 0.8, 0.1, 0.5, 0.9, 100000))






# Inicializar las cantidades iniciales de bloques
bloques_madera = 3
bloques_acero = 5
bloques_concreto = 8
velocidad = cocinero(120, 8, 0.8, 0.8, 0.1, 0.5, 0.9, 100000)
# Bucle for para repetir el bloque de código 10 veces
for _ in range(10000):
    # Actualizar la velocidad en cada iteración (puedes ajustar los valores según sea necesario)
    

    # Actualizar la cantidad de bloques en cada iteración
    bloques_madera += (1 /bloques_madera)*velocidad
    bloques_acero += (1 /bloques_acero)/velocidad
    bloques_concreto += (1 /bloques_concreto)/velocidad

    # Imprimir los resultados para cada tipo de bloque
    print("Iteración:", _ + 1)
    print("Cantidad final de bloques de madera:", bloques_madera)
    print("Cantidad final de bloques de acero:", bloques_acero)
    print("Cantidad final de bloques de concreto:", bloques_concreto)
    print("")
