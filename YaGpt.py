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


