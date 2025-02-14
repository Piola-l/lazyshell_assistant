from gtts import gTTS
import pygame

pygame.init()

def match(text):  #функция проверки на русский язык
    alphabet = set('абвгдеёжзийклмнопрстуфхцчшщъыьэюя')
    return not alphabet.isdisjoint(text.lower())

def generate_tts(text):
    if match(text) == True:   #если язык русский (True) то генерировать ответ на русском если нет то на английском
        tts = gTTS(text, lang='ru')  #настройка gTTS с руским языком
    else:
        tts = gTTS(text, lang='en')  # настройка gTTS с английским языков
    tts.save('output.mp3')


def play_tts():
    pygame.mixer.music.load('output.mp3')
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
