import sys
import json
import queue
import sounddevice as sd
from vosk import Model, KaldiRecognizer

# Загружаем модель
model = Model("vosk/vosk-model-small-ru-0.22")  # Укажи путь к модели

# Настраиваем аудио-поток
samplerate = 16000
device = None  # Можно указать конкретный микрофон, если их несколько

q = queue.Queue()

recognized_text_history = []

def callback(indata, frames, time, status):
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))

# Создаем распознаватель
rec = KaldiRecognizer(model, samplerate)

def recognize_speech():
    with sd.RawInputStream(samplerate=samplerate, blocksize=8000, device=device,
                        dtype="int16", channels=1, callback=callback):
        print("Говори что-нибудь...")
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                print(result["text"])  # Выводим распознанный текст
                recognized_text.append(result["text"])
                return recognized_text_history
