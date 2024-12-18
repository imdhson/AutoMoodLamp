# YAMNet기반 적응형 무드램프

## 소개

YAMNet 기반 적응형 무드램프는 사용자의 환경과 감정을 인식하여 맞춤형 조명을 제공하는 혁신적인 프로젝트입니다. 대구대학교 컴퓨터공학과 공학제 작품으로, 라즈베리 파이, 마이크, LED를 활용하여 주변 소리를 분석하고, 대화 내용을 기반으로 사용자의 감정을 파악합니다. 이를 통해 사용자의 심리적 안정감을 높이고 전반적인 삶의 질 향상을 목표로 합니다.

## 개발 배경
- 최근 5년간 우울증 및 불안장애 발생률의 급격한 증가
- 다양한 색의 빛이 개인의 감정에 미치는 긍정적 영향에 대한 연구 결과
- 사용자 맞춤형 조명을 통한 심리적 안정감 제공 및 삶의 질 향상 필요성

## 주요 기능

- 온디바이스 AI(YAMNet)를 통한 실시간 환경 소리 분석 및 분류
- 환경 소음에 따른 무드등의 자동 밝기 및 색상 조절
- 대화 인식을 통한 심리 상담 보조 기능
- Azure Speech-to-Text를 이용한 대화 내용 텍스트 변환
- AI 모델을 통한 감정 분석 및 0-10 단계 점수화
- 분석 결과에 따른 맞춤형 LED 조명 제어
- Django 서버를 통한 데이터 저장 및 웹 페이지에서의 시각화
- 펌웨어 원격 업데이트 시스템

## 설치 및 구성

### 1. Requirements
#### Raspberry Pi 4 본체
- Raspberry Pi 4(사양 무관)
- USB-A 형식의 마이크를 연결해야 함
- neopixel 형태의 [SMG] 8 x WS2812B 5050 RGB LED 모듈 RING-Black [SZH-LD086] 을 GPIO로 연결해야 함

GPIO board.D18에서 neopixel을 제어하게 됨. neopixel은 +, - 연결이 별도로 필요함. RPi 5에서는 neopixel 라이브러리가 11/2024 기준으로 동작하지 않음.

#### Server
- Django 서버를 구동할 수 있는 시스템

### 2. 관련 라이브러리 설치
프로젝트 실행을 위해 다음 라이브러리를 설치해야 합니다:

```bash
pip install pyaudio tensorflow tensorflow-hub azure-cognitiveservices-speech scipy django djangorestframework requests django-cors-headers python-dotenv
```

### 3. 프로젝트 설정
```bash

```

### 4. 환경 변수 설정
`.env` 파일을 생성하여 아래 내용을 붙여넣고 필요한 환경 변수를 설정합니다.

```env
PPLX_API=___
PPLX_API_URL="https://api.perplexity.ai/chat/completions"
AUTH_ID=___
AUTH_PW=___
SERVER_URL=___
# 끝에 / 사용하면 안됨
AZURE_API=___
AZURE_API_LOC=koreacentral
```

### 5. 클라이언트 펌웨어 설정 (라즈베리 파이 환경)
1. 가상 환경 생성: `python -m venv 가상환경이름`
2. 가상 환경 활성화: `source 가상환경이름/bin/activate`
3. 필요한 패키지 설치 및 systemctl에 등록

- [automoodlamp.service](client_firmware/booting/automoodlamp.service)에서 '/home/계정명'을 수정하세요.
- [automoodlamp.sh](client_firmware/booting/automoodlamp.sh)에서 '/home/계정명'을 수정하세요.

```bash
git clone https://github.com/imdhson/AutoMoodLamp.git ; 
pip install pyaudio tensorflow tensorflow-hub azure-cognitiveservices-speech scipy django djangorestframework requests django-cors-headers python-dotenv ; 
cd AutoMoodLamp ;
cp client_firmware/booting/automoodlamp.service /etc/systemd/system/automoodlamp.service ;
cp client_firmware/booting/automoodlamp.sh ~/automoodlamp.sh
```

### 6. RPi4 본체에서 데몬 가동 시작

```bash
systemctl enable automoodlamp
systemctl start automoodlamp
```

## 작동 원리

1. YAMNet을 통한 환경 분석: 디바이스에서 온디바이스 AI를 사용하여 주변 소리를 분석합니다.
2. 자동 조명 조절: 현재 환경 소음에 따라 무드등의 밝기와 색상이 자동으로 변화합니다.
3. 대화 모드: YAMNet을 통해 일정 주기 이상으로 대화가 감지되면 대화 모드로 진입합니다.
4. 대화 분석: 대화 모드에서는 일정 기준으로 대화를 구분하여 Speech to Text 변환 후 LLM을 통해 감정을 분석합니다.
4. 대화가 아닌 소리의 분석: 대화모드가 아니더라도 텍스트 인식, 감정 분석 기능을 제외하고 현재 어떠한 형식의 소리가 들리는지 서버에 업로드합니다. 소리는 업로드되지 않고 on-device로 처리됩니다.
5. LED 제어: 분석된 감정에 따라 LED를 제어합니다.
6. 데이터 업로드: 분석 결과(transcript, 감정 인식 결과)를 서버에 업로드합니다.
7. 데이터 시각화: 서버에서는 YAMNet 결과를 chart.js로 시각화하고, 대화 모드의 감정 인식 결과를 표로 시각화합니다.

## 서버의 기능

- API 방식 로그인 구현
- 디바이스 연결 및 관리
- 환경 분석 결과 시각화 (그래프 형태)
- 대화 내용(Azure STT API) 및 감정 분석 결과 열람

## 발표, 구동 영상

### Youtube:
[![Video Title](https://img.youtube.com/vi/1lgL65r2zTU/0.jpg)](https://www.youtube.com/watch?v=1lgL65r2zTU)


## 라이선스

이 프로젝트는 [MIT LICENSE](LICENSE.md) 하에 배포됩니다.

### YAMNet 라이센스

이 프로젝트는 Google의 YAMNet 모델을 사용합니다. YAMNet은 Apache License 2.0 하에 배포됩니다. YAMNet 사용에 대한 자세한 내용은 [TensorFlow Model Garden 저장소](https://github.com/tensorflow/models)를 참조하세요.

#### 주의사항

YAMNet 모델 사용 시 Apache License 2.0의 조건을 준수해야 합니다. 이는 원본 저작권 표시 및 라이센스 고지를 포함하는 것을 의미합니다. 또한, 이 프로젝트에서 YAMNet을 사용한다는 사실을 명시적으로 언급해야 합니다.

## 연락처

개발자: 손동휘, 최태영, 황주은

손동휘의 이메일: mail@imdhson.com

Instagram: @imdhson

GitHub: [https://github.com/imdhson](https://github.com/imdhson)