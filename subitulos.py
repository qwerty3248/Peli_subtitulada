import sys
import subprocess
import speech_recognition as sr
from googletrans import Translator
from moviepy.editor import VideoFileClip

def transcribir_audio(audio_path):
    recognizer = sr.Recognizer()

    with sr.AudioFile(audio_path) as audio_file:
        audio = recognizer.record(audio_file)

    try:
        transcripcion = recognizer.recognize_google(audio, language='es-ES')
        return transcripcion
    except sr.UnknownValueError:
        return ""

def traducir_texto(texto, idioma_destino):
    translator = Translator()
    traduccion = translator.translate(texto, dest=idioma_destino)
    return traduccion.origin, traduccion.text

def extraer_audio(video_path):
    audio_temp_file = "temp_audio.wav"

    # Extraer el audio del archivo MP4 y guardarlo en formato WAV
    video_clip = VideoFileClip(video_path)
    video_clip.audio.write_audiofile(audio_temp_file, codec='pcm_s16le')

    # Leer el archivo WAV convertido
    with open(audio_temp_file, 'rb') as audio_file:
        audio = audio_file.read()

    # Eliminar el archivo temporal
    subprocess.run(['rm', audio_temp_file])

    return audio

def agregar_subtitulos(video_path, idioma_destino, video_salida):
    audio_path = "temp_audio.wav"
    audio = extraer_audio(video_path)

    with open(audio_path, "wb") as audio_file:
        audio_file.write(audio)

    transcripcion = transcribir_audio(audio_path)
    _, subtitulos_traducidos = traducir_texto(transcripcion, idioma_destino)

    with open("subtitulos.srt", "w", encoding="utf-8") as archivo_subtitulos:
        archivo_subtitulos.write("1\n")
        archivo_subtitulos.write("00:00:00,000 --> 00:00:10,000\n")
        archivo_subtitulos.write(subtitulos_traducidos)

    comando = [
        'ffmpeg',
        '-i', video_path,
        '-vf', f'subtitles=subtitulos.srt',
        '-c:a', 'copy',
        video_salida
    ]

    subprocess.run(comando)

    # Eliminar archivos temporales
    subprocess.run(['rm', audio_path])
    subprocess.run(['rm', 'subtitulos.srt'])

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print('Uso: python subitulos.py <video_path> <idioma_destino> <video_salida>')
        sys.exit(1)

    video_path = sys.argv[1]
    idioma_destino = sys.argv[2]
    video_salida = sys.argv[3]

    agregar_subtitulos(video_path, idioma_destino, video_salida)

