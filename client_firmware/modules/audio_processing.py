import numpy as np
import scipy
from scipy.io import wavfile
from classification import *
from rest import *
from azure_stt import *
from CacheManager import *

def audio_processing(data, RATE, SPEECH_THRESHOLD , model, token, class_names, current_time_before):
    single_ton = CacheManager()


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

    #평균 볼륨 계산
    # 데이터를 16비트 정수 배열로 변환
    audio_array = np.frombuffer(data, dtype=np.int16)
    # RMS(Root Mean Square) 값 계산
    rms = np.sqrt(np.mean(np.square(audio_array.astype(np.float32))))
    # RMS를 데시벨(dB)로 변환
    avg_volume = 20 * np.log10(rms)
    avg_volume = round(avg_volume, 2)
        
    #출력
    print(f"{current_time_before}", end=" | ")
    print("평균 볼륨: ", avg_volume, end=' | ')
    print(f"대화모드점수:{single_ton.get('speech_detect_score'):.2f}", end = ' | ')
    print(f"{top_class}[{top_class_index}]: {top_class_score}%", end = '')
    if single_ton.get('speech_detect_score') >= SPEECH_THRESHOLD:
        print(f"[대화모드]", end = '')
        single_ton.set('conv_mode_bool', True)
        #대화모드 상태이면 conv_mode_data에 append.
        single_ton.set('conv_mode_data', single_ton.get('conv_mode_data').append(np.frombuffer(data, dtype=np.int16)))
    elif single_ton.get('conv_mode_bool') and single_ton.get('speech_detect_score') <= SPEECH_THRESHOLD:
        conv_mode_data_s = np.concatenate(single_ton.get('conv_mode_data'))
        wavfile.write("api_audio.wav", RATE, conv_mode_data_s)
        print("\napi_audio.wav 저장완료. Azure STT 활용 시작")

        #이곳에 Azure STT API 넣기 
        wav_to_text_to_pplx(token, current_time_before)
        single_ton.set('conv_mode_data', [])
        single_ton.set('conv_mode_bool', False)
                  
        print()
        #매 3초마다 결과 나오면 server/accounts/add-sequence-data/ 여기다가 결과 시간, class_name, 정확도를 
        # 서버의 로그인중인 계정(token)에 업로드
        add_sequence_data_rest(token=token, timestamp=current_time_before,
                        class_idx=top_class_index, 
                        class_name=top_class, 
                        percent=top_class_score,
                        volume=avg_volume)