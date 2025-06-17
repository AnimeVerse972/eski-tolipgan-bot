import os
import asyncio

from aiogram import Bot, Dispatcher, F, types
from aiogram.client.default import DefaultBotProperties
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web

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
    "3": {"channel": "@AniVerseClip", "message_id": 35},
    "4": {"channel": "@AniVerseClip", "message_id": 49},
    "5": {"channel": "@AniVerseClip", "message_id": 76},
    "6": {"channel": "@AniVerseClip", "message_id": 104},
    "7": {"channel": "@AniVerseClip", "message_id": 851},
    "8": {"channel": "@AniVerseClip", "message_id": 127},
    "9": {"channel": "@AniVerseClip", "message_id": 131},
    "10": {"channel": "@AniVerseClip", "message_id": 135},
    "11": {"channel": "@AniVerseClip", "message_id": 148},
    "12": {"channel": "@AniVerseClip", "message_id": 200},
    "13": {"channel": "@AniVerseClip", "message_id": 216},
    "14": {"channel": "@AniVerseClip", "message_id": 222},
    "15": {"channel": "@AniVerseClip", "message_id": 235},
    "16": {"channel": "@AniVerseClip", "message_id": 260},
    "17": {"channel": "@AniVerseClip", "message_id": 360},
    "18": {"channel": "@AniVerseClip", "message_id": 379},
    "19": {"channel": "@AniVerseClip", "message_id": 392},
    "20": {"channel": "@AniVerseClip", "message_id": 405},
    "21": {"channel": "@AniVerseClip", "message_id": 430},
    "22": {"channel": "@AniVerseClip", "message_id": 309},
    "23": {"channel": "@AniVerseClip", "message_id": 343},
    "24": {"channel": "@AniVerseClip", "message_id": 501},
    "25": {"channel": "@AniVerseClip", "message_id": 514},
    "26": {"channel": "@AniVerseClip", "message_id": 462},
    "27": {"channel": "@AniVerseClip", "message_id": 527},
    "28": {"channel": "@AniVerseClip", "message_id": 542},
    "29": {"channel": "@AniVerseClip", "message_id": 555},
    "30": {"channel": "@AniVerseClip", "message_id": 569},
    "31": {"channel": "@AniVerseClip", "message_id": 586},
    "32": {"channel": "@AniVerseClip", "message_id": 624},
    "33": {"channel": "@AniVerseClip", "message_id": 638},
    "34": {"channel": "@AniVerseClip", "message_id": 665},
    "35": {"channel": "@AniVerseClip", "message_id": 696},
    "36": {"channel": "@AniVerseClip", "message_id": 744},
    "37": {"channel": "@AniVerseClip", "message_id": 776},
    "38": {"channel": "@AniVerseClip", "message_id": 789},
    "39": {"channel": "@AniVerseClip", "message_id": 802},
    "40": {"channel": "@AniVerseClip", "message_id": 815},
    "41": {"channel": "@AniVerseClip", "message_id": 835},
    "42": {"channel": "@AniVerseClip", "message_id": 864},
    "43": {"channel": "@AniVerseClip", "message_id": 918},
    "44": {"channel": "@AniVerseClip", "message_id": 931},
    "45": {"channel": "@AniVerseClip", "message_id": 946}
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

# ▶️ Webhook server
async def on_startup(app: web.Application):
    webhook_url = os.getenv("WEBHOOK_URL") + f"/{API_TOKEN}"
    await bot.set_webhook(webhook_url)

async def on_shutdown(app: web.Application):
    await bot.delete_webhook()
def main():
    app = web.Application()
    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)

    # Bot uchun webhook
    SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path=f"/{API_TOKEN}")

    # UptimeRobot yoki boshqa monitoring uchun asosiy sahifa
    async def index(request):
        return web.Response(text="✅ Bot ishlayapti!")

    app.router.add_get("/", index)

    setup_application(app, dp, bot=bot)
    web.run_app(app, host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))


if __name__ == "__main__":
    main()
