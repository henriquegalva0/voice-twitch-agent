# Tufo: Charismatic Stateless Agent
Simple zero-context impersonated agent (Tufo) for speech recognition (TTS) integrated with the Twitch API.

-----

## IMPORTS
Frameworks used to develop the agent.

### pipeline
The framework ``asyncio`` manages the Twitch API's functions. ``threading`` is used only to foward the functions in the pipeline. The main framework is ``langchain_ollama``, which calls the language model with the function ``OllamaLLM``.
### visual
``pygame`` is responsible for showing the character _Tufo_.
### support
System management or code simple functions.
### audio
The framework ``sounddevice`` is used with ``speech_recognition`` by recording the audio, then understanding the language, STT (Speech-to-text). Lastly, ``pyttsx3`` comes to manage TTS (Text-to-speech).
### twitch
Twitch API framework and ```queue`` to manage twitch chat's requests.

## VARIÁVEIS GLOBAIS
All variables and API keys.

## SISTEMA DE AUDIO
Audio management.
### windows pt-br voice
Select the TTS voice as the windows default portuguese narrator.
### tts
Text-to-speech functions.
### stt
Speech-to-text functions.

## TWITCH LOGIC
Script communicating with Twitch's chat through Twitch API.
### filtrar mensagens
Filter chat only selecting messages that has not only _"Tufo"_ but also _"?"_.
### auth twitch
Authenticate on the Twitch channel.

## LANGCHAIN LOGIC
The core of our script.
### llm invoke
Calls the Ollama language model.
### agent central
Controls all the functions around the agent.
#### streamer message
Calls the LLM to the streamer message.
#### chat message
Calls the LLM to chat's message.

# VISUAL INTERFACE
Pygame controls our whole script adding visual representation while the TTS speaks.

-----

## Setup

Firstly, create a `.env` file inserting your own info in each variable. You can obtain your twitch app *CLIENT_ID* and *CLIENT_SECRET* by accessing [dev.twitch](https://dev.twitch.tv/console/apps). After that, click on `Register Your Application` and copy the useful info.

```
CLIENT_ID=your_twitch_app_id
CLIENT_SECRET=your_twitch_app_secret
NAME=your_twitch_channel_name
STREAMER_NAME=your_name
```

Now, to run the code, start by cloning the github repository.

```
git init
git clone https://github.com/henriquegalva0/voice-twitch-agent.git
```

Create a python environment, activate it and install all project requirements.

```
python -m venv .venv
./.venv/Scripts/Activate.ps1
pip install -r requirements.txt
```

Run the code:

```
python ./agentcode.py
```