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
import math

# 오디오 설정
CHUNK = 16000  # 한번에 처리할 오디오 수
SECOND = 3
FORMAT = pyaudio.paFloat32
CHANNELS = 1
RATE = 16000

#대화모드 설정 0.x~...
SPEECH_THRESHOLD = 0.5

# YAMNet 모델 로드
model = tf.saved_model.load('client_firmware/yamnetModel')
#오류시 Current working directory 확인

# 클래스 이름 로드
import tensorflow as tf
import csv

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

#대화모드 발화 여부 점수
speech_detect_score = 0

try:
    while True:
        # 오디오 데이터 읽기
        current_time_before = datetime.now().strftime("%H:%M[%S]")
        data = stream.read(CHUNK*SECOND)
        current_time_after = datetime.now().strftime("%H:%M:[%S]")
        audio = np.frombuffer(data, dtype=np.float32)

        #YAMNet 모델 예측 by frame 평균 내서 n초동안의 최적 결과만 도출
        scores, embeddings, spectrogram = model(audio)
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
            print(f"[대화모드]", end = '')
        print()

except KeyboardInterrupt:
    print("* 녹음 종료")

# 스트림 정리
stream.stop_stream()
stream.close()
pyaudio.terminate()






'''
        # YAMNet 모델로 예측
        scores, embeddings, spectrogram = model(audio)
        scores = scores.numpy()
        # print("scores shape", scores.shape)

        # 상위 n개 예측 결과 출력
        socresOfClasses = np.argsort(scores[0])[-1:][::-1] 
        #[클래스의 idx] 내림차순으로 가장 높은 n개
        avg_volume = np.frombuffer(data, dtype=np.int16)
        print(datetime.now(), end='|')
        print("평균 볼륨: ", int(np.average(np.abs(avg_volume))), end=' | ')
        # print("예측 결과 [클래스]:float",  end=' | ')
        for i in socresOfClasses: # i에는 클래스idx가 들어감
            #scores[프레임idx][class종류] 따라서 프레임 idx는 SECOND에 따라 바뀔 수 있음
            print(f"{class_names[i]}: {scores[0][i]:.3f}")
'''