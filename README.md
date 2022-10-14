# GCP 기반 트위터 스트리밍 데이터 엔지니어링

[https://github.com/homechan77/gcp-twitter.git](https://github.com/homechan77/gcp-twitter.git)

<aside>
💡 *<Tacademy_데이터 엔지니어링 기초 강의>를 통한 실습 진행*

> [*https://tacademy.skplanet.com/live/player/onlineLectureDetail.action?seq=187*](https://tacademy.skplanet.com/live/player/onlineLectureDetail.action?seq=187)
> 

***** Twitter API v2로 업데이트된 코드들로 진행 *****

</aside>

![Screenshot from 2022-09-28 15-52-46.png](GCP%20%E1%84%80%E1%85%B5%E1%84%87%E1%85%A1%E1%86%AB%20%E1%84%90%E1%85%B3%E1%84%8B%E1%85%B1%E1%84%90%E1%85%A5%20%E1%84%89%E1%85%B3%E1%84%90%E1%85%B3%E1%84%85%E1%85%B5%E1%84%86%E1%85%B5%E1%86%BC%20%E1%84%83%E1%85%A6%E1%84%8B%E1%85%B5%E1%84%90%E1%85%A5%20%E1%84%8B%E1%85%A6%E1%86%AB%E1%84%8C%E1%85%B5%E1%84%82%E1%85%B5%E1%84%8B%E1%85%A5%E1%84%85%E1%85%B5%E1%86%BC%205fb083cae81a4c8d8fab5f200f93c940/Screenshot_from_2022-09-28_15-52-46.png)

- **GCP(Google Cloud Platform)**
    - 서비스 개요
        
        ![img.png](GCP%20%E1%84%80%E1%85%B5%E1%84%87%E1%85%A1%E1%86%AB%20%E1%84%90%E1%85%B3%E1%84%8B%E1%85%B1%E1%84%90%E1%85%A5%20%E1%84%89%E1%85%B3%E1%84%90%E1%85%B3%E1%84%85%E1%85%B5%E1%84%86%E1%85%B5%E1%86%BC%20%E1%84%83%E1%85%A6%E1%84%8B%E1%85%B5%E1%84%90%E1%85%A5%20%E1%84%8B%E1%85%A6%E1%86%AB%E1%84%8C%E1%85%B5%E1%84%82%E1%85%B5%E1%84%8B%E1%85%A5%E1%84%85%E1%85%B5%E1%86%BC%205fb083cae81a4c8d8fab5f200f93c940/img.png)
        
        ![img1.daumcdn.png](GCP%20%E1%84%80%E1%85%B5%E1%84%87%E1%85%A1%E1%86%AB%20%E1%84%90%E1%85%B3%E1%84%8B%E1%85%B1%E1%84%90%E1%85%A5%20%E1%84%89%E1%85%B3%E1%84%90%E1%85%B3%E1%84%85%E1%85%B5%E1%84%86%E1%85%B5%E1%86%BC%20%E1%84%83%E1%85%A6%E1%84%8B%E1%85%B5%E1%84%90%E1%85%A5%20%E1%84%8B%E1%85%A6%E1%86%AB%E1%84%8C%E1%85%B5%E1%84%82%E1%85%B5%E1%84%8B%E1%85%A5%E1%84%85%E1%85%B5%E1%86%BC%205fb083cae81a4c8d8fab5f200f93c940/img1.daumcdn.png)
        
    - *Google Cloud Functions은 무엇인가?*
        - 서버리스 아키텍처를 구현하기 위한 구글 클라우드 서비스
            - *서버리스 아키텍처란?*
                
                [클라우드 컴퓨팅](https://www.notion.so/2dbba28b5feb4c1484b4dca6c1420dc4)
                
        - aws의 Lambda와 같은 기능을 수행
        - 이벤트가 발생하면, 이벤트에 따라서 코드를 수행해주는 형태

1. **Twitter API로 부터 데이터를 받아와 출력**
    
    <aside>
    💡 현재 Stream 클래스를 사용하는 Twitter API v1.1은 deprecated 된 것으로 보이므로(코드 실행시 아무런 결과값도 출력되지 않는 문제), API v2.2(StreamClient)로의 코드 업데이트가 필요하다
    
    ```python
    import tweepy
    
    class TwitterStream(tweepy.StreamingClient):
        def on_data(self, raw_data):
            print(raw_data)
    
    client = TwitterStream('***Bearer Token***')
    
    client.add_rules(tweepy.StreamRule(value='data'))
    
    client.filter()
    ```
    
    > *참고) _KHK-tweepy 로 트위터 API V2 스트리밍 하기 [https://devkhk.tistory.com/37](https://devkhk.tistory.com/37)*
    > 
    </aside>
    
2. **Tweet Stream to GCP PUB/SUB**
    - 앞서 tweet stream을 단순히 출력했던 것에서 더 나아가 json 형태로 변환하여 pub/sub에 publish한다.
    
    > *참고) DS stream-Streaming Twitter data with Google Cloud Pub/Sub and Apache Beam [https://dsstream.com/streaming-twitter-data-with-google-cloud-pub-sub-and-apache-beam/](https://dsstream.com/streaming-twitter-data-with-google-cloud-pub-sub-and-apache-beam/)*
    > 
    - 코드 실행 전 준비사항
        - gcp 서비스 계정(pub/sub editor 권한)을 생성하여 해당 계정의 비공개 키 파일(.json)을 다운받고 프로젝트 파일로 이동시킨다.
        - 키 파일을 코드 실행전에 환경변수에 지정시켜 주어야 한다.
        `export GOOGLE_APPLICATION_CREDENTIALS="key_path”`
    - 코드
        - StreamingClient 클래스를 상속받는 Client를 클래스를 생성한다. 여기서 주의할 점은 앞선 코드에서는 on_data() 메소드를 오버라이딩 하였으나 지금은 on_response() 메소드를 오버라이딩한다.두 메소드 모두 tweet stream들을 인자로 받아 출력할 수 있게 한다.(`reponse.data.data`로 출력된 결과물이 더 정돈된 느낌? 그리고 dict 자료 형태로 키 값을 가지고 컨트롤 하기도 편하였다.)
        *참고) [https://docs.tweepy.org/en/stable/streamingclient.html](https://docs.tweepy.org/en/stable/streamingclient.html)*
        - [`response.data`](http://response.data)는 해당 tweet의 text를 출력하고 `response.data.data`는 그 text와 함께 우리가 지정한 tweet_field를 포함한 값들을 보여준다.
        - [`response.data.data`](http://response.data.data) 의 객체를 write_to_pubsub() 메소드에 보내 json으로 변형시키고 pub/sub으로 write한다.
        - tweepy v2의 변화점으로 필터 규칙을 설정해 주어야 하는데, 이 규칙들은 엔드포인트에 “적체되어서” 남아 있게된다. 따라서 새로운 규칙들을 필터링 하기 위해서는 기존 규칙의 id를 파악(`get_rules().data`)하여 모두 지우어야 한다.(혹은 필요하지 않은 규칙들을)
3. **Cloud Functions에서 Pub/Sub 트리거에 의한 Pub/Sub 메시지를 응답하여 함수를 호출, BIgQuery로 이동**
    - BigQuery 내 dataset(’tweet_data’)과 table(’tweets’) 생성
    - table(’tweet’) 스키마 필드와 유형을 다음과 같이 설정
        - id(integer), created_at(datetime), text(string)
        - Tweet stream이 PUB/SUB으로 갈 때 각 필드 유형에 맞게끔 형변환 되어져서 보내지도록 코드를 수정한다.
            
            > 참고) Tweet Stream Datetime values info [https://developer.twitter.com/en/docs/twitter-ads-api/timezones](https://developer.twitter.com/en/docs/twitter-ads-api/timezones)
            > 
            
            ![Screenshot from 2022-10-07 21-17-45.png](GCP%20%E1%84%80%E1%85%B5%E1%84%87%E1%85%A1%E1%86%AB%20%E1%84%90%E1%85%B3%E1%84%8B%E1%85%B1%E1%84%90%E1%85%A5%20%E1%84%89%E1%85%B3%E1%84%90%E1%85%B3%E1%84%85%E1%85%B5%E1%84%86%E1%85%B5%E1%86%BC%20%E1%84%83%E1%85%A6%E1%84%8B%E1%85%B5%E1%84%90%E1%85%A5%20%E1%84%8B%E1%85%A6%E1%86%AB%E1%84%8C%E1%85%B5%E1%84%82%E1%85%B5%E1%84%8B%E1%85%A5%E1%84%85%E1%85%B5%E1%86%BC%205fb083cae81a4c8d8fab5f200f93c940/Screenshot_from_2022-10-07_21-17-45.png)
            
            ![Screenshot from 2022-10-07 21-19-02.png](GCP%20%E1%84%80%E1%85%B5%E1%84%87%E1%85%A1%E1%86%AB%20%E1%84%90%E1%85%B3%E1%84%8B%E1%85%B1%E1%84%90%E1%85%A5%20%E1%84%89%E1%85%B3%E1%84%90%E1%85%B3%E1%84%85%E1%85%B5%E1%84%86%E1%85%B5%E1%86%BC%20%E1%84%83%E1%85%A6%E1%84%8B%E1%85%B5%E1%84%90%E1%85%A5%20%E1%84%8B%E1%85%A6%E1%86%AB%E1%84%8C%E1%85%B5%E1%84%82%E1%85%B5%E1%84%8B%E1%85%A5%E1%84%85%E1%85%B5%E1%86%BC%205fb083cae81a4c8d8fab5f200f93c940/Screenshot_from_2022-10-07_21-19-02.png)
            
4. **DataStudio에서 BigQuery 테이블을 불러와 시각화**
    
    <aside>
    💡 * ***시각화 결과물 보기***
    [***https://datastudio.google.com/reporting/902d77fe-9fe6-434c-90fd-9ec32eafef59***](https://datastudio.google.com/reporting/902d77fe-9fe6-434c-90fd-9ec32eafef59)
    
    </aside>
    
5. **Kubernetes를 활용한 자동화**
    
    ```bash
    # Dockerfile build
    $ **docker build -t tweet .**
    
    # gcloud auth configure-docker adds the Docker credHelper entry to Docker's configuration file, or creates the file if it doesn't exist. This will register gcloud as the credential helper for all Google-supported Docker registries.
    $ **gcloud auth configure-docker**
    
    # Create a tag TARGET_IMAGE that refers to SOURCE_IMAGE
    $ **docker tag tweet gcr.io/handy-station-364110/tweet**
    
    # docker push to gcloud Container Registry
    $ **docker push gcr.io/handy-station-364110/tweet**
    ```