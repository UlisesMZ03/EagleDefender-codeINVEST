### 🦅 EagleDefender - Juego de Estrategia con Interfaz Gráfica en Python

<p align="center">
  <img width="300" src="https://i.imgur.com/7cl3a2M.png" alt="EagleDefender Banner">
</p>

**EagleDefender** es un juego de estrategia y defensa construido en Python, que combina gráficos personalizados, audio inmersivo y una interfaz de usuario interactiva.  
Desarrollado como parte de un proyecto académico, ofrece múltiples pantallas, perfiles de usuario, música de fondo, efectos de sonido y una base de datos local para almacenar progreso.

---

### 🎮 Características principales

- 🧑‍💻 Sistema de usuarios con login y registro
- 🕹️ Pantallas interactivas: menú principal, instrucciones, configuración, Hall of Fame
- 🔥 Efectos visuales y sonoros personalizados
- 💾 Persistencia mediante base de datos SQLite
- 🧱 Componentes reutilizables (botones, entradas de texto, perfiles)
- 🎵 Sistema de música y efectos con selección personalizada

---

### ⚙️ Tecnologías utilizadas

- 🐍 **Python 3**
- 🎨 `pygame` para gráficos y sonidos
- 🗃️ `sqlite3` como base de datos embebida
- 🧱 Arquitectura modular orientada a objetos

---

### 🚀 ¿Cómo ejecutarlo?

#### 1. Clonar el repositorio

```bash
git clone https://github.com/UlisesMZ03/EagleDefender.git
cd EagleDefender
```

#### 2. Crear entorno virtual (opcional pero recomendado)

```bash
python -m venv venv
source venv/bin/activate  # en Linux/macOS
venv\Scripts\activate   # en Windows
```

#### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

#### 4. Ejecutar el juego

```bash
python menu.py
```

---

### 📁 Estructura del proyecto

- `menu.py`: Entrada principal del juego
- `login.py`, `register.py`, `halloffame.py`: Módulos de navegación
- `gameWindow.py`: Pantalla del juego
- `baseDatos.py`, `database.db`: Gestión de usuarios y progreso
- `/images`: Sprites, fondos, y texturas
- `/sounds`: Música y efectos sonoros
- `/font`: Tipografías personalizadas

---

### 📝 Requisitos

- Python 3.7+
- `pygame`

---

### 📚 Recursos útiles

- [pygame Documentation](https://www.pygame.org/docs/)
- [SQLite3 en Python](https://docs.python.org/3/library/sqlite3.html)

