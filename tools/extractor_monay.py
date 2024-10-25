import json
import os
import sys

def decrypt_content(content):
    """Desencripta el contenido aplicando XOR con 0xFF."""
    return bytearray(b ^ 0xFF for b in content)

def load_binary_file(filename):
    """Carga el contenido de un archivo binario."""
    if not os.path.exists(filename):
        print(f"Error: No se encontró el archivo '{filename}'.")
        sys.exit(1)

    with open(filename, "rb") as f:
        return f.read()

def extract_section(binary_content, start, length):
    """Extrae una sección específica del contenido binario."""
    return binary_content[start:start + length]

def parse_monster_names(decrypted_content):
    """Extrae nombres de monstruos del contenido desencriptado."""
    try:
        # Decodificar el contenido como texto usando EUC-KR
        decoded_text = decrypted_content.decode('euc-kr', errors='replace')

        # Supongamos que los nombres de monstruos están en líneas separadas
        monster_names = decoded_text.strip().split('\n')  # Cambia '\n' por el delimitador adecuado

        return monster_names
    except UnicodeDecodeError as e:
        print(f"Error de decodificación: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error al analizar el contenido: {e}")
        sys.exit(1)

def save_json(filename, data):
    """Guarda los datos en formato JSON."""
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"Datos guardados en '{filename}'.")

def main():
    input_file = "p_monai.bin"  # Archivo binario por defecto
    output_file = "monster_names.json"  # Archivo JSON de salida

    print(f"Procesando el archivo '{input_file}'...")

    # Cargar y desencriptar el archivo binario
    binary_content = load_binary_file(input_file)
    decrypted_content = decrypt_content(binary_content)

    # Ajusta los índices según la estructura de tu archivo binario
    start_index = 0  # Cambia según lo que necesites extraer
    length = len(decrypted_content)  # Cambia si solo deseas una parte específica

    # Extraer la sección deseada
    section = extract_section(decrypted_content, start_index, length)

    # Convertir a nombres de monstruos
    monster_names = parse_monster_names(section)

    # Guardar los nombres en un archivo JSON
    save_json(output_file, monster_names)

    # Mostrar una vista previa de los primeros 5 nombres
    print("\n=== Vista Previa de los Primeros Nombres de Monstruos ===\n")
    for name in monster_names[:5]:
        print(name)

if __name__ == "__main__":
    main()
