import math
from OpenGL.GL import *
from OpenGL.GLU import *
from PIL import Image

#carrega a textura e retorna o text id
def load_texture(path):

    image = Image.open(path).convert("RGBA")
    width, height = image.size
    image = image.transpose(Image.FLIP_TOP_BOTTOM)
    img_data = image.tobytes()

    tex_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, tex_id)

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)

    glTexImage2D(
        GL_TEXTURE_2D, 0, GL_RGBA,
        width, height, 0,
        GL_RGBA, GL_UNSIGNED_BYTE, img_data
    )

    glBindTexture(GL_TEXTURE_2D, 0)
    return tex_id, width, height

# Helper para não repetir sempre o set da cor
def _set_color(color):
    if color is not None:
        r, g, b = color
        glColor3f(r, g, b)

# Desenha um toro (donut) simples
def draw_torus(inner_radius=0.1, outer_radius=0.3, sides=24, rings=24, color=None):
    _set_color(color)

    two_pi = 2.0 * math.pi

    for i in range(rings):
        theta     = i * two_pi / rings
        theta_next = (i + 1) * two_pi / rings

        glBegin(GL_QUAD_STRIP)
        for j in range(sides + 1):
            phi = j * two_pi / sides

            cx  = math.cos(theta)
            sx  = math.sin(theta)
            cos_phi = math.cos(phi)
            sin_phi = math.sin(phi)

            r   = outer_radius + inner_radius * cos_phi
            x   = r * cx
            y   = inner_radius * sin_phi
            z   = r * sx

            nx  = cos_phi * cx
            ny  = sin_phi
            nz  = cos_phi * sx

            glNormal3f(nx, ny, nz)
            glVertex3f(x, y, z)

            cx2 = math.cos(theta_next)
            sx2 = math.sin(theta_next)

            r2  = outer_radius + inner_radius * cos_phi
            x2  = r2 * cx2
            y2  = inner_radius * sin_phi
            z2  = r2 * sx2

            nx2 = cos_phi * cx2
            ny2 = sin_phi
            nz2 = cos_phi * sx2

            glNormal3f(nx2, ny2, nz2)
            glVertex3f(x2, y2, z2)

        glEnd()


# Desenha um disco simples
def draw_disk(inner_radius=0.0, outer_radius=0.5,
              slices=32, loops=1, color=None):
    
    _set_color(color)

    quad = gluNewQuadric()
    gluQuadricNormals(quad, GLU_SMOOTH)

    gluDisk(quad, inner_radius, outer_radius, slices, loops)

    gluDeleteQuadric(quad)

# Desenha um paralelepípedo com ou sem textura
def draw_block(hx=0.5, hy=0.5, hz=0.5,color=None, texture_path=None):
    
    if texture_path:
        texture_id, width, height = load_texture(texture_path)
        glEnable(GL_TEXTURE_2D) 
        _set_color(color)
        glBindTexture(GL_TEXTURE_2D, texture_id)
        glBegin(GL_QUADS)
    # +X
        glTexCoord2f(1.0, 0.0)
        glVertex3f( hx, -hy, -hz)
        glTexCoord2f(1.0, 1.0)
        glVertex3f( hx, -hy,  hz)
        glTexCoord2f(0.0, 1.0)
        glVertex3f( hx,  hy,  hz)
        glTexCoord2f(0.0, 0.0)
        glVertex3f( hx,  hy, -hz)

    # -X

        glTexCoord2f(1.0, 0.0)
        glVertex3f(-hx, -hy,  hz)
        glTexCoord2f(1.0, 1.0)
        glVertex3f(-hx, -hy, -hz)
        glTexCoord2f(0.0, 1.0)
        glVertex3f(-hx,  hy, -hz)
        glTexCoord2f(0.0, 0.0)
        glVertex3f(-hx,  hy,  hz)

    # +Y
        glTexCoord2f(1.0, 0.0)
        glVertex3f(-hx,  hy, -hz)
        glTexCoord2f(1.0, 1.0)
        glVertex3f( hx,  hy, -hz)
        glTexCoord2f(0.0, 1.0)
        glVertex3f( hx,  hy,  hz)
        glTexCoord2f(0.0, 0.0)
        glVertex3f(-hx,  hy,  hz)

    # -Y
        glTexCoord2f(1.0, 0.0)
        glVertex3f(-hx, -hy,  hz)
        glTexCoord2f(1.0, 1.0)
        glVertex3f( hx, -hy,  hz)
        glTexCoord2f(0.0, 1.0)
        glVertex3f( hx, -hy, -hz)
        glTexCoord2f(0.0, 0.0)
        glVertex3f(-hx, -hy, -hz)

    # +Z
        glTexCoord2f(1.0, 0.0)
        glVertex3f(-hx, -hy,  hz)
        glTexCoord2f(1.0, 1.0)
        glVertex3f(-hx,  hy,  hz)
        glTexCoord2f(0.0, 1.0)
        glVertex3f( hx,  hy,  hz)
        glTexCoord2f(0.0, 0.0)
        glVertex3f( hx, -hy,  hz)

    # -Z
        glTexCoord2f(1.0, 0.0)
        glVertex3f( hx, -hy, -hz)
        glTexCoord2f(1.0, 1.0)
        glVertex3f( hx,  hy, -hz)
        glTexCoord2f(0.0, 1.0)
        glVertex3f(-hx,  hy, -hz)
        glTexCoord2f(0.0, 0.0)
        glVertex3f(-hx, -hy, -hz)

        glEnd()
        glDisable(GL_TEXTURE_2D) 
    else:
        draw_block_no_text(hx, hy, hz, color)


# Desenha um paralelepípedo sem textura
def draw_block_no_text(hx=0.5, hy=0.5, hz=0.5, color=None,texture_path=None):
    _set_color(color)

    glBegin(GL_QUADS)
    # +X
    glNormal3f(1.0, 0.0, 0.0)
    glVertex3f( hx, -hy, -hz)
    glVertex3f( hx, -hy,  hz)
    glVertex3f( hx,  hy,  hz)
    glVertex3f( hx,  hy, -hz)

    # -X
    glNormal3f(-1.0, 0.0, 0.0)
    glVertex3f(-hx, -hy,  hz)
    glVertex3f(-hx, -hy, -hz)
    glVertex3f(-hx,  hy, -hz)
    glVertex3f(-hx,  hy,  hz)

    # +Y
    glNormal3f(0.0, 1.0, 0.0)
    glVertex3f(-hx,  hy, -hz)
    glVertex3f( hx,  hy, -hz)
    glVertex3f( hx,  hy,  hz)
    glVertex3f(-hx,  hy,  hz)

    # -Y
    glNormal3f(0.0, -1.0, 0.0)
    glVertex3f(-hx, -hy,  hz)
    glVertex3f( hx, -hy,  hz)
    glVertex3f( hx, -hy, -hz)
    glVertex3f(-hx, -hy, -hz)

    # +Z
    glNormal3f(0.0, 0.0, 1.0)
    glVertex3f(-hx, -hy,  hz)
    glVertex3f(-hx,  hy,  hz)
    glVertex3f( hx,  hy,  hz)
    glVertex3f( hx, -hy,  hz)

    # -Z
    glNormal3f(0.0, 0.0, -1.0)
    glVertex3f( hx, -hy, -hz)
    glVertex3f( hx,  hy, -hz)
    glVertex3f(-hx,  hy, -hz)
    glVertex3f(-hx, -hy, -hz)
    glEnd()

# Desenha um chão texturizado
def draw_floor_quad(size=20.0, color=(1, 1, 1),mosaics =10.0,texture_path=None):
    texture_id, width, height = load_texture(texture_path)
    glEnable(GL_TEXTURE_2D) 
    _set_color(color)
    glBindTexture(GL_TEXTURE_2D, texture_id)

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
                                    
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0); glVertex3f(-size, 0.0,  size)
    glTexCoord2f(mosaics, 0.0); glVertex3f( size, 0.0,  size)
    glTexCoord2f(mosaics, mosaics); glVertex3f( size, 0.0, -size)
    glTexCoord2f(0.0, mosaics); glVertex3f(-size, 0.0, -size)
    glEnd()
    glDisable(GL_TEXTURE_2D)

# Desenha um cilindro simples
def draw_cylinder(radius=0.5, height=1.0, slices=24, color=None):

    _set_color(color)

    half_h = height * 0.5
    two_pi = 2.0 * math.pi

    # Lateral
    glBegin(GL_QUAD_STRIP)
    for i in range(slices + 1):
        ang = two_pi * i / slices
        x = math.cos(ang)
        z = math.sin(ang)
        glNormal3f(x, 0.0, z)
        glVertex3f(radius * x, -half_h, radius * z)
        glVertex3f(radius * x,  half_h, radius * z)
    glEnd()

    # Tampa de cima
    glBegin(GL_TRIANGLE_FAN)
    glNormal3f(0.0, 1.0, 0.0)
    glVertex3f(0.0, half_h, 0.0)  
    for i in range(slices + 1):
        ang = two_pi * i / slices
        x = math.cos(ang)
        z = math.sin(ang)
        glVertex3f(radius * x, half_h, radius * z)
    glEnd()

    # Tampa de baixo
    glBegin(GL_TRIANGLE_FAN)
    glNormal3f(0.0, -1.0, 0.0)
    glVertex3f(0.0, -half_h, 0.0) 
    for i in range(slices + 1):
        ang = two_pi * i / slices
        x = math.cos(ang)
        z = math.sin(ang)
        glVertex3f(radius * x, -half_h, radius * z)
    glEnd()

# Desenha uma pirâmide triangular (prisma triangular)
def draw_prism(hx, hy, hz, color=(0.7, 0.75, 0.9)):
    r, g, b = color
    glColor3f(r, g, b)

    # ---------- Triângulos frontal e traseiro ----------
    glBegin(GL_TRIANGLES)

    # Frente (z = +hz) – normal +Z
    glNormal3f(0.0, 0.0, 1.0)
    glVertex3f(0.0,  0.0, hz)  
    glVertex3f(hx,   0.0, hz)   
    glVertex3f(0.0,  hy,  hz)   

    # Trás (z = -hz) – normal -Z
    glNormal3f(0.0, 0.0, -1.0)
    glVertex3f(hx,   0.0, -hz) 
    glVertex3f(0.0,  0.0, -hz)  
    glVertex3f(0.0,  hy, -hz)   

    glEnd()

    # ---------- Faces rectangulares ----------
    glBegin(GL_QUADS)

    # 1) Base AB (plano Y = 0) – normal para baixo (-Y)
    glNormal3f(0.0, -1.0, 0.0)
    glVertex3f(0.0,  0.0, -hz)  # A'
    glVertex3f(hx,   0.0, -hz)  # B'
    glVertex3f(hx,   0.0,  hz)  # B
    glVertex3f(0.0,  0.0,  hz)  # A

    # 2) Lado vertical AC (plano X = 0) – normal para -X
    glNormal3f(-1.0, 0.0, 0.0)
    glVertex3f(0.0,  0.0, -hz)  # A'
    glVertex3f(0.0,  0.0,  hz)  # A
    glVertex3f(0.0,  hy,  hz)   # C
    glVertex3f(0.0,  hy, -hz)   # C'

    # 3) Lado da hipotenusa BC – normal num plano inclinado
    length = math.sqrt(hx*hx + hy*hy)
    if length == 0:
        length = 1.0

    nx =  hy / length
    ny =  hx / length
    glNormal3f(nx, ny, 0.0)

    glVertex3f(hx,   0.0, -hz)  
    glVertex3f(0.0,  hy, -hz)   
    glVertex3f(0.0,  hy,  hz)   
    glVertex3f(hx,   0.0,  hz)  

    glEnd()

# Desenha um cone simples
def draw_cone(radius=0.5, height=1.0, slices=24, color=None, cap=True):
    if radius <= 0.0 or height <= 0.0:
        return

    _set_color(color)

    two_pi = 2.0 * math.pi

    # ----- Superfície lateral -----
    k = radius / height
    len_n = math.sqrt(1.0 + k * k)  

    glBegin(GL_TRIANGLE_FAN)

    # vértice (ponta do cone)
    glNormal3f(0.0, 1.0 / len_n * k, 0.0)
    glVertex3f(0.0, height, 0.0)

    for i in range(slices + 1):
        ang = two_pi * i / slices
        cx = math.cos(ang)
        cz = math.sin(ang)

        nx = cx / len_n
        ny = k / len_n
        nz = cz / len_n

        glNormal3f(nx, ny, nz)
        glVertex3f(radius * cx, 0.0, radius * cz)

    glEnd()

    # ----- Tampa da base -----
    if cap:
        glBegin(GL_TRIANGLE_FAN)
        glNormal3f(0.0, -1.0, 0.0)
        glVertex3f(0.0, 0.0, 0.0) 

        for i in range(slices + 1):
            ang = two_pi * i / slices
            cx = math.cos(ang)
            cz = math.sin(ang)
            glVertex3f(radius * cx, 0.0, radius * cz)

        glEnd()

# Desenha uma esfera simples
def draw_sphere(radius=1.0, slices=24, stacks=16, color=None):
   
    _set_color(color)

    for i in range(stacks):
        phi1 = math.pi * i / stacks
        phi2 = math.pi * (i + 1) / stacks

        glBegin(GL_TRIANGLE_STRIP)
        for j in range(slices + 1):
            theta = 2.0 * math.pi * j / slices

            x1 = radius * math.sin(phi1) * math.cos(theta)
            y1 = radius * math.cos(phi1)
            z1 = radius * math.sin(phi1) * math.sin(theta)

            glNormal3f(x1 / radius, y1 / radius, z1 / radius)
            glVertex3f(x1, y1, z1)

            x2 = radius * math.sin(phi2) * math.cos(theta)
            y2 = radius * math.cos(phi2)
            z2 = radius * math.sin(phi2) * math.sin(theta)

            glNormal3f(x2 / radius, y2 / radius, z2 / radius)
            glVertex3f(x2, y2, z2)

        glEnd()

