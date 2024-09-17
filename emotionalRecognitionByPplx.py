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
    "불안한 생각이 머릿속을 맴돈다.",
    "외롭고 쓸쓸한 하루다.",
    "희망이 보이지 않는 것 같아.",
    "슬픔이 가시지 않는다.",
    "어디에도 기댈 수 없는 기분이야.",
    "기분이 나쁠 때는 그 이유를 모르겠다.",
    "세상이 나를 외면하는 것 같아.",
    "모든 것이 무의미하게 느껴진다.",
    "자신감이 완전히 사라진 것 같다.",
    "미래가 불안하고 두렵다.",
    "누구도 나를 이해하지 못하는 것 같아.",
    "모든 일에 의욕이 없어졌다.",
    "내 인생이 실패작인 것만 같아.",
    "주변 사람들이 다 멀어져 가는 것 같다.",
    "아무리 노력해도 상황이 나아지지 않는다.",
    "나 자신이 너무 싫어.",
    "모든 게 내 잘못인 것 같아 괴롭다.",
    "이 고통이 언제 끝날지 모르겠어.",
    "누군가 위로해주길 바라지만 아무도 없다.",
    "세상에 혼자 남겨진 것 같은 기분이다.",
    "더 이상 버틸 힘이 없는 것 같아.",
    "행복했던 순간들이 다 거짓말 같다.",
    "모든 것이 무너져 내리는 기분이야.",
    "내 삶에 의미를 찾을 수 없어.",
    "이 우울함이 영원히 계속될 것만 같아.",
    "오늘은 행복한 날이에요."
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


