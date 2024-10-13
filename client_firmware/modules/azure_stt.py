import azure.cognitiveservices.speech as speechsdk
import time
import os
from dotenv import load_dotenv
import json
from modules.rest import *

load_dotenv()

# Speech 설정
speech_key = os.getenv("AZURE_API")
service_region = os.getenv("AZURE_API_LOC")

def wav_to_text_to_pplx(token, current_time_before):
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    speech_config.speech_recognition_language = "ko-KR"
    audio_config = speechsdk.audio.AudioConfig(filename="api_audio.wav")

    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    done = False
    all_results = []

    def stop_cb(evt):
        nonlocal done
        print('다음 이벤트로 인해 종료됨: {}'.format(evt))
        done = True

    def handle_final_result(evt):
        all_results.append(evt.result.text)

    def handle_canceled(evt):
        print(f'취소됨: {evt.reason}')
        if evt.reason == speechsdk.CancellationReason.Error:
            print(f'취소됨: 오류 상세 정보={evt.error_details}')

    speech_recognizer.recognized.connect(handle_final_result)
    speech_recognizer.session_stopped.connect(stop_cb)
    speech_recognizer.canceled.connect(handle_canceled)

    speech_recognizer.start_continuous_recognition()

    while not done:
        time.sleep(.5)

    speech_recognizer.stop_continuous_recognition()
    result = '\n'.join(all_results)
    llm_score = pplx_api_req(result=result)
    
    # 이곳에 db에 업로드
    add_conversation_data_rest(token, current_time_before, result, llm_score)

def pplx_api_req(result):
    #PPLX API
    PPLX_API = os.getenv("PPLX_API")
    PPLX_API_URL = os.getenv("PPLX_API_URL")
    payload = {
        "model": "llama-3.1-sonar-small-128k-online",
        "messages": [
            {
                "role": "system",
                "content": "You have to analyze your emotions and answer them. Analyze your emotions and rate them from 0 to 10. The lower the number, the worse it feels, and 10 is the best thing to feel. Please answer with only one number. Do not answer anything other than a number."
            },
            {
                "role": "user",
                "content": result
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
        "Authorization": "Bearer "+PPLX_API,
        "Content-Type": "application/json"
    }

    response = requests.request("POST", PPLX_API_URL, json=payload, headers=headers)
    response_dict = json.loads(response.text)
    # print(response_dict)
    try:
        print(response_dict['choices'][0]['message']['content'])
    except KeyError:
        print(response_dict)


if __name__ == "__main__":
    print(wav_to_text_to_pplx())
