from flask import Flask, request, send_file
from werkzeug.utils import secure_filename
import subprocess
import os

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024 

@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Bypass Sony a7 IV</title>
        <style>
            body { font-family: -apple-system, sans-serif; padding: 20px; text-align: center; background: #121212; color: white; }
            .btn { background: #007aff; color: white; padding: 15px 20px; border: none; border-radius: 10px; font-size: 16px; margin-top: 20px; width: 100%; }
            input[type="file"] { margin-top: 20px; }
        </style>
    </head>
    <body>
        <h2>Bypass de Cámara (Sistema Docker)</h2>
        <p>Servidor dedicado con permisos root. 100% a prueba de fallos.</p>
        <form action="/procesar" method="post" enctype="multipart/form-data">
            <input type="file" name="video" accept="video/mp4,video/quicktime,video/*" required><br>
            <button type="submit" class="btn" onclick="this.innerText='Subiendo y Procesando... No cierres esta pantalla'; this.style.opacity='0.7';">Procesar Video</button>
        </form>
    </body>
    </html>
    '''

@app.route('/procesar', methods=['POST'])
def procesar():
    try:
        file = request.files.get('video')
        if not file:
            return "Error: No se recibió ningún archivo.", 400

        filename = secure_filename(file.filename)
        if not filename or not filename.lower().endswith(('.mp4', '.mov')):
            filename = "video_iphone.mp4"
        
        filepath = os.path.join('/tmp', filename)
        file.save(filepath)

        # Ruta absoluta del programa instalado nativamente en Docker
        comando = [
            '/usr/bin/exiftool',
            '-Make=Sony',
            '-Model=ILCE-7M4',
            '-Software=Adobe Premiere Pro',
            '-overwrite_original',
            filepath
        ]
        
        result = subprocess.run(comando, capture_output=True, text=True)
        
        if result.returncode != 0:
            return f"Error interno de ExifTool: {result.stderr}", 500

        return send_file(filepath, as_attachment=True)
        
    except Exception as e:
        return f"Error general del servidor: {str(e)}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
