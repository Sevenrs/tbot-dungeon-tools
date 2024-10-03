import struct
import os

def unpack_dungeon_bin(input_file, output_folder):
    try:
        with open(input_file, 'rb') as f:
            file_data = f.read()

        # Leer el encabezado: fecha y cantidad de scripts
        year, month, day, script_count = struct.unpack_from('<4I', file_data, 0)
        print(f"Fecha: {year}-{month}-{day}, Cantidad de scripts: {script_count}")

        offset = 16  # después del encabezado
        scripts = []

        # Leer los nombres de los scripts
        for _ in range(script_count):
            script_name = file_data[offset:offset + 260].decode('windows-1252', errors='replace').strip('\x00')
            scripts.append(script_name)
            offset += 260

        # Leer los offsets de los scripts
        offsets = []
        for _ in range(script_count):
            script_offset = struct.unpack_from('<I', file_data, offset)[0]
            offsets.append(script_offset)
            offset += 4

        # Desempaquetar cada script
        for i, script_name in enumerate(scripts):
            script_offset = offsets[i]

            # Validar el offset
            if script_offset >= len(file_data):
                print(f"Offset inválido {script_offset} para el script {script_name}. Saltando.")
                continue

            # Leer la longitud del script
            try:
                script_length = struct.unpack_from('<I', file_data, script_offset + 4)[0]
            except struct.error:
                print(f"Error al leer la longitud del script {script_name} en el offset {script_offset}. Saltando.")
                continue

            script_data = file_data[script_offset + 8:script_offset + 8 + script_length]

            # Decodificar y xor los datos del script
            script_decoded = bytearray([b ^ 0xFF for b in script_data])

            try:
                decoded_data = script_decoded.decode('windows-1252', errors='replace').splitlines()
            except Exception as e:
                print(f"Error al decodificar el script '{script_name}': {e}")
                continue

            # Guardar el script desempaquetado
            output_path = os.path.join(output_folder, f"{script_name}.json")
            try:
                with open(output_path, 'w', encoding='utf-8') as output_file:
                    output_file.write("\n".join(decoded_data))
                print(f"Script '{script_name}' desempaquetado y guardado en {output_path}")
            except Exception as e:
                print(f"Error al guardar el script '{script_name}': {e}")

    except Exception as e:
        print(f"Error al desempaquetar {input_file}: {e}")

# Ejecutar el script
unpack_dungeon_bin('dungeon.bin', 'output_folder')
