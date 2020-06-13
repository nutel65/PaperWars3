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


from server import utility
from server import threadwork
from flask import Flask, render_template
from flask_socketio import SocketIO

# cd server
# $env:FLASK_APP = "server/server.py"
# $env:FLASK_ENV = "development"
# $env:FLASK_SECRET_KEY = "test_key"
# flask run --host=0.0.0.0 --port=80


app = Flask(__name__)
socketio = SocketIO(app, logger=True)

dbmanager = threadwork.DBManager()
dbmanager.start()

from server import ws

@app.route('/home')
@app.route('/')
def index():
    return '''
        <html><body>
        <h2>PaperWars</h2>
        Gra jest wciąż rozwijana.
        Postępy można śledzić w <a href="https://github.com/nutel65/PaperWars3">
        repozytorium na GitHubie</a><br>
        
        <h3>Na czym ma polegać gra:</h3>
        Gra turowa, planszowa, przypominająca szachy, ale bardziej rozbudowana:<br>
        - rozbudowane mechaniki poruszania i atakowania figur<br>
        - rekrutacja figur za walutę w grze<br>
        - umiejętności specjalne i pasywne unikalne dla każdej figury<br>
        - biomy modyfikujące zdolności figur i dające bonusy<br>
        - ulepszenia figur za walutę w grze<br>
        <a href="https://docs.google.com/document/d/1HABBGNc6HAreJJlkUUxIOtXmcVgq0Qq_RluzGqmxy9s/edit?usp=sharing">Więcej szczegółów</a><br>
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
