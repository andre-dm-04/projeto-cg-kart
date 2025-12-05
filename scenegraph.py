from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

class Node:
    # Inicializa o nó com nome, geometria, transformação, atualização e estado
    def __init__(self, name, geom=None, transform=None, updater=None, state=None):
        self.name = name  
        self.geom = geom
        self.transform = transform
        self.updater = updater
        self.state = state or {}
        self.children = []
        self.parent = None

    # Adiciona filhos ao nó
    def add(self, *kids):
        for k in kids:
            k.parent = self  
            self.children.append(k)

    # Atualiza o nó se houver função de updater, atualiza os filhos
    def update(self, dt):
        if self.updater:
            self.updater(self, dt)  
        for c in self.children:
            c.update(dt)  

    # Aplica transformação e desenha geometria e filhos
    def draw(self):
        glPushMatrix()
        if self.transform:
            self.transform(self)  
        if self.geom:
            self.geom(self) 
        for c in self.children:
            c.draw() 
        glPopMatrix()

     # Encontra o nó raiz
    def get_root(self):
        n = self
        while n.parent is not None:
            n = n.parent 
        return n

    # Procura um nó pelo nome
    def find(self, name):
        if self.name == name:
            return self 
        for c in self.children:
            res = c.find(name)  
            if res is not None:
                return res
        return None  
