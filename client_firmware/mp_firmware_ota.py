import pyaudio
import numpy as np
import threading
import tensorflow as tf
import tensorflow_hub as hub
from datetime import datetime
import os
import scipy
import requests
from scipy.io import wavfile

from modules.rest import *
from modules.classification import *
from modules.azure_stt import *
from modules.audio_processing import *
from modules.CacheManager import *

import time

import board
import neopixel

single_ton = CacheManager()

def wheel(pos):
    # 0에서 255 사이의 값을 입력하여 색상 값을 얻습니다.
    # 색상은 r - g - b - 다시 r로 전환됩니다.
    if pos < 0 or pos > 255:
        r = g = b = 0
    elif pos < 85:
        r = int(pos * 3)
        g = int(255 - pos * 3)
        b = 0
    elif pos < 170:
        pos -= 85
        r = int(255 - pos * 3)
        g = 0
        b = int(pos * 3)
    else:
        pos -= 170
        r = 0
        g = int(pos * 3)
        b = int(255 - pos * 3)
    return (r, g, b) if ORDER in (neopixel.RGB, neopixel.GRB) else (r, g, b, 0)


def rainbow_cycle(wait):
    for j in range(255):
        for i in range(num_pixels):
            pixel_index = (i * 256 // num_pixels) + j
            pixels[i] = wheel(pixel_index & 255)
        pixels.show()
        time.sleep(wait)

pixel_pin = board.D18
num_pixels = 8
ORDER = neopixel.GRB
pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=0.2, auto_write=False, pixel_order=ORDER
)
rainbow_cycle(0.01)  # 1ms 지연으로 무지개 순환

#대화모드 설정 0.x~...
SPEECH_THRESHOLD = 0.5

#REST API - 서버에 로그인 수행
payload = {
    'username': os.getenv('AUTH_ID'),
    'password': os.getenv('AUTH_PW'),
}
login_server_url = os.getenv('SERVER_URL') + "/auth/login/"
try:
    response = requests.post(login_server_url, data=payload)

    if response.status_code == 200:
        token = response.json().get('token')
        if token:
            print(f"토큰을 성공적으로 받음.{token}")
            single_ton.set('token', token)
        else:
            token=""
            print("토큰 저장 실패")
    else:
        print(f"오류 발생: HTTP 상태 코드 {response.status_code}")
        print(f"오류 메시지: {response.text}")
except requests.exceptions.RequestException as e:
    print(f"requests 오류 {e}")
     
rainbow_cycle(0.01)  # 1ms 지연으로 무지개 순환


# YAMNet 모델 로드
model = tf.saved_model.load('client_firmware/yamnetModel')
single_ton.set('model', model)

#오류시 Current working directory 확인
# 클래스 이름 로드
class_map_path = model.class_map_path().numpy()
single_ton.set('class_names', class_names_from_csv(class_map_path))



pyaudio_0 = pyaudio.PyAudio()
# 오디오 설정
SECOND = 2
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 48000
CHUNK = 1024  # 한번에 처리할 오디오 수

single_ton.set('RATE', RATE)
single_ton.set('SPEECH_THRESHOLD', SPEECH_THRESHOLD)

# 오디오 스트림 열기
stream = pyaudio_0.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)
rainbow_cycle(0.01)  # 1ms 지연으로 무지개 순환
print("* 녹음 시작")

#대화모드 발화 여부 점수
single_ton.set('speech_detect_score', 0)
#대화모드 끊김 감지 시 API로 보낼 데이터
single_ton.set('conv_mode_data' , [])
single_ton.set('conv_mode_bool' , False)
try:
    while True:
        try:
            # 오디오 데이터 읽기
            current_time_before = datetime.now().isoformat()
            data = stream.read(CHUNK * 2 ** SECOND, exception_on_overflow=False)
        except Exception as e:
            print(f"오디오 입력 오류 발생: {e}")
            break
        thread = threading.Thread(target=audio_processing, args=(data, current_time_before))
        thread.start()
        

except KeyboardInterrupt:
    print("* 녹음 종료")

# 스트림 정리
stream.stop_stream()
stream.close()
pyaudio_0.terminate()