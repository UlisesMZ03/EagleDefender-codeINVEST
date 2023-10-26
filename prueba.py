import pygame
import sys

# Definir algunos colores
NEGRO = (0, 0, 0)

# Clase para representar los bloques
class Bloque(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.dragging = False
        self.original_image = image

    def update(self):
        if self.dragging:
            self.rect.center = pygame.mouse.get_pos()

# Clase para manejar colisiones y el grupo de sprites
class Colision:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Colision de Bloques")
        self.clock = pygame.time.Clock()
        self.all_sprites = pygame.sprite.Group()

    def run(self):
        running = True

        # Cargar imágenes de bloques
        bloque1_image = pygame.image.load('images/game/powers/fire.png')
        bloque2_image = pygame.image.load('images/game/powers/fire.png')

        # Crear instancias de bloques y agregarlos al grupo
        bloque1 = Bloque(100, 100, bloque1_image)
        bloque2 = Bloque(200, 200, bloque2_image)
        self.all_sprites.add(bloque1, bloque2)

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for bloque in self.all_sprites:
                        if bloque.rect.collidepoint(event.pos):
                            bloque.dragging = True
                elif event.type == pygame.MOUSEBUTTONUP:
                    for bloque in self.all_sprites:
                        bloque.dragging = False

            self.all_sprites.update()

            # Verificar colisiones y aplicar el filtro rojo transparente
            for bloque1 in self.all_sprites:
                for bloque2 in self.all_sprites:
                    if bloque1 != bloque2 and bloque1.rect.colliderect(bloque2.rect):
                        bloque1.image = self.apply_red_filter(bloque1.original_image)

            self.screen.fill(NEGRO)
            self.all_sprites.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()

    def apply_red_filter(self, image):
        red_filtered = image.copy()
        red_filtered.fill((255, 0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        return red_filtered

if __name__ == "__main__":
    juego = Colision()
    juego.run()
