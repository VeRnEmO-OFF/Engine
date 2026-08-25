import math
import ObjectFunctions
from ObjectFunctions import *
modify_var(SESSION_PATH, 'change_scene_to', "None")

add_object(texture="pause_button", pos=[50, 50], name='jjj', scene='Пауза')
system_message(OBJECTS)
play_sound('vast', 0.05)
while True:
    if get_var(SESSION_PATH, "change_scene_to") != "None":
        break
    mouse = pygame.mouse.get_pos()
    pos = get_object_pos('jjj')
    smooth_set_pos('jjj', mouse)

