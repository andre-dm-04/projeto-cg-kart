from graphics import run
from scene import make_scene
from OpenGL.GLU import *
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

win_w = 800
win_h = 600

# Cria a cena e chama a função para rodar o programa
def main():
    root = make_scene()  
    run(root)

if __name__ == "__main__":
    main()
