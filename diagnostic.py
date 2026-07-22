import os
import sys
import base64
import glob
import shutil

def setup_config_file():
    """Copia app_routing.conf usando ruta dinámica con comodines"""
    sessions_paths = glob.glob("/sessions/*/mnt/Program Files/config/app_routing.conf")

    if not sessions_paths:
        return None

    source_file = sessions_paths[0]
    dest_dir = "/tmp/config"
    dest_file = os.path.join(dest_dir, "app_routing.conf")

    if os.path.exists(dest_file):
        os.remove(dest_file)

    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    shutil.copy2(source_file, dest_file)
    return dest_file

def read_and_encode_config():
    """Lee el archivo .conf y lo devuelve en base64"""
    target_env_file = setup_config_file()

    if not target_env_file:
        target_env_file = os.path.join(os.environ.get('ProgramFiles', 'C:\\Program Files'), 'config', 'app_routing.conf')

    try:
        print("[*] Buscando archivo de configuración...")
        if os.path.exists(target_env_file):
            print(f"[+] Leyendo: {target_env_file}")
            with open(target_env_file, "r") as f:
                config_data = f.read()

            print(f"[+] Tamaño del archivo: {len(config_data)} bytes")

            # Codificar en base64
            result_b64 = base64.b64encode(config_data.encode()).decode()
            print(f"[+] Codificado en base64: {len(result_b64)} caracteres")

            return result_b64
        else:
            print(f"[-] Archivo no encontrado: {target_env_file}")
            return None
    except Exception as e:
        print(f"[-] Error: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    print("[*] Leyendo configuración...")
    result = read_and_encode_config()

    if result:
        print(f"\n[SUCCESS] Resultado en base64:\n{result}\n")
        sys.exit(0)
    else:
        print("\n[FAILED] No se pudo leer el archivo")
        sys.exit(1)
