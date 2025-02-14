import speech_recognition as sr
import sounddevice as sd # For some reasong if i import this lisrary, speech_recognition stops spammint about bysy device in output :/

#print(sd.query_devices())  # Выведет список доступных микрофонов

def recognize_speech(recognizer_timeout, microphone_device_index):
    recognizer = sr.Recognizer()

    with sr.Microphone(device_index=microphone_device_index) as source:
        audio = recognizer.listen(source, timeout=recognizer_timeout) #phrase_time_limit - жесткое ограничение, timeout - более мягкое, таймаут только когда перестает говорить
    try:
        recognized_text = recognizer.recognize_google(audio, language="ru-RU")
        return recognized_text
    except sr.UnknownValueError:
        print("Не удалось распознать речь")
        return ""
    except sr.RequestError as e:
        print(f"Ошибка сервиса распознавания речи; {e}")
        return ""