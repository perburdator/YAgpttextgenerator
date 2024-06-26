# Имена, тексты для функций, место действий,  а также названия жанров вы можете изменить в этом файле.
# Names, texts for functions, setspace and genre names you can change in this file.
# Moreover, you can change all Russian texts into your language in bot.py

bot_token = 'your telegram token for bot'

text_start = ('Здравствуйте! Я ваш помощник в генерации неких сюжетов на базе YaGpt.\n'
              'Для справки о проекте есть команда /about\n'
              'Для начала общения отправьте эту команду /begin и пройдите небольшую регистрацию')

text_choose_setting = '''
Выберите локацию:
Закулисье - Действия происходят в нашумевшей вселенной "Закулисья" подробнее здесь - https://backrooms.fandom.com/ru/wiki/Backrooms_%D0%92%D0%B8%D0%BA%D0%B8
Лос-Анджелес 2049 - События идут в огромном городе, далеком и не самом светлом будущем.
Альбукерка. дом Вайтов - Шуточная локация. Чем же ответит вам нейросеть ?)))
'''
text_for_setting = 'Хорошо, какие-нибудь еще добавления информации?\nЕсли нет нажмите /begin'

ADMIN_ID = 'your telegram id'
MAX_USERS = 3
MAX_MODEL_TOKENS = 1000
MODEL_TEMPERATURE = 0.6
MAX_SESSIONS = 3
MAX_TOKENS_IN_SESSION = 1500

db_dir = 'YAgpttextgenerator/' # rename if u need 
db_name = 'user_of_bot.db' # rename if u need 

HELP_COMMANDS = ['/debug', '/all_tokens', '/new_story']
genres = ['Ужастик', 'Романтика', 'Детектив']
heroes = ['Волтер Хартвелл', 'Айрен', 'Та самая Дина', 'Рик Декарт']
settings = ['Закулисье', 'Лос-Анджелес 2049', 'Альбукерка. дом Вайтов']

IAM_TOKEN = "token from curl ...."
FOLDER_ID = 'your folder_id for YAGPT'
GPT_MODEL = 'yandexgpt-lite'

CONTINUE_STORY = 'Продолжи сюжет в 1-3 предложения и оставь интригу. Не пиши никакой пояснительный текст от себя'
END_STORY = 'Напиши завершение истории c неожиданной развязкой. Не пиши никакой пояснительный текст от себя'

SYSTEM_PROMPT = (
    "Ты пишешь историю вместе с человеком. "
    "Историю вы пишете по очереди. Начинает человек, а ты продолжаешь. "
    "Если это уместно, ты можешь добавлять в историю диалог между персонажами. "
    "Диалоги пиши с новой строки и отделяй тире. "
    "Не пиши никакого пояснительного текста в начале, а просто логично продолжай историю"
)
