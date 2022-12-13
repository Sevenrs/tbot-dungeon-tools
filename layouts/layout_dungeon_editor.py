import PySimpleGUI as gui
import os, sys, main

LAYOUT_DUNGEON_EDITOR = [

    [
        gui.Text('Dungeon Script Overview')
    ],

    [
        gui.Listbox(
            values=[],
            enable_events=True,
            size=(38, 11),
            key='_dungeon_list'
        )
    ],

    [
        gui.Button('Create new script'),
        gui.Button('Compile dungeon.bin')
    ]

]

def process_events(window, event, values):

    if event == 'Dungeon Editor':

        scripts = os.listdir('files/dungeon')
        scripts.sort()

        window['_dungeon_list'].update(scripts)

    elif event == 'Create new script':

        dialog = gui.Window('Enter information', [

            [
                gui.Text('Name', size=(10, 1)), gui.InputText()
            ],

            [
                gui.Submit()
            ]

        ])
        dialog.read()
        dialog.close()

    elif event == 'Compile dungeon.bin':

        args = [
            sys.argv[0],
            'generate_dungeon_bin',
            "/home/xander/.wine/dosdevices/c:/Program Files (x86)/Icseon/T-Bot Rewritten/script/dungeon/dungeon.bin"
        ]

        sys.argv = args
        main.main()