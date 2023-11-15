import pygame
from tkinter import filedialog
import os
import shutil
import pygame_gui

def load_selected_image(image_path,camera_preview_rect):
    if os.path.exists(image_path):
        image_surface = pygame.image.load(image_path).convert()
        return pygame.transform.scale(image_surface, (camera_preview_rect.width, camera_preview_rect.height))
    return None
def select_folder():
     file_path = filedialog.askopenfilename(filetypes=[("Archivos PNG", "*.png"), ("Archivos JPEG", "*.jpg")])
     if file_path:
        global selected_image_surface 
        selected_image_surface= load_selected_image(file_path)          
        # Carpeta donde se guardarán las imágenes con nuevos nombres
        output_folder = os.path.join("profile_photos")

        # Crea la carpeta "profile_photos" si no existe
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        name_photo = Usuario._get_next_id(Usuario)
        # Nuevo nombre para la imagen (puedes cambiar esto según tus necesidades)
        global temp_file_path
        new_image_name = str(name_photo)+".png"
 
       
        # Ruta completa de la nueva imagen
        temp_file_path = os.path.join(output_folder, new_image_name)

        # Copia y renombra la imagen seleccionada a la carpeta "profile_photos"
        shutil.copy(file_path, temp_file_path)

