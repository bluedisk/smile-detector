# smile-detector
it's a smile detector for fun, powered by AWS Rekognition. 

> 재미삼아 만들어본 웃음 검출기입니다. AWS Rekognition 서비스를 사용 했습니다.

# Usage
## Set AWS keys
set the AWS_ACCESS_KEY & AWS_SECRET_KEY to environment variables or change the source code. in case of changing source, you can use your key chaning default value of `getenv` functions that is filled with `# enter the key here #` by default

> 우선 환경변수에 AWS_ACCESS_KEY & AWS_SECRET_KEY 를 본인의 키로 설정하세요. 환경변수 쓰기가 귀찮으면 소스를 바로 수정해도 됩니다. 추천 위치는 소스 상단에 `getenv` 기본값 부분으로 `# enter the key here #`로 채워져 있습니다.

## Install requirements
```
$ pip install -R requirements.txt
```
this requirement file includes `opencv` and `pillow` that are not installed easily in many cases. so, **Good Luck**

> 설치할 프로그램중 `opencv`와 `pillow`가 있습니다. 자주 순순히 설치 안돼주는 패키지이니 행운을 빕니다.

## Run!
```
$ python main.py
```

## Control
It's start with normal mode that is checking the face captured by cam. using key is the following.

* Space Bar: change the mode between NORMAL <-> HOLD
* Enter: Reset the score
* ESC: Quit


> 실행하면 바로 촬영을 시작하는 일반 모드로 시작하고 사용키는 다음과 같습니다.
> * 스페이스바: NORMAL <-> HOLD 간의 모드 전환
> * 앤터: 점수 리셋
> * ESC: 나가기
