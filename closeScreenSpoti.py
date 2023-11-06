import win32gui

# Define la función para ocultar una ventana
def hide_window(window_title):
    # Busca una ventana con el título especificado
    hwnd = win32gui.FindWindow(None, window_title)
    
    if hwnd != 0:
        # Oculta la ventana
        win32gui.ShowWindow(hwnd, win32gui.SW_HIDE)
    else:
        print(f"No se encontró la ventana con el título '{window_title}'")

# Especifica el título de la ventana que deseas ocultar
window_title_to_hide = "Título de la ventana a ocultar"

# Llama a la función para ocultar la ventana
hide_window(window_title_to_hide)

