import os
from dotenv import load_dotenv
import requests

load_dotenv()

def add_sequence_data_rest(token, timestamp, class_idx, class_name, percent, volume):
    rest_url = os.getenv('SERVER_URL')+"/auth/add-sequence-data/"
    try:
        header = {'Authorization': f'token {token}',}
        payload = {'datetime' : timestamp,
                   'class_idx': class_idx,
                   'class_name': class_name,
                   'percent': percent,
                   'volume': volume,}
        response = requests.post(rest_url, data=payload, headers=header)

        if response.status_code == 200:
            message = response.json().get('message')
            if message:
                print(f"{message}")
            else:
                print("add sequence 에러!")
        else:
            print(f": HTTP 상태 코드 {response.status_code}")
            print(f"{response.text}")
    except requests.exceptions.RequestException as e:
        print(f"requests 오류 {e}")


def add_conversation_data_rest(token, timestamp, text, emotion_score):
    rest_url = os.getenv('SERVER_URL')+"/auth/add-conversation-data/"
    try:
        header = {'Authorization': f'token {token}',}
        payload = {'datetime' : timestamp,
                   'text': text,
                   'emotion_score': emotion_score,}
        response = requests.post(rest_url, data=payload, headers=header)

        if response.status_code == 200:
            message = response.json().get('message')
            if message:
                print(f"{message}")
            else:
                print("add sequence 에러!")
        else:
            print(f": HTTP 상태 코드 {response.status_code}")
            print(f"{response.text}")
    except requests.exceptions.RequestException as e:
        print(f"requests 오류 {e}")