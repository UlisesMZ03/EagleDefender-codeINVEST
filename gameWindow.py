import pygame
import sys

pygame.init()

# Definicion de variables
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Mi juego Pygame")

# definicion de colores
gray = (40, 50, 60)
white = (225, 250, 250)
green = (50, 200, 150)
red = (250, 50, 100)
blue = (50, 150, 200)
orange = (250, 140, 20)
black = (0, 0, 0)
colors = {"U": gray, "F": blue, "H": orange, "S": black}

# configuracion ventanas
square_size = 40
X_margin = square_size * 4
Y_margin = square_size
height = square_size * 10 * 2 + X_margin
width = square_size * 10 * 2 + Y_margin
celda_Tamanno = 60

font = pygame.font.Font(None, 36)
# seteo de dimensiones de ventanas
main_window = pygame.display.set_mode((height, width))

main_window = True
CANVAS_WIDTH, CANVAS_HEIGHT = 900, 770

# Matriz para almacenar valores de cuadros
matrix = [[0 for _ in range(CANVAS_WIDTH // celda_Tamanno)] for _ in range(CANVAS_HEIGHT // celda_Tamanno)]

# Matriz para rastrear los golpes en cada celda
block_hits = [[0 for _ in range(CANVAS_WIDTH // celda_Tamanno)] for _ in range(CANVAS_HEIGHT // celda_Tamanno)]

# Crear un objeto Surface para el lienzo
canvas = pygame.Surface((CANVAS_WIDTH, CANVAS_HEIGHT))

# Variable para controlar si estamos en modo de edición o visualización
editing_mode = True

# Metodos para escritura y lectura en base de datos (almacenada localmente, falta aun implementar cifrado)
txt = "C:/Users/eemma/OneDrive/Escritorio/data.txt"  # cuando haya repositorio cambiar por ruta relativa, sino mucho enredo

# Variables Sprite caminado
# Carga de las imágenes de caminar
scale_factor = 3
walk_images = [pygame.image.load(f"C://Users//eemma//OneDrive//Escritorio//{i}.png") for i in range(1, 8)]
for i in range(len(walk_images)):
    walk_images[i] = pygame.transform.scale(walk_images[i], (int(walk_images[i].get_width() * scale_factor), int(walk_images[i].get_height() * scale_factor)))
# Configuración de la animación de caminar
walk_index = 0
walk_speed = 3  # Velocidad de cambio de imagen (ajusta según sea necesario)
walk_rect = walk_images[0].get_rect()
walk_rect.topleft = (100, 300)  # Posición inicial del sprite

# Carga de la imagen de la bala
bullet_image = pygame.image.load("C://Users//eemma//OneDrive//Escritorio//bullet.png")

# Escala la imagen de la bala para hacerla más pequeña
scale_factor_bullet = 0.05  # Ajusta este valor según el tamaño deseado
bullet_image = pygame.transform.scale(bullet_image, (int(bullet_image.get_width() * scale_factor_bullet), int(bullet_image.get_height() * scale_factor_bullet)))

# Configuración de la posición de la bala (inicialmente fuera de la pantalla)
bullet_rect = bullet_image.get_rect()
bullet_rect.topleft = (-bullet_rect.width, -bullet_rect.height)

# Configuración de la velocidad del personaje
player_speed = 7  # Velocidad de movimiento del personaje

clock = pygame.time.Clock()

# Función para escribir en .txt. nota aun falta implementar cifrado, de lo contrario no tiene sentido
def open_and_read():
    global lista_de_escrituras
    arc = open(txt, "r")
    lista_de_escrituras = arc.readlines()
    arc.close()
    lista_de_escrituras.sort()
    return lista_de_escrituras

def write(data):
    file = open(txt, "a")
    file.write(data + "\n")
    file.close()

nuevo_ancho = 40  # Cambia esto al ancho deseado
nuevo_alto = 40 # Cambia esto al alto deseado
# Redimensiona la imagen a las nuevas dimensiones
img1 = pygame.image.load('C://Users//eemma//OneDrive//Escritorio//IMG.jpg')
ladrillo_pequena = pygame.transform.scale(img1, (nuevo_ancho, nuevo_alto))

brick_images = [ladrillo_pequena]
# Define las nuevas dimensiones deseadas (ancho y alto)

# Función para dibujar la matriz sobre el canvas
def draw_matrix(surface):
    for row in range(len(matrix)):
        for col in range(len(matrix[0])):
            cell_value = matrix[row][col]
            if cell_value == 1 and block_hits[row][col] < 2:
                # Dibuja la imagen de ladrillo en lugar de un cuadro blanco
                surface.blit(brick_images[0], (col * celda_Tamanno, row * celda_Tamanno))

# Función para guardar la matriz en un archivo de texto
def save_matrix(filename):
    with open(filename, 'w') as file:
        for row in matrix:
            file.write(' '.join(map(str, row)) + '\n')

# Función para cargar la matriz desde un archivo de texto
def load_matrix(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
        for i, line in enumerate(lines):
            matrix[i] = list(map(int, line.strip().split()))

bloques_jugador= 30
# Bucle principal (Main window)
while main_window:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                # Guardar la matriz en un archivo
                save_matrix(txt)
                print("Matriz guardada en 'matrix.txt'")
            elif event.key == pygame.K_l and pygame.key.get_mods() & pygame.KMOD_CTRL:
                # Cargar la matriz desde un archivo
                load_matrix(txt)
                print("Matriz cargada desde 'matrix.txt'")
                
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if bloques_jugador != 0:
                if event.button == 1:
                    x, y = event.pos
                    x -= 40
                    y -= 40
                    # Calcular la fila y columna en la matriz
                    row = y // celda_Tamanno
                    col = x // celda_Tamanno
                    if (
                        0 <= row < len(matrix)
                        and 0 <= col < len(matrix[0])
                        and matrix[row][col] == 0  # Verificar si la celda está vacía
                    ):
                        # Verificar si las celdas adyacentes están vacías (espacio de 40 píxeles)
                        adjacent_cells = [
                            (row - 1, col),
                            (row + 1, col),
                            (row, col - 1),
                            (row, col + 1),
                        ]
                        if all(
                            0 <= adj_row < len(matrix)
                            and 0 <= adj_col < len(matrix[0])
                            and matrix[adj_row][adj_col] == 0
                            for adj_row, adj_col in adjacent_cells
                        ):
                            # Cambiar el valor de la celda en la matriz
                            matrix[row][col] = 1
                            block_hits[row][col] = 0  # Reiniciar los golpes
                            bloques_jugador -= 1  # Reducir el contador de bloques
                        else:
                            print("No se puede colocar un bloque aquí debido al espacio requerido.")
                    else:
                        print("No se puede colocar un bloque aquí")
                else:
                    print("No quedan más bloques")

    # Manejo de eventos de teclado para mover al personaje
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        walk_rect.y -= player_speed
    if keys[pygame.K_s]:
        walk_rect.y += player_speed
    if keys[pygame.K_a]:
        walk_rect.x -= player_speed
    if keys[pygame.K_d]:
        walk_rect.x += player_speed

    # Actualización de la animación de caminar
    walk_index += 1
    if walk_index >= len(walk_images):
        walk_index = 0

   
    # Movimiento de la bala si está disparando
    if bullet_rect.x > 0:
        # Dar margen a la bala antes de verificar la colisión con los bloques
        bullet_rect_with_margin = bullet_rect.inflate(40, 40)
        col = bullet_rect_with_margin.centerx // celda_Tamanno
        row = bullet_rect_with_margin.centery // celda_Tamanno

        # Verificar colisión con los bloques antes de mover la bala
        if 0 <= row < len(matrix) and 0 <= col < len(matrix[0]) and matrix[row][col] == 1:
            block_hits[row][col] += 1
            if block_hits[row][col] == 2:
                # Si el bloque ha sido golpeado dos veces, destrúyelo
                matrix[row][col] = 0
                block_hits[row][col] = 0
                # No muevas la bala aquí
        else:
            # Mueve la bala solo si no hay colisión en la fila actual
            bullet_rect.x += 40

        if bullet_rect.right > 900:
            # Reiniciar la posición de la bala si sale de la pantalla
            bullet_rect.topleft = (-bullet_rect.width, -bullet_rect.height)

    # Disparar con la tecla de espacio
    if keys[pygame.K_SPACE]:
        if bullet_rect.x < 0:
            bullet_rect.topleft = (walk_rect.right, walk_rect.centery - bullet_rect.height // 2)

    # Llenar la pantalla principal con blanco
    screen.fill(white)

    # Dibujar el lienzo en la ventana principal
    canvas.fill(black)  # Limpiar el lienzo con blanco
    canvas.blit(walk_images[walk_index], walk_rect)
    canvas.blit(bullet_image, bullet_rect)
    draw_matrix(canvas)  # Dibujar la matriz en el lienzo
    screen.blit(canvas, (30, 30))  # Ajustar la posición del lienzo en la ventana principal

    clock.tick(60)  # Limitar el número de fotogramas por segundo
    pygame.display.flip()

pygame.quit()
sys.exit()
 