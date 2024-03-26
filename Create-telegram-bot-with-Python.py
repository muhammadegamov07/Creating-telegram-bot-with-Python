# Import necessary libraries
import logging
import sqlite3
from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import InputFile
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from spotipy.oauth2 import SpotifyClientCredentials

# Set up Spotify client credentials
auth_manager = SpotifyClientCredentials(client_id="Insert your API",
                                        client_secret="Insert your API")
sp = spotipy.Spotify(auth_manager=auth_manager)

# Initialize the bot and dispatcher
bot = Bot('Insert your API')
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

# Create SQLite database connection
conn = sqlite3.connect('user_messages.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS user_messages
                  (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  user_id INTEGER,
                  user_name TEXT,
                  message TEXT)''')
conn.commit()
markup2 = types.InlineKeyboardMarkup()
btn1 = types.InlineKeyboardButton('X', callback_data='delete')
markup2.add(btn1)

# Dictionary to store songs
songs = {}

# Start command handler
@dp.message_handler(commands=['start'])
async def on_start(message:types.Message):
    photo = InputFile('Insert your photo direction')
    await bot.send_photo(chat_id=message.chat.id, photo=photo)
    await message.answer(f'Insert your starting message {message.from_user.first_name}')
    text = '''Insert your starting message'''
    await message.answer(text, parse_mode='html')

# Image command handler
@dp.message_handler(commands=['image'])
async def cmd_image(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup()
    button_1 = types.KeyboardButton(text="Nature🏞")
    keyboard.add(button_1)
    button_2 = types.KeyboardButton(text="AI🤖")
    keyboard.add(button_2)
    button_3 = types.KeyboardButton(text="Programming Desktop📺")
    keyboard.add(button_3)
    button_4 = types.KeyboardButton(text="Wallpaper🖼")
    keyboard.add(button_4)
    photo = InputFile('Insert your photo direction')
    await bot.send_photo(chat_id=message.chat.id, photo=photo)
    await message.answer("Qaysi yo'nalishdagi rasmni tanlaysiz?", reply_markup=keyboard)

# Nature category handler
@dp.message_handler(text="Nature🏞")
async def nature(message: types.Message):
    photo = InputFile('Insert your photo direction')
    await bot.send_photo(chat_id=message.chat.id, photo=photo)
    photo = InputFile('Insert your photo direction')
    await bot.send_photo(chat_id=message.chat.id, photo=photo)
    photo = InputFile('Insert your photo direction')
    await bot.send_photo(chat_id=message.chat.id, photo=photo)

# AI category handler
@dp.message_handler(text="AI🤖")
async def ai(message: types.Message):
    photo = InputFile('Insert your photo direction')
    await bot.send_photo(chat_id=message.chat.id, photo=photo)
    photo = InputFile('Insert your photo direction')
    await bot.send_photo(chat_id=message.chat.id, photo=photo)
    photo = InputFile('Insert your photo direction')
    await bot.send_photo(chat_id=message.chat.id, photo=photo)

# Programming Desktop category handler
@dp.message_handler(text="Programming Desktop📺")
async def ai(message: types.Message):
    photo = InputFile('Insert your photo direction')
    await bot.send_photo(chat_id=message.chat.id, photo=photo)
    photo = InputFile('Insert your photo direction')
    await bot.send_photo(chat_id=message.chat.id, photo=photo)
    photo = InputFile('Insert your photo direction')
    await bot.send_photo(chat_id=message.chat.id, photo=photo)

# Wallpaper category handler
@dp.message_handler(text="Wallpaper🖼")
async def ai(message: types.Message):
    photo = InputFile('Insert your photo direction')
    await bot.send_photo(chat_id=message.chat.id, photo=photo)
    photo = InputFile('Insert     photo direction')
    await bot.send_photo(chat_id=message.chat.id, photo=photo)
    photo = InputFile('Insert your photo direction')
    await bot.send_photo(chat_id=message.chat.id, photo=photo)

# Games command handler
@dp.message_handler(commands=['games'])
async def cmd_inline_url(message: types.Message):
    buttons = [
        types.InlineKeyboardButton(text="Time Shooter", url='Insert your link'),
        types.InlineKeyboardButton(text="Draw Car", url='Insert your link'),
        types.InlineKeyboardButton(text="Snyper", url='Insert your link'),
        types.InlineKeyboardButton(text="Street Drift", url='Insert your link'),
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    photo = InputFile('Insert your photo direction')
    await bot.send_photo(chat_id=message.chat.id, photo=photo)
    await message.answer("Qaysi o'yinni o'ynaysiz?", reply_markup=keyboard)

# Video command handler
@dp.message_handler(commands=['video'])
async def cmd_inline_url(message: types.Message):
    buttons = [
        types.InlineKeyboardButton(text="Eng Ko'p Ko'rilgan Video", url='Insert your link'),
        types.InlineKeyboardButton(text="Tenoplov", url='Insert your link'),
        types.InlineKeyboardButton(text="Kunduziy", url='Insert your link'),
        types.InlineKeyboardButton(text="Yaratuvchining Yoqtirgan Videosi", url='Insert your link'),
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    photo = InputFile('Insert your photo direction')
    await bot.send_photo(chat_id=message.chat.id, photo=photo)
    await message.answer("Qaysi videoni ko'rasiz?", reply_markup=keyboard)

# Search command handler
@dp.message_handler(commands=['search'])
async def search_spotipy(message: types.Message):
    qoshiq_nomi = message.text.replace('/search ', '').strip()
    markup = types.InlineKeyboardMarkup(row_width=3)
    buttons = []
    natija = sp.search(q=qoshiq_nomi, limit=5, type='track')

    text = ''
    for i in range(len(natija['tracks']['items'])):
        nomi = natija['tracks']['items'][i]['artists'][0]['name']
        song_name = natija['tracks']['items'][i]['name']
        text += f'{i+1}.{nomi}-{song_name}\n'
        url = natija['tracks']['items'][i]['preview_url']
        if url == None:
            btn = types.InlineKeyboardButton(str(i+1), callback_data='None')
            buttons.append(btn)
        else:
            songs[str(i+1)] = url
            btn = types.InlineKeyboardButton(str(i+1), callback_data=str(i+1))
            buttons.append(btn)
    markup.add(*buttons)
    await message.answer_photo(natija['tracks']['items'][0]['album']['images'][0]['url'], caption=text, reply_markup=markup)
    await message.answer_audio(natija['tracks']['items'][0]['album']['external_urls']['spotify'])

# Callback query handler
@dp.callback_query_handler()
async def handle_call(callback_query: types.CallbackQuery):
    if callback_query.data.isdigit():
        await callback_query.message.answer_audio(songs[callback_query.data])
        await callback_query.message.answer('Ochirib yuborish', reply_markup=markup2)
    elif callback_query.data == 'delete':
        await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id-1)
    elif callback_query.data == 'None':
        await callback_query.message.answer(callback_query.data)

# Social command handler
@dp.message_handler(commands="social")
async def cmd_social(message: types.Message):
    buttons = [
        types.InlineKeyboardButton(text="GitHub", url="https://github.com"),
        types.InlineKeyboardButton(text="Google", url="https://google.com"),
        types.InlineKeyboardButton(text="YouTube", url="https://youtube.com"),
        types.InlineKeyboardButton(text="Instagram", url="https://instagram.com"),
        types.InlineKeyboardButton(text="Facebook", url="https://facebook.com"),
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    photo = InputFile('Insert your photo direction')
    await bot.send_photo(chat_id=message.chat.id, photo=photo)
    await message.answer("Havolalar", reply_markup=keyboard)


# Movie command handler
@dp.message_handler(commands="movie")
async def cmd_movie(message: types.Message):
    buttons = [
        types.InlineKeyboardButton(text="Lookmovie", url="https://lookmovie2.to"),
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    photo = InputFile('Insert your photo direction')
    await bot.send_photo(chat_id=message.chat.id, photo=photo)
    await message.answer("Hozir Sizlarga Men ko'p foydalanadigan, Premyera kinolarni birinchilardan bo'lib yuklanadigan saytning havolasini beraman", reply_markup=keyboard)

# Message command handler
@dp.message_handler(commands=['message'])
async def message_command(message: types.Message):
    photo = InputFile('Insert your photo direction')
    await bot.send_photo(chat_id=message.chat.id, photo=photo)
    await message.reply("AI: Yaxshi, Siz hozir Yaratuvchimga xabar yuborishingiz mumkun!.")

# Handle user messages
@dp.message_handler(lambda message: not message.text.startswith('/'))
async def handle_message(message: types.Message):
    user_id = message.from_user.id
    user_name = message.from_user.username if message.from_user.username else "Unknown"
    user_text = message.text
    
    # Echo user message
    await message.reply(f"You: {user_text}")
    
    # Store user message in the database
    cursor.execute("INSERT INTO user_messages (user_id, user_name, message) VALUES (?, ?, ?)", (user_id, user_name, user_text))
    conn.commit()
    
    # Simulate AI response (in this case, a predefined response)
    ai_response = "AI: Xabaringiz muvaffaqiyatli yuborildi. Yaratuvchim siz bilan tez orada bog'lanadi"
    await message.answer(ai_response)

# Run the bot
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp)


