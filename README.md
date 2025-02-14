# Asshole AI Assistant written in python

It's an AI Linux assistant powered by [Google Gemini Flash Lite 2.0](https://openrouter.ai/google/gemini-2.0-flash-lite-preview-02-05:free) and using OpenRouter free API because i'm poor. I've tried using LLaMA 3.2 but my PC is potato.

Supports **gnome-terminal** and **phyxis** terminal, but you can easily add yours!

### Settings.json

- input_mode - Voice or text
- read_aloud - Will be model asnwers voiced
- language - Model answers language
- system - Your system
- root_password - Password for superuser. Won`t be given to model.
- execute*root_automatically - Will execute \_sudo* commands without asking to enter password
- subprocess_terminal - Open terminal as a new task or not (Hightly reccomend set to "True")
