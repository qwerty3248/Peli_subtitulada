#subitulos 
from google.cloud import speech_v1p1beta1 as speech
from google.cloud import translate_v2 as translate
import subprocess
import sys

def transcribir_audio(video_path, idioma_destino):
    cliente_speech = speech.SpeechClient()

    audio = speech.RecognitionAudio(content=extraer_audio(video_path))
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code='es-ES'  # Puedes ajustar el código del idioma si es diferente.
    )

    respuesta = cliente_speech.recognize(config=config, audio=audio)

    transcripcion = ""
    for resultado in respuesta.results:
        transcripcion += resultado.alternatives[0].transcript + " "

    return transcripcion

def extraer_audio(video_path):
    comando = [
        'ffmpeg',
        '-i', video_path,
        '-vn',
        '-ac', '1',
        '-ar', '16000',
        '-acodec', 'pcm_s16le',
        '-f', 'wav',
        '-'
    ]

    return subprocess.check_output(comando)

def traducir_texto(texto, idioma_destino):
    cliente_translate = translate.Client()

    traduccion = cliente_translate.translate(texto, target_language=idioma_destino)
    return traduccion['input'], traduccion['translatedText']

def agregar_subtitulos(video_path, idioma_destino, video_salida):
    transcripcion = transcribir_audio(video_path, idioma_destino)
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

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print('Uso: python agregar_subtitulos_auto.py <video_path> <idioma_destino> <video_salida>')
        sys.exit(1)

    video_path = sys.argv[1]
    idioma_destino = sys.argv[2]
    video_salida = sys.argv[3]

    agregar_subtitulos(video_path, idioma_destino, video_salida)


