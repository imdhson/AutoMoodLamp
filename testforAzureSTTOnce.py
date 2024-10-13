import azure.cognitiveservices.speech as speechsdk
import time

# Speech 설정
speech_key = ""
service_region = ""
speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
speech_config.speech_recognition_language = "ko-KR"

# 오디오 소스 설정 (wav 파일)
audio_config = speechsdk.audio.AudioConfig(filename="api_audio.wav")

# Speech Recognizer 객체 생성
speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

# 결과를 저장할 변수
all_results = []

# 콜백 함수 정의
def recognized_cb(evt):
    all_results.append(evt.result.text)
    print('RECOGNIZED: {}'.format(evt.result.text))

# 이벤트 핸들러 연결
speech_recognizer.recognized.connect(recognized_cb)

# 연속 인식 시작
print('인식 시작...')
speech_recognizer.start_continuous_recognition()

# 인식이 완료될 때까지 대기
try:
    while True:
        time.sleep(0.5)
except KeyboardInterrupt:
    print('인식 중지...')

# 연속 인식 중지
speech_recognizer.stop_continuous_recognition()

# 전체 결과 출력
print('\n전체 인식 결과:')
print(' '.join(all_results))