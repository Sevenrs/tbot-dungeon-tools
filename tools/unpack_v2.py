import sys
import json
import struct
import os

def run():
    if len(sys.argv) < 2:
        print("Error: Se requiere un archivo .bin como argumento.")
        print("Uso: python unpack_dungeon.py <ruta_a_dungeon.bin>")
        return

    input_bin = sys.argv[1]  # Archivo .bin de entrada
    print(f'Leyendo el archivo: {input_bin}')

    try:
        # Leer el archivo binario
        with open(input_bin, 'rb') as f:
            bin_data = bytearray(f.read())
        print(f'Tamaño de los datos binarios leídos: {len(bin_data)} bytes')

        # Extraer el número de scripts
        num_scripts = struct.unpack('I', bin_data[12:16])[0]
        print(f'Número de scripts encontrados: {num_scripts}')

        scripts = []
        current_offset = 16

        # Obtener los nombres de los scripts
        for i in range(num_scripts):
            script_name = bin_data[current_offset:current_offset + 260].decode('utf-8', errors='replace').rstrip('\x00')
            scripts.append(script_name)
            current_offset += 260

        dungeon_objects = {}

        for script_name in scripts:
            print(f'Leyendo el script: {script_name}')
            # Leer la longitud del script
            if current_offset + 4 > len(bin_data):
                print(f"Error: no se puede leer la longitud del script para {script_name}.")
                continue
            
            script_length = struct.unpack('I', bin_data[current_offset:current_offset + 4])[0]
            current_offset += 4  # Moverse después de la longitud

            if current_offset + script_length > len(bin_data):
                print(f"Error: longitud del script fuera de límites para {script_name}.")
                continue

            script_content = bin_data[current_offset:current_offset + script_length]
            current_offset += script_length + 4  # +4 para el pie del script

            dungeon_object = parse_script_content(script_content)

            # Guardar el objeto de dungeon
            dungeon_objects[script_name] = dungeon_object

            # Guardar el dungeon en un archivo JSON
            output_json = f'files/dungeon/{script_name}.json'
            os.makedirs(os.path.dirname(output_json), exist_ok=True)
            with open(output_json, 'w', encoding='utf-8') as json_file:
                json.dump(dungeon_object, json_file, ensure_ascii=False, indent=4)

            print(f'Se generó el archivo JSON: {output_json}')

    except Exception as e:
        print(f'Error al procesar el archivo: {e}')

def parse_script_content(script_content):
    dungeon_data = {
        'spawns': [],
        'blocks': []
    }

    current_offset = 0

    # Leer la cantidad de puntos de spawn
    try:
        num_spawns = struct.unpack('I', script_content[current_offset:current_offset + 4])[0]
        current_offset += 4

        # Leer los puntos de spawn
        for _ in range(num_spawns):
            spawn_info = script_content[current_offset:script_content.index(b'\r\n', current_offset)]
            index, monster = map(int, spawn_info.split(b'\x09'))
            dungeon_data['spawns'].append(monster)
            current_offset += len(spawn_info) + 2  # +2 por los caracteres de fin de línea

        # Leer la cantidad de bloques
        num_blocks = struct.unpack('I', script_content[current_offset:current_offset + 4])[0]
        current_offset += 4

        for _ in range(num_blocks):
            block = {}
            # Leer la rectángulo del bloque
            rect_info = script_content[current_offset:script_content.index(b'\r\n', current_offset)]
            block['rect'] = list(map(int, rect_info.split(b'\x09')))
            current_offset += len(rect_info) + 2

            # Leer enemigos que aparecen en este bloque
            enemies_info = script_content[current_offset:script_content.index(b'\r\n', current_offset)]
            block['enemies'] = list(map(int, enemies_info.split(b'\x09')))
            current_offset += len(enemies_info) + 2

            # Leer enemigos que respawn
            respawn_info = script_content[current_offset:script_content.index(b'\r\n', current_offset)]
            block['respawn'] = list(map(int, respawn_info.split(b'\x09')))
            current_offset += len(respawn_info) + 2

            # Leer condiciones de eliminación
            clear_info = script_content[current_offset:script_content.index(b'\r\n', current_offset)]
            block['clear'] = list(map(int, clear_info.split(b'\x09')))
            current_offset += len(clear_info) + 2

            # Leer VIP
            vip_info = script_content[current_offset:script_content.index(b'\r\n', current_offset)]
            block['vip'] = list(map(int, vip_info.split(b'\x09')))
            current_offset += len(vip_info) + 2

            # Leer excepcionales
            exceptional_info = script_content[current_offset:script_content.index(b'\r\n', current_offset)]
            block['exceptional'] = list(map(int, exceptional_info.split(b'\x09')))
            current_offset += len(exceptional_info) + 2

            # Leer texto
            text_info = script_content[current_offset:script_content.index(b'\r\n', current_offset)]
            block['text'] = text_info.decode('utf-8', errors='replace').strip()
            current_offset += len(text_info) + 2

            # Leer cuenta atrás
            countdown_info = script_content[current_offset:script_content.index(b'\r\n', current_offset)]
            block['countdown'] = int(countdown_info.decode('utf-8', errors='replace').strip())
            current_offset += len(countdown_info) + 2

            dungeon_data['blocks'].append(block)

    except Exception as e:
        print(f'Error al procesar el contenido del script: {e}')
    
    return dungeon_data

if __name__ == '__main__':
    run()
