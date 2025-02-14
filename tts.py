import os, subprocess
import re
import pygame

pygame.init()

def match(text):  # True - russian, False - english
    alphabet = set('абвгдеёжзийклмнопрстуфхцчшщъыьэюя')
    return not alphabet.isdisjoint(text.lower())

def generate_tts(text, ru_tts_model: str, en_tts_model: str, *auto_play: bool):
    clean_text = re.sub(r'[\$#]\s*.*?\s*[\$#]', '', text).strip()
    model = ru_tts_model if match(text) else en_tts_model
    command = f"echo '{clean_text}' | ./piper/piper --model piper/{model} --output_file output.wav"
    
    subprocess.run(command, shell=True, check=True)
    
    if auto_play:
        play_tts()


def play_tts():
    pygame.mixer.music.load('output.wav')
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
