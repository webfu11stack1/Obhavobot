from aiogram.types import Message
from aiogram.types.reply_keyboard import ReplyKeyboardMarkup,ReplyKeyboardRemove
from aiogram.types.inline_keyboard import InlineKeyboardButton,InlineKeyboardMarkup
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
logging.basicConfig(level=logging.INFO)


bot_token = "6538347478:AAFQjfvXBxFea1N_ukjYVnZdQAUKDUi1DAM"
bot = Bot(token=bot_token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

user_stats={}
#Admin panel
@dp.message_handler(commands=["panel"],state="*")
async def panel(msg:types.Message,state:FSMContext):
   await msg.answer("👤 <b>Panel bo'limiga faqat adminlar o'tishi mumkin. Agar siz admin bo'lsangiz parolingizni kiriting!</b>  ",parse_mode="HTML")
   await state.set_state("parol")

@dp.message_handler(state="parol")
async def password(msg:Message,state:FSMContext):
    parol=(msg.text)
    if parol=="Darkweb2003":
        await msg.delete()
        await msg.answer("<b>Parol Tasdiqlandi!</b>✅",parse_mode="HTML")
        panellar=ReplyKeyboardMarkup(
        keyboard=[
           ["📊Statistika","✍️Xabar yuborish"],
            ["🔙Ortga"]  
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
 

@dp.message_handler(text="✍️Xabar yuborish", state="*")
async def xabar(msg: types.Message, state: FSMContext):
    await msg.answer("<b>❕Xabaringiz qoldiring</b>", parse_mode="HTML")
    await state.set_state("xab")

@dp.message_handler(content_types=types.ContentType.TEXT,state="xab")
async def send_xabar(msg: types.Message, state: FSMContext):
    xabar_text = msg.text
   

    for user_id in user_stats:
        try:
            await bot.send_message(user_id, xabar_text)
        except Exception as e:
            logging.error(f"Error sending message to user {user_id}: {e}")

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
   

    for user_id in user_stats:
        try:
            await bot.send_photo(user_id,photo=photo,caption=izoh)
        except Exception as e:
            logging.error(f"Error sending message to user {user_id}: {e}")

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
   

    for user_id in user_stats:
        try:
            await bot.send_video(user_id,video=videoo,caption=izoh_v)
        except Exception as e:
            logging.error(f"Error sending message to user {user_id}: {e}")

    await msg.answer(f"<b>Xabar barcha foydalanuvchilarga muvaffaqiyatli yuborildi!</b>✅",parse_mode="HTML")
    await state.set_state("kino")


# Statistikani hisoblash
@dp.message_handler(text="📊Statistika",state="*")
async def statistika(msg:types.Message,state:FSMContext):
    total_users = len(user_stats)
    await msg.reply(f"📊Statistika : <b>{total_users} ta</b> 👤foydalanuvchi mavjud✅",parse_mode="HTML")
    await msg.answer(f"Foydalanuvchilar \n{user_stats}")

@dp.message_handler(text="🔙Ortga",state="*")
async def xabar(msg:Message,state:FSMContext):
    await start(msg,state)

#Start 
@dp.message_handler(commands=['start'],state="*")
async def start(message:types.Message,state:FSMContext):
    user_id = message.from_user.id
    user_stats[user_id] = user_stats.get(user_id, 0) + 1
    header=InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔀Umumiy yo'nalish",callback_data='umumiy'),
             InlineKeyboardButton(text="🔄Mahalliy yo'nalish",callback_data='mahalliy')],      
              [InlineKeyboardButton(text="📍Joylashuv",callback_data='joylashuv',url="https://maps.app.goo.gl/LbfDuuto5Y5vhytM7")]
        ],row_width=2
    )
   
    await  message.answer(f"<b>❗️Assalomu alaykum {message.from_user.first_name} botimizga xush kelibsiz</b> \n\n\t🏠Asosiy menyu",reply_markup=header,parse_mode="HTML")
    await state.set_state("header")


#Mahalliy
@dp.callback_query_handler(lambda c:c.data=="mahalliy",state="*")
async def mahalliy(call:types.CallbackQuery,state:FSMContext):
    mahaliy=ReplyKeyboardMarkup(
        keyboard=[
            ["Xovos-Toshkent","Bekobod-Toshkent"],
            ["Toshkent-Xovos","Guliston-Toshkent"],
            ["Toshkent-Guliston","Toshkent-Bekobod"]
        ],resize_keyboard=True
    )
    await call.message.answer(f"<b>🗒Ushbu menyudan o'zingizga kerakli yo'nalishni tanlang👇</b>",reply_markup=mahaliy,parse_mode="HTML")
    await state.set_state("mahal")

@dp.message_handler(text="Xovos-Toshkent",state="*")
async def xt(msg:Message,state:FSMContext):
    asosiy_menyu=InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🏠Asosiy menyu",callback_data='asos')]
        ],row_width=2
    )
    await msg.answer(f"""<b>🔢No : </b>6453 - <b>Xovos-Toshkent</b> yo'nalishi \n<b>📆Kelish kunlari</b> : <i>Har Kuni</i> 
<b>🕒Kelish vaqti</b> : <i>04:45</i> \n<b>🛑Turish vaqti</b> : <b>2</b> minut \n<b>🚈Jo'nash vaqti</b> : <i>04:47</i> \n<b>⌛️Yetib borish vaqti</b> : <i>07:38</i>""",parse_mode="HTML",reply_markup=asosiy_menyu)
    await state.set_state("asosiy")

@dp.message_handler(text="Bekobod-Toshkent",state="*")
async def xt(msg:Message,state:FSMContext):
    asosiy_menyu=InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🏠Asosiy menyu",callback_data='asos')]
        ],row_width=2
    )
    await msg.answer(f"""<b>🔢No : </b>6449 - <b>Bekobod-Toshkent</b> yo'nalishi \n<b>📆Kelish kunlari</b> : <i>Har Kuni</i> 
<b>🕒Kelish vaqti</b> : <i>08:18</i> \n<b>🛑Turish vaqti</b> : <b>2</b> minut \n<b>🚈Jo'nash vaqti</b> : <i>08:20</i> \n<b>⌛️Yetib borish vaqti</b> : <i>10:00</i>""",parse_mode="HTML",reply_markup=asosiy_menyu)
    await state.set_state("asosiy")

@dp.message_handler(text="Toshkent-Xovos",state="*")
async def xt(msg:Message,state:FSMContext):
    asosiy_menyu=InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🏠Asosiy menyu",callback_data='asos')]
        ],row_width=2
    )
    await msg.answer(f"""<b>🔢No : </b>6411 - <b>Toshkent-Xovos</b> yo'nalishi \n<b>📆Kelish kunlari</b> : <i>Har Kuni</i> 
<b>🕒Kelish vaqti</b> : <i>13:58</i> \n<b>🛑Turish vaqti</b> : <b>2</b> minut \n<b>🚈Jo'nash vaqti</b> : <i>14:00</i> \n<b>⌛️Yetib borish vaqti</b> : <i>16:25</i>
<b>\nKechqurun</b>\n\n<b>🕒Kelish vaqti</b> : <i>21:00</i> \n<b>🛑Turish vaqti</b> : <b>2</b> minut \n<b>🚈Jo'nash vaqti</b> : <i>21:02</i>""",parse_mode="HTML",reply_markup=asosiy_menyu)
    await state.set_state("asosiy")

@dp.message_handler(text="Guliston-Toshkent",state="*")
async def xt(msg:Message,state:FSMContext):
    asosiy_menyu=InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🏠Asosiy menyu",callback_data='asos')]
        ],row_width=2
    )
    await msg.answer(f"""<b>🔢No : </b>6413 - <b>Guliston-Toshkent</b> yo'nalishi \n<b>📆Kelish kunlari</b> : <i>Har Kuni</i> 
<b>🕒Kelish vaqti</b> : <i>15:30</i> \n<b>🛑Turish vaqti</b> : <b>15</b> minut \n<b>🚈Jo'nash vaqti</b> : <i>15:45</i> \n<b>⌛️Yetib borish vaqti</b> : <i>18:06</i>""",parse_mode="HTML",reply_markup=asosiy_menyu)
    await state.set_state("asosiy")

@dp.message_handler(text="Toshkent-Guliston",state="*")
async def xt(msg:Message,state:FSMContext):
    asosiy_menyu=InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🏠Asosiy menyu",callback_data='asos')]
        ],row_width=2
    )
    await msg.answer(f"""<b>🔢No : </b>6414 - <b>Toshkent-Guliston</b> yo'nalishi \n<b>📆Kelish kunlari</b> : <i>Har Kuni</i> 
<b>🕒Kelish vaqti</b> : <i>15:30</i> \n<b>🛑Turish vaqti</b> : <b>30</b> minut \n<b>🚈Jo'nash vaqti</b> : <i>16:00</i> """,parse_mode="HTML",reply_markup=asosiy_menyu)
    await state.set_state("asosiy")

@dp.message_handler(text="Toshkent-Bekobod",state="*")
async def xt(msg:Message,state:FSMContext):
    asosiy_menyu=InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🏠Asosiy menyu",callback_data='asos')]
        ],row_width=2
    )
    await msg.answer(f"""<b>🔢No : </b>6450 - <b>Toshkent-Bekobod</b> yo'nalishi \n<b>📆Kelish kunlari</b> : <i>Har Kuni</i> 
<b>🕒Kelish vaqti</b> : <i>18:31</i> \n<b>🛑Turish vaqti</b> : <b>2</b> minut \n<b>🚈Jo'nash vaqti</b> : <i>18:33</i> """,parse_mode="HTML",reply_markup=asosiy_menyu)
    await state.set_state("asosiy")

#umumiy
@dp.callback_query_handler(lambda c:c.data=="umumiy",state="*")
async def umumiy(call:types.CallbackQuery,state:FSMContext):
    menyu=ReplyKeyboardMarkup(
        keyboard=[
            ["Toshkent-Buxoro(Sharq)","Toshkent-Qo'ng'irot"],
            ["Toshkent-Xiva","Toshkent-Buxoro"],["Andijon-Toshkent-Xiva"],
            ["Toshkent-Termiz-Sariosiyo"],
            ["Toshkent-Shovot","Andijon-Termiz"],["Toshkent-Olot","Andijon-Qo'ng'irot"],
            ["Buxoro(Sharq)-Toshkent","Dushanbe-Toshkent"],
            ["Xiva-Andijon","Qo'ng'irot-Andijon"],["Termiz-Andijon","Olot-Toshkent"],
            ["Xiva-Toshkent","Qo'ng'irot-Toshkent"],["Shovot-Toshkent","Termiz-Toshkent"],
            ["Toshkent-Qarshi","Qarshi-Toshkent"],["Buxoro-Toshkent","Toshkent-Termiz"],
        ],resize_keyboard=True
    )
    await call.message.answer(f"<b>🗒Ushbu menyudan o'zingizga kerakli yo'nalishni tanlang👇</b>",reply_markup=menyu,parse_mode="HTML")
    await state.set_state("header1")

@dp.message_handler(text="Toshkent-Buxoro(Sharq)",state="*")
async def tb(message:types.Message,state:FSMContext):
    asosiy_menyu=InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🏠Asosiy menyu",callback_data='asos')]
        ],row_width=2
    )
    await message.answer(f"""<b>🔢No : </b>10 - <b>Toshkent-Buxoro(Sharq)</b> yo'nalishi \n<b>📆Kelish kunlari</b> : <i>Har Kuni</i> 
<b>🕒Kelish vaqti</b> : <i>10:16</i> \n<b>🛑Turish vaqti</b> : <b>2</b> minut \n<b>🚈Jo'nash vaqti</b> : <i>10:18</i>""",parse_mode="HTML",reply_markup=asosiy_menyu)
    await state.set_state("asosiy")

@dp.message_handler(text="Toshkent-Qo'ng'irot",state="*")
async def tq(message:types.Message,state:FSMContext):
    asosiy_menyu=InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🏠Asosiy menyu",callback_data='asos')]
        ],row_width=2
    )
    await message.answer(f"""<b>🔢No : </b>54 - <b>Toshkent-Qo'ng'irot</b> yo'nalishi \n<b>📆Kelish kunlari</b> : <i>Har Kuni</i> \n<b>🕒Kelish vaqti</b> : <i>15:12</i> 
<b>🛑Turish vaqti</b> : <b>2</b> minut \n<b>🚈Jo'nash vaqti</b> : <i>15:14</i>""",parse_mode="HTML",reply_markup=asosiy_menyu)
    await state.set_state("asosiy")

@dp.message_handler(text="Toshkent-Xiva",state="*")
async def tx(message:types.Message,state:FSMContext):
    asosiy_menyu=InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🏠Asosiy menyu",callback_data='asos')]
        ],row_width=2
    )
    await message.answer(f"""<b>🔢No : </b>56 - <b>Toshkent-Xiva</b> yo'nalishi \n<b>📆Kelish kunlari</b> : <i>Har Kuni</i> 
<b>🕒Kelish vaqti(Kunduzi)</b> : <i>10:16</i> \n<b>🛑Turish vaqti</b> : <b>2</b> minut \n<b>🚈Jo'nash vaqti</b> : <i>10:18</i> 
\n\n<b>🌃Kechqurun</b> \n\n<b>📆Kelish kunlari</b> : <i>Seshanba, Chorshanba, Juma, Shanba</i> \n<b>🕒Kelish vaqti(Kechqurun)</b> : <i>22:12</i> 
<b>🛑Turish vaqti</b> : <b>2</b> minut \n<b>🚈Jo'nash vaqti</b> : <i>22:14</i>""",parse_mode="HTML",reply_markup=asosiy_menyu)
    await state.set_state("asosiy")

@dp.message_handler(text="Andijon-Toshkent-Xiva",state="*")
async def tb(message:types.Message,state:FSMContext):
    asosiy_menyu=InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🏠Asosiy menyu",callback_data='asos')]
        ],row_width=2
    )
    await message.answer(f"""<b>🔢No : </b>126 - <b>Andijon-Toshkent-Xiva</b> yo'nalishi \n<b>📆Kelish kunlari</b> : <i>Har Kuni</i> \n<b>🕒Kelish vaqti</b> : <i>16:51</i> 
<b>🛑Turish vaqti</b> : <b>2</b> minut \n<b>🚈Jo'nash vaqti</b> : <i>16:53</i>""",parse_mode="HTML",reply_markup=asosiy_menyu)
    await state.set_state("asosiy")

@dp.message_handler(text="Toshkent-Buxoro",state="*")
async def tb(message:types.Message,state:FSMContext):
    asosiy_menyu=InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🏠Asosiy menyu",callback_data='asos')]
        ],row_width=2
    )
    await message.answer(f"""<b>🔢No : </b>12 - <b>Toshkent-Buxoro</b> yo'nalishi \n<b>📆Kelish kunlari</b> : <i>Har Kuni</i> 
<b>🕒Kelish vaqti</b> : <i>20:07</i> \n<b>🛑Turish vaqti</b> : <b>2</b> minut \n<b>🚈Jo'nash vaqti</b> : <i>20:09</i>""",parse_mode="HTML",reply_markup=asosiy_menyu)
    await state.set_state("asosiy")

@dp.message_handler(text="Toshkent-Termiz-Sariosiyo",state="*")
async def tb(message:types.Message,state:FSMContext):
    asosiy_menyu=InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🏠Asosiy menyu",callback_data='asos')]
        ],row_width=2
    )
    await message.answer(f"""<b>🔢No : </b>80 - <b>Toshkent-Termiz-Sariosiyo</b> yo'nalishi \n<b>📆Kelish kunlari</b> : <i>Har Kuni</i> 
<b>🕒Kelish vaqti</b> : <i>20:52</i> \n<b>🛑Turish vaqti</b> : <b>2</b> minut \n<b>🚈Jo'nash vaqti</b> : <i>20:54</i>""",parse_mode="HTML",reply_markup=asosiy_menyu)
    await state.set_state("asosiy")

@dp.message_handler(text="Toshkent-Shovot",state="*")
async def tb(message:types.Message,state:FSMContext):
    asosiy_menyu=InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🏠Asosiy menyu",callback_data='asos')]
        ],row_width=2
    )
    await message.answer(f"""<b>🔢No : </b>58 - <b>Toshkent-Shovot</b> yo'nalishi \n<b>📆Kelish kunlari</b> : <i>Dushanba, Payshanba, Yakshanba</i> 
<b>🕒Kelish vaqti</b> : <i>22:12</i> \n<b>🛑Turish vaqti</b> : <b>2</b> minut \n<b>🚈Jo'nash vaqti</b> : <i>22:14</i>""",parse_mode="HTML",reply_markup=asosiy_menyu)
    await state.set_state("asosiy")

@dp.message_handler(text="Andijon-Termiz",state="*")
async def tb(message:types.Message,state:FSMContext):
    asosiy_menyu=InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🏠Asosiy menyu",callback_data='asos')]
        ],row_width=2
    )
    await message.answer(f"""<b>🔢No : </b>130 - <b>Andijon-Termiz</b> yo'nalishi \n<b>📆Kelish kunlari</b> : <i>Seshanba, Payshanba, Juma, Yakshanba</i> 
<b>🕒Kelish vaqti</b> : <i>22:54</i> \n<b>🛑Turish vaqti</b> : <b>2</b> minut \n<b>🚈Jo'nash vaqti</b> : <i>22:56</i>""",parse_mode="HTML",reply_markup=asosiy_menyu)
    await state.set_state("asosiy")

@dp.message_handler(text="Toshkent-Olot",state="*")
async def tb(message:types.Message,state:FSMContext):
    asosiy_menyu=InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🏠Asosiy menyu",callback_data='asos')]
        ],row_width=2
    )
    await message.answer(f"""<b>🔢No : </b>72 - <b>Toshkent-Olot</b> yo'nalishi \n<b>📆Kelish kunlari</b> : <i>Oyning juft kunlari</i> 
<b>🕒Kelish vaqti</b> : <i>23:46</i> \n<b>🛑Turish vaqti</b> : <b>2</b> minut \n<b>🚈Jo'nash vaqti</b> : <i>23:48</i>""",parse_mode="HTML",reply_markup=asosiy_menyu)
    await state.set_state("asosiy")

@dp.message_handler(text="Andijon-Qo'ng'irot",state="*")
async def tb(message:types.Message,state:FSMContext):
    asosiy_menyu=InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🏠Asosiy menyu",callback_data='asos')]
        ],row_width=2
    )
    await message.answer(f"""<b>🔢No : </b>128 - <b>Andijon-Qo'ng'irot</b> yo'nalishi \n<b>📆Kelish kunlari</b> : <i>Chorshanba, Yakshanba</i> 
<b>🕒Kelish vaqti</b> : <i>00:22</i> \n<b>🛑Turish vaqti</b> : <b>2</b> minut \n<b>🚈Jo'nash vaqti</b> : <i>00:24</i>""",parse_mode="HTML",reply_markup=asosiy_menyu)
    await state.set_state("asosiy")

@dp.message_handler(text="Buxoro(Sharq)-Toshkent",state="*")
async def tb(message:types.Message,state:FSMContext):
    asosiy_menyu=InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🏠Asosiy menyu",callback_data='asos')]
        ],row_width=2
    )
    await message.answer(f"""<b>🔢No : </b>11 - <b>Buxoro(Sharq)-Toshkent</b> yo'nalishi \n<b>📆Kelish kunlari</b> : <i>Har Kuni</i> 
<b>🕒Kelish vaqti</b> : <i>11:20</i> \n<b>🛑Turish vaqti</b> : <b>2</b> minut \n<b>🚈Jo'nash vaqti</b> : <i>11:22</i>
\n<b>🌃Kechqurun</b> \n\n<b>🕒Kelish vaqti</b> : <i>21:22</i> \n<b>🛑Turish vaqti</b> : <b>4</b> minut \n<b>🚈Jo'nash vaqti</b> : <i>21:26</i>""",parse_mode="HTML",reply_markup=asosiy_menyu)
    await state.set_state("asosiy")

@dp.message_handler(text="Dushanbe-Toshkent",state="*")
async def tb(message:types.Message,state:FSMContext):
    asosiy_menyu=InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🏠Asosiy menyu",callback_data='asos')]
        ],row_width=2
    )
    await message.answer(f"""<b>🔢No : </b>301 - <b>Dushanbe-Toshkent</b> yo'nalishi \n<b>📆Kelish kunlari</b> : <i>Seshanba</i> 
<b>🕒Kelish vaqti</b> : <i>12:13</i> \n<b>🛑Turish vaqti</b> : <b>2</b> minut \n<b>🚈Jo'nash vaqti</b> : <i>12:15</i>""",parse_mode="HTML",reply_markup=asosiy_menyu)
    await state.set_state("asosiy")

@dp.message_handler(text="Xiva-Andijon",state="*")
async def tb(message:types.Message,state:FSMContext):
    asosiy_menyu=InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🏠Asosiy menyu",callback_data='asos')]
        ],row_width=2
    )
    await message.answer(f"""<b>🔢No : </b>125 - <b>Xiva-Andijon</b> yo'nalishi \n<b>📆Kelish kunlari</b> : <i>Har Kuni</i> 
<b>🕒Kelish vaqti</b> : <i>23:12</i> \n<b>🛑Turish vaqti</b> : <b>2</b> minut \n<b>🚈Jo'nash vaqti</b> : <i>23:14</i>
\n🌄<b>Sahar</b> \n\n<b>📆Kelish kunlari</b> : <i>Chorshanba</i> \n<b>🕒Kelish vaqti</b> : <i>03:24</i> \n<b>🛑Turish vaqti</b> : <b>2</b> minut 
<b>🚈Jo'nash vaqti</b> : <i>03:26</i>""",parse_mode="HTML",reply_markup=asosiy_menyu)
    await state.set_state("asosiy")

@dp.message_handler(text="Qo'ng'irot-Andijon",state="*")
async def tb(message:types.Message,state:FSMContext):
    asosiy_menyu=InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🏠Asosiy menyu",callback_data='asos')]
        ],row_width=2
    )
    await message.answer(f"""<b>🔢No : </b>127 - <b>Qo'ng'irot-Andijon</b> yo'nalishi \n<b>📆Kelish kunlari</b> : <i>Chorshanba, Yakshanba</i> 
<b>🕒Kelish vaqti</b> : <i>03:24</i> \n<b>🛑Turish vaqti</b> : <b>2</b> minut \n<b>🚈Jo'nash vaqti</b> : <i>03:26</i>""",parse_mode="HTML",reply_markup=asosiy_menyu)
    await state.set_state("asosiy")

@dp.message_handler(text="Termiz-Andijon",state="*")
async def tb(message:types.Message,state:FSMContext):
    asosiy_menyu=InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🏠Asosiy menyu",callback_data='asos')]
        ],row_width=2
    )
    await message.answer(f"""<b>🔢No : </b>129 - <b>Termiz-Andijon</b> yo'nalishi \n<b>📆Kelish kunlari</b> : <i>Seshanba, Payshanba, Shanba, Yakshanba</i> 
<b>🕒Kelish vaqti</b> : <i>04:23</i> \n<b>🛑Turish vaqti</b> : <b>3</b> minut \n<b>🚈Jo'nash vaqti</b> : <i>04:26</i>""",parse_mode="HTML",reply_markup=asosiy_menyu)
    await state.set_state("asosiy")

@dp.message_handler(text="Olot-Toshkent",state="*")
async def tb(message:types.Message,state:FSMContext):
    asosiy_menyu=InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🏠Asosiy menyu",callback_data='asos')]
        ],row_width=2
    )
    await message.answer(f"""<b>🔢No : </b>71 - <b>Olot-Toshkent</b> yo'nalishi \n<b>📆Kelish kunlari</b> : <i>Oyning juft kunlari</i> 
<b>🕒Kelish vaqti</b> : <i>04:16</i> \n<b>🛑Turish vaqti</b> : <b>2</b> minut \n<b>🚈Jo'nash vaqti</b> : <i>04:18</i>""",parse_mode="HTML",reply_markup=asosiy_menyu)
    await state.set_state("asosiy")

@dp.message_handler(text="Xiva-Toshkent",state="*")
async def tb(message:types.Message,state:FSMContext):
    asosiy_menyu=InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🏠Asosiy menyu",callback_data='asos')]
        ],row_width=2
    )
    await message.answer(f"""<b>🔢No : </b>75 - <b>Xiva-Toshkent</b> yo'nalishi \n<b>📆Kelish kunlari</b> : <i>Har Kuni</i> 
<b>🕒Kelish vaqti</b> : <i>05:16</i> \n<b>🛑Turish vaqti</b> : <b>2</b> minut \n<b>🚈Jo'nash vaqti</b> : <i>05:18</i>
va <b>📆Kelish kunlari</b> : <i>Dushanba, Payshanba, Juma, Yakshanba</i> \n<b>🕒Kelish vaqti</b> : <i>06:24</i> 
<b>🛑Turish vaqti</b> : <b>6</b> minut \n<b>🚈Jo'nash vaqti</b> : <i>06:30</i>""",parse_mode="HTML",reply_markup=asosiy_menyu)
    await state.set_state("asosiy")

@dp.message_handler(text="Qo'ng'irot-Toshkent",state="*")
async def kt(message:types.Message,state:FSMContext):
    asosiy_menyu=InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🏠Asosiy menyu",callback_data='asos')]
        ],row_width=2
    )
    await message.answer(f"""<b>🔢No : </b>53 - <b>Qo'ng'irot-Toshkent</b> yo'nalishi \n<b>📆Kelish kunlari</b> : <i>Dushanba, Seshanba, Payshanba, Juma, SHanba, Yakshanba</i> 
<b>🕒Kelish vaqti</b> : <i>04:49</i> \n<b>🛑Turish vaqti</b> : <b>2</b> minut \n<b>🚈Jo'nash vaqti</b> : <i>04:51</i>""",parse_mode="HTML",reply_markup=asosiy_menyu)
    await state.set_state("asosiy")

@dp.message_handler(text="Shovot-Toshkent",state="*")
async def sht(message:types.Message,state:FSMContext):
    asosiy_menyu=InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🏠Asosiy menyu",callback_data='asos')]
        ],row_width=2
    )
    await message.answer(f"""<b>🔢No : </b>57 - <b>Shovot-Toshkent</b> yo'nalishi \n<b>📆Kelish kunlari</b> : <i>Seshanba, Chorshanba, Shanba</i> 
<b>🕒Kelish vaqti</b> : <i>06:24</i> \n<b>🛑Turish vaqti</b> : <b>6</b> minut \n<b>🚈Jo'nash vaqti</b> : <i>06:30</i>""",parse_mode="HTML",reply_markup=asosiy_menyu)
    await state.set_state("asosiy")

@dp.message_handler(text="Termiz-Toshkent",state="*")
async def ttt(message:types.Message,state:FSMContext):
    asosiy_menyu=InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🏠Asosiy menyu",callback_data='asos')]
        ],row_width=2
    )
    await message.answer(f"""<b>🔢No : </b>80 - <b>Termiz-Toshkent</b> yo'nalishi \n<b>📆Kelish kunlari</b> : <i>Har Kuni</i> 
<b>🕒Kelish vaqti</b> : <i>07:08</i> \n<b>🛑Turish vaqti</b> : <b>29</b> minut \n<b>🚈Jo'nash vaqti</b> : <i>07:37</i>""",parse_mode="HTML",reply_markup=asosiy_menyu)
    await state.set_state("asosiy")

@dp.message_handler(text="Toshkent-Qarshi",state="*")
async def tq(message:types.Message,state:FSMContext):
    asosiy_menyu=InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🏠Asosiy menyu",callback_data='asos')]
        ],row_width=2
    )
    await message.answer(f"""<b>🔢No : </b>16 - <b>Toshkent-Qarshi</b> yo'nalishi \n<b>📆Kelish kunlari</b> : <i>Har Kuni</i> 
<b>🕒Kelish vaqti</b> : <i>10:09</i> \n<b>🛑Turish vaqti</b> : <b>2</b> minut \n<b>🚈Jo'nash vaqti</b> : <i>10:11</i>""",parse_mode="HTML",reply_markup=asosiy_menyu)
    await state.set_state("asosiy")

@dp.message_handler(text="Qarshi-Toshkent",state="*")
async def qt(message:types.Message,state:FSMContext):
    asosiy_menyu=InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🏠Asosiy menyu",callback_data='asos')]
        ],row_width=2
    )
    await message.answer(f"""<b>🔢No : </b>003 - <b>Qarshi-Toshkent</b> yo'nalishi \n<b>📆Kelish kunlari</b> : <i>Har Kuni</i> 
<b>🕒Kelish vaqti</b> : <i>11:42</i> \n<b>🛑Turish vaqti</b> : <b>2</b> minut \n<b>🚈Jo'nash vaqti</b> : <i>11:44</i>
\n<b>🌃Kechqurun</b> \n\n<b>📆Kelish kunlari</b> : <i>Har Kuni</i> \n<b>🕒Kelish vaqti</b> : <i>21:16</i> \n<b>🛑Turish vaqti</b> : <b>2</b> minut \n<b>🚈Jo'nash vaqti</b> : <i>21:18</i>""",parse_mode="HTML",reply_markup=asosiy_menyu)
    await state.set_state("asosiy")

@dp.message_handler(text="Buxoro-Toshkent",state="*")
async def bt(message:types.Message,state:FSMContext):
    asosiy_menyu=InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🏠Asosiy menyu",callback_data='asos')]
        ],row_width=2
    )
    await message.answer(f"""<b>🔢No : </b>011 - <b>Buxoro-Toshkent</b> yo'nalishi \n<b>📆Kelish kunlari</b> : <i>Har Kuni</i> 
<b>🕒Kelish vaqti</b> : <i>11:42</i> \n<b>🛑Turish vaqti</b> : <b>2</b> minut \n<b>🚈Jo'nash vaqti</b> : <i>11:44</i>
\n<b>🌃Kechqurun \n\n<b>📆Kelish kunlari</b> : <i>Har Kuni</i> \n<b>🕒Kelish vaqti</b> : <i>21:17</i> \n<b>🛑Turish vaqti</b> : <b>2</b> minut \n<b>🚈Jo'nash vaqti</b> : <i>21:19</i>""", parse_mode="HTML", reply_markup=asosiy_menyu)

    await state.set_state("asosiy")

@dp.message_handler(text="Toshkent-Termiz",state="*")
async def tt(message:types.Message,state:FSMContext):
    asosiy_menyu=InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🏠Asosiy menyu",callback_data='asos')]
        ],row_width=2
    )
    await message.answer(f"""<b>🔢No : </b>80 - <b>Toshkent-Termiz</b> yo'nalishi \n<b>📆Kelish kunlari</b> : <i>Har Kuni</i> 
<b>🕒Kelish vaqti</b> : <i>20:52</i> \n<b>🛑Turish vaqti</b> : <b>2</b> minut \n<b>🚈Jo'nash vaqti</b> : <i>20:54</i>""",parse_mode="HTML",reply_markup=asosiy_menyu)
    await state.set_state("asosiy")

@dp.callback_query_handler(lambda d:d.data=="asos",state="*")
async def asosi(call:types.CallbackQuery,state:FSMContext):
    await start(call.message,state)


if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
