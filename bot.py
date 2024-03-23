# new project

from sqlite3forgpt import *

from validation import *

from YaGpt import *

# ---------------------------------------------get starting------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename="log_file.txt",
    filemode="w",
)

token = bot_token
bot = telebot.TeleBot(token=token)

user_data = {}


@bot.message_handler(commands=["start"])
def start_func(message):
    logging.info("Sending start text")
    user_id = message.from_user.id
    user_data[user_id] = {
        'session_id': 0,
        'genre': None,
        'hero': None,
        'setting': None,
        'additional_info': None,
        'state': 'registration',
        'test_mod': False
    }
    bot.send_sticker(user_id,
                     "CAACAgIAAxkBAAEDqttl1tZVKZFp4PO5YtGJN8XVwcj9SwAC2A8AAkjyYEsV-8TaeHRrmDQE")  # добавил стикер для приветствования
    bot.send_message(user_id, text_start, reply_markup=create_keyboard(['/new_story']))


@bot.message_handler(commands=['about'])
def about_func(message):
    with open("README.md", "rb") as f:
        bot.send_document(message.chat.id, f)


# ----------------------------------------start of gpt scenery---------------------------------------------------------
@bot.message_handler(commands=['begin'])
def begin_story(message):
    user_id = message.from_user.id
    if not user_data.get(user_id):
        bot.send_message(message.chat.id, 'Type /start , because you are not registered',
                         reply_markup=create_keyboard(['/start']))
        bot.register_next_step_handler(message, begin_story)
    if user_data[user_id]['state'] == 'registration':
        bot.send_message(message.chat.id, 'To start story - proydi small registration /new_story - to da',
                         reply_markup=create_keyboard(['/new_story']))
        bot.register_next_step_handler(message, registration)
    if user_data[user_id]['state'] == 'in storyline':
        bot.send_message(user_id, 'Напишите начало истории:')
        bot.register_next_step_handler(message, get_story)

# useless functions :) vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
@bot.message_handler(commands=['debug'])
def send_logs(message):
    user_id = message.from_user.id
    if user_id == ADMIN_ID:
        if os.path.exists('log_file.txt'):
            with open("log_file.txt", "rb") as f:
                bot.send_document(message.chat.id, f)
        if os.path.exists('log_file_sqlite3.txt'):
            with open("log_file_sqlite3.txt", "rb") as file:
                bot.send_document(message.chat.id, file)
        else:
            bot.send_message(message.chat.id, 'File not found')


@bot.message_handler(commands=['debug_mod_on'])
def debug_mod_on(message):
    user_id = message.from_user.id
    if user_data.get(user_id):
        user_data[user_id]['test_mod'] = True
        bot.send_message(message.chat.id, 'Test mod is on')


@bot.message_handler(commands=['debug_mod_off'])
def debug_mod_off(message):
    user_id = message.from_user.id
    if user_data.get(user_id):
        user_data[user_id]['test_mod'] = False
        bot.send_message(message.chat.id, 'Test mod is off')
# useless functions :) ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# ----------------------------------------getting info for answer------------------------------------------------------
@bot.message_handler(commands=['new_story'])
def registration(message):
    user_id = message.from_user.id
    user_data[user_id]['state'] = 'in storyline'
    bot.send_message(message.chat.id, 'Окей, выберите ваш жанр:',
                     reply_markup=create_keyboard(genres))
    bot.register_next_step_handler(message, get_genre)


def get_genre(message):
    user_id = message.from_user.id
    genre = message.text
    if genre not in genres:
        bot.send_message(message.chat.id, 'Такого жанра на данный момент не существует, попробуйте еще раз.',
                         reply_markup=create_keyboard(genres))
        bot.register_next_step_handler(message, get_genre)
        return

    user_data[user_id]['genre'] = genre
    user_data[user_id]['status'] = 'in storyline'
    bot.send_message(message.chat.id, 'Выбери своего героя:', reply_markup=create_keyboard(heroes))
    bot.register_next_step_handler(message, get_hero)


def get_hero(message):
    user_id = message.from_user.id
    hero = message.text
    if hero not in heroes:
        bot.send_message(message.chat.id, 'Такого персонажа на данный момент не существует, попробуйте еще раз.',
                         reply_markup=create_keyboard(heroes))
        bot.register_next_step_handler(message, get_hero)
        return
    user_data[user_id]['hero'] = hero
    bot.send_message(message.chat.id, text_choose_setting, reply_markup=create_keyboard(settings))
    bot.register_next_step_handler(message, get_setting)


def get_setting(message):
    user_id = message.from_user.id
    setting = message.text
    if setting not in settings:
        bot.send_message(message.chat.id, 'Такого персонажа на данный момент не существует, попробуйте еще раз.',
                         reply_markup=create_keyboard(settings))
        bot.register_next_step_handler(message, get_setting)
        return
    user_data[user_id]['setting'] = setting
    user_data[user_id]['status'] = 'registered'
    bot.send_message(message.chat.id, text_for_setting,
                     reply_markup=create_keyboard(['/begin']))
    bot.register_next_step_handler(message, get_additional_info)


def get_additional_info(message):
    user_id = message.from_user.id
    additional_info = message.text
    if additional_info == '/begin':
        begin_story(message)
    else:
        user_data[user_id]['additional_info'] = additional_info
        bot.send_message(message.chat.id, 'Записал, напишите /begin чтобы начать.',
                         reply_markup=create_keyboard(['/begin']))


# ------------------------------------main func maybe :)---------------------------------------------------------------
@bot.message_handler(content_types=['text'])
def get_story(message: types.Message):
    user_id = message.from_user.id
    genre = user_data[user_id]['genre']
    hero = user_data[user_id]['hero']
    setting = user_data[user_id]['setting']
    if user_data.get(user_id, "additional_info"):
        additional_info = user_data[user_id]['additional_info']
    else:
        additional_info = ''
    upd_user_data = {
        user_id: {
            'genre': genre,
            'hero': hero,
            'setting': setting,
            'additional_info': additional_info
        }}
    user_collection = {
        user_id: [{'role': 'system', 'content': create_system_prompt(upd_user_data, user_id)}]
    }
    user_content = message.text

    if user_content.lower() != 'end':
        user_collection[user_id].append({'role': 'user', 'content': user_content})
        assistant_content = ask_gpt(user_collection[user_id])
        user_collection[user_id].append({'role': 'assistant', 'content': assistant_content})
        bot.send_message(user_id, f'YandexGPT: {assistant_content}')
        bot.send_message(user_id, 'Напиши продолжение истории. Чтобы закончить нажми end: \n',
                         reply_markup=create_keyboard(['end']))
        bot.register_next_step_handler(message, get_end)

# ------------------------------------------sending full story---------------------------------------------------------
def get_end(message):
    user_collection, upd_user_data = very_dumb_func(message)
    user_id = message.from_user.id
    if message.text == 'end':
        assistant_content = ask_gpt(user_collection[user_id], 'end')
        user_collection[user_id].append({'role': 'assistant', 'content': assistant_content})

        for mes in user_collection[user_id]:
            bot.send_message(user_id, f'{mes["content"]}')
        bot.send_message(user_id, 'Конец истории, чтобы начать новую - нажмите на кнопку',
                         reply_markup=create_keyboard(['/start']))
    elif message.text != 'end':
        bot.register_next_step_handler(message, get_story)

# эта функция необходима для работы той, что выше, тк ей необходимы эти параметры, а мне уже не хватает мозгов для
# придумывания более правильного решения этой проблемы боооо:(((((
def very_dumb_func(message):
    user_id = message.from_user.id
    genre = user_data[user_id]['genre']
    hero = user_data[user_id]['hero']
    setting = user_data[user_id]['setting']
    if user_data.get(user_id, "additional_info"):
        additional_info = user_data[user_id]['additional_info']
    else:
        additional_info = ''
    upd_user_data = {
        user_id: {
            'genre': genre,
            'hero': hero,
            'setting': setting,
            'additional_info': additional_info
        }}
    user_collection = {
        user_id: [{'role': 'system', 'content': create_system_prompt(upd_user_data, user_id)}]
    }
    return user_collection, upd_user_data


if __name__ == "__main__":

    logging.info('bot is now running')
    bot.infinity_polling()
