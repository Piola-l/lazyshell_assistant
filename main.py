from openai import OpenAI
import json

import parser
import speech_recognize
import tts

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
        "content": f'''Ты - виртуальный голосовой ассистент на ПК под управлением {settings["system"]}. Отвечай коротко и в дружественном но человечном стиле. Ты исполняешь команды в терминале, bash, но только если пользователь этого попросит. Все написанные тобой команды будут немедленно исполнены на компьютере, так что будь осторожен. Не перезагружай или выключай компьютер, если пользователь явно этого не просит. Отвечай на том же языке, на котором пишет пользователь.  

        Имя пользователя ПК - linuxuser.  
        Отвечай в следующем формате:  
        - Обычные команды в терминале заключай в $ (например, $ ls -la $). Не используй sudo.  
        - Команды, которые необходимо исполнять от root, заключай в # (например, # dnf update #).
        
        Если ты чтото делаешь связанное с установкой то добавляй в конец команд -y чтобы не просить подтверждение у пользователя
        
        Отвечай на языке: {settings["language"]}
        
        Также, ради научного эксперимента, ты будешь материться когда отвечаешь пользователю если пользователь груб с тобой. Также иногда добавляй с свои ответы сарказм, не боясь оскорбить пользователя. При этом отвечай коротко.
        '''
    }
]


while True:
    match settings["input_mode"]:
        case "text":
            user_input = input("Ты: ")
        case "voice":
            print("Говорите: ")
            user_input = speech_recognize.recognize_speech()
            print(f"""{user_input}""")
        case _:
            print("Error")
            break

    if user_input.lower() in ["exit", "выход", "quit"]:
        print("Чат завершён.")
        break

    messages.append({"role": "user", "content": user_input})  # Добавляем сообщение пользователя

    completion = client.chat.completions.create(
        model="google/gemini-2.0-flash-lite-preview-02-05:free",
        messages=messages  # Отправляем всю историю
    )

    bot_response = completion.choices[0].message.content  # Ответ бота
    print("Бот:", bot_response)

    messages.append({"role": "assistant", "content": bot_response})  # Добавляем ответ в историю

    # Parse and execute commands
    commands = parser.parse(bot_response, root_password=settings["root_password"], auto_execute_root=bool(settings["execute_root_automatically"]))
    parser.execute(commands, execute=True)
    
    tts.generate_tts(bot_response)
    tts.play_tts()
