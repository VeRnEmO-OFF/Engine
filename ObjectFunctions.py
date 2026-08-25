import inspect
import os
import time
import math
import pygame
import ProgramFunctions
from ProgramFunctions import *

OBJECTS = get_var("session.json", "OBJECTS")
system_message(OBJECTS)
BG_COLOR = (0, 0, 0)
# Все клавиши
KEY_NAMES = {
    pygame.K_BACKSPACE: "Backspace",
    pygame.K_TAB: "Tab",
    pygame.K_CLEAR: "Clear",
    pygame.K_RETURN: "Enter",
    pygame.K_PAUSE: "Pause",
    pygame.K_ESCAPE: "Escape",
    pygame.K_SPACE: "Space",
    pygame.K_EXCLAIM: "!",
    pygame.K_QUOTEDBL: '"',
    pygame.K_HASH: "#",
    pygame.K_DOLLAR: "$",
    pygame.K_AMPERSAND: "&",
    pygame.K_QUOTE: "'",
    pygame.K_LEFTPAREN: "(",
    pygame.K_RIGHTPAREN: ")",
    pygame.K_ASTERISK: "*",
    pygame.K_PLUS: "+",
    pygame.K_COMMA: ",",
    pygame.K_MINUS: "-",
    pygame.K_PERIOD: ".",
    pygame.K_SLASH: "/",
    pygame.K_0: "0",
    pygame.K_1: "1",
    pygame.K_2: "2",
    pygame.K_3: "3",
    pygame.K_4: "4",
    pygame.K_5: "5",
    pygame.K_6: "6",
    pygame.K_7: "7",
    pygame.K_8: "8",
    pygame.K_9: "9",
    pygame.K_COLON: ":",
    pygame.K_SEMICOLON: ";",
    pygame.K_LESS: "<",
    pygame.K_EQUALS: "=",
    pygame.K_GREATER: ">",
    pygame.K_QUESTION: "?",
    pygame.K_AT: "@",
    pygame.K_LEFTBRACKET: "[",
    pygame.K_BACKSLASH: "\\",
    pygame.K_RIGHTBRACKET: "]",
    pygame.K_CARET: "^",
    pygame.K_UNDERSCORE: "_",
    pygame.K_BACKQUOTE: "`",
    pygame.K_a: "a",
    pygame.K_b: "b",
    pygame.K_c: "c",
    pygame.K_d: "d",
    pygame.K_e: "e",
    pygame.K_f: "f",
    pygame.K_g: "g",
    pygame.K_h: "h",
    pygame.K_i: "i",
    pygame.K_j: "j",
    pygame.K_k: "k",
    pygame.K_l: "l",
    pygame.K_m: "m",
    pygame.K_n: "n",
    pygame.K_o: "o",
    pygame.K_p: "p",
    pygame.K_q: "q",
    pygame.K_r: "r",
    pygame.K_s: "s",
    pygame.K_t: "t",
    pygame.K_u: "u",
    pygame.K_v: "v",
    pygame.K_w: "w",
    pygame.K_x: "x",
    pygame.K_y: "y",
    pygame.K_z: "z",
    pygame.K_DELETE: "Delete",
    pygame.K_KP0: "KP0",
    pygame.K_KP1: "KP1",
    pygame.K_KP2: "KP2",
    pygame.K_KP3: "KP3",
    pygame.K_KP4: "KP4",
    pygame.K_KP5: "KP5",
    pygame.K_KP6: "KP6",
    pygame.K_KP7: "KP7",
    pygame.K_KP8: "KP8",
    pygame.K_KP9: "KP9",
    pygame.K_KP_PERIOD: "KP.",
    pygame.K_KP_DIVIDE: "KP/",
    pygame.K_KP_MULTIPLY: "KP*",
    pygame.K_KP_MINUS: "KP-",
    pygame.K_KP_PLUS: "KP+",
    pygame.K_KP_ENTER: "KPEnter",
    pygame.K_KP_EQUALS: "KP=",
    pygame.K_UP: "Up",
    pygame.K_DOWN: "Down",
    pygame.K_RIGHT: "Right",
    pygame.K_LEFT: "Left",
    pygame.K_INSERT: "Insert",
    pygame.K_HOME: "Home",
    pygame.K_END: "End",
    pygame.K_PAGEUP: "PageUp",
    pygame.K_PAGEDOWN: "PageDown",
    pygame.K_F1: "F1",
    pygame.K_F2: "F2",
    pygame.K_F3: "F3",
    pygame.K_F4: "F4",
    pygame.K_F5: "F5",
    pygame.K_F6: "F6",
    pygame.K_F7: "F7",
    pygame.K_F8: "F8",
    pygame.K_F9: "F9",
    pygame.K_F10: "F10",
    pygame.K_F11: "F11",
    pygame.K_F12: "F12",
    pygame.K_F13: "F13",
    pygame.K_F14: "F14",
    pygame.K_F15: "F15",
    pygame.K_NUMLOCK: "NumLock",
    pygame.K_CAPSLOCK: "CapsLock",
    pygame.K_SCROLLOCK: "ScrollLock",
    pygame.K_RSHIFT: "RShift",
    pygame.K_LSHIFT: "LShift",
    pygame.K_RCTRL: "RCtrl",
    pygame.K_LCTRL: "LCtrl",
    pygame.K_RALT: "RAlt",
    pygame.K_LALT: "LAlt",
    pygame.K_RMETA: "RMeta",
    pygame.K_LMETA: "LMeta",
    pygame.K_LSUPER: "LSuper",
    pygame.K_RSUPER: "RSuper",
    pygame.K_MODE: "Mode",
    pygame.K_HELP: "Help",
    pygame.K_PRINT: "Print",
    pygame.K_SYSREQ: "SysReq",
    pygame.K_BREAK: "Break",
    pygame.K_MENU: "Menu",
    pygame.K_POWER: "Power",
    pygame.K_EURO: "Euro",
}

TEXTURES = load_sprites(path=os.path.join(get_var(SESSION_PATH, 'project_path'),'Resources', 'Sprites'))
system_message("TEXTURES -", TEXTURES)

SOUNDS = load_sounds(path=os.path.join(get_var(SESSION_PATH, 'project_path'),'Resources', 'Sounds'))
system_message("SOUNDS -", SOUNDS)

def system_message(*args, **kwargs):
    """Сообщения с временем и названием файла"""
    # Получаем вызывающий файл из стека функций (это список)
    caller_frame = inspect.stack()[1] # получаем файл исполнитель функции из стека
    caller_file = os.path.basename(caller_frame.filename) # Название файла из стека
    text = ' '.join(str(arg) for arg in args) # Создаём 1 строку для вывода
    message_time = time.strftime("%I:%M:%S", time.localtime())
    return print(f"[{message_time}] {caller_file}:: {text}")

def is_pressed(key):
    keys = pygame.key.get_pressed()
    pressed = []
    for key_code in range(len(keys)):
        if keys[key_code]:
            pressed.append(pygame.key.name(key_code))
    if key in pressed:
        return True
    else:
        return False

def change_scene(scene_name):
    current_scene = get_var(SESSION_PATH, 'played_scene')
    scene_obj_path = os.path.join(PLAYED_PROJECT_PATH, current_scene, "scene_objects.json")
    system_message("scene_obj_path",scene_obj_path)
    system_message("OBJECT -", OBJECTS)
    modify_var(scene_obj_path, 'OBJECTS', OBJECTS)
    modify_var(SESSION_PATH, "change_scene_to", os.path.join(get_var(SESSION_PATH, 'project_path'), scene_name))

def get_rotate_to(object_name, target, type="deg", change_rotation=True):
    try:
        pos = OBJECTS[object_name]['pos']
        dx = target[0] - pos[0]
        dy = target[1] - pos[1]
        angle = math.degrees(math.atan2(-dy, dx)) - 90
        if type == "rad":
            angle_rad = math.radians(angle)
            return angle_rad
        elif type == "deg":
            return angle
    except Exception as e:
        system_message("get_rotate_to",e)

def get_rotate(object_name):
    try:
        return globals()['OBJECTS'][object_name]['rotation']
    except Exception as e:
        system_message("get_rotate",e)

def rotate(object_name, rotation):
    try:
        globals()['OBJECTS'][object_name]['rotation'] = rotation
    except Exception as e:
        system_message("rotate",e)

def go_to_mouse_x(object_name):
    try:
        globals()['OBJECTS'][object_name]['pos'][0] = int(pygame.mouse.get_pos()[0])
    except Exception as e:
        system_message("go_to_mouse_x",e)

def go_to_mouse_y(object_name):
    try:
        globals()['OBJECTS'][object_name]['pos'][1] = int(pygame.mouse.get_pos()[1])
    except Exception as e:
        system_message("go_to_mouse_y",e)

def get_object_pos(object_name):
    try:
        posx = globals()['OBJECTS'][object_name]['pos'][0]
        posy = globals()['OBJECTS'][object_name]['pos'][1]
        return posx, posy
    except Exception as e:
        system_message("get_object_pos",e)

def set_sprite(object_name, texture):
    try:
        globals()['OBJECTS'][object_name]['texture'] = texture
    except Exception as e:
        system_message("set_sprite",e)

def get_size(object_name):
    try:
        return globals()['OBJECTS'][object_name]['size']
    except Exception as e:
        system_message("get_size",e)

def set_size(object_name, size):
    try:
        globals()['OBJECTS'][object_name]['size'][0] = size[0]
        globals()['OBJECTS'][object_name]['size'][1] = size[1]
    except Exception as e:
        system_message("set_size",e)

def set_pos(object_name, pos):
    try:
        globals()['OBJECTS'][object_name]['pos'][0] = float(pos[0])
        globals()['OBJECTS'][object_name]['pos'][1] = float(pos[1])
    except Exception as e:
        system_message("set_pos",e)

def smooth_set_pos(object_name, pos, slide_speed=0.1):
    try:
        return set_pos(object_name, (
                       float(get_object_pos(object_name)[0]) + float(float(slide_speed) * float(pos[0] - float(get_object_pos(object_name)[0])) / 100),
                       float(get_object_pos(object_name)[1]) + float(float(slide_speed) * float(pos[1] - float(get_object_pos(object_name)[1])) / 100)
                       ))
    except Exception as e:
        system_message("smooth_set_pos",e)

def add_object(name="Стёпа", pos:list=(0, 0), size:list=(100, 100), rotation:int=0, alpha:int=100, tags:list=(), texture=None, scene=""):
    try:
        globals()['OBJECTS'][name] = {'pos':pos, 'size':size, 'rotation':rotation, 'alpha':alpha, 'tags':tags, 'texture':texture, 'scene':scene}
    except Exception as e:
        system_message("add_object",e)

def del_object(object):
    try:
        if object in globals()['OBJECTS']:
            globals()['OBJECTS'].pop(object)
    except Exception as e:
        system_message("del_object",e)

def play_sound(name, vol):
    try:
        sound = pygame.mixer.Sound(SOUNDS[name])
        sound.set_volume(vol)
        sound.play()
    except Exception as e:
        system_message("del_object",e)


def is_collide(object_name_1, object_name_2):
    obj1 = globals()['OBJECTS'][object_name_1]
    obj2 = globals()['OBJECTS'][object_name_2]
    rect1 = pygame.Rect(obj1['pos'][0], obj1['pos'][1],
                        obj1['size'][0], obj1['size'][1])
    rect2 = pygame.Rect(obj2['pos'][0], obj2['pos'][1],
                        obj2['size'][0], obj2['size'][1])
    return rect1.colliderect(rect2)


