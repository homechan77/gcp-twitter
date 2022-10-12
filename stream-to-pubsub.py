# @ python3 stream_to_pubsub.py --bearer_token "<Bearer-token>" --stream_rule Google --project_id "<your-project-id>" --topic_id "<your-topic-id>"
# @ stream-to-pubsub.py

# export GOOGLE_APPLICATION_CREDENTIALS="/home/ko/workspace/gcptwitter/handy-station-364110-52ff958d11ea.json"
# python3 stream-to-pubsub.py --bearer_token "private" --stream_rule 'data' --project_id "handy-station-364110" --topic_id "tweets"

import argparse
import json
from google.cloud import pubsub_v1
from google.oauth2 import service_account
import tweepy

def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('--bearer_token', type=str, required=True)
    parser.add_argument('--stream_rule', type=str, required=True)
    parser.add_argument('--project_id', type=str, required=True)
    parser.add_argument('--topic_id', type=str, required=True)

    return parser.parse_args()


def write_to_pubsub(data, stream_rule):
    data["stream_rule"] = stream_rule
    data_formatted = json.dumps({'id': data['id'], 'created_at': data['created_at'], 'text': data['text']}).encode("utf-8")
    id = data["id"].encode("utf-8")
    # author_id = data["author_id"].encode("utf-8")

    # future = publisher.publish(
    #     topic_path, data_formatted, id=id, author_id=author_id
    # )
    future = publisher.publish(
        topic_path, data = data_formatted, id=id
    )
    print(future.result())


class Client(tweepy.StreamingClient):
    def __init__(self, bearer_token, stream_rule):
        super().__init__(bearer_token)

        self.stream_rule = stream_rule

    def on_response(self, response):
        tweet_data = response.data.data
        # user_data = response.includes['users'][0].data
        result = tweet_data
        # result["user"] = user_data

        write_to_pubsub(result, self.stream_rule)


if __name__ == "__main__":
    tweet_fields = ['id', 'text', 'created_at']
    # tweet_fields = ['id', 'text', 'author_id', 'created_at', 'lang']
    # user_fields = ['description', 'created_at', 'location']
    # expansions = ['author_id']

    args = parse_args()
    
    streaming_client = Client(args.bearer_token, args.stream_rule)
    
    # @ export GOOGLE_APPLICATION_CREDENTIALS="/home/ko/workspace/gcptwitter/handy-station-364110-52ff958d11ea.json"
    # key_path = "/home/ko/workspace/gcptwitter/handy-station-364110-52ff958d11ea.json" 
    key_path = "./handy-station-364110-52ff958d11ea.json" 

    credentials = service_account.Credentials.from_service_account_file(
        key_path,
        scopes=["https://www.googleapis.com/auth/cloud-platform"] # Client가 Resource Server로부터 인가받을 권한의 범위
        )
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(args.project_id, args.topic_id)

    # @ remove existing rules
    rules = streaming_client.get_rules().data
    if rules is not None:
        existing_rules = [rule.id for rule in streaming_client.get_rules().data]
        streaming_client.delete_rules(ids=existing_rules)

 
    # @ add new rules and run stream
    streaming_client.add_rules(tweepy.StreamRule(args.stream_rule))
    # streaming_client.filter(tweet_fields=tweet_fields, expansions=expansions, user_fields=user_fields)
    streaming_client.filter(tweet_fields=tweet_fields)
