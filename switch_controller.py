import pygame
import pynput
from typing import Optional
from abc import ABC

# def presser(mapping, type):
    
#     def keyboard_presser(mapping):
#         keyboard.press(mapping)
    
#     if type == 'keyboard':
#         return keyboard_presser(mapping)
    
    
keyboard = pynput.keyboard.Controller()

class My_button_mapper(ABC):
    def __init__(self, mapping, key_type: Optional[chr] = 'i'):
        self._state = False
        self._map = mapping
        self._type = key_type
        self._keypresser = pynput.keyboard.Controller() 
    
    @property
    def mapping(self):
        return self._map
    
    def press(self):
        if self._type == 'c':
            self._keypresser.press(self._map)
            self._keypresser.release(self._map)
        elif self._type == 'i':
            if not self._state:
                self._keypresser.press(self._map)
                self._state = True
    
    def release(self):
        if self._state and self._type == 'i':
            self._keypresser.release(self._map)
            self._state = False

class My_button_mapper_key(My_button_mapper):
    def __init__(self, mapping, key_type: Optional[chr] = 'i'):
        super().__init__(mapping, key_type)
        self._keypresser = pynput.keyboard.Controller() 
    
class My_button_mapper_mouse(My_button_mapper):
    def __init__(self, mapping, key_type: Optional[chr] = 'i'):
        super().__init__(mapping, key_type)
        self._keypresser = pynput.mouse.Controller()
            
            
pygame.init()

clock = pygame.time.Clock()

# Initialize the joystick
pygame.joystick.init()

# Ensure a joystick is connected
if pygame.joystick.get_count() < 1:
    print("No controller found!")
else:
    controller = pygame.joystick.Joystick(0)
    controller.init()
    print(f"Using controller: {controller.get_name()}")

pygame.event.pump()  # Updates pygame event queue

mouse = pynput.mouse.Controller()

stickdrift = 0.3
def get_axis(axis):
    axis = controller.get_axis(axis)  # Right joystick X-axis
    if abs(axis) < stickdrift:
        axis = 0.0
    return axis

# Scale movement speed
mouse_speed = 15  # Adjust for sensitivity




button_to_mapper = {
    0: My_button_mapper_key('d', 'c'),
    1: My_button_mapper_key('x', 'c'),
    2: My_button_mapper_key('w', 'c'),
    3: My_button_mapper_key('a', 'c'),
    5: My_button_mapper_key(pynput.keyboard.Key.esc),
    6: My_button_mapper_key('s'),
    9: My_button_mapper_mouse(pynput.mouse.Button.right),
    10: My_button_mapper_mouse(pynput.mouse.Button.left),
    11: My_button_mapper_key(pynput.keyboard.Key.up),
    12: My_button_mapper_key(pynput.keyboard.Key.down),
    13: My_button_mapper_key(pynput.keyboard.Key.left),
    14: My_button_mapper_key(pynput.keyboard.Key.right),
}

# Main loop to read inputs
try:
    while True:
        pygame.event.pump()  # Updates pygame event queue
        
        if controller.get_button(4):
            raise KeyboardInterrupt
        
        # Read joystick axis for mouse movement (adjust axis based on your controller's setup)
        x_axis = get_axis(2)  # Right joystick X-axis
        y_axis = get_axis(3)  # Right joystick Y-axis
        
        
        
        # Update mouse position based on joystick input
        new_x = int(x_axis * mouse_speed)
        new_y = int(y_axis * mouse_speed)
        
        # Move mouse to new position
        mouse.move(new_x, new_y)
        
        # Check each button on the controller
        for button in range(controller.get_numbuttons()):
            if controller.get_button(button):
                print(f"Button {button} is pressed.")
        
        for button, map in button_to_mapper.items():
            if controller.get_button(button):
                map.press()
            else:
                map.release()
                
        # Cap the frame rate to 60 FPS
        clock.tick(10)  # Limits the loop to 60 frames per second
        
except KeyboardInterrupt:
    print("Exited")
finally:
    pygame.quit()
