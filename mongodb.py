import datetime
from pymongo import MongoClient
import os

cosmosdb_url = os.environ['COSMOSDB_URL']
cosmosdb_key = os.environ['COSMOSDB_KEY']
# cosmosdb_database_name = os.environ['COSMOSDB_DATABASE_NAME']
# cosmosdb_collection_name = os.environ['COSMOSDB_COLLECTION_NAME']

cosmosdb_database_name = 'comp7940group'
cosmosdb_collection_name = 'group_data'

cosmosdb_full = f'mongodb+srv://satorip:{cosmosdb_key}@{cosmosdb_url}/?tls=true&authMechanism=SCRAM-SHA-256&retrywrites=true'
client = MongoClient(cosmosdb_full)
print(cosmosdb_full)
db = client[cosmosdb_database_name]
collection = db[cosmosdb_collection_name]


def storage(update, context, bot_reply):
    user_id = update.message.from_user.id
    text = update.message.text
    timestamp = update.message.date
    document = {
        'user_id': user_id,
        'message': {
            'text': text,
            'timestamp': timestamp
        },
        'bot_reply': {
            'text': bot_reply,
            'timestamp': datetime.datetime.now()
        }
    }

    # MongoDB
    collection.insert_one(document)


if __name__ == '__main__':
    post = {"author": "YHCui", "text": "Hello, World!"}
    post_id = collection.insert_one(post).inserted_id
    print(f'Post ID: {post_id}')

    for post in collection.find():
        print(post)
