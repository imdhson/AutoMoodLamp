import azure.cognitiveservices.speech as speechsdk
import time

# Speech 설정
speech_key = ""
service_region = ""
speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
def recognize_from_file():
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    speech_config.speech_recognition_language = "ko-KR"
    audio_config = speechsdk.audio.AudioConfig(filename="api_audio.wav")

    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    done = False
    def stop_cb(evt):
        nonlocal done
        print('CLOSING on {}'.format(evt))
        done = True

    all_results = []
    def handle_final_result(evt):
        all_results.append(evt.result.text)

    speech_recognizer.recognized.connect(handle_final_result)
    speech_recognizer.session_stopped.connect(stop_cb)
    speech_recognizer.canceled.connect(stop_cb)

    speech_recognizer.start_continuous_recognition()

    while not done:
        time.sleep(.5)

    speech_recognizer.stop_continuous_recognition()

    print("인식 결과:")
    result = ''.join(all_results)
    return result

print(recognize_from_file())