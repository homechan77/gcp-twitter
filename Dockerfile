# 베이스 이미지
FROM python:3.9-slim

# 작업 디렉토리 변경
WORKDIR /app

# 현재 프로젝트 디렉토리를 컨테이너 '/app'으로 복사 이동
ADD . /app

# 명령어 실행
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# 환경변수 설정
ENV GOOGLE_APPLICATION_CREDENTIALS='/app/'

# 컨테이너 실행시 명령어 실행
# CMD ["python", "stream-to-pubsub-private"]
CMD python3 stream-to-pubsub-private.py --bearer_token " " --stream_rule 'data' --project_id "handy-station-364110" --topic_id "tweets"
