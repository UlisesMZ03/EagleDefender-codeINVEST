import pygame
class screenEmer():
    def __init__(self,width,height,screen):
        self.width=width
        self.heigth=height
        self.surface=pygame.Surface((width,height))
        self.surface.fill((255,255,255))
        self.rect=self.surface.get_rect()
        self.rect.center=(width//2,height//2)
        self.screen=screen
    def surfaceEmer(self):
        return self.surface
    def show(self,x,y):
        self.screen.blit(self.surface,(x,y))
    def hidden(self):
        self.rect.topleft=(-self.width,-self.heigth)
               
        



