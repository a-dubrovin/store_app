Store app.

Docker run

1. git clone https://github.com/a-dubrovin/store_app.git
2. cd ./store_app/
3. cp ./.env.template ./.env
4. Fill .env, example:

APP_SETTINGS=config.DevelopmentConfig

DATABASE_URL=sqlite:///../database.db

SECRET_KEY=s_key

5. docker-compose up

Installation

1. git clone https://github.com/a-dubrovin/store_app.git
2. virtualenv ./venv
3. source ./venv/bin/activate
4. cd ./store_app/
5. cp ./.env.template ./.env
6. Fill .env, example:

APP_SETTINGS=config.DevelopmentConfig

DATABASE_URL=sqlite:///../database.db

SECRET_KEY=s_key

7. pip install -r ./requirements.txt

Run

export PYTHONPATH=./ && export FLASK_APP=backend/app.py && flask run

Tests

python ./backend/app_tests.py

Docs

http://localhost:5000/docs

