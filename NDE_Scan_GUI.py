import PySimpleGUI as sg
from NDE_Stage_Utility import * # my custom stage library

sg.theme('BluePurple')

layout = [[sg.Text('Always zero machine on startup'), sg.Button('Zero Machine', pad=(10,0))],
          [sg.Text('Home Position, meters:              x                   y                   z')],
          [sg.Canvas(key='-CANVAS2-', size=(150,1)), sg.Input(size=(10,1), key='-xHome-', justification='center'), sg.Input(size=(10,1), key='-yHome-', justification='center'), sg.Input(size=(10,1), key='-zHome-', justification='center'), sg.Button('Move', pad=(10,0))],
          [sg.Text(size=(60,1), key='-OUTPUT-')],
          [sg.Button('Exit')]]

window = sg.Window('NDE Ultrasonic System', layout)

while True:  # Event Loop
    event, values = window.read()
    # print(event, values)
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    
    if event == 'Zero Machine':
        StartUpZero()

    if event == 'Move':
        # Call function to move to Home position
        Str = 'Moving to (x, y, z):     (' + values['-xHome-'] + ', ' + values['-yHome-'] + ', ' + values['-zHome-'] +')'
        window['-OUTPUT-'].update(Str)          #'Moving to (x, y, z):', values['-xHome-'])#, values['-xHome-'], values['-xHome-'])
        #MoveToHome(values['-xHome-'], values['-yHome-'], values['-zHome-'])

        # Impliment a value of where the system is at all times
        # Use the value to calculate how far, and what direction, the system is from imputed points
        # make if statment to reverse motor direction if pos/neg values

window.close()