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

## DATASET BUILDING
Use the data to build a simple dataset to train future models.

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

## VISUAL INTERFACE
Pygame controls our whole script adding visual representation while the TTS speaks.

-----

## Setup

Firstly, access [google collab](https://colab.google/) and paste the following code on one cell:

```
!sudo apt-get update && sudo apt-get install -y zstd
!curl -fsSL https://ollama.com/install.sh | sh
!pip install pyngrok

import os
import threading
import time

def run_ollama():
    os.environ['OLLAMA_HOST'] = '0.0.0.0'
    os.system("ollama serve")

threading.Thread(target=run_ollama, daemon=True).start()
time.sleep(10)
!ollama pull llama3.2:1b
```

After executing the code above, execute the next script in a new cell:

```
from pyngrok import ngrok
import re
from google.colab import userdata

NGROK_TOKEN = userdata.get('NGROK')
ngrok.set_auth_token(NGROK_TOKEN)

ngrok.kill()

try:
    url_publica = ngrok.connect(11434, proto="http")
    # Limpa a string para garantir que pegamos apenas a URL
    endpoint = re.sub(r'http://', 'https://', url_publica.public_url)
    print(f"🔗 Copy the following URL to your base_url:\n{endpoint}")
except Exception as e:
    print(f"Error Ngrok: {e}")
```

With that ready, create a `.env` file inserting your own info in each variable. You can obtain your twitch app *CLIENT_ID* and *CLIENT_SECRET* by accessing [dev.twitch](https://dev.twitch.tv/console/apps). After that, click on `Register Your Application` and copy the useful info.

```
CLIENT_ID=your_twitch_app_id
CLIENT_SECRET=your_twitch_app_secret
NAME=your_twitch_channel_name
STREAMER_NAME=your_name
AUTH_TOKEN=ngrok_redirect_link
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

Run the code and you're ready!

```
python ./agentcode.py
```

Trigger to interact in twitch chat:

```
!tufo <msg>
```

Trigger to interact by voice recognition:

```
Speaker: "tufo responda"
wait for its reponse
Speaker: <question>
```