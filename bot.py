import os
import feedparser
import sqlite3
import asyncio
import re
import html
from telegram import Bot
from dotenv import load_dotenv
from deep_translator import GoogleTranslator as Translator

# Carregar variáveis de ambiente
load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CANAL_ID = os.getenv("CANAL_ID")

# Inicializações
bot = Bot(token=TELEGRAM_TOKEN)

# Banco de dados
conn = sqlite3.connect('noticias_ciber.db')
cursor = conn.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS noticias (link TEXT PRIMARY KEY)')
conn.commit()

# Feeds RSS confiáveis
RSS_FEEDS = [
    'https://canaltech.com.br/busca/?q=golpes/rss/',
    'https://www.tecmundo.com.br/tags/golpes-e-fraudes/rss/',
    'https://olhardigital.com.br/feed/',
    'https://www.cisoadvisor.com.br/feed/',
    'https://www.serpro.gov.br/menu/sala-de-imprensa/noticias/RSS',
]

# Palavras-chave de interesse
PALAVRAS_CHAVE = [
    "golpe", "fraude", "vazamento", "malware", "phishing",
    "ransomware", "dados vazados", "vazou", "invasão", "hacker",
    "ciberataque", "segurança", "cibersegurança", "dica de segurança"
]

def limpar_texto(texto):
    texto = re.sub(r'<[^>]+>', '', texto)
    texto = html.unescape(texto)
    texto = texto.replace('*', '').replace('_', '').replace('[', '').replace(']', '')
    return texto.strip()

def contem_palavra_chave(texto):
    texto = texto.lower()
    return any(palavra in texto for palavra in PALAVRAS_CHAVE)

async def buscar_e_enviar_noticias():
    print("[BOT] Iniciando busca e envio de notícias...")
    for url in RSS_FEEDS:
        print(f"[BUSCANDO] Feed: {url}")
        feed = feedparser.parse(url)
        for entry in feed.entries[:5]:
            titulo = limpar_texto(getattr(entry, 'title', ''))
            link = getattr(entry, 'link', '')
            resumo = limpar_texto(getattr(entry, 'summary', ''))

            if not titulo or not link:
                print("[IGNORADO] Título ou link ausente.")
                continue

            # Verifica se o conteúdo tem relação com os temas
            if not contem_palavra_chave(titulo + " " + resumo):
                continue

            cursor.execute("SELECT 1 FROM noticias WHERE link = ?", (link,))
            if cursor.fetchone():
                continue

            mensagem = f"🛡️ *{titulo}*\n\n{resumo}\n\n🔗 [Leia mais]({link})"

            # Tenta extrair imagem
            imagem_url = None
            if 'media_content' in entry:
                imagem_url = entry.media_content[0].get('url')
            elif 'links' in entry:
                for l in entry.links:
                    if l.get('type', '').startswith('image'):
                        imagem_url = l.get('href')
                        break

            try:
                if imagem_url:
                    legenda = mensagem[:1024]
                    await bot.send_photo(chat_id=CANAL_ID, photo=imagem_url, caption=legenda, parse_mode='Markdown')
                else:
                    await bot.send_message(chat_id=CANAL_ID, text=mensagem, parse_mode='Markdown')

                print(f"[ENVIADO] {titulo}")
                cursor.execute("INSERT INTO noticias (link) VALUES (?)", (link,))
                conn.commit()
                await asyncio.sleep(30)  # espera 30s entre mensagens

            except Exception as e:
                print(f"[ERRO AO ENVIAR] {e}")
                continue

async def main_loop():
    while True:
        await buscar_e_enviar_noticias()
        await asyncio.sleep(1800)  # 30 minutos

if __name__ == "__main__":
    asyncio.run(main_loop())
