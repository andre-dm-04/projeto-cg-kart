import math
from OpenGL.GL import *
from scenegraph import Node
from geometry import *
import glfw
from materials import *

# ----------------- INPUT GLOBAL (WASD) -----------------

input_state = {
    "forward": False,  # W
    "back":    False,  # S
    "left":    False,  # A
    "right":   False,  # D
    "doors":   False,  #spacebar
    "garage":  False   # O
}

steering_state = {
    "front_steer": 0.0
}

doors_open = False          
doors_prev_input = False 

DOOR_OPEN_ANGLE   = 70.0    
DOOR_ROT_SPEED    = 120.0 


garage_door_open = False
garage_door_prev_input = False
garage_door_angle = 0.0  
garage_door_translate = 0.0 

# ----------------- CHÃO -----------------

def draw_ground(node):
    draw_floor_quad(size=20.0, color=(1, 1, 1),mosaics =5.0,texture_path="floor.jpg")


def tf_ground(node):
    pass

# ---------- GEOMETRIAS PARA OS NÓS DO KART ----------

# chassis principal
def geom_kart_chassis(node):
    mat_kart_paint_red()
    draw_block(hx=1.5, hy=0.15, hz=0.8, color=(0.9, 0.1, 0.1))

# capô
def geom_kart_hood(node):
    mat_kart_paint_red()
    draw_prism(hx=0.5, hy=0.30, hz=0.8, color=(0.9, 0.1, 0.1))
    glTranslatef(-0.2, 0.0, 0.0)
    draw_block(hx=0.2, hy=0.3, hz=0.65, color=(0.9, 0.1, 0.1))

 # banco 
def geom_kart_seat(node):
    mat_rubber_dark()
    draw_block(hx=0.3, hy=0.05, hz=0.6, color=(0.2, 0.2, 0.2))
    glTranslatef(-0.3, 0.40, 0.0)
    draw_block(hx=0.05, hy=0.45, hz=0.6, color=(0.2, 0.2, 0.2))


# roda
def geom_kart_wheel(node):
    spin = node.state.get("spin", 0.0)

    glRotatef(spin, 0.0, 0.0, 1.0)

    glRotatef(90.0, 90.0, 0.0, 1.0)   
    mat_rubber_dark()
    draw_torus(inner_radius=0.10, outer_radius=0.30,
               sides=24, rings=24, color=(0.1, 0.1, 0.1))
    glRotatef(90.0, 1.0, 0.0, 0.0)
    mat_metal_silver()
    draw_disk(inner_radius=0.0, outer_radius=0.30,
              slices=32, loops=1, color=(0.7, 0.7, 0.7))
    glRotatef(180.0, 1.0, 0.0, 0.0)
    glTranslatef(0.0, 0.0, -0.01)
    draw_disk(inner_radius=0.0, outer_radius=0.30,
              slices=32, loops=1, color=(0.7, 0.7, 0.7))

    # jante
    draw_block(hx=0.025, hy=0.25, hz=0.025, color=(0.5, 0.5, 0.5))
    glRotatef(45.0, 0.0, 0.0, 1.0)
    draw_block(hx=0.025, hy=0.25, hz=0.025, color=(0.5, 0.5, 0.5))
    glRotatef(45.0, 0.0, 0.0, 1.0)
    draw_block(hx=0.025, hy=0.25, hz=0.025, color=(0.5, 0.5, 0.5))
    glRotatef(45.0, 0.0, 0.0, 1.0)
    draw_block(hx=0.025, hy=0.25, hz=0.025, color=(0.5, 0.5, 0.5))


# volante simples
def geom_kart_steering_wheel(node):
    draw_torus(inner_radius=0.05, outer_radius=0.20, sides= 24, rings=24, color=(0.1, 0.1, 0.1))
    glRotatef(90.0, 1.0, 0.0, 0.0)
    draw_disk (inner_radius=0.0, outer_radius=0.15, slices=32, loops=1, color = (0.7, 0.7, 0.7))
    glRotatef(-90.0, 1.0, 0.0, 0.0)
    glTranslatef(0.0, -0.40, 0.0)
    draw_cylinder(radius=0.05, height=0.80, color=(0.05, 0.05, 0.05))

# estrutura do kart
def geom_kart_structure(node):
    mat_kart_paint_red()
    glTranslatef(0.75, 0.30, 0.70)
    draw_block(hx=0.25, hy=0.15 , hz=0.10, color=(0.9, 0.1, 0.1))

    glTranslatef(-0.75, 0, 0)
    glTranslatef(-0.8, 0, 0)
    draw_block(hx=0.25, hy=0.45 , hz=0.10, color=(0.9, 0.1, 0.1))
    glTranslatef(0.20, 0.40, 0.0 )
    draw_cylinder(radius=0.05, height=1.70, color=(0.05, 0.05, 0.05))
    glTranslatef(-0.20, -0.40, 0.0 )
    glTranslatef(0.8, 0, -0.70)


    glTranslatef(0.75, 0, -0.70)
    draw_block(hx=0.25, hy=0.15 , hz=0.10, color=(0.9, 0.1, 0.1))

    glTranslatef(-0.75, 0, 0)
    glTranslatef(-0.8, 0, 0)
    draw_block(hx=0.25, hy=0.45 , hz=0.10, color=(0.9, 0.1, 0.1))
    glTranslatef(0.20, 0.40, 0.0 )
    draw_cylinder(radius=0.05, height=1.70, color=(0.05, 0.05, 0.05))
    glTranslatef(-0.20, -0.40, 0.0 )

    glTranslatef(0.3, 0, 0.70)
    draw_block(hx=0.05, hy=0.45 , hz=0.8, color=(0.9, 0.1, 0.1))
    glTranslatef(-0.3, 0, -0.70)

    glTranslatef(1.3, 0.15, 0.0 )
    draw_prism(hx=0.45, hy=0.10 , hz=0.10, color=(0.9, 0.1, 0.1))
    glTranslatef(0.20, 0.20, 0.0 )
    draw_cylinder(radius=0.05, height=1.70, color=(0.05, 0.05, 0.05))

    glTranslatef(-0.20, -0.20, 0.0 )

    glTranslatef(0.0, 0.0, 1.40)
    draw_prism(hx=0.45, hy=0.10 , hz=0.10, color=(0.9, 0.1, 0.1))
    glTranslatef(0.20, 0.20, 0.0 )
    draw_cylinder(radius=0.05, height=1.70, color=(0.05, 0.05, 0.05))

    glTranslatef(0.20, 0.0, -0.70 )

    glTranslatef(-0.90, 0.90, 0.0 )
    draw_block(hx=1.0, hy=0.05, hz=0.8, color=(0.9, 0.1, 0.1) )

# porta
def geom_kart_door(node):
    mat_kart_paint_red()
    draw_block(hx=0.475, hy=0.20 , hz=0.05, color=(0.1, 0.1, 0.1))

# puxador da porta
def geom_kart_doorhandle(node):
    mat_metal_silver()
    draw_block(hx=0.05, hy=0.03 , hz=0.05, color=(0.5, 0.5, 0.5))

# bagageira
def geom_kart_trunk(node):
    mat_kart_paint_red()
    draw_block(hx=0.25, hy=0.05 , hz=0.6, color=(0.9, 0.1, 0.1))

    glTranslatef(-0.25, -0.55, 0.70)
    glRotatef(180.0, 0.0, 1.0, 0.0)
    draw_prism(hx=0.45, hy=0.60 , hz=0.10, color=(0.9, 0.1, 0.1))

    glTranslatef(0.0, 0.0, 1.40)
    draw_prism(hx=0.45, hy=0.60 , hz=0.10, color=(0.9, 0.1, 0.1))

# porta da bagageira
def geom_kart_trunk_door(node):
    mat_kart_paint_red()
    glTranslatef(0.205, 0.275, -0.70)
    glRotatef(-52.3, 0.0, 0.0, 1.0)
    draw_block(hx=0.38, hy=0.04 , hz=0.6, color=(0.9, 0.1, 0.1))
    glTranslatef(0.1, 0.05, 0.0)
    draw_block(hx=0.05, hy=0.05 , hz=0.15, color=(0.5, 0.5, 0.5))

# para-choques
def geom_kart_bumber(node):
    mat_metal_silver()
    draw_block(hx=0.05, hy=0.15, hz=0.85, color=(0.5, 0.5, 0.5))

# matrícula
def geom_kart_numplate(node):
    mat_metal_silver()
    draw_block(hx=0.02, hy=0.07, hz=0.20, color=(0.8, 0.8, 0.8))

# luzes do tejadilho
def geom_kart_roof_lights(node):
    mat_metal_silver()
    draw_block(hx=0.1, hy=0.1, hz=0.55, color=(0.5, 0.5, 0.5))
    glTranslatef(0.15, 0.04, 0.0)
    glRotatef(90.0, 0.0, 0.0, 1.0)
    mat_light_yellow()
    draw_cone(radius=0.09, height=0.2, slices=24, color=(1.0, 1.0, 0.6))
    glTranslatef(0.0, 0.0, 0.2)
    draw_cone(radius=0.09, height=0.2, slices=24, color=(1.0, 1.0, 0.6))
    glTranslatef(0.0, 0.0, 0.2)
    draw_cone(radius=0.09, height=0.2, slices=24, color=(1.0, 1.0, 0.6))
    glTranslatef(0.0, 0.0, -0.6)
    draw_cone(radius=0.09, height=0.2, slices=24, color=(1.0, 1.0, 0.6))
    glTranslatef(0.0, 0.0, -0.2)
    draw_cone(radius=0.09, height=0.2, slices=24, color=(1.0, 1.0, 0.6))
    mat_clear_emission()

# luzes dianteiras
def geom_kart_lights_front(node):
    mat_light_yellow()
    draw_cone(radius=0.09, height=0.25, slices=24, color=(1.0, 1.0, 0.6))
    mat_clear_emission()
    glTranslatef(0.0, 0.2, 0.0)
    draw_cylinder(radius=0.10, height=0.25, color=(0.9, 0.1, 0.1))


# luzes traseiras
def geom_kart_lights_rear(node):
    mat_light_red()
    draw_cone(radius=0.09, height=0.25, slices=24, color=(1.0, 0.55, 0.45))
    mat_clear_emission()
    glTranslatef(0.0, 0.2, 0.0)
    draw_cylinder(radius=0.10, height=0.25, color=(0.9, 0.1, 0.1))

# proteção das rodas
def geom_kart_wheelprotection(node):
    mat_kart_paint_red()
    draw_block(hx=0.25, hy=0.05 , hz=0.2, color=(0.9, 0.1, 0.1))
    glTranslatef(-0.32, -0.087, 0.0)
    glRotatef(45.0, 0.0, 0.0, 1.0)
    draw_block(hx=0.15, hy=0.05 , hz=0.2, color=(0.9, 0.1, 0.1))
    glRotatef(-45.0, 0.0, 0.0, 1.0)
    glTranslatef(0.32, 0.087, 0.0)
    glTranslatef(0.32, -0.087, 0.0)
    glRotatef(-45.0, 0.0, 0.0, 1.0)
    draw_block(hx=0.15, hy=0.05 , hz=0.2, color=(0.9, 0.1, 0.1))

    
# ---------- GEOMS DA GARAGEM ----------
def geom_garage_wall(node):
    draw_block(
        hx=node.state["hx"],
        hy=node.state["hy"],
        hz=node.state["hz"],
        color=(1.0, 1.0, 1.0),texture_path="wall.png"
    )    

def geom_garage_door(node):
    draw_block(hx=3.00, hy=1.55, hz=0.05, color=(0.35, 0.35, 0.35),texture_path="garage-door.png")



# ---------- GEOMS DA SOL ----------

def geom_sun(node):
    glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION, (1.0, 0.9, 0.4, 1.0))
    draw_sphere(radius=0.6, slices=32, stacks=24, color=(1.0, 0.9, 0.4))
    glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION, (0.0, 0.0, 0.0, 1.0))

# ---------- GEOM DO POSTE DE LUZ ----------
def geom_light_pole(node):
    glPushMatrix()
    glTranslatef(0.0, 2.0, 0.0)
    draw_cylinder(radius=0.10, height=4.0, slices=24, color=(0.2, 0.2, 0.2))
    glPopMatrix()

    glTranslatef(0.0, 4.0, 0.0)
    draw_sphere(radius=0.25, slices=24, stacks=24, color=(1.0, 1.0, 0.8)) 

# ---------- GEOM DA ARVORE----------    
def geom_tree(node):
    glPushMatrix()
    glTranslatef(0.0, 0.0, 0.0)  
    glColor3f(0.5, 0.25, 0.1)  
    draw_cylinder(radius=0.2, height=5.0, slices=24) 
    glPopMatrix()

    glPushMatrix()
    glTranslatef(0.0, 2.5, 0.0)  
    glRotatef(45, 1.0, 0.0, 0.0)  
    glColor3f(0.5, 0.25, 0.1)  
    draw_cylinder(radius=0.1, height=2.0, slices=24) 
    glPopMatrix()

    glPushMatrix()
    glTranslatef(0.0, 2.5, 0.0)
    glRotatef(-45, 1.0, 0.0, 0.0)  
    glColor3f(0.5, 0.25, 0.1)
    draw_cylinder(radius=0.1, height=2.0, slices=24)  
    glPopMatrix()

    glPushMatrix()
    glTranslatef(0.0, 4.5, 0.0)  
    glColor3f(0.1, 0.7, 0.1) 
    draw_sphere(radius=1.0, slices=24, stacks=24) 
    glPopMatrix()

    glPushMatrix()
    glTranslatef(0.5, 4.0, 0.5)  
    glColor3f(0.1, 0.7, 0.1)  
    draw_sphere(radius=0.8, slices=24, stacks=24)  
    glPopMatrix()

    glPushMatrix()
    glTranslatef(-0.5, 4.0, -0.5)  
    glColor3f(0.1, 0.7, 0.1) 
    draw_sphere(radius=0.8, slices=24, stacks=24)  
    glPopMatrix()

    glPushMatrix()
    glTranslatef(0.5, 3.5, -0.5)  
    glColor3f(0.1, 0.7, 0.1) 
    draw_sphere(radius=0.8, slices=24, stacks=24) 
    glPopMatrix()

    glPushMatrix()
    glTranslatef(-0.5, 3.5, 0.5)  
    glColor3f(0.1, 0.7, 0.1)  
    draw_sphere(radius=0.8, slices=24, stacks=24) 
    glPopMatrix()    
  




# ---------- TRANSFORMS DO KART + MOVIMENTO DO KART ----------

def tf_kart_root(node):
    pos_x = node.state.get("pos_x", 0.0)
    pos_z = node.state.get("pos_z", 0.0)
    ang   = node.state.get("angle_y", 0.0)

    glTranslatef(pos_x, 1.0, pos_z)  
    glRotatef(ang, 0.0, 1.0, 0.0)    



MOVE_SPEED = 5.0     # unidades/seg
TURN_SPEED = 60.0    # graus/seg


def upd_kart_movement(node, dt):
    global doors_open, doors_prev_input

    ang   = node.state.get("angle_y", 0.0)
    pos_x = node.state.get("pos_x", 0.0)
    pos_z = node.state.get("pos_z", 0.0)

    old_x, old_z = pos_x, pos_z

    # -----------------------------
    #   CINEMÁTICA TIPO CARRO
    # -----------------------------
    speed = 0.0
    if input_state["forward"]:
        speed += MOVE_SPEED     
    if input_state["back"]:
        speed -= MOVE_SPEED     

  
    steer = steering_state.get("front_steer", 0.0)

    if abs(speed) > 1e-4 and abs(steer) > 1e-3:
        L = 2.0  
        steer_rad = math.radians(steer)
        omega_rad = (speed / L) * math.tan(steer_rad)  
        ang += math.degrees(omega_rad * dt)            

    rad   = math.radians(ang)
    dir_x = math.cos(rad)
    dir_z = -math.sin(rad)

    pos_x += dir_x * speed * dt
    pos_z += dir_z * speed * dt

    # ---------------------------------------------------
    #  COLISÃO COM AS PAREDES DA GARAGEM — DIMENSÕES AJUSTADAS
    # ---------------------------------------------------
    garage_xmin = -2.00
    garage_xmax =  6.00
    garage_zmin = -4.60
    garage_zmax =  3.90

    kart_half_width  = 1.05
    kart_half_length = 1.70

    inside_garage_x = (pos_x + kart_half_width  > garage_xmin and
                       pos_x - kart_half_width  < garage_xmax)

    inside_garage_z = (pos_z + kart_half_length > garage_zmin and
                       pos_z - kart_half_length < garage_zmax)

    if inside_garage_x and inside_garage_z:
        collided = False

        if pos_x - kart_half_width < garage_xmin:
            collided = True
        if pos_x + kart_half_width > garage_xmax:
            collided = True
        if pos_z - kart_half_length < garage_zmin:
           collided = True
        if pos_z + kart_half_length > garage_zmax:
             if not garage_door_open:
                collided = True

        if collided:
            pos_x, pos_z = old_x, old_z

    # ---------------------------------------------------
    #  COLISÃO COM O POSTE DE LUZ
    # ---------------------------------------------------
    pole_x = 7.0
    pole_z = 0.0
    pole_radius = 0.55

    kart_radius = math.sqrt(kart_half_width**2 + kart_half_length**2)

    dx = pos_x - pole_x
    dz = pos_z - pole_z
    dist = math.sqrt(dx*dx + dz*dz)

    min_dist = pole_radius + kart_half_width

    if dist < min_dist:
        pos_x, pos_z = old_x, old_z

    # ---------------------------------------------------
    #  COLISÃO COM A ÁRVORE
    # ---------------------------------------------------
    tree_x = 10.0  
    tree_z = -5.0  
    tree_radius = 0.7 
    dx_tree = pos_x - tree_x
    dz_tree = pos_z - tree_z
    dist_tree = math.sqrt(dx_tree**2 + dz_tree**2)
    collision_threshold = tree_radius + kart_half_width 

    if dist_tree < collision_threshold:
 
        pos_x, pos_z = old_x, old_z  


    # --------- TOGGLE PORTAS (SPACE) ---------
    doors_pressed = input_state.get("doors", False)
    if doors_pressed and not doors_prev_input:
        doors_open = not doors_open
    doors_prev_input = doors_pressed

    node.state["angle_y"] = ang
    node.state["pos_x"]   = pos_x
    node.state["pos_z"]   = pos_z



# ---------- ANIMAÇÃO DAS RODAS ----------

WHEEL_RADIUS    = 0.30
WHEEL_ANG_SPEED = MOVE_SPEED / WHEEL_RADIUS * 180.0 / math.pi 

MAX_STEER   = 45.0  
STEER_SPEED = 120.0 



def upd_front_wheel_steer(node, dt):
    steer = node.state.get("steer", 0.0)

    if input_state["left"] and not input_state["right"]:
        steer += STEER_SPEED * dt

    elif input_state["right"] and not input_state["left"]:
        steer -= STEER_SPEED * dt
    else:
       
       
        if steer > 0.0:
            steer = max(0.0, steer - STEER_SPEED * dt)
        elif steer < 0.0:
            steer = min(0.0, steer + STEER_SPEED * dt)

    if steer > MAX_STEER:
        steer = MAX_STEER
    if steer < -MAX_STEER:
        steer = -MAX_STEER

    node.state["steer"] = steer

    steering_state["front_steer"] = steer


def upd_wheel_spin(node, dt):
    ang = node.state.get("spin", 0.0)

    if input_state["forward"]:
        ang -= WHEEL_ANG_SPEED * dt   
    if input_state["back"]:
        ang += WHEEL_ANG_SPEED * dt   

    node.state["spin"] = ang % 360.0



def upd_front_wheel(node, dt):
    upd_wheel_spin(node, dt)
    upd_front_wheel_steer(node, dt)


#-----------ANIMAÇÃO DA PORTA DA GARAGEM----------

def upd_garage_door(node, dt):
    global garage_door_open, garage_door_prev_input, garage_door_angle, garage_door_translate

    o_pressed = input_state.get("garage", False)
    if o_pressed and not garage_door_prev_input:
        garage_door_open = not garage_door_open
    garage_door_prev_input = o_pressed

    if garage_door_open:
        garage_door_angle = min(90.0, garage_door_angle + 90.0 * dt)
        garage_door_translate = min(1.5, garage_door_translate + 0.75 * dt)  
    else:
        garage_door_angle = max(0.0, garage_door_angle - 90.0 * dt)
        garage_door_translate = max(0.0, garage_door_translate - 0.75 * dt)

    node.state["door_angle"] = garage_door_angle
    node.state["door_translate"] = garage_door_translate



# ---------- ANIMAÇÃO DO VOLANTE ----------

MAX_STEER_WHEEL = 540.0 

def upd_steering_wheel(node, dt):
    front_steer = steering_state.get("front_steer", 0.0)

    factor = MAX_STEER_WHEEL / MAX_STEER
    angle = front_steer * factor

    if angle > MAX_STEER_WHEEL:
        angle = MAX_STEER_WHEEL
    if angle < -MAX_STEER_WHEEL:
        angle = -MAX_STEER_WHEEL

    node.state["steer_angle"] = angle


# ---------- ANIMAÇÃO DAS PORTAS --------------

def upd_side_door(node, dt):
    """Anima uma porta lateral para o target (aberto/fechado)."""
    target = DOOR_OPEN_ANGLE if doors_open else 0.0
    angle = node.state.get("door_angle", 0.0)

    if angle < target:
        angle = min(target, angle + DOOR_ROT_SPEED * dt)
    elif angle > target:
        angle = max(target, angle - DOOR_ROT_SPEED * dt)

    node.state["door_angle"] = angle


# ---------- TRANSFORMS LOCAIS DAS PEÇAS ----------

def tf_chassis(node):
    glTranslatef(0.0, -0.5, 0.0)  


def tf_hood(node):
    glTranslatef(1.0, 0.15, 0.0)


def tf_seat(node):
    glTranslatef(0.0, 0.2, 0.0)


def tf_wheel_fl(node):
    glTranslatef(1.0, -0.15, 0.9)
    steer = node.state.get("steer", 0.0)
    glRotatef(steer, 0.0, 1.0, 0.0)

def tf_wheel_fr(node):
    glTranslatef(1.0, -0.15, -0.9)
    steer = node.state.get("steer", 0.0)
    glRotatef(steer, 0.0, 1.0, 0.0)


def tf_wheel_rl(node):
    glScalef(1.25, 1.25, 1.25)
    glTranslatef(-0.75, 0.0, 0.75)


def tf_wheel_rr(node):
    glScalef(1.25, 1.25, 1.25)
    glTranslatef(-0.75, 0.0, -0.75)


def tf_steering_wheel(node):
    glTranslatef(0.5, 0.7, -0.3)
    glRotatef(45.0, 0.0, 0.0, 1.0)
    angle = node.state.get("steer_angle", 0.0)
    glRotatef(angle, 0.0, 1.0, 0.0)

    
def tf_kart_r_door(node):
    angle = node.state.get("door_angle", 0.0)
    glTranslatef(0.025, 0.30, 0.70)
    glTranslatef(0.475, 0.0, 0.0)
    glRotatef(angle, 0.0, 1.0, 0.0)
    glTranslatef(-0.475, 0.0, 0.0)


def tf_kart_l_door(node):
    angle = node.state.get("door_angle", 0.0)

    glTranslatef(0.025, 0.30, -0.70)
    glTranslatef(0.475, 0.0, 0.0)
    glRotatef(-angle, 0.0, 1.0, 0.0)
    glTranslatef(-0.475, 0.0, 0.0)


def tf_kart_r_doorhandle(node):
    glTranslatef(-0.20, 0.05, 0.05)


def tf_kart_l_doorhandle(node):
    glTranslatef(-0.20, 0.05, -0.05)


def tf_kart_structure(node):
    pass

def tf_kart_trunk(node):
    glTranslatef(-0.80,0.70,0.0)

def tf_kart_r_bumber(node):
    glTranslatef(-1.5,0.0,0.0)

def tf_kart_f_bumber(node):
    glTranslatef(1.5,0.0,0.0)

def tf_kart_r_numplate(node):
    glTranslatef(-0.05,0.0,0.0)

def tf_kart_f_numplate(node):
    glTranslatef(0.05,0.0,0.0)

def tf_kart_roof_lights(node):
    glTranslatef(0.85, 0.1, 0.0)

def tf_kart_fr_light(node):
    glTranslatef(0.525, 0.2, 0.6)
    glRotatef(90.0, 0.0, 0.0, 1.0)

def tf_kart_fl_light(node):
    glTranslatef(0.525, 0.2,-0.6)
    glRotatef(90.0, 0.0, 0.0, 1.0)

def tf_kart_rl_light(node):
    glTranslatef(0.4, 0.2,0.0)
    glRotatef(90.0, 0.0, 0.0, 1.0)

def tf_kart_rr_light(node):
    glTranslatef(0.4, 0.2, -1.4)
    glRotatef(90.0, 0.0, 0.0, 1.0)

def tf_kart_r_wheelprotection(node):
    glTranslatef(1.0, 0.25, 0.75)

def tf_kart_l_wheelprotection(node):
    glTranslatef(1.0, 0.25, -0.75)
# ============ TRANSFORMS DA GARAGEM ============

def tf_garage_back(node):
    glTranslatef(0.0, node.state["hy"], 3.90)


def tf_garage_left(node):
    glTranslatef(-3.20, node.state["hy"], 0.20)


def tf_garage_right(node):
    glTranslatef(3.20, node.state["hy"], 0.20)


def tf_garage_roof(node):
    glTranslatef(0.0, 3.2, 0.0)


def tf_garage_door(node):
    angle = node.state.get("door_angle", 0.0)
    translate = node.state.get("door_translate", 0.0)

    glTranslatef(0.0, 1.55, -3.8)
    
    glTranslatef(0.0, 1.55, 0.0)
    
    glRotatef(angle, 1.0, 0.0, 0.0)
    
    glTranslatef(0.0, -1.55, 0.0)
    
    if angle == 90.0:
        glTranslatef(0.0, translate, 0.0)





# ---------- TRANSFORMS DO SOL ----------
def tf_sun(node):
    t = glfw.get_time()

    ORBIT_RADIUS = 40.0  
    ORBIT_SPEED  = 0.1

    x = math.cos(t * ORBIT_SPEED) * ORBIT_RADIUS
    y = math.sin(t * ORBIT_SPEED) * ORBIT_RADIUS
    z = -15 

    node.state["pos"] = (x, y, z)
    glTranslatef(x, y, z)


def upd_sun_light(node, dt):
    x, y, z = node.state.get("pos", (10,10,0))

    intensity = max(0.0, min(1.0, y / 20.0))

    glLightfv(GL_LIGHT0, GL_DIFFUSE,  (1.2 * intensity, 1.2 * intensity, 1.2 * intensity, 1.0))
    glLightfv(GL_LIGHT0, GL_SPECULAR, (1.2 * intensity, 1.2 * intensity, 1.2 * intensity, 1.0))


    glLightfv(GL_LIGHT0, GL_AMBIENT, (0.0, 0.0, 0.0, 1.0))



    glLightfv(GL_LIGHT0, GL_POSITION, (x, y, z, 1.0))

    # --------------------------
    # PASSAR A ALTURA DO SOL PARA O POSTE
    # --------------------------
    root = node.get_root()
    lp   = root.find("light_pole")
    if lp:
        lp.state["sun_y"] = y

    t = max(0.0, min(1.0, y / 20.0))

    r = (1-t)*0.02 + t*0.5
    g = (1-t)*0.05 + t*0.7
    b = (1-t)*0.10 + t*1.0

    glClearColor(r, g, b, 1.0 )  


# ---------- TRANSFORMS DO POSTE LUZ ----------    
def tf_light_pole(node):
    glTranslatef(7.0, 0.0, 0.0)

def upd_light_pole(node, dt):
    sun_y = node.state.get("sun_y", 10.0)

    t = 0.0
    if sun_y < 0:
        t = min(1.0, max(0.0, (-sun_y) / 5.0))

    if t > 0:
        glEnable(GL_LIGHT1)
    else:
        glDisable(GL_LIGHT1)

    glLightfv(GL_LIGHT1, GL_DIFFUSE,  ( 0.1 * t, 0.1 *  t,  0.1 * t, 1.0))
    glLightfv(GL_LIGHT1, GL_SPECULAR, ( 0.1 * t,  0.1 * t,  0.1 * t, 1.0))


    glLightfv(GL_LIGHT1, GL_AMBIENT, (0.6 * t, 0.6 * t, 0.6 * t, 1.0))


  #---------- TRANSFORMS DA ARVORE ----------    
def tf_tree(node):
    glTranslatef(10.0, 0.0, -5.0)    

# ----------------- CONSTRUÇÃO DA CENA -----------------

def make_scene():
    root = Node("root")

    ground = Node(
        "ground",
        geom=draw_ground,
        transform=tf_ground
    )

    # nó raiz do kart (move/roda o kart inteiro)
    kart_root = Node(
        "kart_root",
        geom=None,
        transform=tf_kart_root,
        updater=upd_kart_movement,
        state={
            "angle_y": -90.0, 
            "pos_x":  -6.0,   
            "pos_z":  0.0,   
        }
    )

    # chassis_node
    chassis_node = Node(
        "chassis_node",
        geom=geom_kart_chassis,
        transform=tf_chassis
    )

    # filhos do chassis
    hood_node = Node(
        "hood_node",
        geom=geom_kart_hood,
        transform=tf_hood
    )

    seat_node = Node(
        "seat_node",
        geom=geom_kart_seat,
        transform=tf_seat
    )

    wheel_fl = Node(
        "wheel_fl",
        geom=geom_kart_wheel,
        transform=tf_wheel_fl,
        updater=upd_front_wheel,
        state={"spin": 0.0, "steer": 0.0}
    )

    wheel_fr = Node(
        "wheel_fr",
        geom=geom_kart_wheel,
        transform=tf_wheel_fr,
        updater=upd_front_wheel,
        state={"spin": 0.0, "steer": 0.0}
    )

    wheel_rl = Node(
        "wheel_rl",
        geom=geom_kart_wheel,
        transform=tf_wheel_rl,
        updater=upd_wheel_spin,
        state={"spin": 0.0}
    )

    wheel_rr = Node(
        "wheel_rr",
        geom=geom_kart_wheel,
        transform=tf_wheel_rr,
        updater=upd_wheel_spin,
        state={"spin": 0.0}
    )

    steering_wheel = Node(
        "steering_wheel",
        geom=geom_kart_steering_wheel,
        transform=tf_steering_wheel,
        updater=upd_steering_wheel,
        state={"steer_angle": 0.0}
    )

    kart_structure = Node(
        "kart_structure",
        geom=geom_kart_structure,
        transform=tf_kart_structure
    )

    kart_door_r = Node(
        "kart_door_r",
        geom=geom_kart_door,
        transform=tf_kart_r_door,
        updater=upd_side_door,
        state={"door_angle": 0.0}
    )

    kart_door_l = Node(
        "kart_door_l",
        geom=geom_kart_door,
        transform=tf_kart_l_door,
        updater=upd_side_door,
        state={"door_angle": 0.0}
    )


    kart_doorhandle_r = Node(
        "kart_doorhandle_r",
        geom=geom_kart_doorhandle,
        transform=tf_kart_r_doorhandle
    )
    kart_doorhandle_l = Node(
        "kart_doorhandle_l",
        geom=geom_kart_doorhandle,
        transform=tf_kart_l_doorhandle
    )

    kart_door_r.add(kart_doorhandle_r)
    kart_door_l.add(kart_doorhandle_l)


    kart_trunk = Node(
        "kart_trunk",
        geom=geom_kart_trunk,
        transform=tf_kart_trunk
    )

    kart_bumper_front = Node(
        "kart_bumper_front",
        geom=geom_kart_bumber,
        transform=tf_kart_f_bumber
    )

    
    kart_bumper_back = Node(
        "kart_bumper_back",
        geom=geom_kart_bumber,
        transform=tf_kart_r_bumber
    )

    kart_r_numplate = Node(
        "kart_r_numplate",
        geom=geom_kart_numplate,
        transform=tf_kart_r_numplate
    )
    kart_f_numplate = Node(
        "kart_f_numplate",
        geom=geom_kart_numplate,
        transform=tf_kart_f_numplate
    )
    kart_roof_lights = Node(
        "kart_roof_lights", 
        geom=geom_kart_roof_lights,
        transform=tf_kart_roof_lights
    )

    kart_fr_lights = Node(
        "kart_fr_lights",
        geom=geom_kart_lights_front,
        transform=tf_kart_fr_light
    )
    kart_fl_lights = Node(
        "kart_fr_lights",
        geom=geom_kart_lights_front,
        transform=tf_kart_fl_light
    )
    kart_rl_lights = Node(
        "kart_rl_lights",
        geom=geom_kart_lights_rear,
        transform=tf_kart_rl_light
    )
    kart_rr_lights = Node(
        "kart_rr_lights",
        geom=geom_kart_lights_rear,
        transform=tf_kart_rr_light
    )
    kart_trunk_door = Node(
        "kart_trunk_door",
        geom=geom_kart_trunk_door,
        transform=None
    )

    kart_r_wheelprotection = Node(
        "kart_r_wheelprotection",
        geom=geom_kart_wheelprotection,
        transform=tf_kart_r_wheelprotection
    )
    kart_l_wheelprotection = Node(
        "kart_l_wheelprotection",
        geom=geom_kart_wheelprotection,
        transform=tf_kart_l_wheelprotection
    )

    kart_trunk.add(kart_trunk_door)
    kart_trunk.add(kart_rl_lights)
    kart_trunk.add(kart_rr_lights)
    hood_node.add(kart_fl_lights)
    hood_node.add(kart_fr_lights)
    kart_bumper_back.add(kart_r_numplate)
    kart_bumper_front.add(kart_f_numplate)
    kart_structure.add(kart_roof_lights)

    # montar a árvore do kart:
    chassis_node.add(
        hood_node,
        seat_node,
        wheel_fl, wheel_fr, wheel_rl, wheel_rr,
        steering_wheel,
        kart_structure,
        kart_door_r,kart_door_l,
        kart_trunk,
        kart_bumper_front, kart_bumper_back,
        kart_r_wheelprotection, kart_l_wheelprotection
    )

    kart_root.add(chassis_node)


     # ============ GARAGEM ============

    garage_back = Node(
    "garage_back",
    geom=geom_garage_wall,
    transform=tf_garage_back,
    state={"hx": 3.20, "hy": 1.66, "hz": 0.40}
)


    garage_left = Node(
    "garage_left",
    geom=geom_garage_wall,
    transform=tf_garage_left,
    state={"hx": 0.20, "hy": 1.66, "hz": 4.1}
    )

    garage_right = Node(
    "garage_right",
    geom=geom_garage_wall,
    transform=tf_garage_right,
    state={"hx": 0.20, "hy": 1.66,"hz": 4.1}
    )


    garage_roof = Node(
    "garage_roof",
    geom=geom_garage_wall,
    transform=tf_garage_roof,
    state={"hx": 3.20, "hy": 0.12, "hz": 3.90}
    )


    garage_root = Node(
        "garage_root",
        transform=lambda n: (
            glTranslatef(2.0, 0.0, 0.0),  
            glRotatef(180, 0, 1, 0)      
     )
    )

    garage_door = Node(
    "garage_door",
    geom=geom_garage_door,
    transform=tf_garage_door,
    updater=upd_garage_door  
)
    garage_root.add(garage_back, garage_left, garage_right, garage_roof, garage_door)

# ---------- SOL ----------
    sun = Node(
        "sun",
        geom=geom_sun,
        transform=tf_sun,
        updater=upd_sun_light
    )
 # ---------- POSTE DE LUZ ----------   
    light_pole = Node(
        "light_pole",
        geom=geom_light_pole,
        transform=tf_light_pole,
        updater=upd_light_pole,
        state={"sun_y": 10.0}
    )  

 # ---------- ARVORE ----------    
    tree = Node(
        "tree",
        geom=geom_tree,
        transform=tf_tree  
    )    

    # raiz do mundo
    root.add(ground, garage_root, kart_root, sun, light_pole,tree)
    return root    