# IMPORTS


# pipeline
import asyncio
import threading
from langchain_ollama import OllamaLLM
# visual
import pygame
# support
import os
import sys
import random as rd
from dotenv import load_dotenv
# audio
import speech_recognition as sr
import sounddevice as sd
import pyttsx3 as tts
# twitch
from twitchAPI.twitch import Twitch
from twitchAPI.chat import Chat, ChatMessage, ChatEvent
from twitchAPI.oauth import UserAuthenticator
from twitchAPI.type import AuthScope
import queue
# csv
import csv

# VARIÁVEIS GLOBAIS


load_dotenv()

# twitch info
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
CANAL = os.getenv('NAME')
USER_SCOPE = [AuthScope.CHAT_READ]
fila_mensagens = queue.Queue()

# audio info
ESTA_FALANDO = False
ENCERRAR_PROGRAMA = False
FAIXA_DE_AUDIO = 44100

# visual info
COR_FUNDO = (255, 255, 0)

# llm info
AUTH_TOKEN = os.getenv('AUTH_TOKEN')
llm = OllamaLLM(model="llama3.2:1b", base_url=AUTH_TOKEN)
gatilhos_definidos = ['tufo responda', 'tofu responda', 'tudo responda', 'tu responda']
nome_streamer = os.getenv('STREAMER_NAME')

# SISTEMA DE AUDIO


# windows pt-br voice
def config_vozpt(engine_instanciada):
    voices = engine_instanciada.getProperty('voices')
    found = False
    for voice in voices:
        if 'brazil' in voice.id.lower() or 'pt-br' in voice.id.lower() or 'portuguese' in voice.name.lower():
            engine_instanciada.setProperty('voice', voice.id)
            found = True
            break
    if not found:
        print("Voz PT-BR não encontrada.")
    
    engine_instanciada.setProperty('rate', 190)
    engine_instanciada.setProperty('volume', 1.0)

# tts
def falar(texto):
    global ESTA_FALANDO
    
    try:
        ESTA_FALANDO = True
        
        engine = tts.init()
        config_vozpt(engine)

        texto_limpo = str(texto).replace('*', '')
        print(f'Tufo: {texto_limpo}')

        engine.say(texto_limpo)
        engine.runAndWait()
        engine.stop()
        
    except Exception as e:
        print(f'Erro no TTS: {e}')
    finally:
        ESTA_FALANDO = False

# stt
def dispositivo_de_ouvir(segundos=3):
    reconhecedor = sr.Recognizer()
    
    try:
        print(f"👂 Ouvindo ({segundos}s)...")
        gravacao = sd.rec(int(segundos * FAIXA_DE_AUDIO), samplerate=FAIXA_DE_AUDIO, channels=1, dtype='int16')
        sd.wait()
        audio_data = sr.AudioData(gravacao.tobytes(), FAIXA_DE_AUDIO, 2)

        texto = reconhecedor.recognize_google(audio_data, language='pt-BR')
        return texto.lower()
    
    except sr.UnknownValueError:
        return ""
    except Exception as e:
        print(f"Erro na captura: {e}")
        return ""

# TWITCH LOGIC


# filtrar mensagens
async def on_message(msg: ChatMessage):
    if '?' in msg.text and any(nome in msg.text for nome in ['tufo', 'tufinho', 'tufão', 'tufao', 'papagaio']):
        dados = {"origem": "chat", "usuario": msg.user.name, "mensagem": msg.text}
        fila_mensagens.put(dados)
        print(f"📥 Chat de {msg.user.name} na fila.")

# auth twitch
async def iniciar_twitch():
    try:
        twitch = await Twitch(CLIENT_ID, CLIENT_SECRET)
        auth = UserAuthenticator(twitch, USER_SCOPE)
        token, refresh_token = await auth.authenticate()
        await twitch.set_user_authentication(token, USER_SCOPE, refresh_token)
        chat = await Chat(twitch)
        chat.register_event(ChatEvent.MESSAGE, on_message)
        chat.start()
        await chat.join_room(CANAL)
        while not ENCERRAR_PROGRAMA:
            await asyncio.sleep(1)
        chat.stop()
    except Exception as e:
        print(f"Erro Twitch: {e}")

# DATASET BUILDING

def salvar_no_dataset(usuario, pergunta, resposta):
    arquivo_csv = 'dataset_tufo.csv'
    file_exists = os.path.isfile(arquivo_csv)
    
    try:
        with open(arquivo_csv, mode='a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['user', 'question', 'answer'])
            if not file_exists:
                writer.writeheader()
            writer.writerow({
                'user': usuario,
                'question': pergunta.strip(),
                'answer': resposta.strip()
            })

    except Exception as e:
        print(f"Erro ao salvar no CSV: {e}")

# LANGCHAIN LOGIC


# llm invoke
def processar_texto(comando_usuario):
    comando_inicial = f"""
<|begin_of_text|><|start_header_id|>system<|end_header_id|>
Você é um papagaio brasileiro chamado Tufo que é sarcástico e muito engraçado.
Seu dono se chama {nome_streamer} e ele é um streamer.
Responda SEMPRE em Português do Brasil.
Seja EXTREMAMENTE breve e curto em suas respostas, mas muito criativo.
Responda no MÁXIMO com 20 palavras.
<|eot_id|><|start_header_id|>user<|end_header_id|>
Tufo, me responda: {comando_usuario}?
<|eot_id|><|start_header_id|>assistant<|end_header_id|>
"""
    try:
        return llm.invoke(comando_inicial)
    except:
        return "Minha cabeça pifou."

# agent central
def cerebro_do_tufo():
    global ENCERRAR_PROGRAMA
    falar("Tufo na área, chefe! Pode falar ou mandar no chat.")

    while not ENCERRAR_PROGRAMA:
        # streamer message
        try:
            texto_ouvido = dispositivo_de_ouvir()

            if not texto_ouvido:
                continue
            if texto_ouvido == "":
                falar(rd.choice(["Oi chat!", "Sou Tufo!", "Que fome!"]))

            print(f'Usuário disse: {texto_ouvido}?')

            if any(gatilho in texto_ouvido for gatilho in gatilhos_definidos):
                falar(rd.choice(["To na escuta, chefe!", "Manda a boa pro Tufo, chefe!", "Tufo ta te ouvindo!"]))

                while True:
                    try:
                        pergunta_ouvida = dispositivo_de_ouvir(segundos=5)

                        if not pergunta_ouvida:
                            continue
                        
                        if texto_ouvido == "":
                            falar(rd.choice(["Oi chat!", "Sou Tufo!", "Que fome!"]))

                        print(f'Usuário perguntou: {pergunta_ouvida}')

                        if pergunta_ouvida:
                            falar(rd.choice(["Vou pensar aqui, chefe!", "To pensando, chefe, calma aí!", "Espera um segundo, chefe!"]))
                            resposta = processar_texto(pergunta_ouvida)
                            falar(resposta)
                            salvar_no_dataset("Henrique (Voz)", pergunta_ouvida, resposta)
                            break
                        else:
                            falar('Fala logo, chefe.')

                    except Exception as e:
                        falar('Deu um erro menos macabro, chefe.')
                        print(f"Erro no loop da resposta: {e}")
        except Exception as e:
            falar('Deu um erro macabro, chefe.')
            print(f"Erro no loop do cérebro: {e}")


        # chat message
        if not fila_mensagens.empty() and not ESTA_FALANDO:
            item = fila_mensagens.get()
            usuario = item['usuario']
            texto = item['mensagem']
            origem = item['origem']

            prompt = f'''
<|begin_of_text|><|start_header_id|>system<|end_header_id|>
Você é um papagaio brasileiro chamado Tufo que é sarcástico e muito engraçado.
Seu dono se chama {nome_streamer} e ele é um streamer.
Você está interagindo com o usuário "{usuario}" da stream de {nome_streamer}.
Responda SEMPRE em Português do Brasil.
Seja EXTREMAMENTE breve e curto em suas respostas, mas muito criativo.
Responda no MÁXIMO com 15 palavras.
<|eot_id|><|start_header_id|>user<|end_header_id|>
Tufo, responda: {texto}.
<|eot_id|><|start_header_id|>assistant<|end_header_id|>'''
            try:
                if origem == "chat":
                    falar(f"{usuario} perguntou: {texto}")
                    falar(rd.choice(["Vou pensar aqui!", "To pensando calma aí!", "Espera um segundo!"]))
                resposta = llm.invoke(prompt)
                falar(resposta)
                salvar_no_dataset(usuario, texto, resposta)
            except Exception as e:
                print(f"Erro LLM: {e}")
            
            fila_mensagens.task_done()
        
        pygame.time.wait(100)

# VISUAL INTERFACE


# main function
def main():
    global ENCERRAR_PROGRAMA
    pygame.init()
    LARGURA, ALTURA = 500, 500
    tela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("Tufo Assistant Unificado")

    try:
        img_fechada = pygame.image.load("img/bocafechada.png")
        img_aberta = pygame.image.load("img/bocaaberta.png")
        img_fechada = pygame.transform.scale(img_fechada, (300, 300))
        img_aberta = pygame.transform.scale(img_aberta, (300, 300))
    except:
        print("Erro: Imagens não encontradas!")
        return

    rect_img = img_fechada.get_rect(center=(LARGURA//2, ALTURA//2))

    threading.Thread(target=lambda: asyncio.run(iniciar_twitch()), daemon=True).start()
    threading.Thread(target=cerebro_do_tufo, daemon=True).start()

    clock = pygame.time.Clock()
    boca_aberta_agora = False
    tempo_troca = 0

    while not ENCERRAR_PROGRAMA:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ENCERRAR_PROGRAMA = True

        tela.fill(COR_FUNDO)

        if ESTA_FALANDO:
            agora = pygame.time.get_ticks()
            if agora - tempo_troca > 110:
                boca_aberta_agora = not boca_aberta_agora
                tempo_troca = agora
            imagem_atual = img_aberta if boca_aberta_agora else img_fechada
        else:
            imagem_atual = img_fechada

        tela.blit(imagem_atual, rect_img)
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

