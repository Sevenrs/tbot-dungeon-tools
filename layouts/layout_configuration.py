import PySimpleGUI as gui

LAYOUT_CONFIGURATION = [

    [
        gui.Text('Layout for the application configuration')
    ]

]

def process_events(event, values):

    print(event)