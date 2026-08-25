import inspect
import os
import threading
import time
import json
import pygame
import CONSTANTS
from CONSTANTS import *

hold_time = 0
is_action = False
scroll = 0

def system_message(*args, **kwargs):
    """Сообщения с временем и названием файла"""
    # Получаем вызывающий файл из стека функций (это список)
    caller_frame = inspect.stack()[1] # получаем файл исполнитель функции из стека
    caller_file = os.path.basename(caller_frame.filename) # Название файла из стека
    text = ' '.join(str(arg) for arg in args) # Создаём 1 строку для вывода
    message_time = time.strftime("%I:%M:%S", time.localtime())
    return print(f"[{message_time}] {caller_file}:: {text}")
    """try:
        match kwargs['color']:
            case "red":
                return print(f"\033[31m[{message_time}] {caller_file}:: {text}")
            case "green":
                return print(f"\033[32m[{message_time}] {caller_file}:: {text}")
            case "yellow":
                return print(f"\033[33m[{message_time}] {caller_file}:: {text}")
            case None:
                return print(f"[{message_time}] {caller_file}:: {text}")
    except Exception as e:
        pass
    """

def modify_var(path_to_json, var_name, value) -> None:
    """Меняет переменную в файле формата json"""
    with open(path_to_json, "r", encoding='utf-8') as file:
        data = json.load(file)
    data[var_name] = value
    with open(path_to_json, "w", encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def get_var(path_to_json, var_name):
    """Возвращает переменную в файле формата json"""
    try:
        with open(path_to_json, "r", encoding='utf-8') as file:
            data = json.load(file)
            value = data[var_name]
        return value
    except Exception as e:
        return None

def dir_list(dir, in_dir="", output=False):
    """Выводит список файлов/директорий по указанному пути"""
    for file in os.listdir(os.path.join(in_dir, dir)):
        if output:
            system_message(os.path.join(dir, file))
        if os.path.isdir(os.path.join(dir, file)):
            dir_list(os.path.join(dir, file))

def dir_find(dir, in_dir="", name=""):
    """Возвращает путь к искомому файлу"""
    for file in os.listdir(os.path.join(in_dir, dir)):
        if file == name:
            return os.path.join(dir, file)
        elif os.path.isdir(os.path.join(dir, file)):
            dir_list(os.path.join(dir, file))


if get_var('session.json', 'py_init') != 1:

    system_message("Прямой запуск... Попытка инициализации...")
    MAIN_PATH = os.path.dirname(os.path.realpath(__file__))
    system_message("MAIN_PATH -",MAIN_PATH)

    SESSION_PATH = os.path.join(MAIN_PATH, "session.json")
    system_message("SESSION_PATH -",SESSION_PATH)


    if not os.path.isfile(get_var('session.json', 'project_path')):
        system_message("Отсутствует ссылки на проекты... Поиск проектов...")
        for project in os.listdir(os.path.join(MAIN_PATH, "_Projects")):
            system_message(os.path.join(MAIN_PATH, "_Projects", project))
            modify_var("session.json", "project_path", os.path.join(MAIN_PATH, "_Projects", project))

    PLAYED_PROJECT_PATH = get_var(SESSION_PATH, "project_path")
    system_message("PLAYED_PROJECT_PATH -", PLAYED_PROJECT_PATH)

    PROJECT_CONF_FILE_PATH = dir_find(PLAYED_PROJECT_PATH, name="conf.json")
    system_message("PROJECT_CONF_FILE_PATH -",PROJECT_CONF_FILE_PATH)

    file = open(PROJECT_CONF_FILE_PATH, "r", encoding='utf-8')
    PLAYED_PROJECT_CONFIG = json.load(file)
    system_message("PLAYED_PROJECT_CONFIG -",PLAYED_PROJECT_CONFIG)

    pygame.init()
    pygame.font.init()
    pygame.mixer.init()
    font = pygame.font.SysFont("Arial", 30)
    MENU_SCREEN = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Проекты")

    modify_var('session.json', 'py_init', 1)
    system_message("war moded!", get_var('session.json', 'py_init'))



def load_sprites(path, with_path="", textures_list:list={}): # Загрузка ресурса по пути указанному в аргументе
    # Для текстур которые лежат сразу в папке path
    try:
        for file in os.listdir(path): # Проходимся по всем файлам находящимся по указанному пути
            if os.path.isdir(os.path.join(path, file)): # Проверка на то что файл это директория и если это истина то мы рекурсивно вызываем функцию для этой директории
                load_sprites(os.path.join(path, file), with_path+file+".")
            elif file.endswith((".png",".jpg",".webp")): # Если файл не директория, то мы выполняем эту часть кода и заносим в загруженные спрайты
                if not file.endswith(".jpg"):
                    sprite = pygame.image.load(os.path.join(path, file)).convert_alpha()
                else:
                    sprite = pygame.image.load(os.path.join(path, file)).convert()

                system_message("LOAD:", os.path.splitext(file)[0])
                if with_path != "":
                    textures_list[os.path.splitext(str(with_path)+file)[0]] = sprite
                else:
                    textures_list[os.path.splitext(file)[0]] = sprite

                system_message("LOADED:", str(with_path)+file)
        return textures_list
    except Exception as e:
        system_message("!!! Ошибка загрузки текстур: "+str(e))


def load_sounds(path, with_path="", sounds_list:list={}): # Загрузка ресурса по пути указанному в аргументе
    # Для звуков которые лежат сразу в папке path
    try:
        for file in os.listdir(path): # Проходимся по всем файлам находящимся по указанному пути
            if os.path.isdir(os.path.join(path, file)): # Проверка на то что файл это директория и если это истина то мы рекурсивно вызываем функцию для этой директории
                load_sounds(os.path.join(path, file), with_path+file+".")
            elif file.endswith((".wav",".mp3",".ogg")): # Если файл не директория, то мы выполняем эту часть кода и заносим в загруженные звуки
                sound = pygame.mixer.Sound(os.path.join(path, file))
                system_message("LOAD:", os.path.splitext(file)[0])
                if with_path != "":
                    sounds_list[os.path.splitext(str(with_path)+file)[0]] = sound
                else:
                    sounds_list[os.path.splitext(file)[0]] = sound
                system_message("LOADED:", str(with_path)+file)
        return sounds_list
    except Exception as e:
        system_message("!!! Ошибка загрузки звуков: "+str(e))


def draw_rect(screen, pos:list, size:list, color, auto_update=False) -> None:
    """Отображает прямоугольник, что указан в арг. добавляя зону отрисовки в кадр"""
    rect = pygame.Rect(pos[0], pos[1], size[0], size[1])
    pygame.draw.rect(screen, color, rect)
    if auto_update: pygame.display.update(rect)

def draw_sprite(screen, sprite, pos:list, size:list, alpha=100, auto_update=False) -> None:
    """Отображает спрайт, что указан в арг. добавляя зону отрисовки в кадр"""
    scaled_sprite = pygame.transform.scale(sprite, (size[0], size[1])).set_alpha(alpha)
    rect = pygame.Rect(pos[0], pos[1], size[0], size[1])
    screen.blit(scaled_sprite, rect)
    if auto_update: pygame.display.update(rect)

def draw_text(screen, string="", pos=(0, 0), color=BLACK, auto_update=False):
    text = font.render(string, True, color)
    screen.blit(text, pos)
    rect = pygame.Rect(pos[0], pos[1], 800, 50)
    if auto_update: pygame.display.update(rect)

class Button:
    def __init__(self, name, size:list=(100, 100), pos:list=(0, 0), string:str="Empty", color=WHITE, tap_action=None, args=(), scrolling=False, hover_action=None, hover_args=()):
        self.name = name
        self.size = size
        self.pos = pos
        self.string = string
        self.color = color
        self.hover_action = hover_action
        self.hover_args = hover_args
        self.tap_action = tap_action
        self.args = args
        self.scrolling = scrolling

    def set_args(self, value):
        self.args = value

    def set_hover_args(self, value):
        self.hover_args = value

    def draw(self, screen, auto_update=False):
        if self.is_hover():
            draw_rect(screen, self.pos, self.size,
                      (self.color[0], self.color[1], self.color[2]))
            pygame.draw.rect(screen, (255 - self.color[0], 255 - self.color[1], 255 - self.color[2]), (self.pos[0], self.pos[1], self.size[0], self.size[1]), 3)
            draw_text(screen, str(" >" + self.string), (self.pos[0], self.pos[1]+5),
                      (255 - self.color[0], 255 - self.color[1], 255 - self.color[2]))
            try:
                if self.is_click():
                    self.tap_action(self.args)
            except Exception as e:
                system_message("Class BUTTONS Ошибка клика: "+str(e))
        else:
            draw_rect(screen, self.pos, self.size, self.color)
            draw_text(screen, str(" " + self.string), (self.pos[0], self.pos[1]+5),
                      (255 - self.color[0], 255 - self.color[1], 255 - self.color[2]))
        if auto_update: pygame.display.update((self.pos[0], self.pos[1], self.size[0], self.size[0]))

    def is_hover(self):
        mouse_pos = pygame.mouse.get_pos()
        if mouse_pos[0] in range(self.pos[0], self.pos[0] + self.size[0]) and mouse_pos[1] in range(self.pos[1], self.pos[1] + self.size[1]):
            return True
        else:
            return False

    def is_click(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()
        if mouse_pressed[0]:
            if pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1]).collidepoint(mouse_pos):
                return True
        return False
#def button(screen, size:list=[100, 100], pos:list=[0, 0], string:str="", color=WHITE, action=None, args=(), scrolling=False, hover_action=None, hover_args=()) -> None:
#
#    rect = pygame.Rect(pos[0], pos[1], size[0], size[1])
#    if scrolling:
#        pos[1] += globals()['scroll'] * size[1]
#        globals()['scroll'] = max(0, globals()['scroll'])
#    globals()['hold_time']
#    if mpos[0] in range(pos[0], pos[0]+size[0]) and mpos[1] in range(pos[1], pos[1]+size[1]):
#        if pygame.mouse.get_pressed()[0]:
#            if globals()['is_action'] == False:
#                draw_rect(screen, pos, size, BLACK)
#                draw_text(screen, str(""+string), pos, WHITE)
#                globals()['is_action'] = True
#                action(args)
#        if pygame.mouse.get_pressed()[0] == False:
#            globals()['is_action'] = False
#        draw_rect(screen, pos, size, (160, 160, 160))
#        draw_text(screen, str(" "+string), pos, color)
#        if hover_action is not None:
#            hover_action(hover_args)
#    else:
#        draw_rect(screen, pos, size, color)
#        draw_text(screen, str(""+string), pos, BLACK)
#    pygame.display.update(rect)


def QUIT():
    system_message("Завершение...")
    modify_var(os.path.join(MAIN_PATH, "session.json"), "py_init", 0)
    system_message("Py_init:", get_var(os.path.join(MAIN_PATH, "session.json"), "py_init"))
    pygame.quit()

