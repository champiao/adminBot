import whois
import datetime
from telegram import Bot
import dotenv
import os
dotenv.load_dotenv()
import asyncio
from time import sleep

TELEGRAM_BOT_TOKEN = os.getenv('ID')
TELEGRAM_CHAT_ID = os.getenv('CHAT')

domains = os.getenv('DOMAINS').split(',')

bot = Bot(token=TELEGRAM_BOT_TOKEN)

async def send_messages():
    for domain in domains:
        w = whois.whois(domain)
        if isinstance(w.expiration_date, list):
            expiration_date = w.expiration_date[0]
            print(expiration_date)
        else:
            expiration_date = w.expiration_date
            print(expiration_date)

        if expiration_date is not None:
            days_to_expire = (expiration_date - datetime.datetime.now()).days
            if days_to_expire < 120:
                print(f'days to expire {domain}: '+ str(days_to_expire))
                message = f'O domínio {domain} irá expirar em {days_to_expire} dias.'
                await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)
                sleep(20)
asyncio.run(send_messages())