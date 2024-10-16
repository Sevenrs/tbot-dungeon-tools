from scapy.all import *
import itertools
import time

HEADER_SIZE = 2
FOOTER_SIZE = 8
PRINTABLE_CHARS = set(range(32, 127))  # ASCII imprimible

# Lista expandida de claves XOR posibles
XOR_KEYS = list(range(0x00, 0x100))  # 0x00 - 0xFF

OUTPUT_FILE = "xor_results.txt"

def xor_decrypt(data, key):
    """Aplica XOR con una clave específica."""
    return bytearray(byte ^ key for byte in data)

def store_result(key, decrypted):
    """Escribe el resultado en un archivo TXT."""
    with open(OUTPUT_FILE, 'a', encoding='latin-1') as f:
        f.write(f"Key: 0x{key:02X}, Result: {decrypted}\n")
        f.flush()  # Asegura que el resultado se almacena de inmediato

def analyze_packet(packet):
    """Analiza un paquete capturado, prueba claves XOR y almacena resultados válidos."""
    payload = bytes(packet[TCP].payload.load)  # Extrae el payload del paquete

    # Extrae contenido, header y footer
    content = payload[HEADER_SIZE:-FOOTER_SIZE] if len(payload) > HEADER_SIZE + FOOTER_SIZE else b""

    # Prueba cada clave XOR
    for key in XOR_KEYS:
        decrypted = xor_decrypt(content, key)

        try:
            # Decodifica a latin-1 para garantizar legibilidad de binarios
            decrypted_str = decrypted.decode('latin-1')
            print(f"Key: 0x{key:02X}, Result: {decrypted_str}")
            
            # Almacena solo los resultados con caracteres mayormente legibles
            if all(char in PRINTABLE_CHARS for char in decrypted):
                store_result(key, decrypted_str)

        except Exception as e:
            # En caso de error en la decodificación, sigue con la siguiente clave
            print(f"Error al decodificar con clave 0x{key:02X}: {e}")

def packet_handler(packet):
    """Maneja cada paquete capturado."""
    if packet.haslayer(TCP) and packet[TCP].payload:
        analyze_packet(packet)

def start_sniffer():
    """Inicia el sniffer en la interfaz y puerto especificado."""
    print("Iniciando el sniffer en 0.0.0.0:11000...")
    try:
        sniff(filter="tcp port 11000", prn=packet_handler, store=0)
    except KeyboardInterrupt:
        print("\nSniffer detenido por el usuario.")
    except Exception as e:
        print(f"Error al iniciar el sniffer: {e}")

if __name__ == "__main__":
    # Limpia el archivo de resultados antes de iniciar
    with open(OUTPUT_FILE, 'w') as f:
        f.write("Resultados del análisis de XOR en tiempo real:\n")
    start_sniffer()
