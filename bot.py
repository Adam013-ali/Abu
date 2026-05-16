
import os, random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, CallbackQueryHandler, filters, ContextTypes

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

ROASTS = [
    # === UMUMIY ===
    "Siz shunchalik sekin yugurасизки, turtles sizdan kechirim so'raydi! 🐢",
    "Siz shunchalik balandparavozki, hatto Google Maps sizni topa olmaydi! 📍",
    "Siz shunchalik kamgapki, jimlik sizdan gapiradi! 🤫",
    "Siz shunchalik uyquchanki, kofe sizdan ruxsat so'raydi! ☕",
    "Siz shunchalik kechikasizki, o'z tug'ilgan kuningizga ham kech kelgansiz! 🎂",
    "Siz shunchalik charchaysizki, o'tirgan kursi ham dam oladi! 🪑",
    "Siz shunchalik sekin yurasizki, snail sizga yo'l beradi! 🐌",
    "Siz shunchalik ko'p ovqat yeyasizki, restoran sizni ko'rsa narxlarini oshiradi! 🍽️",
    "Siz shunchalik aqllisizki, Google ham ba'zan sizdan so'raydi! 🧠",
    "Siz shunchalik optimistki, hatto kompyuter viruslari sizga umid bag'ishlaydi! 💻",
    "Siz shunchalik baxtlisizki, muammolar ham sizga hasad qiladi! 🍀",
    "Siz shunchalik go'zalsizki, ko'zgu sizga iltimos qilib qaraydi! 🪞",
    "Siz shunchalik dono'siz, entsiklopediya sizdan ma'lumot oladi! 📚",
    "Siz shunchalik kuchli, devor sizdan yo'l so'raydi! 💪",
    "Siz shunchalik mashhursiz, hatto toshlar sizni taniydi! 🪨",
    # === MUHABBAT ===
    "Siz shunchalik romantikki, Valentine's Day sizni ko'rsa qochadi! 💔",
    "Crush sizga qaraydi, siz esa stolga qarasangiz! Klassik! 😅",
    "Sevgi deb yig'laysiz, lekin series ko'rib ko'proq yig'laysiz! 📺",
    "Siz shunchalik romantikki, gullar sizdan kechirim so'raydi! 🌹",
    "Like bosasiz, u ko'rmaydi. Ko'radi, javob bermaydi. Hayot shu! 😂",
    "Siz shunchalik sevgiga to'lasizki, exes ham sizni sog'inadi — lekin qaytmaydi! 💘",
    "DM yozasiz, u 'seen' qo'yadi. Siz yana yozasiz. Qahramonlik! 📱",
    "Sevgida shunchalik yomon omad bor, Cupid sizni ko'rsa kamonini yashiradi! 🏹",
    "Romantik film ko'rasiz, yig'laysiz, keyin uyquga ketasiz — yolg'iz! 😭",
    "Siz sevgi haqida shoir yozgandan ko'ra ko'proq gaplashasiz, lekin bitta ham crush yo'q! 😂",
    # === XOTIN QO'RQUVI ===
    "Xotiningizdan shunchalik qo'rqasizki, telefon jiringlasa avval ismini tekshirасиз! 📵",
    "Do'stlar chaqirsa 'xotinim qo'ymaydi' deysiz — bu endi klassik bahona! 😂",
    "Siz uyda prezident emassiz — siz shunchaki vazir! Xotinim — prezident! 👑",
    "Xotinim yo'q deb o'ylaysiz, lekin u doim biladi! Doim! 👁️",
    "Do'stlar bilan futbol ko'rmoqchisiz, lekin avval 'ruxsat' olasiz! ⚽",
    "Siz shunchalik botirki, xotiningiz uyquda bo'lgandagina qaror qilasiz! 😴",
    "Xotinim oldida sher, tashqarida — mushuk! 🐱",
    "Kechqurun do'stlar bilan chiqmoqchi, lekin telefon jiringladi — o'yin tugadi! 📞",
    "Siz 'erkakman' deysiz, lekin xotinim 'kel' desa kapalak bo'lasiz! 🦋",
    "Xotinim bilmaydi deb o'ylaysiz — u hammasini biladi, shunchaki kutadi! 😏",
    "Pul so'rasangiz do'stlaringizdan emas — xotiningizdan ruxsat olasiz! 💸",
    "Uyda ovoz baland gaplashib ko'ring — xotinim qarash bilan jimlatadi! 👀",
    # === FUTBOL ===
    "Barca muxlisi bo'lsangiz, Real Madrid Champions League o'ynayotganda nima ko'rasiz? Yig'i! 😭",
    "FCB muxlisi bo'lsangiz, Haaland goldan keyin nima his qilasiz? Tanish his! ⚽",
    "Barca 'La Masia' deya maqtanadi, Real Madrid esa Champions League kubogi bilan! 🏆",
    "FCB muxlisi: 'Biz eng yaxshimiz!' Real Madrid: '15 ta UCL. Gaplashing!' 👑",
    "Barca har yili 'bu yil bizning yilimiz' deydi — 2009 dan beri! 😂",
    "Real Madrid yo'qotsa — baxtsiz kun. Barca yo'qotsa — oddiy kun! 😄",
    "Barca muxlisi bo'lish = har yili umid bilan boshlab, yig'i bilan tugatish! 💔",
    "FCB muxlisi Mbappeni ko'rsa nima his qiladi? O'zingiz biling! 😅",
    "Real Madrid — club. Barca — telenovela! 📺",
    "Barca trophy cabinet: changlar. Real Madrid: kuboklar! 🏆",
    # === PS3 VA PES 2013 ===
    "Siz shunchalik eskiki, hali PS3 da o'ynaysiz va buni maqtanasiz! 🎮",
    "PES 2013 da Messi bilan o'ynaysiz — hayotda esa o'zingiz ham o'ynay olmaysiz! ⚽",
    "PS3 — bu antika. Siz — muzey eksponati! 🏛️",
    "PES 2013 grafika: piksel. Sizning hayot grafika: undan ham past! 😂",
    "Hali PES 2013 o'ynayapsizmi? FIFA 2025 chiqdi, do'stim! 🎮",
    "PS3 jiringlaydi, siz yugurasiz — xotinim chaqirsa bunday yugurmayman deysiz! 😂",
    "PES 2013 da Ronaldo bilan gol urdingiz — real hayotda esa gol urolmaysiz! ⚽",
    "Siz shunchalik eskiki, PS3 sizni ko'rsa 'aka' deydi! 🎮",
    "PES 2013 — o'sha davrning eng zo'ri. Siz — o'sha davrning qoldig'i! 😄",
    "Hali PS3 controller ushlaysizmi? Qo'llaringiz eskirib ketmadimi? 🕹️",
    # === SARCASM ===
    "Voy, siz kelibsiz! Bugun bayram ekan! 🎉 (yo'q, emas)",
    "Zo'r fikr! Rostdan ham! (umuman emas) 👏",
    "Siz shunchalik aqllisiz, har safar og'iz ochsangiz — hayratda qolaman! 🤯",
    "Ajoyib keldingiz! Umuman kutmagan edik! 😏",
    "Ha, albatta siz hamma narsani bilasiz! Google yopilsin endi! 🔍",
    "Sizning fikringiz juda muhim! Yozib qo'ydim! (axlatga tashlash uchun) 📝",
    "Zo'r plan! Hech narsani o'ylamagansiz — lekin zo'r! 🧠",
    "Siz bilan suhbatlashish — doimo ilhom beradi! (uxlash ilhomi) 😴",
    # === KO'NGILCHAN ===
    "Siz shunchalik ko'ngilchansizki, mushuklar ham sizdan pul so'raydi! 😺",
    "Do'st desa yordamlashasiz, tanish desa yordamlashasiz, begona desa ham — siz ATM emassiz! 🏧",
    "Siz 'yo'q' deyolmaysiz — bu sizning kuchingiz ham, kulfatingiz ham! 😅",
    "Hamma sizdan pul so'raydi, siz esa 'albatta' deysiz — keyin o'zingiz non topolmaysiz! 🍞",
    "Ko'ngilchanlik — yaxshi xislat. Sizniki esa kasallik darajasida! 🏥",
    "Hamma muammosini sizga aytadi, chunki siz doktor emassiz lekin doktordan yaxshi tinglaysiz! 👂",
    "Siz 'yo'q' deyolmasligingiz sababli, hozir 10 ta ish bajarasiz — barchasini boshqalar uchun! 😂",
    "Siz shunchalik yaxshisizki, yomonlar ham sizni yaxshi ko'radi! 😇",
]

QUIZ = [
    {"q": "Dunyodagi eng yaxshi futbol klubi qaysi?", "a": "A) Barca", "b": "B) FCB", "joke": "Ikkalasi ham noto'g'ri — to'g'ri javob: Real Madrid! 👑🏆"},
    {"q": "Xotiningizdan qo'rqasizmi?", "a": "A) Ha, albatta", "b": "B) Ha, juda ko'p", "joke": "Ikkalasi ham to'g'ri — farqi yo'q! 😂👑"},
    {"q": "PES 2013 yoki FIFA 2025?", "a": "A) PES 2013 — klassik!", "b": "B) PES 2013 — eng zo'r!", "joke": "Ikkalasi ham PES 2013 — siz hali 2013 da yashaysiz! 🎮😂"},
    {"q": "Barca necha marta UCL yutgan so'nggi 10 yilda?", "a": "A) Ko'p marta", "b": "B) Juda ko'p marta", "joke": "Ikkalasi ham yolg'on — Real Madrid yutgan! 😂🏆"},
    {"q": "Siz romantik odamsizmi?", "a": "A) Ha, juda ham", "b": "B) Ha, albatta", "joke": "Ikkalasi ham yolg'on — crush sizga qaramaydi! 💔😂"},
    {"q": "PS3 yoki PS5?", "a": "A) PS3 — chunki boshqa yo'q", "b": "B) PS3 — klassik!", "joke": "Ikkalasi ham PS3 — siz hali o'sha davrdasiz! 🎮😅"},
    {"q": "Erkak uyda kim?", "a": "A) Xotin", "b": "B) Albatta xotin", "joke": "Ikkalasi ham to'g'ri — savol noto'g'ri edi! 👑😂"},
    {"q": "Hayotdagi eng katta yolg'on nima?", "a": "A) Men dietadaman", "b": "B) 5 daqiqada kelaman", "joke": "Ikkalasi ham to'g'ri — lekin uchinchisi: 'Xotinim bilmaydi!' 😂"},
    {"q": "Messi yoki Ronaldo?", "a": "A) Messi — u yaxshiroq", "b": "B) Ronaldo — u yaxshiroq", "joke": "To'g'ri javob: RONALDO! CR7 GOAT! 🐐"},
    {"q": "Do'stingiz pul so'rasa nima qilasiz?", "a": "A) Beraman, men ko'ngilchanman", "b": "B) Beraman, u qaytaradi (deb o'ylayman)", "joke": "Pul ketdi, do'stlik qoldi — pul qaytmaydi! 😂💸"},
    {"q": "Kechqurun do'stlar chaqirsa?", "a": "A) Xotinim qo'ymaydi", "b": "B) Xotinim ruxsat bermaydi", "joke": "Ikkalasi ham to'g'ri — xotinim prezident! 👑😂"},
    {"q": "Siz sportzalsizmi?", "a": "A) Ha, telefonda sport ko'raman", "b": "B) Ha, PES o'ynayman", "joke": "Ikkalasi ham sport — lekin o'tirgan holda! 😂🛋️"},
    {"q": "Hayotda eng muhim narsa nima?", "a": "A) Sog'liq", "b": "B) Pul", "joke": "Ikkalasi ham noto'g'ri — to'g'ri javob: WiFi parol! 📶😂"},
    {"q": "Eng yaxshi diyeta nima?", "a": "A) Ertaga boshlayman", "b": "B) Dushanbadan boshlayman", "joke": "Ikkalasi ham to'g'ri — diyeta hech qachon boshlanmaydi! 😂🍕"},
    {"q": "Nega kech qoldingiz?", "a": "A) Tiqilinch bo'ldi", "b": "B) Soat to'xtab qoldi", "joke": "Ikkalasi ham yolg'on — haqiqat: uydan kech chiqdingiz! 😂⏰"},
    {"q": "Siz futbol o'ynay olasizmi?", "a": "A) Ha, PES da", "b": "B) Ha, YouTube da ko'raman", "joke": "Ikkalasi ham to'g'ri — real maydonga chiqmagan! ⚽😂"},
    {"q": "Eng yaxshi mashina qaysi?", "a": "A) Nexia", "b": "B) Matiz", "joke": "Ikkalasi ham noto'g'ri — to'g'ri javob: xotiningizniki! 😂🚗"},
    {"q": "Necha yil PS3 o'ynaysiz?", "a": "A) 10 yildan ortiq", "b": "B) Hali ham o'ynamoqdaman", "joke": "Ikkalasi ham to'g'ri — PS3 sizning umr yo'ldoshingiz! 🎮😂"},
    {"q": "Barca nima?", "a": "A) Real Madriddan pastroq klub", "b": "B) UCL'dan chiqib ketadigan klub", "joke": "Ikkalasi ham to'g'ri! Barca muxlislari yig'lamasin! 😂🏆"},
    {"q": "Nonushta uchun nima yaxshi?", "a": "A) Osh", "b": "B) Yana osh", "joke": "Ikkalasi ham to'g'ri — o'zbek nonushtasi = osh! 🍲😄"},
]

waiting = {}

def main_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🤣 Kimni mazax qilaylik?", callback_data="roast"),
            InlineKeyboardButton("🎲 Tasodifiy mazax", callback_data="random_roast"),
        ],
        [
            InlineKeyboardButton("🧠 Kulgili Quiz", callback_data="random_quiz"),
        ],
    ])

def quiz_keyboard(q):
    return InlineKeyboardMarkup([[
        InlineKeyboardButton(q["a"], callback_data="quiz_wrong"),
        InlineKeyboardButton(q["b"], callback_data="quiz_wrong"),
    ]])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Salom! 👋 Do'stlar guruhi uchun kulgili bot!\n\nTanlang:",
        reply_markup=main_keyboard()
    )

async def menu_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎉 Menyuni tanlang:",
        reply_markup=main_keyboard()
    )

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    cat = query.data
    chat_id = query.message.chat_id
    user = query.from_user.first_name

    if cat == "roast":
        waiting[chat_id] = "roast"
        # Send NEW message so old menu stays
        await query.message.reply_text("😈 Kim haqida mazax qilaylik?\n\nIsm yozing:")

    elif cat == "random_roast":
        roast = random.choice(ROASTS)
        # Send NEW message so it stays in chat
        await query.message.reply_text(
            f"🤣 Mazax:\n\n{roast}",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("🎲 Yana mazax", callback_data="random_roast"),
            ]])
        )

    elif cat == "random_quiz":
        q = random.choice(QUIZ)
        context.bot_data[f"quiz_{chat_id}"] = q
        # Send NEW message so it stays in chat
        await query.message.reply_text(
            f"🧠 Quiz!\n\n{q['q']}",
            reply_markup=quiz_keyboard(q)
        )

    elif cat == "quiz_wrong":
        q = context.bot_data.get(f"quiz_{chat_id}", {})
        joke = q.get("joke", "Ikkalasi ham noto'g'ri! 😂")
        # Send NEW message so it stays in chat
        await query.message.reply_text(
            f"😂 Noto'g'ri!\n\n{joke}",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("🧠 Yana quiz", callback_data="random_quiz"),
                InlineKeyboardButton("🎲 Mazax", callback_data="random_roast"),
            ]])
        )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    if not msg or not msg.text:
        return
    text = msg.text.strip()
    chat_id = msg.chat_id
    user = msg.from_user.first_name
    state = waiting.get(chat_id)

    if state == "roast":
        waiting.pop(chat_id, None)
        roast = random.choice(ROASTS)
        await msg.reply_text(
            f"🤣 {text} haqida mazax:\n\n{roast}",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("🎲 Yana mazax", callback_data="random_roast"),
                InlineKeyboardButton("🧠 Quiz", callback_data="random_quiz"),
            ]])
        )
    else:
        t = text.lower()
        if any(w in t for w in ["salom", "hello", "hi", "hey", "boshlash", "start", "menyu", "menu"]):
            await msg.reply_text(
                f"Salom, {user}! 👋\n\nTanlang:",
                reply_markup=main_keyboard()
            )

app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("menyu", menu_cmd))
app.add_handler(CommandHandler("menu", menu_cmd))
app.add_handler(CallbackQueryHandler(handle_callback))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
print("✅ Fun bot running!")
app.run_polling()
