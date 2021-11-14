import PySimpleGUI as sg
from NDE_Stage_Utility import * # my custom stage library

sg.theme('BluePurple')

layout = [[sg.Text('Always zero machine on startup'), sg.Button('Zero Machine', pad=(10,0))],
          [sg.Text('Home Position (cm):                  x                   y                    z')],
          [sg.Canvas(size=(150,1)), sg.Input(size=(10,1), key='-xHome-', justification='center'), sg.Input(size=(10,1), key='-yHome-', justification='center'), sg.Input(size=(10,1), key='-zHome-', justification='center'), sg.Button('Move', pad=(10,0))],
          [sg.Text('Specimin Size for Rectangular Scan (cm):   x Length         y Length')],
          [sg.Canvas(size=(235,1)), sg.Input(size=(10,1), key='-xLength-', justification='center'), sg.Input(size=(10,1), key='-yLength-', justification='center')],
          [sg.Text('Physical Distance between scan (mm):'),sg.Canvas(size=(4,1), pad=(0,0)), sg.Input(size=(10,1), key='-ScanWidth-')],
          [sg.Text('Scan speed (mm/s):'), sg.Canvas(size=(103,1)), sg.Input(size=(10,1), key='-ScanSpeed-'), sg.Canvas(size=(74,1)), sg.Button('Scan', pad=(10,0))],
          [sg.Canvas(size=(1,40))],
          [sg.Text('File Name of Scan: '), sg.Input(size=(50,1), key='-FileName-')],
          [sg.Text('Where to Save File:')],
          [sg.Text('Your Folder', size=(15, 1), auto_size_text=False, justification='right'),
            sg.InputText('Default Folder'), sg.FolderBrowse()],
          [sg.Button('Save')],
          [sg.Canvas(size=(1,20))],
          [sg.Text('System Output:')],
          [sg.Text(size=(60,1), key='-OUTPUT-', background_color = 'white')],
          [sg.Button('Exit')]]

window = sg.Window('NDE Ultrasonic System', layout)

# Initialize variables
MachineZeroed = False
MachineHomed = False
pos = [250, 250, 250]

while True:  # Event Loop
    event, values = window.read()
    # print(event, values)
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    
    if event == 'Zero Machine':
        pos = StartUpZero()
        while pos[0] != 0 or pos[1] != 0 or pos[2] != 0:
            pos = StartUpZero()     # Keep running startup zero until zeroed
        #print('Stage is at:\nx: ' + str(pos[0]) + '\ny: ' + str(pos[1]) + '\nz: ' + str(pos[2]))
        window['-OUTPUT-'].update('The stage is zeroed')   # Print to GUI that stage is zeroed
        MachineZeroed = True

    if event == 'Move':
        if MachineZeroed == False:
            window['-OUTPUT-'].update('You must zero the machine upon startup')
        elif pos[0] == 250 or pos[1] == 250 or pos[2] == 250:
            window['-OUTPUT-'].update('You must enter coordinates to move to')
        else:
            # Call function to move to Home position
            if values['-xHome-'] == '' or values['-yHome-'] == '' or values['-zHome-'] == '':
                window['-OUTPUT-'].update('You must enter coordinates to move to')
            else:
                xn = float(values['-xHome-'])*0.01;    yn = float(values['-yHome-'])*0.01;    zn = float(values['-zHome-'])*0.01    # Convert string cm to float m home values
                Str = 'Moving to (x, y, z) cm:     (' + str(xn/0.01) + ', ' + str(yn/0.01) + ', ' + str(zn/0.01) +')'               # Display moving position in cm
                window['-OUTPUT-'].update(Str)
                
                MoveToHome(xn, yn, zn, pos[0], pos[1], pos[2])
                pos = [xn, yn, zn]
                Str = 'Moved to (x, y, z):     (' + str(pos[0]/0.01) + ', ' + str(pos[1]/0.01) + ', ' + str(pos[2]/0.01) +')'       # Display moved position in cm
                window['-OUTPUT-'].update(Str)
                MachineHomed = True
                #print(pos)

                # Impliment a value of where the system is at all times
                # Use the value to calculate how far, and what direction, the system is from imputed points
                # make if statment to reverse motor direction if pos/neg values
    
    if event == 'Scan':
        if MachineZeroed == False:
            window['-OUTPUT-'].update('You must zero the machine upon startup')
        elif MachineHomed == False:
            window['-OUTPUT-'].update('You must move the machine to home to start scan')
        else:
            xL = float(values['-xLength-'])*0.01; yL = float(values['-yLength-'])*0.01; ScanWidth = float(values['-ScanWidth-'])*0.001; speed = float(values['-ScanSpeed-'])*0.001
                                                # Convert string cm/mm to float m home values
            RectScan(xL, yL, ScanWidth, speed)


window.close()