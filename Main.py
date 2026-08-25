import json
import math
import os
import random
import sys
import threading
import time
from turtledemo import clock

import pygame
import subprocess

from pygame.time import Clock

import CONSTANTS
from CONSTANTS import *

with open("session_default.json", "r", encoding='utf-8') as default:
    data = json.load(default)
    with open("session.json", "w", encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

import ProgramFunctions
from ProgramFunctions import *


played_project = ""
description_text = ""
selected_project_name = ""
in_run = False

MAIN_PATH = os.path.dirname(os.path.realpath(__file__))
system_message("MAIN_PATH -",MAIN_PATH)
PROJECTS_FOLDER_PATH = os.path.join(MAIN_PATH, '_Projects')
system_message("PROJECTS_FOLDER_PATH -",PROJECTS_FOLDER_PATH)
modify_var(os.path.join(MAIN_PATH, "session.json"), "played_project", "None")
modify_var(os.path.join(MAIN_PATH, "session.json"), "py_init", 0)

game_clock = pygame.time.Clock()

# Вывод списка проектов и проверка валидности проекта
def check_projects(out_put=False):
    projects = []
    system_message("Список прокетов:")
    for id, project in enumerate(os.listdir(PROJECTS_FOLDER_PATH)):
        if "conf.json" in os.listdir(os.path.join(PROJECTS_FOLDER_PATH,project)):
            if out_put:system_message(str(id)+".",project)
            projects.append([id, project])
        else:
            if out_put:system_message(str(id)+".",project,"--- !Отсутствует файл свойств запуска!")
            projects.append([id, project])
    return projects

def run_project(path_to_project,output=True):
    # Запускаем проект
    if len(os.path.split(path_to_project)[-1]) <= 2:
        return system_message("Проект не выбран!")
    system_message("in_run:", in_run)
    if in_run != True:
        pygame.display.quit()
        system_message("Попытка запуска...", "'"+str(path_to_project)+"'")
        modify_var(os.path.join(MAIN_PATH, "session.json"), "played_project", path_to_project)
        modify_var(os.path.join(MAIN_PATH, "session.json"), "project_path", os.path.join(PROJECTS_FOLDER_PATH, path_to_project))
        subprocess.run(['python', 'RunProject.py'])
    else:
        system_message("Проект уже запускается!")

def run_redactor(path_to_project,output=True):
    # Запускаем редактор проекта
    if len(globals()['selected_project_name']) <= 2:
        return system_message("Проект не выбран!")

    pygame.display.quit()
    system_message("Попытка запуска редактора для:", "'"+str(path_to_project)+"'")
    modify_var(os.path.join(MAIN_PATH, "session.json"), "redact_project", path_to_project)
    modify_var(os.path.join(MAIN_PATH, "session.json"), "redact_dir_path", path_to_project)
    subprocess.run(['python', 'Redactor.py'])


def change_description(project_name) -> None:
    globals()['selected_project_name'] = project_name
    project_path = os.path.join(PROJECTS_FOLDER_PATH, project_name)
    if get_var(os.path.join(project_path, "conf.json"), "description") is not None:
        globals()['description_text'] = get_var(os.path.join(project_path, "conf.json"), "description")
    else:
        globals()['description_text'] = ["Описания нет! Но есть..."]

projects = check_projects(out_put=True)
project_count = len(os.listdir(PROJECTS_FOLDER_PATH))
system_message("Проекты:",projects)
def draw_menu():
    draw_rect(MENU_SCREEN, [0, 0], [400, 800], DARK_GREY)
    draw_rect(MENU_SCREEN, [400, 0], [400, 800], GREY)
    try:
        for id, project in projects:
            button = Button(name=project, size=[380, 50], color=WHITE, pos=[10, 10+(60*id)], string=project,
                            tap_action=change_description, args=project)
            button.draw(MENU_SCREEN)
        for button in menu_buttons:
            button.set_args(os.path.join(PROJECTS_FOLDER_PATH, selected_project_name))
            button.draw(MENU_SCREEN)
        for id, row in enumerate(description_text):
            draw_text(MENU_SCREEN, pos=[410, 50 + 35 * id], string=row, color=WHITE)
        draw_text(MENU_SCREEN, pos=[470, 10], string="Описание проекта", color=WHITE)
        pygame.display.update()
    except Exception as e:
        system_message('Draw menu:', e)
"""    
    button(screen=MENU_SCREEN, size=[380, 50], pos=[10, (55*id)+10], frame=frame, string=str(projects[id][1]),
        action=change_description, args=projects[id][1])
    button(screen=MENU_SCREEN, size=[180, 50], pos=[600, 600-50-10], string="Играть",
                action=run_project, args=os.path.join(PROJECTS_FOLDER_PATH, selected_project_name))
    button(screen=MENU_SCREEN, size=[180, 50], pos=[410, 600-50-10], string="Редактировать",
                action=run_redactor, args=os.path.join(PROJECTS_FOLDER_PATH, selected_project_name))

    for id, row in enumerate(description_text):
        draw_text(MENU_SCREEN, pos=[410, 50+35*id], string=row, color=WHITE)

    draw_text(MENU_SCREEN, pos=[470, 10], string="Описание проекта", color=WHITE)
"""
menu_buttons = [
    Button(name="Играть", size=[185, 50], color=WHITE, pos=[410, 540], string='Играть',
           tap_action=run_project, args=str(os.path.join(PROJECTS_FOLDER_PATH, selected_project_name))),
    Button(name="Редактировать", size=[185, 50], color=WHITE, pos=[410+195, 540], string='Редактор',
           tap_action=run_redactor, args=str(os.path.join(PROJECTS_FOLDER_PATH, selected_project_name)))]


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            QUIT()
    draw_menu()
    game_clock.tick(240)
# Завершение игры
system_message("Завершение...")
sys.exit(0)
