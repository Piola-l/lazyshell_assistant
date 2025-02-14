import speech_recognition as sr

def recognize_speech():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Говорите что-нибудь...")
        audio = recognizer.listen(source, timeout=1, phrase_time_limit=5) #phrase_time_limit - жесткое ограничение, timeout - более мягкое, таймаут только когда перестает говорить
    try:
        recognized_text = recognizer.recognize_google(audio, language="ru-RU")
        return recognized_text
        # print(f"Вы сказали: {text}")
    except sr.UnknownValueError:
        print("Не удалось распознать речь")
    except sr.RequestError as e:
        print(f"Ошибка сервиса распознавания речи; {e}")