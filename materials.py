from OpenGL.GL import *

def mat_kart_paint_red():
    #Pintura vermelha brilhante (chassis, capô, etc).
    face = GL_FRONT_AND_BACK
    glMaterialfv(face, GL_AMBIENT,  (0.2, 0.02, 0.02, 1.0))
    glMaterialfv(face, GL_DIFFUSE,  (0.8, 0.1,  0.1,  1.0))
    glMaterialfv(face, GL_SPECULAR, (0.6, 0.6,  0.6,  1.0))
    glMaterialf(face,  GL_SHININESS, 64.0)

def mat_rubber_dark():
    #pneus
    face = GL_FRONT_AND_BACK
    glMaterialfv(face, GL_AMBIENT,  (0.02, 0.02, 0.02, 1.0))
    glMaterialfv(face, GL_DIFFUSE,  (0.10, 0.10, 0.10, 1.0))
    glMaterialfv(face, GL_SPECULAR, (0.01, 0.01, 0.01, 1.0))
    glMaterialf(face,  GL_SHININESS, 10.0)

def mat_metal_silver():
    #Metal prateado jantes, pára-choques, etc.
    face = GL_FRONT_AND_BACK
    glMaterialfv(face, GL_AMBIENT,  (0.25, 0.25, 0.25, 1.0))
    glMaterialfv(face, GL_DIFFUSE,  (0.4,  0.4,  0.4,  1.0))
    glMaterialfv(face, GL_SPECULAR, (0.9,  0.9,  0.9,  1.0))
    glMaterialf(face,  GL_SHININESS, 96.0)

def mat_light_yellow():
    #Material emissivo para os faróis (aceso).
    face = GL_FRONT_AND_BACK
    glMaterialfv(face, GL_AMBIENT,  (0.2, 0.2, 0.05, 1.0))
    glMaterialfv(face, GL_DIFFUSE,  (1.0, 1.0, 0.6, 1.0))
    glMaterialfv(face, GL_SPECULAR, (0.0, 0.0, 0.0, 1.0))
    glMaterialfv(face, GL_EMISSION, (0.8, 0.8, 0.4, 1.0))
    glMaterialf(face,  GL_SHININESS, 0.0)

def mat_light_red():
    #Material emissivo para luzes traseiras / travão.
    face = GL_FRONT_AND_BACK
    glMaterialfv(face, GL_AMBIENT,  (0.2, 0.02, 0.02, 1.0))
    glMaterialfv(face, GL_DIFFUSE,  (1.0, 0.4,  0.3,  1.0))
    glMaterialfv(face, GL_SPECULAR, (0.0, 0.0,  0.0,  1.0))
    glMaterialfv(face, GL_EMISSION, (0.9, 0.3,  0.2,  1.0))
    glMaterialf(face,  GL_SHININESS, 0.0)

def mat_clear_emission():
    #Voltar a ter emissão 0 depois das luzes
    face = GL_FRONT_AND_BACK
    glMaterialfv(face, GL_EMISSION, (0.0, 0.0, 0.0, 1.0))
