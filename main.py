import os
import asyncio

from aiogram import Bot, Dispatcher, F, types
from aiogram.client.default import DefaultBotProperties
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.fsm.storage.memory import MemoryStorage

# 🔐 Token va sozlamalar
API_TOKEN = os.getenv("BOT_TOKEN")
CHANNELS = ['@AniVerseClip']
ADMINS = [6486825926, 7575041003]

bot = Bot(token=API_TOKEN, default=DefaultBotProperties(parse_mode="Markdown"))
dp = Dispatcher(storage=MemoryStorage())

# ✅ Kodlar bazasi (anime_posts)
anime_posts = {
    "1": {"channel": "@AniVerseClip", "message_id": 10},
    "2": {"channel": "@AniVerseClip", "message_id": 23},
    # Qolganlari xuddi oldingidek...
}

# 🔒 Obuna tekshirish
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

# ▶️ /start
@dp.message(CommandStart())
async def start_handler(message: Message):
    print("✅ /start buyrug‘i qabul qilindi.")
    user_id = message.from_user.id
    not_subscribed = await check_subscription(user_id)

    if not_subscribed:
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=f"🔔 {ch}", url=f"https://t.me/{ch.strip('@')}")] for ch in not_subscribed
        ] + [[InlineKeyboardButton(text="🔁 Tekshirish", callback_data="check_subs")]])
        await message.answer("⛔ Iltimos, quyidagi kanallarga obuna bo‘ling:", reply_markup=keyboard)
        return

    buttons = [[KeyboardButton(text="📢 Reklama"), KeyboardButton(text="💼 Homiylik")]]
    if user_id in ADMINS:
        buttons.append([KeyboardButton(text="🛠 Admin panel")])

    markup = ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
    await message.answer("✅ Anime kodi yuboring (masalan: 1, 2, 3, ...)", reply_markup=markup)

# 🔁 Tekshirish
@dp.callback_query(F.data == "check_subs")
async def check_subscription_callback(callback: CallbackQuery):
    user_id = callback.from_user.id
    not_subscribed = await check_subscription(user_id)

    if not_subscribed:
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=f"🔔 {ch}", url=f"https://t.me/{ch.strip('@')}")] for ch in not_subscribed
        ] + [[InlineKeyboardButton(text="🔁 Tekshirish", callback_data="check_subs")]])
        await callback.message.edit_text("⛔ Hali ham kanalga obuna emassiz:", reply_markup=keyboard)
    else:
        await callback.message.delete()
        await start_handler(callback.message)

# 📢 Reklama
@dp.message(F.text == "📢 Reklama")
async def reklama_handler(message: Message):
    await message.answer("Reklama uchun: @DiyorbekPTMA")

# 💼 Homiylik
@dp.message(F.text == "💼 Homiylik")
async def homiy_handler(message: Message):
    await message.answer("Homiylik uchun karta: 8800904257677885")

# 🛠 Admin panel
@dp.message(F.text == "🛠 Admin panel")
async def admin_handler(message: Message):
    if message.from_user.id in ADMINS:
        await message.answer("👮‍♂️ Admin paneliga xush kelibsiz!")
    else:
        await message.answer("⛔ Siz admin emassiz!")

# 🔍 Kod orqali anime yuborish
@dp.message()
async def code_handler(message: Message):
    code = message.text.strip()

    if code in ["📢 Reklama", "💼 Homiylik", "🛠 Admin panel"]:
        return

    if code in anime_posts:
        info = anime_posts[code]
        channel = info["channel"]
        msg_id = info["message_id"]

        await bot.copy_message(
            chat_id=message.chat.id,
            from_chat_id=channel,
            message_id=msg_id,
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[[
                InlineKeyboardButton(text="📥 Yuklab olish", url=f"https://t.me/{channel.strip('@')}/{msg_id}")
            ]])
        )
    else:
        await message.answer("❌ Bunday kod topilmadi. Iltimos, to‘g‘ri kod yuboring.")

# 🟢 Polling ishga tushirish
if __name__ == "__main__":
    async def main():
        print("🚀 Bot polling rejimda ishlayapti...")
        await dp.start_polling(bot)

    asyncio.run(main())
