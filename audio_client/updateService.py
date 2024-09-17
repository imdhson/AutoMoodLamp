import requests
import os

def download_file(url, filename='mp_firmware.py'):
    # 파일 다운로드
    response = requests.get(url)
    
    # 요청이 성공적인지 확인
    if response.status_code == 200:
        # 파일 쓰기 모드로 열기 (이미 존재하면 덮어쓰기)
        with open(filename, 'wb') as file:
            file.write(response.content)
        print(f"mp_firmware loaded.")
    else:
        print(f"Download fail: {response.status_code}")

url = "https://github.com/imdhson/AutoMoodLamp/raw/master/audio_client/audioProcess.py"  # 다운로드할 파일의 URL
download_file(url)