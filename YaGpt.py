import logging

import requests
from other import *


def ask_gpt(collection, mode='continue'):
    url = f"https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
    headers = {
        'Authorization': f'Bearer {IAM_TOKEN}',
        'Content-Type': 'application/json'
    }
    data = {
        "modelUri": f"gpt://{FOLDER_ID}/{GPT_MODEL}/latest",
        "completionOptions": {
            "stream": False,
            "temperature": MODEL_TEMPERATURE,
            "maxTokens": MAX_MODEL_TOKENS
        },
        "messages": []
    }
    for row in collection:
        content = row['content']
        # Добавляем дополнительный текст к сообщению пользователя в зависимости от режима
        if mode == 'continue' and row['role'] == 'user':
            content += '\n' + CONTINUE_STORY
        elif mode == 'end' and row['role'] == 'user':
            content += '\n' + END_STORY
        data["messages"].append(
            {
                "role": row["role"],
                "text": content
            }
        )
    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code != 200:
            result = f"Status code {response.status_code}"
            return result
        result = response.json()['result']['alternatives'][0]['message']['text']
    except Exception as e:
        result = "Произошла непредвиденная ошибка. Подробности см. в журнале."
        logging.error(f'this error- {e}')
    return result


def create_system_prompt(user_data, user_id):
    prompt = SYSTEM_PROMPT
    prompt += (f"\nНапиши начало истории в стиле {user_data[user_id]['genre']} "
               f"с главным героем {user_data[user_id]['hero']}. "
               f"Вот начальный сеттинг: \n{user_data[user_id]['setting']}. \n"
               "Начало должно быть коротким, 1-3 предложения.\n")
    if user_data[user_id]['additional_info']:
        prompt += (f"Так же пользователь попросил учесть "
                   f"следующую дополнительную информацию: {user_data[user_id]['additional_info']}")
    prompt += 'Не пиши никакие подсказки пользователю, что делать дальше. Он сам знает'
    return prompt


('\n'
 'def main(user_id=1):\n'
 '    print("Привет! Я помогу тебе составить классный сценарий!")\n'
 '    genre = input("Для начала напиши жанр, в котором хочешь составить сценарий: ")\n'
 '    character = input("Теперь опиши персонажа, который будет главным героем: ")\n'
 '    setting = input("И последнее. Напиши сеттинг, в котором будет жить главный герой: ")\n'
 '\n'
 '    # Примеры, уже заполненных настроек\n'
 '  \n'
 '    genre = "драма"\n'
 '    character = (\'Тридцати девяти летний Дэвид Смит: в прошлом — офицер полиции, в настоящем — детектив на пол ставки, еле-еле сводящий концы с концами.\' \n'
 '    \'Одна ошибка несколько лет назад поставила крест на всей его карьере, а характер стал твёрже недельного сухаря.\n\'\n'
 '    \'Высокий, мускулистый мужчина с тёмными волосами, карими глазами и лёгкой щетиной, обладающий острым умом и проницательными способностями.\n\' \n'
 '    \'Его стиль — старый прокуренный пиджак, оставшийся после развода с любимой. Его хобби — помощь людям, у которых нет денег на настоящего детектива.\n\' \n'
 '    \'Он не любит, когда его зовут по имени. Он вообще не любит, когда его зовут. \'\n'
 '    \'Вся его жизнь — отражение криминальных драм в жанре нуар.\')\n'
 '\n'
 '    setting = (\'Город теней — это мрачный и загадочный мегаполис. Он является местом, где обитают самые разные преступники, от мелких воришек до серьёзных группировок.\n\'\n'
 '    \'Над этим городом нависает свинцовое небо и гнетущие тучи, через которые с трудом пробиваются блеклые солнечные лучи.\'\n'
 '    \'Кажется, что дождь никогда не перестаёт лить и распространять аромат алчности и ужаса.\n\'\n'
 '    \'В городе живут абсолютно разные персонажи, каждый из которых имеет свою историю и свои тайны.\'\n'
 '    \'Город теней является местом, где сталкиваются добро и зло, где герои и злодеи сражаются за своё место под солнцем.\n\' \n'
 '    \'Каждый новый день приносит новые испытания и опасности.\')\n'
 '\n'
 '\n'
 '    user_data = {\n'
 '        user_id: {\n'
 '            \'genre\': genre,\n'
 '            \'character\': character,\n'
 '            \'setting\': setting,\n'
 '            \'additional_info\': \'\'\n'
 '        }\n'
 '    }\n'
 '\n'
 '    user_collection = {\n'
 '        user_id: [\n'
 '            {\'role\': \'system\', \'content\': create_system_prompt(user_data, user_id)},\n'
 '        ]\n'
 '    }\n'
 '\n'
 '    user_content = input(\'Напиши начало истории: \n\')\n'
 '    while user_content.lower() != \'end\':\n'
 '        user_collection[user_id].append({\'role\': \'user\', \'content\': user_content})\n'
 '        assistant_content = ask_gpt(user_collection[user_id])\n'
 '        user_collection[user_id].append({\'role\': \'assistant\', \'content\': assistant_content})\n'
 '        print(\'YandexGPT: \', assistant_content)\n'
 '        user_content = input(\'Напиши продолжение истории. Чтобы закончить введи end: \n\')\n'
 '    assistant_content = ask_gpt(user_collection[user_id], \'end\')\n'
 '    user_collection[user_id].append({\'role\': \'assistant\', \'content\': assistant_content})\n'
 '\n'
 '    print(\'\nВот, что у нас получилось:\n\')\n'
 '\n'
 '    for mes in user_collection[user_id]:\n'
 '        print(mes[\'content\'])\n'
 '\n'
 '    input(\'\nКонец... \')\n'
 '\n'
 '\n'
 'if __name__ == "__main__":\n')