import requests
import time
import os
import telebot

# Configuración de APIs
CRYPTO_PANIC_API_KEY = os.getenv("CRYPTO_PANIC_API_KEY", "cf7906b446352b2cdb6806a113f2c554ef5215ae")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "7629558636:AAF2r-Ere8nHmBnWgj5GAPYQuSw6QasBkjg")
CHAT_ID = os.getenv("CHAT_ID", "1057327038")

# Monedas a monitorear
MONITORED_COINS = ["xrp", "pepe", "pengu", "trump", "bitcoin", "ethereum", "qdt"]

# Inicializar el bot de Telegram
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

# Función para obtener noticias de Crypto Panic
def get_crypto_news():
    url = f"https://cryptopanic.com/api/v1/posts/?auth_token={CRYPTO_PANIC_API_KEY}&currencies={','.join(MONITORED_COINS)}"
    response = requests.get(url)
    if response.status_code == 200:
        news = response.json().get("results", [])
        return news
    return []

# Función para enviar alertas a Telegram
def send_telegram_alert(message):
    bot.send_message(CHAT_ID, message)

# Monitoreo de noticias y precios
def monitor():
    print("Iniciando monitoreo de criptomonedas...")
    while True:
        try:
            # Obtener noticias
            news = get_crypto_news()
            for item in news:
                title = item.get("title", "")
                url = item.get("url", "")
                message = f"🚨 **Nueva noticia** 🚨\n{title}\n{url}"
                send_telegram_alert(message)

            # Esperar 5 minutos antes de la siguiente verificación
            time.sleep(300)
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(60)

# Iniciar el bot
if __name__ == "__main__":
    monitor()
