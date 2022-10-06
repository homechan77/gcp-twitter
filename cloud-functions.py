import base64
import json
import datetime as dt
from google.cloud import bigquery

def tweets_to_bq(tweet):
    client = bigquery.Client()

    dataset_ref = client.dataset("tweet_data")
    
    table_ref = dataset_ref.table("tweets")
    
    table = client.get_table(table_ref)

    tweet_dict = json.loads(tweet)
    
    createdat = tweet_dict['created_at']
    # '%Y-%m-%d %H:%M:%S'
    Y, m, d, H, M, S = int(createdat[:4]), int(createdat[5:7]), int(createdat[8:10]), int(createdat[11:13]), int(createdat[14:16]), int(createdat[17:19])
    todatetime = dt.datetime(Y, m, d, H, M, S)

    rows_to_insert = [
        (int(tweet_dict['id']), todatetime, tweet_dict['text'])
        ]

    # error = client.insert_rows(table, rows_to_insert)

    client.insert_rows(table, rows_to_insert)

    # print(error)

def hello_pubsub(event, context):
    """Triggered from a message on a Cloud Pub/Sub topic.
    Args:
        event (dict): Event payload.
        context (google.cloud.functions.Context): Metadata for the event.
    """

    if 'data' in event:
        name = base64.b64decode(event['data']).decode('utf-8')
    else:
        name = 'World'
    
    print('Hello {}!'.format(name))

    tweets_to_bq(name)
