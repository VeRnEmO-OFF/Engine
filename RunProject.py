import os
import time
import pygame
import subprocess
import threading
from pygame import FULLSCREEN
from ProgramFunctions import *
import ObjectFunctions
from ObjectFunctions import *


MAIN_PATH = os.path.dirname(os.path.realpath(__file__))
system_message("MAIN_PATH -",MAIN_PATH)
PROJECTS_FOLDER_PATH = os.path.join(MAIN_PATH, '_Projects')
system_message("PROJECTS_FOLDER_PATH -",PROJECTS_FOLDER_PATH)


project_name = get_var(os.path.join(MAIN_PATH, "session.json"), 'played_project')
PLAYED_PROJECT_PATH = os.path.join(MAIN_PATH, '_Projects', project_name)
system_message("PLAYED_PROJECT_PATH -",PLAYED_PROJECT_PATH)
system_message("Поиск файла свойств запуска...:\n")
dir_list(PLAYED_PROJECT_PATH)

DISPLAY_SIZE = pygame.display.get_desktop_sizes()
# если чо там по моникам, 1 элемент это список с высотой и шириной 1 моника, если моника два то будет 2 элемента

CONF_FILE_PATH = ""
CONF_FILE_PATH = dir_find(PLAYED_PROJECT_PATH, name="conf.json")
system_message("CONF_FILE_PATH -",CONF_FILE_PATH)
with open(CONF_FILE_PATH, "r", encoding='utf-8') as file:
    PROJECT_CONFIG = json.load(file)
system_message("PROJECT_CONFIG -",PROJECT_CONFIG)

START_SCENE_NAME = get_var(CONF_FILE_PATH, 'start_scene')
system_message("START_SCENE_NAME -",START_SCENE_NAME)
START_SCENE_PATH = os.path.join(PLAYED_PROJECT_PATH, START_SCENE_NAME)
system_message("START_SCENE_PATH -",START_SCENE_PATH)

CURRENT_SCENE_NAME = START_SCENE_NAME
system_message("CURRENT_SCENE_NAME -",CURRENT_SCENE_NAME)
CURRENT_SCENE_PATH = START_SCENE_PATH
system_message("CURRENT_SCENE_PATH -",CURRENT_SCENE_PATH)


PROJECT_RESOURCES_PATH = os.path.join(PLAYED_PROJECT_PATH, get_var(CONF_FILE_PATH, 'resources_path'))
system_message("PROJECT_RESOURCES_PATH -",PROJECT_RESOURCES_PATH)
PROJECT_SPRITES_PATH = os.path.join(PLAYED_PROJECT_PATH, get_var(CONF_FILE_PATH, 'resources_path'), 'Sprites')
system_message("PROJECT_SPRITES_PATH -",PROJECT_SPRITES_PATH)
PROJECT_SOUNDS_PATH = os.path.join(PLAYED_PROJECT_PATH, get_var(CONF_FILE_PATH, 'resources_path'), 'Sounds')
system_message("PROJECT_SOUNDS_PATH -",PROJECT_SOUNDS_PATH)


TEXTURES = load_sprites(path=PROJECT_SPRITES_PATH)
system_message("TEXTURES -", TEXTURES)

SOUNDS = load_sounds(path=PROJECT_SOUNDS_PATH)
system_message("SOUNDS -",get_var("session.json", 'SOUNDS'))
# Объект имеет параметры: name, pos[], size[], rotation, alpha, tags[], texture
OBJECTS = {}
modify_var('session.json', 'OBJECTS', {})
system_message("OBJECTS -",get_var("session.json", 'OBJECTS'))

CLONES = {}
system_message("CLONES -",get_var("session.json", 'CLONES'))

if PLAYED_PROJECT_CONFIG['screen_conf']['mode'] == "window":
    PROJECT_SCREEN = pygame.display.set_mode((PLAYED_PROJECT_CONFIG['screen_conf']['resolutionX'], PLAYED_PROJECT_CONFIG['screen_conf']['resolutionY']))
elif PLAYED_PROJECT_CONFIG['screen_conf']['mode'] == "full":
    PROJECT_SCREEN = pygame.display.set_mode((DISPLAY_SIZE[0][0], DISPLAY_SIZE[0][1]), FULLSCREEN)
pygame.display.set_caption("Проект")

# Список переменных доступных пользователю, а так же отключение ненужного
user_globals = {
    "__builtins__": {"__import__":__import__, "__file__":__file__},  # отключаем опасные функции (open, eval, import) и разрешаем только мои функции
    "float" : float,
    "int": int,
    "min": min,
    "max": max,
    "len": len,
    "range": range,
    "print": print,
    "rotate" : rotate,
    "set_pos": set_pos,
    "set_size": set_size,
    "get_size": get_size,
    "play_sound": play_sound,
    "del_object": del_object,
    "add_object": add_object,
    "set_sprite": set_sprite,
    "get_rotate" : get_rotate,
    "is_pressed" : is_pressed,
    "change_scene": change_scene,
    "go_to_mouse_x": go_to_mouse_x,
    "go_to_mouse_y": go_to_mouse_y,
    "get_rotate_to" : get_rotate_to,
    "smooth_set_pos": smooth_set_pos,
    "get_object_pos": get_object_pos,
}

def run_scrypt(scrypt_code, user_globals=globals()['user_globals']):
    try:
        exec(scrypt_code, user_globals)
    except Exception as e:
        system_message(f"Ошибка run_scrypt: {e}")

system_message("Ресурсы проекта загружены. Попытка старта сцены...\n")

def play_scene(scene_path=CURRENT_SCENE_PATH):
    system_message("SCENE PATH TO START SCRYPT -", scene_path)
    for scrypt in os.listdir(scene_path):
        scrypt_path = os.path.join(scene_path, scrypt)
        threading.Thread(target=run_scrypt, args=(scrypt_path, )).start()

def play_scene_once(scene_path=CURRENT_SCENE_PATH):
    modify_var(SESSION_PATH, 'played_scene', os.path.split(scene_path)[-1])
    system_message("SCENE PATH TO START SCRYPT -", scene_path)
    for scrypt in os.listdir(scene_path):
        if scrypt.endswith(".py"):
            scrypt_path = os.path.join(scene_path, scrypt)
            system_message("scrypt path -", scrypt_path)
            with open(scrypt_path, "r", encoding="utf-8") as code:
                code = code.read()
            threading.Thread(target=run_scrypt, args=(code, )).start()

def change_scene(scene_path=CURRENT_SCENE_PATH):
    if get_var(SESSION_PATH, "change_scene_to") != "STOP":
        play_scene_once(get_var(SESSION_PATH, "change_scene_to"))
    else:
        pass

def draw_objects(output=False, debug=False):
    OBJECTS = ObjectFunctions.OBJECTS
    rects = []
    PROJECT_SCREEN.fill(WHITE)
    bg_rect = pygame.Rect(0, 0, PLAYED_PROJECT_CONFIG['screen_conf']['resolutionX'], PLAYED_PROJECT_CONFIG['screen_conf']['resolutionY'])
    rects.append(bg_rect)
    if OBJECTS is None:
        return
    try:
        for obj in list(OBJECTS.keys()):
            if OBJECTS[obj]['scene'] == get_var(SESSION_PATH, 'played_scene'):
                if output: system_message('SCENE -', get_var(SESSION_PATH, 'played_scene'), 'OBJ scene -', OBJECTS[obj]['scene'], "OBJ -", OBJECTS[obj])
                if get_var(SESSION_PATH, 'played_scene') != OBJECTS[obj]['scene']:
                    return
                if output: system_message("OBJECT -", obj)
                pos = OBJECTS[obj]['pos']
                texture = OBJECTS[obj]['texture']
                if texture is not None:
                    texture_scaled = pygame.transform.scale(TEXTURES[OBJECTS[obj]['texture']], (OBJECTS[obj]['size'][0], OBJECTS[obj]['size'][1]))
                    texture_rotated = pygame.transform.rotate(texture_scaled, OBJECTS[obj]['rotation'])
                    rect = texture_rotated.get_rect(center=(pos[0], pos[1]))
                    PROJECT_SCREEN.blit(texture_rotated, rect)
                    rects.append(rect)
                    if debug:
                        pygame.draw.rect(PROJECT_SCREEN, (255, 0, 0), rect, 1)

                    #pygame.display.update(rect)
        for rect in rects:
            pygame.display.update(rect)
    except Exception as e:
        system_message("Draw_objects:", e)


play_scene_once(CURRENT_SCENE_PATH)


fps_marker = time.time() + 1
fps = 0
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            modify_var('session.json', 'played_project', "")
            modify_var('session.json', 'project_path', "")
            modify_var('session.json', 'py_init', 0)
            modify_var('session.json', "change_scene_to", "STOP")
            system_message("Завершение...")
            QUIT()

    if get_var(SESSION_PATH, "change_scene_to") != "None":
        change_scene(get_var(SESSION_PATH, "change_scene_to"))

    if fps_marker < time.time():
        draw_text(PROJECT_SCREEN, pos=[200, 200], string=str(fps), color=BLACK)
        #system_message("FPS -", fps)
        fps = 0
        fps_marker = time.time() + 1

    draw_objects()
    fps += 1
    time.sleep(1/240)






