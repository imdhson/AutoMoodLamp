import requests

#이 스크립트는 GitHub 퍼블릭 repository에서 클라이언트를 위한 펌웨어를 매 부팅시 마다 다운로드 받아 OTA를 구현함.
#인터넷 연결 없을 경우 다운로드 받지않고 기존 스크립트를 사용함.

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

url = "https://github.com/imdhson/AutoMoodLamp/raw/master/audio_client/mp_firmware.py"  # 다운로드할 파일의 URL
download_file(url)