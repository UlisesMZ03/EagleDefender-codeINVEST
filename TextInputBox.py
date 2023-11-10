import pygame
import pygame_gui
from pygame.locals import *
from tkinter import filedialog
pygame.init()
TITLE_FONT = pygame.font.Font("font/KarmaFuture.ttf", 50)
FONT = pygame.font.Font("font/DejaVuSans.ttf", 20)
FONT_SEC = pygame.font.Font("font/DejaVuSans.ttf", 20)
special_symbols = ['!', '@', '#', '$', '%', '&', '*', '+', '-', '=', '_', '?', '<', '>', '.', ',', ':', ';']
class TextInputBox:
    
    def __init__(self, x, y, width, height, color, color2, placeholder="", is_password=False):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.text = ""
        self.height=height
        self.width=width
        self.placeholder = placeholder
        self.active = False
        self.cursor_pos = 0  # Posición del cursor en el texto
        self.is_password = is_password  # Nuevo parámetro para indicar si es una contraseña
        self.real_text = ""  # Variable para almacenar el texto real

    def handle_event(self, event, color, color2):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = True
                # Calcular la posición del cursor en función de la posición del clic
                click_x = event.pos[0] - (self.rect.x + 5)
                
                self.cursor_pos = len(self.text)
                txt_surface = FONT_SEC.render(self.text, True, self.color)
                for i in range(len(self.text)):
                    if txt_surface.get_width() > click_x:
                        self.cursor_pos = i
                        break
                    click_x -= txt_surface.subsurface((i, 0, 1, 1)).get_width()
            else:
                self.active = False
            self.color = color2 if self.active else color
        if event.type == pygame.KEYDOWN:
            if self.active:
                
                if event.key == pygame.K_BACKSPACE and self.cursor_pos > 0 and not self.is_password:
                    self.real_text = self.real_text[:self.cursor_pos - 1] + self.real_text[self.cursor_pos:]
                    self.cursor_pos -= 1
                    
                    self.text = self.real_text
                elif event.key == pygame.K_BACKSPACE and self.cursor_pos > 0 and self.is_password:
                    self.real_text = self.real_text[:self.cursor_pos - 1] + self.real_text[self.cursor_pos:]
                    self.cursor_pos -= 1
                    self.text = u'\u25C6' * len(self.real_text)

                elif event.key == pygame.K_DELETE and self.cursor_pos < len(self.text):
                    self.text = self.text[:self.cursor_pos] + self.text[self.cursor_pos + 1:]
                elif event.key == pygame.K_LEFT and self.cursor_pos > 0:
                    self.cursor_pos -= 1
                elif event.key == pygame.K_RIGHT and self.cursor_pos < len(self.text):
                    self.cursor_pos += 1
                elif event.key == pygame.K_RETURN:
                    self.active = False
                elif self.is_password==True and (event.unicode.isalpha() or event.unicode.isdigit() or event.unicode in special_symbols):  # Permitir solo letras y números
                    # Mostrar el rombo si es una contraseña
                    char = u'\u25C6' if self.is_password else event.unicode
                    self.text = self.text[:self.cursor_pos] + char + self.text[self.cursor_pos:]
                    self.real_text = self.real_text[:self.cursor_pos] + event.unicode + self.real_text[self.cursor_pos:]
                    self.cursor_pos += 1
                elif not self.is_password and (event.unicode.isalpha() or event.unicode.isdigit() or event.unicode.isspace() or event.key == pygame.K_TAB or event.unicode in special_symbols):
                    if event.key == pygame.K_TAB:
                        # Ignorar la tecla Tab
                        pass
                    else:
                        char = event.unicode
                        self.text = self.text[:self.cursor_pos] + char + self.text[self.cursor_pos:]
                        self.real_text = self.real_text[:self.cursor_pos] + char + self.real_text[self.cursor_pos:]
                        self.cursor_pos += 1
    def get_text(self):
        """
        Obtiene el texto real del TextInputBox, incluso si is_password es True.
        """
        return self.real_text
    def update(self):
        txt_surface = FONT_SEC.render(self.text, True, self.color)
        # Establece el ancho mínimo del campo de texto
        min_width = self.width
        self.rect.w = max(min_width, txt_surface.get_width() + 10)
    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect, 2)
        
        txt_surface = FONT_SEC.render(self.text if self.text else self.placeholder, True, self.color)
        surface.blit(txt_surface, (self.rect.x + 5, self.rect.y + 5))
        if self.active and self.text:  # Mostrar el cursor solo si el cuadro de texto está activo y tiene texto
            cursor_x = self.rect.x + 5 + FONT_SEC.render(self.text[:self.cursor_pos], True, self.color).get_width()
            pygame.draw.line(surface, self.color, (cursor_x, self.rect.y + 5),
                            (cursor_x, self.rect.y + 5 + txt_surface.get_height()), 2)
            