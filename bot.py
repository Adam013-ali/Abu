import os, re
from dotenv import load_dotenv
from google import genai
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, CallbackQueryHandler, filters, ContextTypes
import random

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY)

def ask_gemini(prompt, lang="uz"):
    try:
        if lang == "uz":
            system = "Sen o'zbek tilida javob beradigan qiziqarli va kulgili botsan. Har doim o'zbek tilida javob ber. Qisqa va kulgili bo'l."
        else:
            system = "You are a fun and hilarious bot. Always respond in English. Keep it short and funny."
        response = client.models.generate_content(
            model="gemini-2.0-flash-lite",
            contents=f"{system}\n\n{prompt}"
        )
        return response.text.strip()
    except Exception as e:
        print(f"Gemini error: {e}")
        if lang == "uz":
            return "Voy, xatolik yuz berdi! Keyinroq urinib ko'ring 😅"
        return "Oops, something went wrong! Try again 😅"

def detect_lang(text):
    uzbek_chars = set("qg'ʻğşçöüıÇÖÜĞŞ")
    uzbek_words = ["men", "sen", "u", "biz", "siz", "ular", "va", "bu", "ha", "yo'q",
                   "nima", "qani", "qayer", "kim", "qachon", "nega", "qanday", "yaxshi",
                   "rahmat", "salom", "xayr", "bo'ldi", "kerak", "emas", "bor", "yo",
                   "lekin", "chunki", "agar", "ham", "ham", "bir", "ikki", "uch"]
    text_lower = text.lower()
    if any(c in text_lower for c in uzbek_chars):
        return "uz"
    if any(f" {w} " in f" {text_lower} " for w in uzbek_words):
        return "uz"
    return "en"

def main_keyboard():
    buttons = [
        [
            InlineKeyboardButton("🤣 Mazax qil", callback_data="roast"),
            InlineKeyboardButton("😈 Rost/Yolg'on", callback_data="truthdare"),
        ],
        [
            InlineKeyboardButton("🎱 Sehrli shar", callback_data="magic8"),
            InlineKeyboardButton("🔥 Vibe check", callback_data="vibe"),
        ],
        [
            InlineKeyboardButton("🧠 Viktorina", callback_data="quiz"),
            InlineKeyboardButton("🎭 Ikkalasidan biri", callback_data="wouldyou"),
        ],
        [
            InlineKeyboardButton("🍕 Ovqat tanlash", callback_data="food"),
            InlineKeyboardButton("🎬 Film tanlash", callback_data="movie"),
        ],
        [
            InlineKeyboardButton("💰 Hisobni bo'lish", callback_data="bill"),
            InlineKeyboardButton("🎤 Rap jang", callback_data="rap"),
        ],
        [
            InlineKeyboardButton("📖 Hikoya yozish", callback_data="story"),
            InlineKeyboardButton("🤖 Har narsani so'ra", callback_data="ask"),
        ],
    ]
    return InlineKeyboardMarkup(buttons)

# Store waiting states
waiting = {}

async def start(update: Update, context):
    lang = detect_lang(update.message.text or "")
    if lang == "uz":
        text = "Salom! 👋 Men do'stlar guruhi uchun kulgili botman!\n\nNimani xohlaysiz?"
    else:
        text = "Hey! 👋 I'm a fun bot for your friends group!\n\nWhat do you want to do?"
    await update.message.reply_text(text, reply_markup=main_keyboard())

async def menu(update: Update, context):
    await update.message.reply_text(
        "🎉 Menyuni tanlang:",
        reply_markup=main_keyboard()
    )

async def handle_callback(update: Update, context):
    query = update.callback_query
    await query.answer()
    user = query.from_user.first_name
    cat = query.data
    chat_id = query.message.chat_id

    if cat == "roast":
        waiting[chat_id] = "roast"
        await query.edit_message_text(
            f"😈 Kim haqida mazax qilaylik?\nIsm yozing yoki @ bilan tag qiling:"
        )

    elif cat == "truthdare":
        lang = "uz"
        prompt = "Rost yoki do'q o'yini uchun qiziqarli va kulgili 1 ta savol yoz. O'zbek tilida."
        result = ask_gemini(prompt, lang)
        await query.edit_message_text(
            f"😈 Rost yoki Do'q!\n\n{result}",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("🔄 Yana biri", callback_data="truthdare"),
                InlineKeyboardButton("🏠 Menyu", callback_data="back")
            ]])
        )

    elif cat == "magic8":
        waiting[chat_id] = "magic8"
        await query.edit_message_text("🎱 Sehrli sharga savolingizni yozing:")

    elif cat == "vibe":
        vibes = [
            "🔥 Guruh bugun OLOVDA! Hamma energiyasi zo'r!",
            "😴 Guruh bugun uxlamoqda... Kimdir yoqib yuboring!",
            "🤪 Guruh bugun aqldan ozgan! Yaxshi ma'noda 😄",
            "💀 Guruh bugun o'lik... Kimdir kulgili narsa yuboring!",
            "👑 Guruh bugun KING mode'da! Hamma zo'r!",
            "🌊 Guruh bugun chill. Hammasi yaxshi.",
            "⚡ Guruh bugun elektrlanган! Nima bo'lyapti?!",
            "🎭 Guruh bugun drama bor shekilli 👀",
        ]
        await query.edit_message_text(
            f"🔥 Vibe Check!\n\n{random.choice(vibes)}",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("🔄 Yana", callback_data="vibe"),
                InlineKeyboardButton("🏠 Menyu", callback_data="back")
            ]])
        )

    elif cat == "quiz":
        prompt = "Qiziqarli viktorina savoli yoz. 4 ta javob varianti ber (A, B, C, D). To'g'ri javobni ham ayt. O'zbek tilida. Kulgili bo'lsin."
        result = ask_gemini(prompt, "uz")
        await query.edit_message_text(
            f"🧠 Viktorina!\n\n{result}",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("🔄 Yana savol", callback_data="quiz"),
                InlineKeyboardButton("🏠 Menyu", callback_data="back")
            ]])
        )

    elif cat == "wouldyou":
        prompt = "Would you rather o'yini uchun qiziqarli va kulgili 1 ta savol yoz. Ikkita variant ber. O'zbek tilida."
        result = ask_gemini(prompt, "uz")
        await query.edit_message_text(
            f"🎭 Ikkalasidan birini tanlang!\n\n{result}",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("🔄 Yana biri", callback_data="wouldyou"),
                InlineKeyboardButton("🏠 Menyu", callback_data="back")
            ]])
        )

    elif cat == "food":
        prompt = "Toshkentdagi yoki o'zbek oshxonasidan bitta tasodifiy taom tavsiya qil. Nomi, tavsifi va nega yeyish kerakligini kulgili tarzda yoz. O'zbek tilida."
        result = ask_gemini(prompt, "uz")
        await query.edit_message_text(
            f"🍕 Bugun shu yeng!\n\n{result}",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("🔄 Boshqa taom", callback_data="food"),
                InlineKeyboardButton("🏠 Menyu", callback_data="back")
            ]])
        )

    elif cat == "movie":
        prompt = "Bitta tasodifiy film tavsiya qil. Film nomi, janri, qisqa tavsifi va nega ko'rish kerakligini kulgili tarzda yoz. O'zbek tilida."
        result = ask_gemini(prompt, "uz")
        await query.edit_message_text(
            f"🎬 Bugun shu filmni ko'ring!\n\n{result}",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("🔄 Boshqa film", callback_data="movie"),
                InlineKeyboardButton("🏠 Menyu", callback_data="back")
            ]])
        )

    elif cat == "rap":
        waiting[chat_id] = "rap"
        await query.edit_message_text(
            "🎤 Rap jang!\n\nKim haqida rap yozaylik? Ism yozing:"
        )

    elif cat == "story":
        waiting[chat_id] = "story"
        context.bot_data[f"story_{chat_id}"] = []
        await query.edit_message_text(
            "📖 Birga hikoya yozamiz!\n\nBirinchi jumla siz yozing — men davom ettiraman:"
        )

    elif cat == "ask":
        waiting[chat_id] = "ask"
        await query.edit_message_text(
            "🤖 Savolingizni yozing — har qanday narsani so'rang!"
        )

    elif cat == "back":
        await query.edit_message_text(
            "🎉 Menyuni tanlang:",
            reply_markup=main_keyboard()
        )

async def handle_message(update: Update, context):
    msg = update.message
    if not msg or not msg.text:
        return
    text = msg.text.strip()
    chat_id = msg.chat_id
    user = msg.from_user.first_name
    lang = detect_lang(text)

    state = waiting.get(chat_id)

    if state == "roast":
        waiting.pop(chat_id, None)
        prompt = f"{user} do'stini mazax qilmoqchi. Maqsad: {text}. Kulgili, lekin yomon emas, do'stona mazax yoz. 3-4 ta jumla. O'zbek tilida."
        result = ask_gemini(prompt, "uz")
        await msg.reply_text(
            f"🤣 {text} haqida mazax:\n\n{result}",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("🔄 Yana", callback_data="roast"),
                InlineKeyboardButton("🏠 Menyu", callback_data="back")
            ]])
        )

    elif state == "magic8":
        waiting.pop(chat_id, None)
        answers_uz = [
            "Ha, albatta! ✅", "Yo'q, umuman! ❌",
            "Balki... 🤔", "100% ha! 🎯",
            "Hech qachon! 😤", "Bugun emas, ertaga 😅",
            "Katta ehtimol bor! 🌟", "Men ham bilmayman 🤷",
            "Qo'lingizni ko'taringchi... HA! ✋",
            "Uy hayvonlaringizdan so'rang 🐱"
        ]
        await msg.reply_text(
            f"🎱 Savol: {text}\n\nSehrli shar javob berdi:\n\n{random.choice(answers_uz)}",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("🔄 Yana savol", callback_data="magic8"),
                InlineKeyboardButton("🏠 Menyu", callback_data="back")
            ]])
        )

    elif state == "rap":
        waiting.pop(chat_id, None)
        prompt = f"{text} haqida kulgili o'zbek tilida rap yoz. 4-8 qator. Qofiyali bo'lsin. Kulgili va do'stona."
        result = ask_gemini(prompt, "uz")
        await msg.reply_text(
            f"🎤 {text} haqida rap:\n\n{result}",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("🔄 Yana rap", callback_data="rap"),
                InlineKeyboardButton("🏠 Menyu", callback_data="back")
            ]])
        )

    elif state == "story":
        story_key = f"story_{chat_id}"
        story = context.bot_data.get(story_key, [])
        story.append(f"{user}: {text}")
        prompt = f"Bu hikoyaning davomi:\n{chr(10).join(story)}\n\nBir jumla bilan davom ettir. O'zbek tilida. Qiziqarli va kulgili bo'lsin."
        result = ask_gemini(prompt, "uz")
        story.append(f"Bot: {result}")
        context.bot_data[story_key] = story
        await msg.reply_text(
            f"📖 Bot davom ettirdi:\n\n{result}\n\nSiz davom ettiring yoki /menyu bosing:",
        )

    elif state == "ask":
        waiting.pop(chat_id, None)
        prompt = text
        result = ask_gemini(prompt, lang)
        await msg.reply_text(
            f"🤖 Javob:\n\n{result}",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("🔄 Yana so'ra", callback_data="ask"),
                InlineKeyboardButton("🏠 Menyu", callback_data="back")
            ]])
        )

    else:
        # No state — check if it's a command-like message
        t = text.lower()
        if any(w in t for w in ["salom", "hello", "hi", "hey", "start", "boshlash"]):
            if lang == "uz":
                await msg.reply_text(
                    "Salom! 👋 Men do'stlar guruhi uchun kulgili botman!\n\nNimani xohlaysiz?",
                    reply_markup=main_keyboard()
                )
            else:
                await msg.reply_text(
                    "Hey! 👋 I'm a fun bot for your friends group!\n\nWhat do you want to do?",
                    reply_markup=main_keyboard()
                )

app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("menyu", menu))
app.add_handler(CommandHandler("menu", menu))
app.add_handler(CallbackQueryHandler(handle_callback))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
print("✅ Fun bot is running!")
app.run_polling()
