
import subprocess
import sys

def agregar_subtitulos(video_path, subtitulos_path, idioma, video_salida):
    comando = [
        'ffmpeg',
        '-i', video_path,
        '-vf', f'subtitles={subtitulos_path}:force_style=\'Language={idioma}\'',
        '-c:a', 'copy',
        video_salida
    ]

    try:
        subprocess.run(comando, check=True)
        print(f'Se ha creado el video con subtítulos en español en {video_salida}')
    except subprocess.CalledProcessError as e:
        print(f'Error al ejecutar ffmpeg: {e}')

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print('Uso: python main.py <video_path> <subtitulos_path> <idioma> <video_salida>')
        sys.exit(1)

    video_path = sys.argv[1]
    subtitulos_path = sys.argv[2]
    idioma = sys.argv[3]  # Cambia a 'es' para español
    video_salida = sys.argv[4]

    agregar_subtitulos(video_path, subtitulos_path, idioma, video_salida)
