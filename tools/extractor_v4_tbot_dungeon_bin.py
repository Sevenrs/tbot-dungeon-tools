import struct
import os

def unpack_dungeon_bin(input_file, output_folder):
    try:
        print(f"Iniciando el desempaquetado del archivo {input_file}")
        with open(input_file, 'rb') as f:
            file_data = f.read()

        # Leer el encabezado: fecha y cantidad de scripts
        year, month, day, script_count = struct.unpack_from('<4I', file_data, 0)
        print(f"Encabezado leído: Fecha: {year}-{month}-{day}, Cantidad de scripts: {script_count}")

        offset = 16  # después del encabezado
        scripts = []

        # Leer los nombres de los scripts
        print("Leyendo nombres de scripts...")
        for _ in range(script_count):
            script_name = file_data[offset:offset + 260].decode('windows-1252', errors='replace').strip('\x00')
            scripts.append(script_name)
            print(f"Nombre de script encontrado: {script_name}")
            offset += 260

        # Leer los offsets de los scripts
        offsets = []
        print("Leyendo offsets de los scripts...")
        for _ in range(script_count):
            script_offset = struct.unpack_from('<I', file_data, offset)[0]
            offsets.append(script_offset)
            print(f"Offset del script agregado: {script_offset}")
            offset += 4

        # Desempaquetar cada script
        print("Desempaquetando cada script...")
        for i, script_name in enumerate(scripts):
            script_offset = offsets[i]
            print(f"Procesando script {i+1}/{script_count}: {script_name}, Offset: {script_offset}")

            # Validar el offset
            if script_offset >= len(file_data):
                print(f"Offset inválido {script_offset} para el script {script_name}. Saltando.")
                continue

            # Leer la longitud del script
            try:
                script_length = struct.unpack_from('<I', file_data, script_offset + 4)[0]
                print(f"Longitud del script {script_name}: {script_length}")
            except struct.error:
                print(f"Error al leer la longitud del script {script_name} en el offset {script_offset}. Saltando.")
                continue

            script_data = file_data[script_offset + 8:script_offset + 8 + script_length]

            # Decodificar y aplicar XOR a los datos del script
            script_decoded = bytearray([b ^ 0xFF for b in script_data])
            print(f"Datos decodificados (xor aplicados) para el script {script_name}: {script_decoded[:20]}...")  # Mostramos solo los primeros 20 bytes

            try:
                decoded_data = script_decoded.decode('windows-1252', errors='replace').splitlines()
                print(f"Datos decodificados para el script '{script_name}' (primeras líneas): {decoded_data[:5]}")  # Mostramos solo las primeras 5 líneas
            except Exception as e:
                print(f"Error al decodificar el script '{script_name}': {e}")
                continue

            # Guardar el script desempaquetado en formato JSON
            output_path = os.path.join(output_folder, f"{script_name}.json")
            try:
                with open(output_path, 'w', encoding='utf-8') as output_file:
                    output_file.write("\n".join(decoded_data))
                print(f"Script '{script_name}' desempaquetado y guardado en {output_path}")
            except Exception as e:
                print(f"Error al guardar el script '{script_name}': {e}")

            # Guardar el bytearray decodificado en un archivo de texto con la extensión .txt
            bytearray_output_path = os.path.join(output_folder, f"{script_name}.txt")
            try:
                # Guardamos el contenido en el formato requerido (lista de strings)
                with open(bytearray_output_path, 'w', encoding='utf-8') as bytearray_file:
                    bytearray_file.write(str(decoded_data))  # Convertimos 'decoded_data' a string para que se guarde como lista
                print(f"Bytearray decodificado del script '{script_name}' guardado en {bytearray_output_path}")
            except Exception as e:
                print(f"Error al guardar el bytearray del script '{script_name}': {e}")

    except Exception as e:
        print(f"Error al desempaquetar {input_file}: {e}")

# Ejecutar el script
unpack_dungeon_bin('dungeon.bin', 'output_folder')
