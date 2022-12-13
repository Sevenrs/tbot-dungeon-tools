import PySimpleGUI as gui

gui.theme('SystemDefault')

from layouts import layout_dungeon_editor, layout_configuration

layout = [

    [
        gui.Menu([

            [
                '&File', [
                    'Configuration'
                ]
            ],

            [
                '&Tools', [
                    'Dungeon Editor',
                    'Map Entry Editor',
                    'Server Controller'
                ]
            ]

        ], pad=(200, 1)),

        gui.Column(layout_configuration.LAYOUT_CONFIGURATION, visible=False, key='Configuration'),
        gui.Column(layout_dungeon_editor.LAYOUT_DUNGEON_EDITOR, visible=False, key='Dungeon Editor')
    ],

    [
        gui.Text('Output Window')
    ],

    [
        gui.Output(key='_output', size=(100, 10), background_color='black', text_color='white')
    ]

]

window  = gui.Window("T-Bot Tools", layout, layout,size=(600, 400),)
layouts = ['Configuration', 'Dungeon Editor']

while True:
    event, values = window.read()

    layout_dungeon_editor.process_events(window, event, values)

    if event in layouts:

        for layout in layouts:
            window[layout].update(visible=False)

        window[event].update(visible=True)

    elif event == 'OK' or event == gui.WIN_CLOSED:
        break

window.close()