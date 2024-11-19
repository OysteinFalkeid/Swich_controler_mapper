import pygame
import pynput
from typing import Optional
from abc import ABC
import pydirectinput
import ctypes

# Define constants
INPUT_MOUSE = 0
MOUSEEVENTF_MOVE = 0x0001  # Move the mouse
MOUSEEVENTF_ABSOLUTE = 0x8000  # Absolute movement (optional)

class MOUSEINPUT(ctypes.Structure):
    _fields_ = [
        ("dx", ctypes.c_long),  # X movement
        ("dy", ctypes.c_long),  # Y movement
        ("mouseData", ctypes.c_ulong),  # Mouse data
        ("dwFlags", ctypes.c_ulong),  # Flags
        ("time", ctypes.c_ulong),  # Timestamp (0 for system-provided)
        ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong))  # Additional data
    ]

class INPUT(ctypes.Structure):
    _fields_ = [
        ("type", ctypes.c_ulong),  # Input type (mouse/keyboard)
        ("mi", MOUSEINPUT),  # Mouse input structure
    ]

class My_button_mapper(ABC):
    def __init__(self, mapping, key_type: Optional[chr] = 'interupted'):
        self._state = False
        self._map = mapping
        self._type = key_type
        self._keypresser = pynput.keyboard.Controller() 
    
    @property
    def mapping(self):
        return self._map
    
    def press(self):
        if self._type == 'continous':
            self._keypresser.press(self._map)
            self._keypresser.release(self._map)
        elif self._type == 'interupted':
            if not self._state:
                self._keypresser.press(self._map)
                self._state = True
    
    def release(self):
        if self._state and self._type == 'interupted':
            self._keypresser.release(self._map)
            self._state = False

class My_button_mapper_key(My_button_mapper):
    def __init__(self, mapping, key_type: Optional[chr] = 'interupted'):
        super().__init__(mapping, key_type)
        self._keypresser = pynput.keyboard.Controller() 
    
class My_button_mapper_mouse(My_button_mapper):
    def __init__(self, mapping, key_type: Optional[chr] = 'interupted'):
        super().__init__(mapping, key_type)
        self._keypresser = pynput.mouse.Controller()

class Mapper:
    def __init__(self, stickdrift: float, mouse_speed: float, mapping: str, debugg: bool = False):
        pygame.init()
        self._clock = pygame.time.Clock()
        pygame.joystick.init()
        pygame.event.pump()  # Updates pygame event queue
        self._mouse = pynput.mouse.Controller()
        self._stickdrift = stickdrift
        self._mouse_speed = mouse_speed
        self._button_to_mapper: dict[int, My_button_mapper] = self._button_to_mapper_factory(mapping)
        self._debugg = debugg
        self._right_trigger = My_button_mapper_key(' ')
        self._left_trigger = My_button_mapper_key('c')

    def _button_to_mapper_factory(self, mapping: str):
        mapper: dict[dict[int, My_button_mapper]] = {
            'ROS2': {
                0: My_button_mapper_key('d', 'continous'),
                1: My_button_mapper_key('x', 'continous'),
                2: My_button_mapper_key('w', 'continous'),
                3: My_button_mapper_key('a', 'continous'),
                5: My_button_mapper_key(pynput.keyboard.Key.esc),
                6: My_button_mapper_key('s'),
                9: My_button_mapper_mouse(pynput.mouse.Button.right),
                10: My_button_mapper_mouse(pynput.mouse.Button.left),
                11: My_button_mapper_key(pynput.keyboard.Key.up),
                12: My_button_mapper_key(pynput.keyboard.Key.down),
                13: My_button_mapper_key(pynput.keyboard.Key.left),
                14: My_button_mapper_key(pynput.keyboard.Key.right),
                },
            'Satisfactory': {
                0: My_button_mapper_key('q'),
                1: My_button_mapper_key('f'),
                2: My_button_mapper_key(pynput.keyboard.Key.shift_l),
                3: My_button_mapper_key('c'),
                5: My_button_mapper_key(pynput.keyboard.Key.esc),
                6: My_button_mapper_key(pynput.keyboard.Key.tab),
                8: My_button_mapper_mouse(pynput.mouse.Button.middle),
                9: My_button_mapper_key('e'),
                10: My_button_mapper_mouse(pynput.mouse.Button.left),
                11: My_button_mapper_key('w'),
                12: My_button_mapper_key('s'),
                13: My_button_mapper_key('a'),
                14: My_button_mapper_key('d'),
                },
        }
        
        button_to_mapper = mapper[mapping]
        
        return button_to_mapper
    
    def connect_controller(self):
        # Ensure a joystick is connected
        while pygame.joystick.get_count() < 1:
            self._clock.tick(2)
            print("No controller found!")
        if pygame.joystick.get_count() < 1:
            print("No controller found!")
        else:
            self._controller = pygame.joystick.Joystick(0)
            self._controller.init()
            print(f"Using controller: {self._controller.get_name()}")
        
    def _get_axis(self, axis):
            axis = self._controller.get_axis(axis)  # Right joystick X-axis
            if abs(axis) < self._stickdrift:
                axis = 0.0
            return axis
    
    def _move_mouse(self):
        # Read joystick axis for mouse movement (adjust axis based on your controller's setup)
        x_axis = self._get_axis(2)  # Right joystick X-axis
        y_axis = self._get_axis(3)  # Right joystick Y-axis
        
        # Update mouse position based on joystick input
        new_x = int(x_axis * self._mouse_speed)
        new_y = int(y_axis * self._mouse_speed)
        
        flags = MOUSEEVENTF_MOVE

        # print(f'{new_x}, {new_y}')
        # Move mouse to new position
        mi = MOUSEINPUT(dx=new_x, dy=new_y, mouseData=0, dwFlags=flags, time=0, dwExtraInfo=None)
        input_structure = INPUT(type=INPUT_MOUSE, mi=mi)
        
        # Call SendInput with ctypes
        ctypes.windll.user32.SendInput(1, ctypes.pointer(input_structure), ctypes.sizeof(input_structure))
    
    def _button_handler(self):
        # Check each button on the controller
        if self._debugg:
            for button in range(self._controller.get_numbuttons()):
                if self._controller.get_button(button):
                    print(f"Button {button} is pressed.")
            
        for button, map in self._button_to_mapper.items():
            if self._controller.get_button(button):
                map.press()
            else:
                map.release()
                
    def spin(self, tick):
        while True:
            # Cap the frame rate to 60 FPS
            self._clock.tick(tick)  # Limits the loop to 60 frames per second
            
            pygame.event.pump()  # Updates pygame event queue
            
            # interupt listener from controlle
            if self._controller.get_button(4):
                raise KeyboardInterrupt
            
            self._move_mouse()
            
            self._button_handler()
            
            if self._controller.get_axis(5) > 0:
                self._right_trigger.press()
            else:
                self._right_trigger.release()
                
            if self._controller.get_axis(4) > 0:
                self._left_trigger.press()
            else:
                self._left_trigger.release()
                                          
    def quit(self):
        pygame.quit()
        
        
def main():  
    tick = 60
    speed = 1000/tick      
    mapper = Mapper(0.2, speed, 'ROS2')
    mapper.connect_controller()
    
    # Main loop to read inputs
    try:  
        mapper.spin(tick)
    except KeyboardInterrupt:
        print("Exited")
    finally:
        mapper.quit()

if __name__ == '__main__':
    main()
