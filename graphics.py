import sys
import time
import math

import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import (
    glutInit,
    glutBitmapCharacter,
    GLUT_BITMAP_HELVETICA_18,
)


import scene  


WINDOW_WIDTH  = 800
WINDOW_HEIGHT = 600
WINDOW_TITLE  = "Kart 3D - CG"

# ---------- ESTADO DA CÂMARA (ORBIT) ----------

cam_dist      = 12.0  
cam_azimuth   = 45.0   
cam_elevation = 20.0  

CAM_ROT_SPEED  = 60.0 
CAM_ZOOM_SPEED = 10.0 
CAM_DIST_MIN   = 4.0
CAM_DIST_MAX   = 40.0
CAM_ELEV_MIN   = -80.0
CAM_ELEV_MAX   =  80.0


# modo da câmara: "orbit" ou "fp" (first person)
cam_mode   = "orbit"
cam_prev_p = False


fp_yaw   = 0.0   
fp_pitch = 0.0  

FP_YAW_MAX   = 90.0   
FP_PITCH_MAX = 70.0   



# ---------- criação da janela ----------

def init_window():
    if not glfw.init():
        print("Erro ao inicializar GLFW")
        sys.exit(1)

    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 2)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 1)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_ANY_PROFILE)

    window = glfw.create_window(
        WINDOW_WIDTH,
        WINDOW_HEIGHT,
        WINDOW_TITLE,
        None,
        None
    )
    if not window:
        glfw.terminate()
        print("Erro ao criar a janela GLFW")
        sys.exit(1)

    glfw.make_context_current(window)
    glfw.swap_interval(1)  

    glutInit()

    return window


# ---------- setup de OpenGL (projecção, estados) ----------

def setup_opengl(width, height):
    if height == 0:
        height = 1

    glViewport(0, 0, width, height)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    aspect = width / float(height)
    gluPerspective(60.0, aspect, 0.1, 100.0)

    glClearColor(0.5, 0.7, 1.0, 1.0)   # céu azul
    glEnable(GL_DEPTH_TEST)

    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)

    glLightfv(GL_LIGHT0, GL_AMBIENT,  (0.05, 0.05, 0.05, 1.0))
    glLightfv(GL_LIGHT0, GL_DIFFUSE,  (0.9, 0.9, 0.9, 1.0))
    glLightfv(GL_LIGHT0, GL_SPECULAR, (1.0, 1.0, 1.0, 1.0))

    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)


# ---------- câmara (fixa) ----------

def setup_camera(kart_node=None):
    global cam_dist, cam_azimuth, cam_elevation, cam_mode
    global fp_yaw, fp_pitch

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    # ---------- MODO FIRST-PERSON ----------
    if cam_mode == "fp" and kart_node is not None:
        ang   = kart_node.state.get("angle_y", 0.0)
        pos_x = kart_node.state.get("pos_x", 0.0)
        pos_z = kart_node.state.get("pos_z", 0.0)

        base_rad = math.radians(ang)
        base_dir_x = math.cos(base_rad)
        base_dir_z = -math.sin(base_rad)

        right_x = -base_dir_z
        right_z =  base_dir_x

        # posição da "cabeça" da câmara
        offset_forward = -0.2   
        offset_up      = 0.7   
        offset_right   = -0.35  

        eye_x = (pos_x
                 + base_dir_x * offset_forward
                 + right_x    * offset_right)
        eye_y = 1.0 + offset_up
        eye_z = (pos_z
                 + base_dir_z * offset_forward
                 + right_z    * offset_right)

        # aplicar yaw/pitch da cabeça ao vector de olhar
        heading_deg = ang + fp_yaw
        heading_rad = math.radians(heading_deg)
        pitch_rad   = math.radians(fp_pitch)

        dir_x = math.cos(heading_rad) * math.cos(pitch_rad)
        dir_y = math.sin(pitch_rad)
        dir_z = -math.sin(heading_rad) * math.cos(pitch_rad)

        center_x = eye_x + dir_x * 5.0
        center_y = eye_y + dir_y * 5.0
        center_z = eye_z + dir_z * 5.0

    # ---------- MODO ORBIT ----------
    else:
        center_x, center_y, center_z = 0.0, 0.5, 0.0

        az = math.radians(cam_azimuth)
        el = math.radians(cam_elevation)

        eye_x = center_x + cam_dist * math.cos(el) * math.sin(az)
        eye_y = center_y + cam_dist * math.sin(el)
        eye_z = center_z + cam_dist * math.cos(el) * math.cos(az)

    gluLookAt(
        eye_x,    eye_y,    eye_z,
        center_x, center_y, center_z,
        0.0, 1.0, 0.0
    )


# ---------- TEXTO 2D / HUD ----------

def draw_text_2d(x, y, text, width, height):

    matrix_mode = glGetIntegerv(GL_MATRIX_MODE)
    viewport = glGetIntegerv(GL_VIEWPORT)

    lighting_was_on = glIsEnabled(GL_LIGHTING)
    depth_was_on    = glIsEnabled(GL_DEPTH_TEST)

    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, width, 0, height)

    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    glDisable(GL_LIGHTING)
    glDisable(GL_DEPTH_TEST)

    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(ch))

    if lighting_was_on:
        glEnable(GL_LIGHTING)
    else:
        glDisable(GL_LIGHTING)

    if depth_was_on:
        glEnable(GL_DEPTH_TEST)
    else:
        glDisable(GL_DEPTH_TEST)

    glPopMatrix()                 
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()                 
    glMatrixMode(matrix_mode)   


def draw_hud(width, height):
    lines = [
        "Kart movement: W/A/S/D",
        "Zoom control: Q/E",
        "Camera orbit: arrows",
        "First-person: P",
        "Open doors: SPACE",
        "Open garage: O",
    ]

    margin      = 20
    line_height = 20

    x = width - 280       
    y = height - margin

    for line in lines:
        draw_text_2d(x, y, line, width, height)
        y -= line_height


def find_node_by_name(node, name):
    if node.name == name:
        return node
    for c in node.children:
        res = find_node_by_name(c, name)
        if res is not None:
            return res
    return None



# ---------- main loop ----------

def run(root_node):
    """
    root_node: nó raiz do scenegraph (Node do teu scenegraph.py)
    """
    window = init_window()
    fbw, fbh = glfw.get_framebuffer_size(window)
    setup_opengl(fbw, fbh)

    last_time = time.time()

    kart_node = None
    if root_node is not None:
        kart_node = find_node_by_name(root_node, "kart_root")


    while not glfw.window_should_close(window):
        now = time.time()
        dt = now - last_time
        last_time = now

        glfw.poll_events()

        # --- ler inputs e actualizar estado global ---
        scene.input_state["forward"] = (glfw.get_key(window, glfw.KEY_W) == glfw.PRESS)
        scene.input_state["back"]    = (glfw.get_key(window, glfw.KEY_S) == glfw.PRESS)
        scene.input_state["left"]    = (glfw.get_key(window, glfw.KEY_A) == glfw.PRESS)
        scene.input_state["right"]   = (glfw.get_key(window, glfw.KEY_D) == glfw.PRESS)
        scene.input_state["doors"]   = (glfw.get_key(window, glfw.KEY_SPACE) == glfw.PRESS)
        scene.input_state["garage"] = (glfw.get_key(window, glfw.KEY_O) == glfw.PRESS)



        # ---- CONTROLO DA CÂMERA ----
        global cam_dist, cam_azimuth, cam_elevation, cam_mode
        global fp_yaw, fp_pitch

        if cam_mode == "orbit":
            if glfw.get_key(window, glfw.KEY_RIGHT) == glfw.PRESS:
                cam_azimuth += CAM_ROT_SPEED * dt
            if glfw.get_key(window, glfw.KEY_LEFT) == glfw.PRESS:
                cam_azimuth -= CAM_ROT_SPEED * dt

            if glfw.get_key(window, glfw.KEY_UP) == glfw.PRESS:
                cam_elevation += CAM_ROT_SPEED * dt
            if glfw.get_key(window, glfw.KEY_DOWN) == glfw.PRESS:
                cam_elevation -= CAM_ROT_SPEED * dt

            if glfw.get_key(window, glfw.KEY_E) == glfw.PRESS:
                cam_dist += CAM_ZOOM_SPEED * dt
            if glfw.get_key(window, glfw.KEY_Q) == glfw.PRESS:
                cam_dist -= CAM_ZOOM_SPEED * dt

            cam_dist = max(CAM_DIST_MIN, min(CAM_DIST_MAX, cam_dist))
            cam_elevation = max(CAM_ELEV_MIN, min(CAM_ELEV_MAX, cam_elevation))

        else:
            # FIRST-PERSON: setas só mexem a cabeça
            if glfw.get_key(window, glfw.KEY_RIGHT) == glfw.PRESS:
                fp_yaw -= CAM_ROT_SPEED * dt   
            if glfw.get_key(window, glfw.KEY_LEFT) == glfw.PRESS:
                fp_yaw += CAM_ROT_SPEED * dt   
            if glfw.get_key(window, glfw.KEY_UP) == glfw.PRESS:
                fp_pitch += CAM_ROT_SPEED * dt  
            if glfw.get_key(window, glfw.KEY_DOWN) == glfw.PRESS:
                fp_pitch -= CAM_ROT_SPEED * dt  

            if fp_yaw >  FP_YAW_MAX:  fp_yaw  =  FP_YAW_MAX
            if fp_yaw < -FP_YAW_MAX:  fp_yaw  = -FP_YAW_MAX
            if fp_pitch >  FP_PITCH_MAX: fp_pitch =  FP_PITCH_MAX
            if fp_pitch < -FP_PITCH_MAX: fp_pitch = -FP_PITCH_MAX



        p_pressed = (glfw.get_key(window, glfw.KEY_P) == glfw.PRESS)
        if p_pressed and not cam_prev_p:
            if cam_mode == "orbit":
                cam_mode = "fp"
                fp_yaw = 0.0
                fp_pitch = 0.0
            else:
                cam_mode = "orbit"
        cam_prev_p = p_pressed



        # UPDATE da cena inteira
        if root_node is not None:
            root_node.update(dt)

        # RENDER
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        setup_camera(kart_node)

        if root_node is not None:
            root_node.draw()

        width, height = glfw.get_framebuffer_size(window)
        draw_hud(width, height)

        glfw.swap_buffers(window)

        fbw, fbh = glfw.get_framebuffer_size(window)
        setup_opengl(fbw, fbh)

    glfw.terminate()
