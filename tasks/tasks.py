from tasks.celeryconfig import make_celery
from flask import Flask
from textblob import TextBlob
from pymongo import MongoClient
from bson.objectid import ObjectId


app = Flask(__name__)
app.config.update(
    CELERY_BROKER_URL='amqp://'
)
celery = make_celery(app)


def connect_to_database():
    # go to Mongodb
    client = MongoClient()
    # use database named muncherdb
    db = client.muncherdb
    return db


@celery.task()
def process_message(message_id):
    # use collection named posts
    posts = connect_to_database().posts
    # converts message_id into an ObjectId called post_id
    post_id = ObjectId(message_id)
    # from posts collection, find message_id
    post = posts.find_one({"_id": post_id})
    # create TextBlob on message from post
    blob = TextBlob(post['message'])
    # create document with tags and sentiment
    updated_post = {
        'username': post['username'],
        'tags': blob.tags,
        'sentiment': blob.sentiment,
        'message': post['message']
    }
    # update post_id document
    posts.update_one(
        {'_id': post_id},
        {'$set': updated_post},
        upsert=False)

