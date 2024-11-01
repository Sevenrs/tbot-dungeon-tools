import os
import sys
import json
import logging

# Configuración del logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

XOR_KEY = 0xFF  # Clave de encriptación

def encrypt_content(content):
    """Encripta el contenido aplicando XOR con XOR_KEY."""
    return bytearray(b ^ XOR_KEY for b in content)

def load_json(filename):
    """Carga los nombres de monstruos desde un archivo JSON."""
    if not os.path.exists(filename):
        logging.error(f"No se encontró el archivo '{filename}'.")
        sys.exit(1)

    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        logging.error(f"El archivo '{filename}' no contiene un JSON válido.")
        sys.exit(1)

def save_binary_file(filename, content):
    """Guarda el contenido en un archivo binario."""
    try:
        with open(filename, "wb") as f:
            f.write(content)
        logging.info(f"Archivo binario guardado como '{filename}'.")
    except IOError as e:
        logging.error(f"Error al guardar el archivo '{filename}': {e}")
        sys.exit(1)

def create_monster_data(monster_list):
    """Convierte los nombres de monstruos a binario."""
    try:
        # Unir los nombres en un solo texto separado por '\n'
        joined_text = "\n".join(monster_list)
        # Codificar el texto en windows-1252
        return joined_text.encode('windows-1252', errors='replace')
    except Exception as e:
        logging.error(f"Error al crear el contenido binario: {e}")
        sys.exit(1)

def main():
    input_file = "monster_names.json"  # Archivo JSON con los nombres
    output_file = "C:/Users/Andrew/Desktop/original/T-Bot Rewritten/script/dungeon/p_monai.bin"  # Archivo binario de salida

    logging.info(f"Procesando el archivo '{input_file}'...")

    # Cargar los nombres de monstruos desde el JSON
    monster_list = load_json(input_file)

    # Crear el contenido binario a partir de los nombres
    binary_content = create_monster_data(monster_list)

    # Encriptar el contenido con XOR
    encrypted_content = encrypt_content(binary_content)

    # Guardar el archivo binario en disco
    save_binary_file(output_file, encrypted_content)

if __name__ == "__main__":
    main()
