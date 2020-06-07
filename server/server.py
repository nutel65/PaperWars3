#!/usr/bin/env python3

from server import config
import random
from server import servercli
from server import threadwork
from server import utility
import flask
from collections import deque
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from server import packetcode
from server import statuscode
import time

# cd server
# $env:FLASK_APP = "server.py" / set FLASK_APP=server.py
# $env:FLASK_ENV = "development" / set FLASK_ENV=development
# $env:FLASK_SECRET_KEY = ""
# flask run --host=0.0.0.0 --port=80

app = Flask(__name__)
redirect = None
# if not app.debug:
    # redirect = "./server/logs/lastrun.log"
logger = utility.setup_logger(__name__, redirect=redirect)
socketio = SocketIO(app, logger=True)
services = {}
# # services["packrec"] = threadwork.PacketReceiver(selector)
# # services["packrec"].start()
# services["dbmanager"] = threadwork.DBManager(
#     user="kndylszorbdwcq",
#     password="f4771035032107cf4be02f33f89db831876600a91b9f297e9610d348ad750854",
#     database="ddhdsngovg5a6n",
#     host="ec2-54-247-79-178.eu-west-1.compute.amazonaws.com"
# )
# services["dbmanager"].start()
# socketio.run(app, host='localhost', port=80, debug=True)

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

# @app.route("/getPlotCSV")
# def getPlotCSV():
#     # with open("outputs/Adjacency.csv") as fp:
#     #     csv = fp.read()
#     csv = '1,2,3\n4,5,6\n'
#     return flask.Response(
#         csv,
#         mimetype="text/csv",
#         headers={"Content-disposition":
#                  "attachment; filename=myplot.csv"})

@socketio.on('connect')
def on_connect():
    app.logger.info("Client connected")

@socketio.on('disconnect')
def on_disconnect():
    app.logger.info('Client disconnected')

@socketio.on(packetcode.LOGIN_REQUEST, namespace='server')
def login_response(message):
    emit(packetcode.LOGIN_RESPONSE, {'status': statuscode.LOGIN_OK})


