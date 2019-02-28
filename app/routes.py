from flask import Flask, jsonify, request
from app import app
from tasks.tasks import process_message, connect_to_database
from werkzeug.security import generate_password_hash, check_password_hash
import random
import string


def password_generator(size=12,
                       chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


@app.route('/login', methods=['POST'])
def new_user():
    req = request.get_json()
    # go into form and get username
    username = req['username']
    # go to collection named users
    users = connect_to_database().users
    # search users collection to find any duplicate usernames
    if users.find_one({"username": username}):
        # if there is a duplicate return statement
        return "pick another username"
    # create password for user
    password_out = password_generator()
    # hash the created password
    password = generate_password_hash(password_out)
    # if username is unique, create user/document
    # create one user in users collection
    # also store hashed password_out
    user = {
        'username': username,
        'password': password
    }
    # insert user into users collection
    users.insert_one(user)

    # send the password_out to the user
    return "your password is: {}".format(password_out)


@app.route('/intake/<username>', methods=['GET', 'POST'])
def intake(username):
    # go to collections named users
    users = connect_to_database().users
    # find user with this username from the users collection
    user_account = users.find_one(
        {"username": username}
    )
    # go into form and get message
    req = request.get_json()
    message = req['message']
    password = req['password']

    if not check_password_hash(user_account['password'], password):
        return "bad password"
    # create post/document (one post in posts collection)
    post = {
        'username': username,
        'tags': None,
        'sentiment': None,
        'message': message
    }
    # go to collection named posts
    posts = connect_to_database().posts
    # insert post in to posts collection
    message_id = posts.insert_one(post).inserted_id

    # call celery task and convert message_id into a string
    process_message.delay(str(message_id))
    return "ok!"


@app.route('/index/<username>', methods=['GET'])
def index(username):
    # go to collection named posts
    posts = connect_to_database().posts
    # find posts from this account
    user_posts = posts.find(
        {"username": username},
        {"tags": 1, "sentiment": 1,
         "message": 1, "_id": 0})

    responses = [x for x in user_posts]

    # return json with posts from this user
    return jsonify(responses)
