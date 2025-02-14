import os
import re
import pygame

pygame.init()

def match(text):  # True - russian, False - english
    alphabet = set('абвгдеёжзийклмнопрстуфхцчшщъыьэюя')
    return not alphabet.isdisjoint(text.lower())

def generate_tts(text):
    clean_text = re.sub(r'[\$#]\s*.*?\s*[\$#]', '', text).strip()
    if match(text) == True:   #если язык русский (True) то генерировать ответ на русском если нет то на английском
        os.system(f"echo '{clean_text}' | ./piper/piper --model piper/ru_RU-dmitri-medium.onnx --output_file output.wav")
    else:
        os.system(f"echo '{clean_text}' | ./piper/piper --model piper/en_GB-alan-medium.onnx --output_file output.wav")


def play_tts():
    pygame.mixer.music.load('output.wav')
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
