import pygame
import pynput

def presser(mapping, type):
    
    def keyboard_presser(mapping):
        keyboard.press(mapping)
    
    if type == 'keyboard':
        return keyboard_presser(mapping)
    
    

class My_button_mapper:
    def __init__(self, mapping):
        self._state = False
        self._map = mapping
        self._type = 'c'
        self._keypresser = presser(self._map, 'keyboard')
    
    @property
    def state(self):
        return self._state
        
    @state.setter
    def state(self, state):
        self._state = state     
    
    def press(self):
        if self._type == 'c':
            keyboard.press(self._map)
            keyboard.release(self._map)
        elif self._type == 'i':
            if not self.state:
                keyboard.press(self._map)
                self.state = True
            else:
                keyboard.release(self._map)
    

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
mouse_right = [False, False]
mouse_left = [False, False]

stickdrift = 0.3

keyboard = pynput.keyboard.Controller()

button_to_key = {
    0: 'd',
    1: 'x',
    2: 'w',
    3: 'a',
    6: 's',
    4: 'ctrl c',
    9: 'mouse right',
    10: 'mouse left',
    14: pynput.keyboard.Key.right,
    11: pynput.keyboard.Key.up,
    13: pynput.keyboard.Key.left,
    12: pynput.keyboard.Key.down,
}

# Main loop to read inputs
try:
    while True:
        pygame.event.pump()  # Updates pygame event queue
        
        # Read joystick axis for mouse movement (adjust axis based on your controller's setup)
        x_axis = controller.get_axis(2)  # Right joystick X-axis
        if abs(x_axis) < stickdrift:
            x_axis = 0.0
        y_axis = controller.get_axis(3)  # Right joystick Y-axis
        if abs(y_axis) < stickdrift:
            y_axis = 0.0
        
        # Scale movement speed
        mouse_speed = 15  # Adjust for sensitivity
        
        # Update mouse position based on joystick input
        new_x = int(x_axis * mouse_speed)
        new_y = int(y_axis * mouse_speed)
        
        # Move mouse to new position
        mouse.move(new_x, new_y)
        
        # Check each button on the controller
        for button in range(controller.get_numbuttons()):
            if controller.get_button(button):
                print(f"Button {button} is pressed.")
        
        # Loop through each button in the mapping
        for button, mapp in button_to_key.items():
            if controller.get_button(button):
                # print(key)
                if mapp == 'ctrl c':
                    with keyboard.pressed(pynput.keyboard.Key.ctrl):
                        keyboard.press('c')
                        keyboard.release('c')
                        raise KeyboardInterrupt
                elif type(mapp) == str:
                    if mapp[0:5] == 'mouse':
                        if mapp == 'mouse right':
                            if mouse_right == [False, False]:
                                # print('click')
                                mouse.press(pynput.mouse.Button.right)
                            mouse_right = [True, True]
                        else:
                            if mouse_left == [False, False]:
                                # print('click2')
                                mouse.press(pynput.mouse.Button.left)
                            mouse_left = [True, True]
                    else:
                        # Press and release the mapped keyboard key
                        keyboard.press(mapp)
                        keyboard.release(mapp)
                else:
                    # Press and release the mapped keyboard key
                    keyboard.press(mapp)
                    keyboard.release(mapp)
                    
        if mouse_right == [False, True]:
            mouse.release(pynput.mouse.Button.right)
            mouse_right[1] = False
            # print(mouse_right)
        mouse_right[0] = False
        
        if mouse_left == [False, True]:
            mouse.release(pynput.mouse.Button.left)
            mouse_left[1] = False
            # print(mouse_left)
        mouse_left[0] = False

                
        # Cap the frame rate to 60 FPS
        clock.tick(60)  # Limits the loop to 60 frames per second
        
except KeyboardInterrupt:
    print("Exited")
finally:
    pygame.quit()
