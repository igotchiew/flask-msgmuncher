from flask import Flask, jsonify, request
from pymongo import MongoClient
from app import app
from tasks.tasks import process_message


@app.route('/login', methods=['POST'])
def new_user():
    req = request.get_json()
    # go into form and get username
    username = req['username']
    # go into form and get password
    password = req['password']
    # connect to Mongodb
    client = MongoClient()
    # go to database named muncherdb
    db = client.muncherdb
    # go to collection named users
    users = db.users
    # search users collection to find any duplicate usernames
    if users.find_one({"username": username}):
        # if there is a duplicate return statement
        return "pick another username"
    # if username is unique, create user (one user in users collection)
    user = {
        'username': username,
        'password': password
    }
    # insert user into users collection
    account_id = users.insert_one(user).inserted_id
    return "got it, thanks!"


@app.route('/intake', methods=['POST'])
def intake():
    # go into form and get message
    req = request.get_json()
    message = req['message']
    # go into form and get account
    account = req['account']
    # create post (one post in posts collection)
    post = {
        'account': account,
        'tags': None,
        'sentiment': None,
        'message': message
    }
    # connect to Mongodb
    client = MongoClient()
    # go to database name muncherdb
    db = client.muncherdb
    # go to collection named posts
    posts = db.posts
    # insert post in to posts collection
    message_id = posts.insert_one(post).inserted_id

    # call celery task and convert message_id into a string
    process_message.delay(str(message_id))
    return "ok!"


@app.route('/index/<account>', methods=['GET'])
def index(account="admin"):
    # go to Mongodb
    client = MongoClient()
    # go to database name muncherdb
    db = client.muncherdb
    # go to collection named posts
    posts = db.posts
    # find posts from this account
    user_posts = posts.find(
        {"account": account},
        {"tags": 1, "sentiment": 1,
         "message": 1, "_id": 0})

    responses = [x for x in user_posts]

    # return json with posts from this user
    return jsonify(responses)
