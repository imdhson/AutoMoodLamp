import azure.cognitiveservices.speech as speechsdk
import time
import os
from dotenv import load_dotenv

load_dotenv()

# Speech 설정
speech_key = os.getenv("AZURE_API")
service_region = os.getenv("AZURE_API_LOC")

def recognize_from_file():
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

    print("\n인식 결과:")
    result = '\n'.join(all_results)
    return result

print(recognize_from_file())