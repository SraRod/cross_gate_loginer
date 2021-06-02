import time
import _thread
import random
import pydirectinput as pdp
import PySimpleGUI as sg

# Hyperparameters
POSITION_MAPPING = {
    "X_START" : 149,
    "Y_START" : 139,
    "X_STEP" : 100,
    "Y_STEP" : 33,
    "X_FAIL" : 319,
    "Y_FAIL" : 299
}


# Some Useful functions
def num2ij(num):
    num = num - 1
    i = num // 5
    j = num % 5
    return i, j

def loop_function(login_times, x, y, fail_delay):
    global stop
    global values
    global window
    i = 0
    while i < login_times and not stop:
        pdp.moveTo(x, y)
        pdp.click(clicks = 2)
        time.sleep(fail_delay)
        pdp.moveTo(POSITION_MAPPING['X_FAIL'], POSITION_MAPPING['Y_FAIL'])
        pdp.click()
        random_break_2 = random.randint(1,5)
        time.sleep(random_break_2)
        window['last_times'].update(int(login_times - i))
        i += 1

# GUI Initilization
sg.theme('DarkBlue13')   # Add a touch of color
sg.SetOptions(window_location = (640, 480))
# All the stuff inside your window.
layout = [  [sg.Text('Release your finger! Now is 2021 already ...')],
            [sg.Text('Server (1-10) : '), sg.Spin([sz for sz in range(1, 11)], size = (3,1), key = 'server')] ,
            [sg.Text('Auto login times : '), sg.Slider(range = (1, 1000), default_value=500, orientation='h', size=(10,20), key = 'login_times'),
             sg.Text('Close Login Fail Time : '), sg.Slider(range = (1, 10), default_value=2, orientation='h', size=(10,20), key = 'fail_delay')],
            [sg.Text('Horizon-Offset : '), sg.Slider(range = (-100, 100), default_value=0, orientation='h', size=(10,20), key = 'x_offset'), 
             sg.Text('Vertical-Offset : '), sg.Slider(range = (-100, 100), default_value=0, orientation='h', size=(10,20), key = 'y_offset')],
            [sg.Button('Start!'), sg.Text('Remaining times : '), sg.Text(size = (5,1), key = 'last_times'), sg.Button('Stop'), sg.Button('Exit')] ]

# Create the Window
window = sg.Window('Cross Gate Auto Loginer', layout)

# Event Loop to process "events" and get the "values" of the inputs
stop = False
while True:
    event, values = window.read(timeout=10)

    if event == 'Start!':
        for key in values.keys():
            values[key] = int(values[key])
        print(values)
        i, j = num2ij(values['server'])
        x = POSITION_MAPPING['X_START'] + i * POSITION_MAPPING['X_STEP'] + values['x_offset']
        y = POSITION_MAPPING['Y_START'] + j * POSITION_MAPPING['Y_STEP'] + values['y_offset']
        print(x,y)
        stop = False
        _thread.start_new_thread(loop_function, (values['login_times'], x, y, values['fail_delay']))
        
    if event == "Stop":
        stop = True

    # closing program
    if event is None or event == 'Exit': # if user closes window or clicks cancel
        break

window.close()




