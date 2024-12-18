# YAMNet기반 적응형 무드램프

## 소개

YAMNet 기반 적응형 무드램프는 사용자의 환경과 감정을 인식하여 맞춤형 조명을 제공하는 혁신적인 프로젝트입니다. 대구대학교 컴퓨터공학과 공학제 작품으로, 라즈베리 파이, 마이크, LED를 활용하여 주변 소리를 분석하고, 대화 내용을 기반으로 사용자의 감정을 파악합니다. 이를 통해 사용자의 심리적 안정감을 높이고 전반적인 삶의 질 향상을 목표로 합니다.

## 개발 배경
- 최근 5년간 우울증 및 불안장애 발생률의 급격한 증가
- 다양한 색의 빛이 개인의 감정에 미치는 긍정적 영향에 대한 연구 결과
- 사용자 맞춤형 조명을 통한 심리적 안정감 제공 및 삶의 질 향상 필요성

## 설치 및 구성

### 1. Requirements
#### Raspberry Pi 4 본체
- Raspberry Pi 4(사양 무관)
- USB-A 형식의 마이크를 연결해야 함
- neopixel 형태의 [SMG] 8 x WS2812B 5050 RGB LED 모듈 RING-Black [SZH-LD086] 을 GPIO로 연결해야 함.

GPIO board.D18에서 neopixel을 제어하게 됨. neopixel은 +, - 연결이 별도로 필요함. RPi 5에서는 neopixel 라이브러리가 11/2024 기준으로 동작하지 않음.

#### Server
- Django 서버를 구동할 수 있는 시스템

### 2. 관련 라이브러리 설치
프로젝트 실행을 위해 다음 라이브러리를 설치해야 합니다:

아래 라이브러리들은 RPi 4 본체와 서버에서 공통적으로 활용하게 되는 라이브러리들입니다.

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
3. 필요한 패키지 설치 및 Systemctl에 등록

### 6. RPi4 본체에서 데몬 가동 시작

```bash
systemctl enable [등록명]
systemctl start [등록명]
```

## 주요 기능

- YAMNet을 활용한 실시간 환경 소리 분석 및 분류
- Azure Speech-to-Text를 이용한 대화 내용 텍스트 변환
- AI 모델을 통한 감정 분석 및 0-10 단계 점수화
- 분석 결과에 따른 맞춤형 LED 조명 제어
- Django 서버를 통한 데이터 저장 및 웹 페이지에서의 시각화

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

## 개발 중 메모 

autolampserver django에서 auth 패키지는 API 방식(토큰) 로그인을 담당.

client 패키지는 실제 Web Application을 나타냄.

[Azure STT API free for 5hr/month](https://portal.azure.com/#create/Microsoft.CognitiveServicesSpeechServices)