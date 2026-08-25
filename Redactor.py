import os.path
import subprocess
import threading
import pygame
from pygame.constants import FULLSCREEN
import ProgramFunctions
from ProgramFunctions import *
import CONSTANTS
from CONSTANTS import *

REDACTOR_SCREEN = pygame.display.set_mode((800, 600))

MAIN_PATH = os.path.dirname(os.path.realpath(__file__))
system_message("MAIN_PATH -",MAIN_PATH)
PROJECTS_FOLDER_PATH = os.path.join(MAIN_PATH, '_Projects')
system_message("PROJECTS_FOLDER_PATH -",PROJECTS_FOLDER_PATH)
PROJECT_FOLDER_PATH = get_var("session.json", "redact_project")
system_message("PROJECT_FOLDER_PATH -",PROJECT_FOLDER_PATH)
REDACT_FOLDER_PATH = get_var("session.json", "redact_dir_path")
system_message("REDACT_FOLDER_PATH -",REDACT_FOLDER_PATH)

pygame.display.set_caption("Редактор")

description_text = ""
selected_project_name = ""
formats = ['.py', '.png', '.jpg', '.jpeg']

# Вывод списка проектов и проверка валидности проекта
def check_projects(out_put=False):
    projects = []
    for id, project in enumerate(os.listdir(PROJECTS_FOLDER_PATH)):
        if "conf.json" in os.listdir(os.path.join(PROJECTS_FOLDER_PATH,project)):
            if out_put:system_message(str(id)+".",project)
            projects.append([id, project])
        else:
            if out_put:system_message(str(id)+".",project,"--- !Отсутствует файл свойств запуска!")
            projects.append([id, project])
    return projects

def change_description(obj_path) -> None:
    if get_var(os.path.join(obj_path, "conf.json"), "description") is not None:
        globals()['description_text'] = get_var(os.path.join(obj_path, "conf.json"), "description")
    else:
        globals()['description_text'] = ["Описания нет! Но есть..."]

def find_conf(path):
    for file in os.listdir(path):
        if file == "conf.json":
            return os.path.join(path, file)

def check_obj_type(conf_path):
    return get_var(conf_path, "obj_type")

def add_obj(path, obj_name):
    if not os.path.exists(obj_name):
        return os.mkdir(obj_name)
    else:
        return system_message("Каталог уже существует!")

def change_dir(path):
    if path == os.path.join(MAIN_PATH, "_Projects"):
        return run_menu()
    modify_var(os.path.join(MAIN_PATH, "session.json"), "redact_dir_path", os.path.join(path))
    globals()['REDACT_FOLDER_PATH'] = path

def draw_button_list(path, icons=False):
    try:
        for id, object in enumerate(os.listdir(path)):
            if os.path.isdir(os.path.join(path, object)):
                button = Button(name=id, size=[480, 50], pos=[10, (55*id)+10], string=str(str(object+"-")+str(get_var(os.path.join(path, object, "conf.json"), "obj_type"))), tap_action=change_dir, args=os.path.join(path, object), hover_action=change_description, hover_args=os.path.join(path, object))
            else:
                button = Button(name=id, size=[480, 50], pos=[10, (55*id)+10], string=str(" "+object), tap_action=system_message, args="---", color=(200, 200, 200))
            button.draw(REDACTOR_SCREEN)
    except Exception as e:
        system_message(str(e))

def run_menu(output=True):
    # Запускаем меню
    pygame.display.quit()
    system_message("Попытка возвращения в меню...")
    modify_var(os.path.join(MAIN_PATH, "session.json"), "redact_project", "")
    modify_var(os.path.join(MAIN_PATH, "session.json"), "redact_dir_path", "")
    subprocess.run(['python', 'Main.py'])



def draw_ui() -> None:
    REDACTOR_SCREEN.fill(GREY)
    draw_rect(REDACTOR_SCREEN, [500, 0], [600, 800], DARK_GREY)
    draw_rect(REDACTOR_SCREEN, [0, 0], [400, 800], GREY)

    for id, row in enumerate(description_text):
        draw_text(MENU_SCREEN, pos=[510, 50+35*id], string=row, color=WHITE)
    draw_text(MENU_SCREEN, pos=[510, 10], string="Описание объекта", color=WHITE)

    draw_button_list(REDACT_FOLDER_PATH, icons=True)
    return_button.draw(REDACTOR_SCREEN)
    pygame.display.update()
return_button = Button(name='return_button', size=[50, 50], pos=[510, 600 - 60], string="<", tap_action=change_dir,
           args=os.path.split(REDACT_FOLDER_PATH)[0], color=WHITE)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            QUIT()
    draw_ui()
    time.sleep(1 / 240)