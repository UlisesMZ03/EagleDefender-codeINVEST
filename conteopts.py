from music import duration_sec

from music import duration_sec2

def calcular_puntaje_atacante(bloques_destruidos, tiempo_ataque):
    if tiempo_ataque == 0:
        return 0  # división por cero
    media_armonica = 2 / ((1 / bloques_destruidos) + (1 / tiempo_ataque))
    return media_armonica

def calcular_puntaje_defensor(tiempo_defensa, bloques_restantes):
    if tiempo_defensa == 0:
        return 0  #división por cero
    media_armonica = 2 / ((1 / tiempo_defensa) + (1 / bloques_restantes))
    return media_armonica

def determinar_ganador(puntaje_atacante, puntaje_defensor):
    if puntaje_atacante > puntaje_defensor:
        return "Atacante"
    elif puntaje_defensor > puntaje_atacante:
        return "Defensor"
    else:
        return "Empate"

# Ejemplo de uso


bloques_destruidos_atacante = 10
tiempo_ataque_atacante = duration_sec
tiempo_defensa_defensor = duration_sec2
bloques_restantes_defensor = 20

print (duration_sec2, duration_sec)
puntaje_atacante = calcular_puntaje_atacante(bloques_destruidos_atacante, tiempo_ataque_atacante)
puntaje_defensor = calcular_puntaje_defensor(tiempo_defensa_defensor, bloques_restantes_defensor)

ganador = determinar_ganador(puntaje_atacante, puntaje_defensor)

print("Puntaje del Atacante:", puntaje_atacante)
print("Puntaje del Defensor:", puntaje_defensor)
print("Ganador:", ganador)
