import requests
import argparse
from PIL import Image
from io import BytesIO

# Banner simplificado
def banner():
    print("""
    _______ _       _         _______ _            _   _
    |__   __| |     | |       |__   __| |          | | | |
       | |  | | __ _| |__     | |  | |__   ___  ___| |_| |__   ___
       | |  | |/ _` | '_ \    | |  | '_ \ / _ \/ __| __| '_ \ / _ \
       | |  | | (_| | | | |   | |  | | | |  __/ (__| |_| | | |  __/
       |_|  |_|\__,_|_| |_|   |_|  |_| |_|\___|\___|\__|_| |_|\___|
    """)

# Función para capturar una imagen de la cámara
def capture_image(camera_url, username, password):
    try:
        response = requests.get(camera_url, auth=(username, password), timeout=10)
        response.raise_for_status()
        img = Image.open(BytesIO(response.content))
        img.show()
        img.save('capture.jpg')
        print("Captura guardada como 'capture.jpg'")
    except requests.exceptions.RequestException as e:
        print(f"Error al capturar la imagen: {e}")

# Función para mostrar el flujo de video
def show_video_stream(camera_url, username, password):
    try:
        response = requests.get(camera_url, auth=(username, password), stream=True, timeout=10)
        response.raise_for_status()
        with open('video_stream.mjpg', 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
        print("Flujo de video guardado como 'video_stream.mjpg'")
    except requests.exceptions.RequestException as e:
        print(f"Error al mostrar el flujo de video: {e}")

# Función para verificar la conexión a la cámara
def check_connection(camera_url):
    try:
        response = requests.get(camera_url, timeout=5)
        if response.status_code == 200:
            print("Conexión a la cámara exitosa.")
        else:
            print(f"La cámara respondió con el código de estado {response.status_code}.")
    except requests.exceptions.RequestException as e:
        print(f"Error al conectar a la cámara: {e}")

# Función principal
def main():
    banner()
    parser = argparse.ArgumentParser(description="Herramienta para acceder a cámaras de seguridad.")
    parser.add_argument('-t', '--target', required=True, help='URL de la cámara de seguridad (ej: http://192.168.1.50:8080/video)')
    parser.add_argument('-u', '--username', required=True, help='Nombre de usuario para la autenticación')
    parser.add_argument('-p', '--password', required=True, help='Contraseña para la autenticación')
    parser.add_argument('-c', '--capture', action='store_true', help='Sacar una captura de la cámara')
    parser.add_argument('-v', '--video', action='store_true', help='Mostrar el flujo de video de la cámara')

    args = parser.parse_args()

    # Verificar la conexión a la cámara
    check_connection(args.target)

    if args.capture:
        capture_image(args.target, args.username, args.password)
    if args.video:
        show_video_stream(args.target, args.username, args.password)

if __name__ == "__main__":
    main()
