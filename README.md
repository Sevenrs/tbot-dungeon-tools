### Bots Dungeon Tools

Modify the paths to your need. You can only test the dungeon binary file while the client is open. The other files are registered once the client initially starts.

Generating dungeon.bin:\
`python main.py generate_dungeon_bin "c:/Program Files (x86)/Icseon/T-Bot Rewritten/script/dungeon/dungeon.bin"`
![expected output](img/expected.png)

Generating map_planet.bin:\
`python main.py generate_map_bin files/map_planet.json "c:/Program Files (x86)/Icseon/T-Bot Rewritten/script/map_planet.bin"`

Generating map_daeth.bin:\
`python main.py generate_map_bin files/map_daeth.json "c:/Program Files (x86)/Icseon/T-Bot Rewritten/script/map_daeth.bin"`

Generating map_base.bin:\
`python main.py generate_map_bin files/map_base.json "c:/Program Files (x86)/Icseon/T-Bot Rewritten/script/map_base.bin"`

There is a work in progress GUI that you could use, but it is incomplete. To start that, run:
`python gui.py`
### Extractor Advance
ohka bots
Unpacking  dungeon.bin:\
![image](https://github.com/user-attachments/assets/d4813831-109b-4c3a-9e5e-c7060ea6218b)

### Update 3
se logró modificar los stats , vida ataque y nombre de los npc
así mismo se obtienen las ids de todos los npcs para la creacion o modificación de nuevos mapas en un formato más limpio
muy pronto estaré actualizando el código.
```
 "id": 1,
        "name": "Alpha",
        "life": 1856,
        "damage": 143,
        "defense": 215,
        ... 
```
![image](https://github.com/user-attachments/assets/b237cb62-382e-4238-9af3-6dc5867621ea)

![image](https://github.com/user-attachments/assets/45eb7015-c1cf-4581-afbd-1f7037aab58d)

![20241028_143804](https://github.com/user-attachments/assets/914939ec-9759-426c-b3d1-756530140c9b)



