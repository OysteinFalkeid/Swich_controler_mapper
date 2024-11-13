import keyboard as key
import numpy as np

import sched, time

def do_something(scheduler):
    scheduler.enter(0.3, 1, do_something, (scheduler,))
    #key.record()
    for row in screen:
        for pixel in row:
            print(pixel, end='')
        print()



solid_char = chr(9608)
space_char = ' w'

screen = np.full((20, 20), ' ', dtype='U1')
cursur_pos = [10, 0]

screen[cursur_pos[0], cursur_pos[1]] = solid_char
    
my_scheduler = sched.scheduler(time.time, time.sleep)
my_scheduler.enter(1, 1, do_something, (my_scheduler,))
my_scheduler.run()  

def w_pressed():
    screen[cursur_pos[0], cursur_pos[1]] = space_char
    cursur_pos[0] = cursur_pos[0] + 1
    screen[cursur_pos[0], cursur_pos[1]] = solid_char

key.add_hotkey('w', w_pressed)