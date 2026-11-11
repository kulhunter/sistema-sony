from flask import Flask, request, send_file
from werkzeug.utils import secure_filename
import subprocess
import os
import traceback

app = Flask(__name__)

# Permitir videos de hasta 500 MB (por defecto Flask es menos tolerante)
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024 

@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Modificador a Sony a7 IV</title>
        <style>
            body { font-family: -apple-system, sans-serif; padding: 20px; text-align: center; background: #121212; color: white; }
            .btn { background: #007aff; color: white; padding: 15px 20px; border: none; border-radius: 10px; font-size: 16px; margin-top: 20px; width: 100%; }
            input[type="file"] { margin-top: 20px; }
        </style>
    </head>
    <body>
        <h2>Bypass de Metadatos V2</h2>
        <p>Sube tu video del iPhone.</p>
        <form action="/procesar" method="post" enctype="multipart/form-data">
            <input type="file" name="video" accept="video/mp4,video/quicktime,video/*" required><br>
            <button type="submit" class="btn" onclick="this.innerText='Subiendo y Procesando... (No cierres la pestaña)'; this.style.opacity='0.7';">Procesar y Descargar</button>
        </form>
    </body>
    </html>
    '''

@app.route('/procesar', methods=['POST'])
def procesar():
    try:
        file = request.files.get('video')
        if not file:
            return "Error: No llegó el archivo al servidor. Intenta con un video más liviano.", 400

        # 1. Limpiar el nombre del archivo para que Linux no colapse por espacios o emojis
        filename = secure_filename(file.filename)
        if not filename:
            filename = "video_iphone.mp4"
        
        filepath = os.path.join('/tmp', filename)
        
        # 2. Guardar el archivo
        file.save(filepath)

        # 3. Procesar con ExifTool
        comando = [
            'exiftool',
            '-Make=Sony',
            '-Model=ILCE-7M4',
            '-Software=Adobe Premiere Pro',
            '-overwrite_original',
            filepath
        ]
        subprocess.run(comando, check=True)

        # 4. Devolver el archivo
        return send_file(filepath, as_attachment=True)
        
    except subprocess.CalledProcessError:
        return "Error 500: ExifTool falló al reescribir los metadatos. El archivo puede estar corrupto.", 500
    except Exception as e:
        return f"Error interno detallado: {str(e)}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
