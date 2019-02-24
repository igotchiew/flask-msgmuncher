# flask-msgmuncher
### Overview

This simple python task queue takes in messages and performs light natural language processing.

### Components Used
1. Flask
2. Celery
3. Rabbitmq
4. Mongodb
5. TextBlob

### Prerequisites
1. Rabbitmq
2. Mongodb

### Install
1. git clone <add repo link>
2. virtualenv -p python3 venv
3. venv/bin/pip3 install -r requirements.text <fix spelling>

### Run Local
1. start Celery worker <insert command>
2. start rabbitmq <insert command>
3. start Mongodb <insert command>
4. export FLASK_APP=msgmuncher.py
5. flask run
