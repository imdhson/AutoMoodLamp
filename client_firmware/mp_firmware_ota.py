# %%
# !pip install pyaudio
# !pip install tensorflow tensorflow_hub scipy

# %%
import pyaudio
import numpy as np
import tensorflow as tf
import tensorflow_hub as hub
from datetime import datetime
import csv
import os
import scipy
import requests
import math

from dotenv import load_dotenv
load_dotenv()

# 오디오 설정
CHUNK = 44100  # 한번에 처리할 오디오 수
SECOND = 3
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

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
        else:
            print("토큰 저장 실패")
    else:
        print(f"오류 발생: HTTP 상태 코드 {response.status_code}")
        print(f"오류 메시지: {response.text}")
except requests.exceptions.RequestException as e:
    print(f"requests 오류 {e}")

def add_sequence_data_rest(token, timestamp, class_idx, class_name, percent):
    rest_url = os.getenv('SERVER_URL')+"/auth/add-sequence-data/"
    try:
        header = {'Authorization': f'token {token}',}
        payload = {'datetime' : timestamp,
                   'class_idx': class_idx,
                   'class_name': class_name,
                   'percent': percent,}
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
            

# YAMNet 모델 로드
model = tf.saved_model.load('client_firmware/yamnetModel')
#오류시 Current working directory 확인

# 클래스 이름 로드
class_map_path = model.class_map_path().numpy()

def class_names_from_csv(class_map_csv_text):
    """Returns list of class names corresponding to score vector."""
    class_names = []
    if tf.io.gfile.exists(class_map_csv_text):
        with open(class_map_csv_text, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                class_names.append(row['display_name'])
    else:
        print(f"File not found: {class_map_csv_text}")
    return class_names

class_names = class_names_from_csv(class_map_path)

#---------------------------
def is_conversation(class_idx):
    speech_arr = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 24, 25, 26, 27, 28, 29, 30, 31, 32, 63, 64, 65}
    #대화와 연관된 클래스의 집합
    if class_idx in speech_arr:
        return True
    return False

def sigmoid(x):
    return 1 / (1 + math.exp(-x))

pyaudio = pyaudio.PyAudio()

# 오디오 스트림 열기
stream = pyaudio.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK*SECOND)

print("* 녹음 시작")
conv_mode_data = None

#대화모드 발화 여부 점수
speech_detect_score = 0

try:
    while True:
        # 오디오 데이터 읽기
        current_time_before = datetime.now().isoformat()
        data = stream.read(CHUNK*SECOND)
        current_time_after = datetime.now().isoformat()

        #YamNet을 위한 변환
        # 바이트 데이터를 16비트 정수 배열로 변환
        audio_data = np.frombuffer(data, dtype=np.int16)

        # 필요한 경우 float32로 변환하고 정규화
        audio_data_float = audio_data.astype(np.float32) / np.iinfo(np.int16).max

        # 리샘플링 계산
        numbers_of_samples = round(len(audio_data_float) * float(16000) / RATE)
        audio_resampled = scipy.signal.resample(audio_data_float, numbers_of_samples)
        
        #YAMNet 모델 예측 by frame 평균 내서 n초동안의 최적 결과만 도출
        scores, embeddings, spectrogram = model(audio_resampled)
        scores = scores.numpy()

        # 모든 프레임의 점수를 평균내어 전체 오디오에 대한 단일 점수 벡터 생성
        average_scores = np.mean(scores, axis=0)

        # 가장 높은 점수를 가진 클래스 찾기
        top_class_index = np.argmax(average_scores)
        top_class = class_names[top_class_index]
        top_class_score = int(average_scores[top_class_index]* 100)  # 최고 점수 클래스의 정확도

        if is_conversation(top_class_index) and speech_detect_score < SPEECH_THRESHOLD*4:
            speech_detect_score += sigmoid(average_scores[top_class_index])
        elif speech_detect_score >= SPEECH_THRESHOLD and not is_conversation(top_class_index):
            speech_detect_score -= sigmoid(speech_detect_score)
        elif not is_conversation(top_class_index) and speech_detect_score > -1:
            speech_detect_score -= sigmoid(average_scores[top_class_index])

        
        #출력
        avg_volume = np.frombuffer(data, dtype=np.int16)
        print(f"{current_time_before} ~ {current_time_after}", end=" | ")
        print("평균 볼륨: ", int(np.average(np.abs(avg_volume))), end=' | ')
        print(f"대화모드점수:{speech_detect_score:.2f}", end = ' | ')
        print(f"{top_class}[{top_class_index}]: {top_class_score}%", end = '')
        if speech_detect_score >= SPEECH_THRESHOLD:
            conv_mode_data.append(data)
            print(f"[대화모드]", end = '')
        elif conv_mode_data != None and speech_detect_score >= SPEECH_THRESHOLD:
            conv_mode_data = None
            # pplx
        print()
        #매 3초마다 결과 나오면 server/accounts/add-sequence-data/ 여기다가 결과 시간, class_name, 정확도를 
        # 서버의 로그인중인 계정(token)에 업로드
        add_sequence_data_rest(token=token, timestamp=current_time_before,
                                class_idx=top_class_index, 
                                class_name=top_class, 
                                percent=top_class_score)

except KeyboardInterrupt:
    print("* 녹음 종료")

# 스트림 정리
stream.stop_stream()
stream.close()
pyaudio.terminate()