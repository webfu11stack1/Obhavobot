import sqlite3
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
import logging
from aiogram.dispatcher import FSMContext
from aiogram.types import Message
from aiogram.types.reply_keyboard import ReplyKeyboardMarkup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types.inline_keyboard import InlineKeyboardButton,InlineKeyboardMarkup

# Initialize SQLite database
conn = sqlite3.connect('netflix_kinolar.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS data (id INTEGER PRIMARY KEY, code TEXT, title TEXT, video TEXT, user_id INTEGER)''')
conn.commit()

bot_token = "6523266288:AAEiTcD4G5CvCY8HnsUOFNlluTJjn_CzyR4"
bot = Bot(token=bot_token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

@dp.message_handler(commands=["panel"],state="*")
async def panel(msg:types.Message,state:FSMContext):
   await msg.answer("👤 <b>Panel bo'limiga faqat adminlar o'tishi mumkin. Agar siz admin bo'lsangiz parolingizni kiriting!</b>  ",parse_mode="HTML")
   await state.set_state("parol")

@dp.message_handler(state="parol")
async def password(msg:Message,state:FSMContext):
    parol=msg.text
    if parol=="Darkweb2003":
        await msg.delete()
        await msg.answer("<b>Parol Tasdiqlandi!</b>✅",parse_mode="HTML")
        panellar=ReplyKeyboardMarkup(
        keyboard=[
           ["📊Statistika",
            "➕Kanal qo'shish"],
            ["📽Kino qo'shish",
             "⛔️Kanal o'chirish"],
            ["✍️Xabar yuborish",
            "🔙Ortga"]  
        ],resize_keyboard=True
    )
        await msg.answer("⬇️<b>Kerakli bo'limni tanlang</b>⬇️",reply_markup=panellar,parse_mode="HTML")
        await state.set_state("panel")
    else:
        sahifa=ReplyKeyboardMarkup(
            keyboard=[
                ["⬅️Bosh sahifaga o'tish"]
            ],resize_keyboard=True
        )
        await msg.answer("<b>❌ Siz Admin emassiz. Panel bo'limi faqat adminlar uchun</b>",reply_markup=sahifa,parse_mode="HTML")
        await state.set_state("sahifa")

@dp.message_handler(text="⬅️Bosh sahifaga o'tish",state="*")
async def sahifa(msg:Message,state:FSMContext):
    await start(msg,state)

@dp.message_handler(text="📽Kino qo'shish",state="*")
async def kinoadd(msg:Message,state:FSMContext):
    await msg.answer("<i>❗️Kino qoshish uchun kino kodini yuboring</i> ",parse_mode="HTML")
    await state.set_state("kode")

@dp.message_handler(state="kode")
async def q(msg: Message, state: FSMContext):
    global kod
    kod = (msg.text)
    if kod.isdigit():
        await msg.answer("<b>🗒Kinoning izohini yuboring</b>",parse_mode="HTML")
        await state.set_state("title")
    elif kod=="📊Statistika":
        await statistika(msg,state)
    elif kod=="⛔️Kanal o'chirish":
        await delet(msg,state)
    elif kod=="➕Kanal qo'shish":
        await kan(msg,state)
    elif kod=="✍️Xabar yuborish":
        await xabar(msg,state)
    elif kod=="📽Kino qo'shish":
        await kinoadd(msg,state)
    elif kod=="🔙Ortga":
        await start(msg,state)
    else:
        await msg.answer("<b>❗️Raqam yuboring</b>",parse_mode="HTML")

@dp.message_handler(state="title")
async def title(msg: Message, state: FSMContext):
    global tit
    tit = msg.text
    await state.set_state("video")
    await msg.answer('<bKinoni yuboring!</b>',parse_mode="HTML")

@dp.message_handler(content_types=types.ContentType.VIDEO, state="video")
async def video(msg: Message, state: FSMContext):
    video = msg.video
    file_id = video.file_id

    cursor.execute("INSERT INTO data (code, title, video) VALUES (?, ?, ?)", (kod, tit, file_id))
    conn.commit()

    await msg.answer(f'''<b>Kino bazaga muvaffaqiyatli qo'shildi!</b>✅''',parse_mode="HTML")
    await start(msg,state)

#Xabar yuborish
@dp.message_handler(text="✍️Xabar yuborish", state="*")
async def xabar(msg: types.Message, state: FSMContext):
    await msg.answer("<b>❕Xabaringiz qoldiring</b>", parse_mode="HTML")
    await state.set_state("xab")

@dp.message_handler(content_types=types.ContentType.TEXT,state="xab")
async def send_xabar(msg: types.Message, state: FSMContext):
    xabar_text = msg.text
    cursor.execute("SELECT DISTINCT user_id FROM data")
    user_ids = cursor.fetchall()

    for user_id in user_ids:
        try:
            await bot.send_message(user_id[0], xabar_text)
        except Exception as e:
            logging.error(f"Error sending message to user {user_id[0]}: {e}")

    await msg.answer(f"<b>Xabar barcha foydalanuvchilarga muvaffaqiyatli yuborildi!</b>✅",parse_mode="HTML")
    await state.set_state("kino")  

@dp.message_handler(content_types=types.ContentType.PHOTO,state="xab")
async def send_xabar(msg: types.Message, state: FSMContext):
    global photo
    photo = msg.photo[-1].file_id
    await msg.answer("<b>✍️Rasmning izohini qoldiring</b>",parse_mode="HTML")
    await state.set_state('Rasm_izoh')

@dp.message_handler(state="Rasm_izoh")
async def rasm(msg:Message,state:FSMContext):
    izoh=msg.text
    cursor.execute("SELECT DISTINCT user_id FROM data")
    user_ids = cursor.fetchall()

    for user_id in user_ids:
        try:
            await bot.send_photo(user_id[0],photo=photo,caption=izoh)
        except Exception as e:
            logging.error(f"Error sending message to user {user_id[0]}: {e}")

    await msg.answer(f"<b>Xabar barcha foydalanuvchilarga muvaffaqiyatli yuborildi!</b>✅",parse_mode="HTML")
    await state.set_state("kino")  

@dp.message_handler(content_types=types.ContentType.VIDEO,state="xab")
async def send_xabar(msg: types.Message, state: FSMContext):
    global videoo
    videoo = msg.video.file_id
    await msg.answer("<b>✍️Videoning izohini qoldiring</b>",parse_mode="HTML")
    await state.set_state('video_izoh')

@dp.message_handler(state="video_izoh")
async def rasm(msg:Message,state:FSMContext):
    izoh_v=msg.text
    cursor.execute("SELECT DISTINCT user_id FROM data")
    user_ids = cursor.fetchall()

    for user_id in user_ids:
        try:
            await bot.send_photo(user_id[0],video=videoo,caption=izoh_v)
        except Exception as e:
            logging.error(f"Error sending message to user {user_id[0]}: {e}")

    await msg.answer(f"<b>Xabar barcha foydalanuvchilarga muvaffaqiyatli yuborildi!</b>✅",parse_mode="HTML")
    await state.set_state("kino")
#Kanal qoshish

channel_ids=[]
channel_urls=[]

@dp.message_handler(text="➕Kanal qo'shish",state="*")
async def kan(msg:Message,state:FSMContext):
    await msg.answer("""
<i>Kanal qoshish uchun kanal id raqam yuboring! \n<b>Eslatma!</b>\nKanalning id raqamini @GetAnyTelegramIdBot⬅️ ushbu botdan olishingiz mumkin! 
\nBotga start berasiz va Kanalingiz url(silka)sini yuborasiz </i>""",parse_mode="HTML")
    await state.set_state("kanal")
    


@dp.message_handler(state="kanal")
async def kanal(msg:types.Message,state:FSMContext):
    
    kanal_id = msg.text

    if kanal_id.startswith("-100"):
        channel_ids.append(kanal_id)
        await msg.answer("<i>Kanal url silkasini yuboring!</i>", parse_mode="HTML")
        await state.set_state("url")
    elif kanal_id == "📊Statistika":
        await statistika(msg, state)
    elif kanal_id == "⛔️Kanal o'chirish":
        await delet(msg, state)
    elif kanal_id == "➕Kanal qo'shish":
        await kan(msg, state)
    elif kanal_id == "✍️Xabar yuborish":
        await xabar(msg, state)
    elif kanal_id == "📽Kino qo'shish":
        await kinoadd(msg, state)
    elif kanal_id == "🔙Ortga":
        await start(msg, state)
    else:
        await msg.answer("❌Xato. Kanal id bunday korinishda bo'lmaydi. Qayta urining!")

@dp.message_handler(state="url")
async def url(msg:Message,state:FSMContext):
    kanal_url=msg.text
    
    urls="https:"
    if urls in kanal_url:
        channel_urls.append(kanal_url)
        await msg.answer("<b>Kanal muvaffaqiyatli qoshildi!</b>✅",parse_mode="HTML")
        await start(msg,state)
    elif kanal_url=="📊Statistika":
        await statistika(msg,state)
    elif kanal_url=="⛔️Kanal o'chirish":
        await delet(msg,state)
    elif kanal_url=="✍️Xabar yuborish":
        await xabar(msg,state)
    elif kanal_url=="📽Kino qo'shish":
        await kinoadd(msg,state)
    elif kanal_url=="🔙Ortga":
        await start(msg,state)
    else:
        await msg.answer("❌Xato. Kanal silkasi to'g'ri ekanligini tekshriring!")


#kanal o'chirish
@dp.message_handler(text="⛔️Kanal o'chirish",state="*")
async def delet(msg:types.Message,state:FSMContext):
    await msg.answer("<i>❗️Kanal id sini jonating</i>",parse_mode="HTML")
    await state.set_state("del")

@dp.message_handler(state="del")
async def dele(msg:types.Message,state:FSMContext):
    global k_id
    k_id=msg.text
    if k_id=="📊Statistika":
        await statistika(msg,state)
    elif k_id=="✍️Xabar yuborish":
        await xabar(msg,state)
    elif k_id=="⛔️Kanal o'chirish":
        await delet(msg,state)
    elif k_id=="➕Kanal qo'shish":
        await kan(msg,state)
    elif k_id=="📽Kino qo'shish":
        await kinoadd(msg,state)
    elif k_id=="🔙Ortga":
        await start(msg,state)
    elif "-100" in k_id: 
        await msg.answer("<i>❗️Kanal silkasini jonating</i>",parse_mode="HTML")
        await state.set_state("silka")
    else:
        await msg.answer("❌Xato. Kanal id bunday korinishda bo'lmaydi. Qayta urining!")


@dp.message_handler(state="silka")
async def delete(msg:types.Message,state:FSMContext):
    global sil
    sil=msg.text
    if "https" in sil  and k_id in channel_ids and sil in channel_urls:
        channel_ids.remove(k_id)
        channel_urls.remove(sil)      
        await msg.answer("<b>Kanal muvaffaqiyatli o'chirildi✅</b>",parse_mode="HTML")
        await state.finish()
    elif sil=="📊Statistika":
        await statistika(msg,state)  
    elif k_id=="✍️Xabar yuborish":
        await xabar(msg,state)
    elif sil=="➕Kanal qo'shish":
        await kan(msg,state)
    elif sil=="📽Kino qo'shish":
        await kinoadd(msg,state)
    elif sil=="🔙Ortga":
        await start(msg,state)    
    else:
        await msg.answer("Bunday kanal yoq")


#Ortga
@dp.message_handler(text="🔙Ortga",state="*")
async def xabar(msg:Message,state:FSMContext):
    await start(msg,state)

# Start komandasini qabul qilish
@dp.message_handler(commands=['start'],state="*")
async def start(msg: Message,state:FSMContext):
    inline = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="📽Tarjima Kinolar | Netflix", url="https://t.me/tarjima_k1nolar_netflix")]
            ],
            row_width=1
        )
    user_id = msg.from_user.id
    cursor.execute("INSERT OR IGNORE INTO data (user_id) VALUES (?)", (user_id,))
    conn.commit()
    check_sub_channels = []
    for channel_id in channel_ids:
        check_sub_channel = await bot.get_chat_member(chat_id=channel_id, user_id=msg.from_user.id)
        check_sub_channels.append(check_sub_channel)

    # Foydalanuvchi kanalga azo bo'lmagan kanallarni aniqlash
    unsubscribed_channels = [channel_id for i, channel_id in enumerate(channel_ids) if check_sub_channels[i].status == "left"]

    if not unsubscribed_channels:
        await msg.answer(f"❗️<b>Assalomu alaykum {msg.from_user.first_name} botimizga xush kelibsiz!</b> \n\n<i>✍️ Kerakli kino kodini yuboring</i>",reply_markup=inline,
                             parse_mode='HTML')
        await state.set_state("code")
    else:
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        for channel_url in channel_urls:
            channel_id = channel_url.split("/")[-1]
            keyboard.add(types.InlineKeyboardButton(text=f"❗️Azo bo'lish ({channel_id})", url=channel_url,callback_data="azo"))
                         
        keyboard.add(types.InlineKeyboardButton(text="Azo boldim✅",callback_data="azo_t"))
            
        await msg.reply(f"⬇️<b>Botdan foydalanish uchun quyidagi kanallarga azo bo'ling:</b>⬇️", reply_markup=keyboard, parse_mode='HTML')
        
        await state.finish()
    
#Azo bolganligini tekshirish
@dp.callback_query_handler(lambda c: c.data == 'azo_t')
async def callback_subscribe(callback_query: types.CallbackQuery, state: FSMContext):
    inline = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="📽Tarjima Kinolar | Netflix", url="https://t.me/tarjima_k1nolar_netflix")]
            ],
            row_width=1
        )
    check_sub_channels = []
    for channel_id in channel_ids:
        check_sub_channel = await bot.get_chat_member(chat_id=channel_id, user_id=callback_query.from_user.id)
        check_sub_channels.append(check_sub_channel)

    # Foydalanuvchi kanalga azo bo'lmagan kanallarni aniqlash
    unsubscribed_channels = [channel_id for i, channel_id in enumerate(channel_ids) if check_sub_channels[i].status == "left"]

    if not unsubscribed_channels:
        await callback_query.message.answer(f"❗️<b>Assalomu alaykum {callback_query.from_user.first_name} botimizga xush kelibsiz!</b> \n\n<i>✍️ Kerakli kino kodini yuboring</i>",reply_markup=inline,
                             parse_mode='HTML')
        await state.set_state("code")
    else:
        keyboard = types.InlineKeyboardMarkup()
        for channel_url in channel_urls:
            channel_id = channel_url.split("/")[-1]
            keyboard.add(types.InlineKeyboardButton(text=f"❗️Azo bo'lish ({channel_id})", url=channel_url,callback_data="azo"))
                         
        keyboard.add(types.InlineKeyboardButton(text="Azo boldim✅",callback_data="azo_t"))

        await callback_query.message.reply(f"⬇️<b>❌Azo bolmadingiz qayta urining!❌</b>⬇️", reply_markup=keyboard, parse_mode='HTML')
        await state.finish()

@dp.message_handler(lambda message: message.text.isdigit(),state="*")
async def check_movie_code(msg: Message,state:FSMContext):
    

    inline = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📽Tarjima Kinolar | Netflix", url="https://t.me/tarjima_k1nolar_netflix")]
        ],
        row_width=2
    )
    pyton_code = msg.text
    check_sub_channels = []
    for channel_id in channel_ids:
        check_sub_channel = await bot.get_chat_member(chat_id=channel_id, user_id=msg.from_user.id)
        check_sub_channels.append(check_sub_channel)

    # Foydalanuvchi kanalga azo bo'lmagan kanallarni aniqlash
    unsubscribed_channels = [channel_id for i, channel_id in enumerate(channel_ids) if check_sub_channels[i].status == "left"]
    if not unsubscribed_channels:
        if pyton_code.isdigit():
                cursor.execute("SELECT title, video FROM data WHERE code = ?", (pyton_code,))
                movie_data = cursor.fetchone()
                if movie_data:
                    title, video_file_id = movie_data
                    await bot.send_video(msg.chat.id, video_file_id,caption=title,reply_markup=inline)
                else:
                    await msg.answer("❌Bunday kodli kino hozircha mavjud emas")
            
        else:
            await msg.answer("<b>❗️Raqam kiriting</b>",parse_mode="HTML")
    else:
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        for channel_url in channel_urls:
            channel_id = channel_url.split("/")[-1]
            keyboard.add(types.InlineKeyboardButton(text=f"❗️Azo bo'lish ({channel_id})", url=channel_url,callback_data="azo"))
                         
        keyboard.add(types.InlineKeyboardButton(text="Azo boldim✅",callback_data="azo_t"))
            
        await msg.reply(f"⬇️<b>Botdan foydalanish uchun quyidagi kanallarga azo bo'ling:</b>⬇️", reply_markup=keyboard, parse_mode='HTML')
        
        await state.finish()


@dp.message_handler(text="📊Statistika",state="*")
async def statistika(msg: Message):
    cursor.execute("SELECT COUNT(DISTINCT user_id) FROM data")
    user_count = cursor.fetchone()[0]
    await msg.reply(f"📊Statistika : <b>{user_count} ta</b> 👤foydalanuvchi mavjud✅",parse_mode="HTML")



if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)


