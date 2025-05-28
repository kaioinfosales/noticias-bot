# Bot de Notícias de Cibersegurança 🇧🇷

Um bot que busca automaticamente notícias sobre **golpes, fraudes, malware, vazamentos de dados e dicas de segurança** em fontes brasileiras confiáveis e envia para um canal do Telegram.

📡 Fontes RSS utilizadas
Canaltech (busca por "golpes")

TecMundo (tag "golpes-e-fraudes")

Olhar Digital

CISO Advisor

Serpro

Fontes internacionais também podem ser utilizadas, 
pois o tradutor já está integrado.

---

## 🚀 Funcionalidades

- Busca notícias relevantes de cibersegurança
- Traduz notícias internacionais (se forem adicionadas no futuro)
- Evita duplicatas com banco de dados SQLite
- Posta com imagem, título, resumo e link
- Espera 30 segundos entre postagens
- Loop infinito: busca notícias a cada 30 minutos

---

## 🛠️ Instalação

1. Clone o repositório:

```bash
git clone https://github.com/kaioinfosales/noticias-bot.git
cd noticias-bot
```

```bash
python3 -m venv venv
source venv/bin/activate
```

```bash
pip install -r requirements.txt
```

Edite suas informações no .env

TELEGRAM_TOKEN=seu_token_aqui
CANAL_ID=@seucanal_ou_id

```bash
python bot.py
```

Para rodar em segundo plano

```bash
nohup python bot.py &
```

📌 Autor
Desenvolvido por [Kaio Sales] - 💻 Segurança, Automação e Bots