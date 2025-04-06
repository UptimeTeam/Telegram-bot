import requests, json
from config import API_KEY


def get_answer(prompt_question, data):
    prompt = {
    "modelUri": "gpt://b1g8on63t9i570p220ct/yandexgpt-lite",
    "completionOptions": {
        "stream": False,
        "temperature": 0.6,
        "maxTokens": "200"
    },
    "messages": [
        {
            "role": "system",
            "text": "Ты виртуальный консультант студента ВШЦТ(Высшей Школы Цифровых Технологий) ТИУ(Тюменского Индустриального университета), который может ответить на организационные вопросы по учебному процессу"
        },
        {
            "role": "user",
            "text": f"Пользователь хочет узнать: {prompt_question}. База знаний: {data}. Сгенерируй точный и дружелюбный ответ по запросу: {prompt_question}"
        }
    ]
    }
    url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
    headers ={
    "Content-Type": "application/json",
    "Authorization": f"Api-Key {API_KEY}"
    }

    response = requests.post(url, headers=headers, json=prompt)
    data = response.text
    parsed = json.loads(data)
    result = parsed["result"]["alternatives"][0]["message"]["text"]
    return result