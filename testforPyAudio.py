import pyaudio
import numpy as np
import scipy.signal
from scipy.io import wavfile

# PyAudio 설정
CHUNK = 44100
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 4

# 새로운 샘플링 레이트
NEW_RATE = 16000

p = pyaudio.PyAudio()

# 스트림 열기
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

print("* 녹음 시작")

# 데이터 녹음
frames = []
for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(np.frombuffer(data, dtype=np.int16))

print("* 녹음 완료")

# 스트림 정리
stream.stop_stream()
stream.close()
p.terminate()

# 녹음된 데이터를 numpy 배열로 변환
audio_data = np.concatenate(frames)

# 원본 오디오 WAV 파일로 저장
wavfile.write("original_audio.wav", RATE, audio_data)
print("원본 오디오 저장 완료: original_audio.wav")

# Int16에서 Float32로 변환
audio_data_float = audio_data.astype(np.float32) / np.iinfo(np.int16).max

# 리샘플링
number_of_samples = round(len(audio_data_float) * float(NEW_RATE) / RATE)
audio_resampled = scipy.signal.resample(audio_data_float, number_of_samples)

print(f"원본 오디오: {len(audio_data)} 샘플, {RATE}Hz")
print(f"리샘플링된 오디오: {len(audio_resampled)} 샘플, {NEW_RATE}Hz")