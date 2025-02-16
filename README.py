from flask import Flask
from threading import Thread
from pyngrok import ngrok
import discord
import os
import time

# تشغيل سيرفر Flask
app = Flask(__name__)

@app.route('/')
def home():
    return "I'm alive!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# إعداد البوت
TOKEN = "YOUR_BOT_TOKEN"  # استبدل هذا بالتوكن الفعلي
CHANNEL_ID = 1340441881573589043  # استبدل بـ ID القناة المسموح بها

# شفرة المافيا
MAFIA_CODE = {
    "أ": "^$", "ا": "^$", "ب": "$^^^", "ت": "$^^$", "ث": "^^$^", "ج": "^$$^", "ح": "^$^^",
    "خ": "$^$^", "د": "$^^", "ذ": "$$^^", "ر": "^$^", "ز": "$$$^", "س": "^^^", "ش": "^$$$",
    "ص": "$$^", "ض": "^^^$", "ط": "$", "ظ": "$^$$", "ع": "$$", "غ": "$$$$", "ف": "^^$$",
    "ق": "$$^", "ك": "$^$", "ل": "$$^$", "م": "$$$$^", "ن": "$^", "ه": "^^^^", "و": "^$$",
    "ي": "^^", " ": " / "  # لفصل الكلمات
}

# عكس القاموس
REVERSE_MAFIA_CODE = {v: k for k, v in MAFIA_CODE.items()}

# تحويل النص إلى شفرة المافيا
def text_to_mafia(text):
    return ' '.join(MAFIA_CODE.get(char, char) for char in text)

# تحويل شفرة المافيا إلى نص
def mafia_to_text(mafia_text):
    words = mafia_text.split(" / ")
    translated_words = []
    for word in words:
        letters = word.split(" ")
        translated_word = ''.join(REVERSE_MAFIA_CODE.get(letter, "?") for letter in letters)
        translated_words.append(translated_word)
    return ' '.join(translated_words)

# إعداد البوت
intents = discord.Intents.default()
intents.message_content = True
bot = discord.Client(intents=intents)

@bot.event
async def on_ready():
    print(f'✅ Logged in as {bot.user}')

@bot.event
async def on_message(message):
    if message.author == bot.user or message.channel.id != CHANNEL_ID:
        return

    if message.content.startswith("!translate"):
        content = message.content[len("!translate "):].strip()

        if all(char in "^$ /" for char in content):
            translation = mafia_to_text(content)
            await message.channel.send(f"📖 **النص:** {translation}")
        else:
            translation = text_to_mafia(content)
            await message.channel.send(f"🕵️ **شفرة المافيا:** {translation}")

# إبقاء البوت شغالًا دائمًا
keep_alive()

while True:
    try:
        bot.run(TOKEN)
    except Exception as e:
        print(f"Error: {e}")
        time.sleep(10)  # إعادة التشغيل بعد 10 ثوانٍ
