import requests
import os
import json
from pprint import pprint
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

url = "https://api.perplexity.ai/chat/completions"
messages = [
    "오늘은 정말 최악의 하루다.",
    "아무것도 하고 싶지 않은 기분이다.",
    "모든 일이 잘 풀리지 않는 것 같아.",
    "누군가와 이야기하고 싶지만 용기가 나지 않는다.",
    "모든 일에 의욕이 없어졌다.",
    "내 삶에 의미를 찾을 수 없어.",
    "이 우울함이 영원히 계속될 것만 같아.",
    "오늘은 행복한 날이에요.",
    "새로운 시작을 할 수 있는 기회야!",
    "작은 것에서 행복을 찾아보자.",
    "나를 믿어, 할 수 있어!",
    "힘든 시기도 지나갈 거야, 조금만 버텨보자.",
    "오늘 하루도 수고했어, 내일은 더 좋은 날이 될 거야.",
    "나 자신을 사랑하는 것부터 시작해보자.",
    "긍정적인 마음가짐이 세상을 바꿀 수 있어.",
    "어려움은 나를 더 강하게 만들 뿐이야."
]

for e in messages:
    payload = {
        "model": "llama-3.1-sonar-small-128k-online",
        "messages": [
            {
                "role": "system",
                "content": "You have to analyze your emotions and answer them. Analyze your emotions and rate them from 0 to 10. The lower the number, the worse it feels, and 10 is the best thing to feel. Please answer with only one number. Do not answer anything other than a number."
            },
            {
                "role": "user",
                "content": e
            }
        ],
        # "max_tokens": "Optional",
        "temperature": 0.2,
        "top_p": 0.9,
        "return_citations": False,
        "search_domain_filter": [],
        "return_images": False,
        "return_related_questions": False,
        "search_recency_filter": "month",
        "top_k": 0,
        "stream": False,
        "presence_penalty": 0,
        "frequency_penalty": 1
    }
    headers = {
        # "Authorization": "Bearer <token>",
        "Authorization": "Bearer "+os.getenv('PPLX_API'),
        "Content-Type": "application/json"
    }

    response = requests.request("POST", url, json=payload, headers=headers)
    response_dict = json.loads(response.text)
    # print(response_dict)
    try:
        print(response_dict['choices'][0]['message']['content'])
    except KeyError:
        pprint(response_dict)


