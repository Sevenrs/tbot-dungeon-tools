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

        # Deshacer la operación XOR a todos los bytes
        bin_data = bytearray(b ^ 0xFF for b in bin_data)

        # Extraer el encabezado
        header_size = 16  # Ajustar esto según la estructura real del encabezado
        header = bin_data[:header_size]
        body = bin_data[header_size:]

        # Leer la cantidad de scripts
        num_scripts = struct.unpack('I', header[12:16])[0]  # Asumiendo que la cantidad de scripts está en bytes 12-16
        print(f'Número de scripts encontrados: {num_scripts}')

        # Obtener los nombres de los scripts
        scripts = []
        for i in range(num_scripts):
            start = 16 + (i * 260)
            script_name = bin_data[start:start + 260].decode('windows-1252', errors='replace').rstrip('\x00')
            scripts.append(script_name)
            print(f'Script {i + 1}: {script_name}')

        # Crear un objeto para almacenar la información de los dungeons
        dungeon_objects = {}

        # Leer los scripts de cada dungeon
        current_offset = 16 + (num_scripts * 260) + 380  # Ajustar el offset después de leer los nombres de scripts
        for script_name in scripts:
            print(f'Leyendo el script: {script_name}')
            # Leer el encabezado del script
            script_length = struct.unpack('I', bin_data[current_offset + 1:current_offset + 5])[0]
            print(f'Largo del script {script_name}: {script_length} bytes')
            current_offset += 5  # Saltar el byte de tipo y mover al tamaño del script

            # Leer el contenido del script
            script_content = bin_data[current_offset:current_offset + script_length]
            current_offset += script_length + 4  # +4 para el pie del script

            # Interpretar el contenido del script
            dungeon_object = parse_script_content(script_content)

            # Guardar el objeto de dungeon
            dungeon_objects[script_name] = dungeon_object

            # Guardar el dungeon en un archivo JSON
            output_json = f'files/dungeon/{script_name}.json'
            with open(output_json, 'w', encoding='utf-8') as json_file:
                json.dump(dungeon_object, json_file, ensure_ascii=False, indent=4)

            print(f'Se generó el archivo JSON: {output_json}')

    except Exception as e:
        print(f'Error al procesar el archivo: {e}')

def parse_script_content(script_content):
    # Aquí debes agregar la lógica para interpretar el contenido del script
    dungeon_data = {
        'spawns': [],
        'blocks': []
    }

    # Analizar el contenido según la estructura esperada
    current_offset = 0
    num_spawns = struct.unpack('I', script_content[current_offset:current_offset + 4])[0]
    print(f'Número de spawns: {num_spawns}')
    current_offset += 4

    for _ in range(num_spawns):
        spawn_id = struct.unpack('I', script_content[current_offset:current_offset + 4])[0]
        dungeon_data['spawns'].append(spawn_id)
        print(f'Spawn ID: {spawn_id}')
        current_offset += 4

    num_blocks = struct.unpack('I', script_content[current_offset:current_offset + 4])[0]
    print(f'Número de bloques: {num_blocks}')
    current_offset += 4

    for _ in range(num_blocks):
        block = {}
        block['rect'] = list(struct.unpack('I' * 4, script_content[current_offset:current_offset + 16]))
        current_offset += 16

        # Aquí se asume que el número de enemigos está definido y seguido por su lista
        num_enemies = struct.unpack('I', script_content[current_offset:current_offset + 4])[0]
        current_offset += 4
        block['enemies'] = list(struct.unpack('I' * num_enemies, script_content[current_offset:current_offset + num_enemies * 4]))
        current_offset += num_enemies * 4

        # Similar para las otras propiedades
        block['respawn'] = []  # Puedes ajustar según la lógica que necesites
        block['clear'] = list(struct.unpack('I' * 4, script_content[current_offset:current_offset + 16]))  # Asumido
        current_offset += 16
        block['vip'] = []  # Puedes ajustar según la lógica que necesites
        block['exceptional'] = list(struct.unpack('I' * 1, script_content[current_offset:current_offset + 4]))  # Asumido
        current_offset += 4
        block['text'] = struct.unpack('64s', script_content[current_offset:current_offset + 64])[0].decode('windows-1252', errors='replace').strip('\x00')
        print(f'Texto del bloque: {block["text"]}')
        current_offset += 64
        block['countdown'] = struct.unpack('I', script_content[current_offset:current_offset + 4])[0]
        print(f'Countdown del bloque: {block["countdown"]}')
        current_offset += 4
        # Agregar más campos según la estructura

        dungeon_data['blocks'].append(block)

    return dungeon_data

if __name__ == '__main__':
    run()
