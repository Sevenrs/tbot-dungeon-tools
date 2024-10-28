import json
import os
import sys

def encrypt_content(content):
    """Encripta el contenido aplicando XOR con 0xFF."""
    return bytearray(b ^ 0xFF for b in content)

def load_json(filename):
    """Carga los nombres de monstruos desde un archivo JSON."""
    if not os.path.exists(filename):
        print(f"Error: No se encontró el archivo '{filename}'.")
        sys.exit(1)

    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)

def save_binary_file(filename, content):
    """Guarda el contenido en un archivo binario."""
    with open(filename, "wb") as f:
        f.write(content)
    print(f"Archivo binario guardado como '{filename}'.")

def create_monster_data(monster_list):
    """Convierte los nombres de monstruos a binario."""
    try:
        # Unir los nombres en un solo texto separado por '\n'
        joined_text = "\n".join(monster_list)

        # Codificar el texto en windows-1252
        binary_content = joined_text.encode('windows-1252', errors='replace')

        return binary_content
    except Exception as e:
        print(f"Error al crear el contenido binario: {e}")
        sys.exit(1)

def main():
    input_file = "monster_names.json"  # Archivo JSON con los nombres
    output_file = "p_monai_new.bin"    # Archivo binario de salida

    print(f"Procesando el archivo '{input_file}'...")

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
