import math
import ObjectFunctions
from ObjectFunctions import *
modify_var(SESSION_PATH, 'change_scene_to', "None")

add_object(texture="logo", name='Стёпа', pos=[0, 0], scene='Игра')
add_object(texture="logo", pos=[200, 200], name='Серёжа', scene='Игра')
add_object(texture="pause_button", pos=[50, 50], name='Выход', scene='Игра')

while True:
    if get_var(SESSION_PATH, "change_scene_to") != "None":
        break
    mouse = pygame.mouse.get_pos()
    pos = get_object_pos('Серёжа')
    size = get_size('Серёжа')



