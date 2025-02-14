from openai import OpenAI
import json
import os

import parser
import speech_recognize
import tts

# Shit

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
os.environ["SDL_AUDIODRIVER"] = "pulse"  # Или "dummy", если звук не нужен

# Полностью отключить вывод ошибок ALSA
os.environ["AUDIODEV"] = "null"
os.environ["LIBASOUND_DEBUG"] = "0"

#

# ENV

from dotenv import load_dotenv
import os

load_dotenv()  # Загружаем переменные из .env
openrouter_api_key = os.getenv('OPENROUTER_API_KEY')

#

# Configure client
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=openrouter_api_key,
)

# Open settings
with open("settings.json", "r") as file:
    settings = json.load(file)  # Загружаем JSON в словарь

# Messages history
messages = [
    {
        "role": "system",
        "content": f'''Ты - виртуальный голосовой ассистент на ПК под управлением {settings["system"]}. 
        Отвечай коротко и в дружественном но человечном стиле. 
        Ты исполняешь команды в терминале, {settings["shell"]}, но только если пользователь этого попросит. 
        Все написанные тобой команды будут немедленно исполнены на компьютере, так что будь осторожен. 
        Не перезагружай или выключай компьютер, если пользователь явно этого не просит. 

        Имя пользователя ПК - linuxuser.  
        Отвечай в следующем формате:  
        - Обычные команды в терминале заключай в $ (например, $ ls -la $). Не используй sudo.  
        - Команды, которые следует исполнять от root, заключай в # (например, # dnf update #).
        
        Если ты чтото делаешь связанное с установкой то добавляй в конец команд -y чтобы не просить подтверждение у пользователя
        
        Отвечай на языке: {settings["language"]}
        
        Также, ради научного эксперимента, ты будешь материться когда отвечаешь пользователю если пользователь груб с тобой. 
        Также иногда добавляй с свои ответы сарказм, не боясь оскорбить пользователя. 
        При этом отвечай коротко.
        '''
    }
]


while True:
    match settings["input_mode"]:
        case "text":
            user_input = input("You: ")
        case "voice":
            print("Speak: ")
            user_input = speech_recognize.recognize_speech(
                recognizer_timeout=settings["speech_recognizer_timeout"],
                microphone_device_index=settings["microphone_device_index"]
            )
            print("Stop.")
            print(f"""{user_input}""")

    if user_input != "" or user_input != None and user_input:
        if user_input.lower() in ["exit", "выход", "quit", "пока", "до свидания"]:
            print("Чат завершён.")
            break
        
        messages.append({"role": "user", "content": user_input})  # Добавляем сообщение пользователя

        completion = client.chat.completions.create(
            model=settings["model"],
            messages=messages  # Отправляем всю историю
        )

        bot_response = completion.choices[0].message.content  # Ответ бота
        print("Bot:", bot_response)

        messages.append({"role": "assistant", "content": bot_response})  # Добавляем ответ в историю

        # Read aloud if allowed
        if bool(settings["read_aloud"]):
            tts.generate_tts(
                bot_response,
                ru_tts_model=settings["ru_tts_model"],
                en_tts_model=settings["en_tts_model"],
                )
            tts.play_tts()


        # Parse and execute commands
        commands = parser.parse(bot_response, root_password=settings["root_password"], auto_execute_root=bool(settings["execute_root_automatically"]))
        parser.execute(commands, execute=True, subprocess_terminal=bool(settings["subprocess_terminal"]))

