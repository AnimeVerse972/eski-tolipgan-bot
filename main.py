from aiogram import Bot, Dispatcher, F, types
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from keep_alive import keep_alive
import asyncio
import os

API_TOKEN = os.getenv("BOT_TOKEN")
CHANNELS = ['@AniVerseClip']
ADMINS = [6486825926, 7575041003]

bot = Bot(token=API_TOKEN, default=DefaultBotProperties(parse_mode="Markdown"))
dp = Dispatcher(storage=MemoryStorage())

# Anime kodlar bazasi
anime_posts = {
    "1": "*Donishmandning qayta tug'ilishi*\n\nhttps://t.me/AniVerseClip/10",
    "2": "*Baholovchi*\n\nhttps://t.me/AniVerseClip/23",
    "3": "*O'ta ehtiyotkor o'lmas qahramon*\n\nhttps://t.me/AniVerseClip/35",
    "4": "*Arifureta*\n\nhttps://t.me/AniVerseClip/49",
    "5": "*Qalqon qahramoni*\n\nhttps://t.me/AniVerseClip/76",
    "6": "*Qalqon qahramoni 2-fasl*\n\nhttps://t.me/AniVerseClip/104",
    "7": "*Oxiridan keyingi boshlanish*\n\nhttps://t.me/AniVerseClip/851",
    "8": "*Daho Shifokorning soyadagi yangi hayoti*\n\nhttps://t.me/AniVerseClip/127",
    "9": "*Qahramon Bo'lish X*\n\nhttps://t.me/AniVerseClip/131",
    "10": "*Real dunyodan haqiqiyroq o'yin*\n\nhttps://t.me/AniVerseClip/135",
    # ... qolgan kodlar ...
}

# 🔒 Obuna tekshirish funksiyasi
async def check_subscription(user_id: int):
    not_subscribed = []
    for channel in CHANNELS:
        try:
            member = await bot.get_chat_member(chat_id=channel, user_id=user_id)
            if member.status not in ["member", "administrator", "creator"]:
                not_subscribed.append(channel)
        except:
            not_subscribed.append(channel)
    return not_subscribed

# ▶️ /start komandasi
@dp.message(F.text == "/start")
async def start_handler(message: Message):
    user_id = message.from_user.id
    not_subscribed = await check_subscription(user_id)

    if not_subscribed:
        keyboard = InlineKeyboardMarkup()
        for ch in not_subscribed:
            keyboard.add(InlineKeyboardButton(f"🔔 {ch}", url=f"https://t.me/{ch.strip('@')}"))
        await message.answer("⛔ Iltimos, quyidagi kanallarga obuna bo‘ling:", reply_markup=keyboard)
        return

    text = "✅ Assalomu alaykum! Anime kodi yuboring (masalan: 1, 2, 3, ...)"

    buttons = [
        [KeyboardButton("📢 Reklama"), KeyboardButton("💼 Homiylik")]
    ]
    if user_id in ADMINS:
        buttons.append([KeyboardButton("🛠 Admin panel")])

    reply_markup = ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
    await message.answer(text, reply_markup=reply_markup)

# 📢 Reklama
@dp.message(F.text == "📢 Reklama")
async def reklama_handler(message: Message):
    await message.answer("📢 Bu yerda bot reklama ma'lumotlari bo'ladi.")

# 💼 Homiylik
@dp.message(F.text == "💼 Homiylik")
async def homiylik_handler(message: Message):
    await message.answer("💼 Bu yerda homiylik haqida ma'lumot beriladi.")

# 🛠 Admin panel
@dp.message(F.text == "🛠 Admin panel")
async def admin_panel_handler(message: Message):
    if message.from_user.id in ADMINS:
        await message.answer("👮‍♂️ Admin paneliga xush kelibsiz!\nHozircha hech qanday amallar yo‘q.")
    else:
        await message.answer("⛔ Siz admin emassiz!")

# 🔍 Kodni aniqlash
@dp.message()
async def anime_code_handler(message: Message):
    code = message.text.strip().upper()
    if text in anime_posts:
        post = anime_posts[text]
        link = f"https://t.me/{post['channel'].strip('@')}/{post['message_id']}"
        button = InlineKeyboardMarkup([[InlineKeyboardButton("⬇️ TOMOSHA QILISH", url=link)]])
        
        # Postni tugma bilan foydalanuvchiga yuborish
        context.bot.copy_message(
            chat_id=user_id,
            from_chat_id=post['channel'],
            message_id=post['message_id'],
            reply_markup=button
    elif code in ["📢 REKLAMA", "💼 HOMIYLIK", "🛠 ADMIN PANEL"]:
        pass
    else:
        await message.answer("❌ Bunday kod topilmadi. Iltimos, to‘g‘ri anime kodini yuboring.")

# ▶️ Botni ishga tushirish
async def main():
    keep_alive()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
