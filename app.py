from flask import Flask, request, send_file
import subprocess
import os

app = Flask(__name__)

@app.route('/')
def index():
    return """
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
        <h2>Bypass de Metadatos (Sony a7 IV)</h2>
        <p>Sube tu video del iPhone aquí. Se procesará rápido en la nube.</p>
        <form action="/procesar" method="post" enctype="multipart/form-data">
            <input type="file" name="video" accept="video/mp4,video/quicktime" required><br>
            <button type="submit" class="btn">Procesar y Descargar</button>
        </form>
    </body>
    </html>
    """

@app.route('/procesar', methods=['POST'])
def procesar():
    file = request.files.get('video')
    if not file:
        return "Falta el video.", 400

    filepath = os.path.join('/tmp', file.filename)
    file.save(filepath)

    comando = [
        'exiftool',
        '-Make=Sony',
        '-Model=ILCE-7M4',
        '-Software=Adobe Premiere Pro',
        '-overwrite_original',
        filepath
    ]
    subprocess.run(comando)

    return send_file(filepath, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
