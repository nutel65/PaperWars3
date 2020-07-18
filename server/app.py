#!/usr/bin/env python3
import logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(name)-16s %(levelname)-8s %(message)s',
    datefmt='%m-%d %H:%M',
    # filename=redirect,
    filemode='w+',
)
logger = logging.getLogger(__name__)


from flask import Flask, render_template
from flask_socketio import SocketIO

from server import utility
from server import threadwork

# cd server
# $env:FLASK_APP = "server/app.py"
# $env:FLASK_ENV = "development"
# $env:FLASK_SECRET_KEY = "test_key"
# flask run --host=0.0.0.0 --port=5000


app = Flask(__name__)
socketio = SocketIO(app, logger=True)

dbmanager = threadwork.DBManager()
dbmanager.start()

rooms = []

from server import ws

@app.route('/home')
@app.route('/')
def index():
    return '''
        <html><body>
        <h2>PaperWars</h2>
        Gra jest wciąż rozwijana, aktualnie w fazie pre-alpha.<br>
        Postępy można śledzić w <a href="https://github.com/nutel65/PaperWars3">
        repozytorium na GitHubie</a><br>
  
        <a href="https://docs.google.com/document/d/1HABBGNc6HAreJJlkUUxIOtXmcVgq0Qq_RluzGqmxy9s/edit?usp=sharing">Szczegóły dot. zasad i przebiegu gry</a><br>
        </body></html>
        '''

@app.route("/debug")
def debug_page():
    raise

@app.route("/insert_test/<a>/<b>/<c>")
def test_insert_user(a, b, c):
    return str(services["dbmanager"].insert_user(a, b, c))

@app.route("/select/<username>")
def test_select_user_by_username(username):
    return str(services["dbmanager"].get_user_by_username(username))
