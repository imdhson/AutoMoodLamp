# 온디바이스 AI 무드램프 프로젝트

## 프로젝트 소개

대구대학교 컴퓨터공학과 공학제.<br>
이 프로젝트는 YAMNet(Yet Another Mobile Net)을 활용한 온디바이스 AI 기반 무드램프입니다. 주변 소리를 분석하여 적절한 조명 효과를 제공합니다.

## 설치 방법

프로젝트 실행을 위해 다음 라이브러리를 설치해야 합니다:

```bash
pip install pyaudio tensorflow  tensorflow-hub  azure-cognitiveservices-speech scipy django djangorestframework requests django-cors-headers python-dotenv
```

## 개발 중 메모 

autolampserver django 에서 auth 패키지는 API 방식(토큰) 로그인을 담당. <br>
client 패키지는 실제 Web Application을 나타냄.<br>
Azure STT API free for 5hr/month - 
https://portal.azure.com/#create/Microsoft.CognitiveServicesSpeechServices
<br>

## 주요 기능

- **실시간 소리 감지**: PyAudio를 사용하여 주변 소리를 실시간으로 캡처합니다.
- **소리 분류**: YAMNet 모델을 통해 캡처된 소리를 분류합니다.
- **조명 제어**: 분류된 소리에 따라 무드램프의 색상과 밝기를 조절합니다.

## 사용 방법

1. 프로젝트를 클론합니다.
2. 필요한 라이브러리를 설치합니다.
3. `.env` 파일을 생성하고 필요한 환경 변수를 설정합니다.
4. 클라이언트 펌웨어 사용시 RPi 환경에 venv 세팅후 Systemctl에 등록하고 .sh 내에 있는 venv 환경 안에서 패키지 import 등의 세팅을 해야함.
    1. python -m venv 가상환경이름 
    2. source 가상환경이름/bin/activate

## 기여 방법

프로젝트 개선에 관심이 있으시다면 이슈를 열거나 풀 리퀘스트를 보내주세요.

## 라이센스

이 프로젝트는 MIT 라이센스 하에 배포됩니다. 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요.

## YAMNet 라이센스

이 프로젝트는 Google의 YAMNet 모델을 사용합니다. YAMNet은 Apache License 2.0 하에 배포됩니다. YAMNet 사용에 대한 자세한 내용은 [TensorFlow Model Garden 저장소](https://github.com/tensorflow/models)를 참조하세요.

## 주의사항

YAMNet 모델 사용 시 Apache License 2.0의 조건을 준수해야 합니다. 이는 원본 저작권 표시 및 라이센스 고지를 포함하는 것을 의미합니다. 또한, 이 프로젝트에서 YAMNet을 사용한다는 사실을 명시적으로 언급해야 합니다.

## 연락처

문의사항이 있으시면 mail@imdhson.com로 연락 주시기 바랍니다.
```

이 README 파일은 프로젝트의 전반적인 정보, 설치 방법, 주요 기능, 사용 방법, 라이센스 정보 및 YAMNet 관련 주의사항을 포함하고 있습니다. 필요에 따라 내용을 수정하거나 추가할 수 있습니다.