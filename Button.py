import pygame
class Button:
    def __init__(self,text,width,height,pos,elevation,color):
        self.pressed = False
        self.elevation = elevation
        self.dynamic_elecation = elevation
        self.original_y_pos = pos[1]
        self.width = width
        self.height = height
		#Core attributes 
		# top rectangle 
        self.top_rect = pygame.Rect(pos,(width,height))
        self.top_color = color

		# bottom rectangle 
        self.bottom_rect = pygame.Rect(pos,(width,height))
        self.bottom_color = color
        
		#text
        self.text_surf = FONT.render(text,True,'#FFFFFF')
        self.text_rect = self.text_surf.get_rect(center = self.top_rect.center)

        



    def draw(self,color,color2):

		# elevation logic 
        
        self.top_rect.y = self.original_y_pos - self.dynamic_elecation
        self.text_rect.center = self.top_rect.center 

        self.bottom_rect.midtop = self.top_rect.midtop
        self.bottom_rect.height = self.top_rect.height + self.dynamic_elecation

        pygame.draw.rect(win,self.bottom_color, self.bottom_rect,border_radius = 12)
        pygame.draw.rect(win,self.top_color, self.top_rect,border_radius = 12)
        win.blit(self.text_surf, self.text_rect)
        self.check_click(color,color2)
    

    def check_click(self, color,color2):
        mouse_pos = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos):
            self.top_color = color2
            
            if pygame.mouse.get_pressed()[0]:
                self.dynamic_elecation = 0
                self.pressed = True
            else:
                self.dynamic_elecation = self.elevation
                if self.pressed == True:
                    self.pressed = False
        else: 
            self.dynamic_elecation = self.elevation
            self.top_color = color
            self.bottom_color = color2
    def update_button(self, new_text, new_size):
        # Actualizar el texto del botón
        self.text_surf = FONT.render(new_text, True, '#FFFFFF')
        self.text_rect = self.text_surf.get_rect(center=self.top_rect.center)

        # Actualizar el tamaño del botón
        self.top_rect.width, self.top_rect.height = new_size
        self.bottom_rect.width, self.bottom_rect.height = new_size