from flask import Flask, render_template, session, request
from flask_session import Session
import jinja2
import psycopg2
from flask_socketio import SocketIO, emit
import json

app = Flask(__name__)
SESSION_TYPE = 'filesystem'
app.secret_key = 'bqkMquUfb4FZ0wcQXsGlalQd49o'
app.config.from_object(__name__)
Session(app)
socketio = SocketIO(app, async_mode=None, logger=True, engineio_logger=True)

@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template('index.html')

@socketio.on('connect', namespace='/test')
def getConnect():
    print ("penislol")

@socketio.on('charts', namespace='/test')
def getData(message):
    print ("dada")
    print (message)
    json_string = '''
        {
              "labels": ["January", "February", "March", "April", "May", "June", "July","du"],
              "datasets": [{
                  "label": "first sensor",
                  "backgroundColor": "rgb(255, 99, 132)",
                  "borderColor": "rgb(255, 99, 132)",
                  "data": [0, 10, 5, 2, 20, 30, 45,56,66],
                  "fill": false
              },
              {
                  "label": "second sensor",
                  "backgroundColor": "rgb(30, 211, 24)",
                  "borderColor": "rgb(30, 211, 24)",
                  "data": [10, 1, 50, 20, 2, 3, 50,67,54],
                  "fill": false
              }]
          }
          '''.replace(" ", "")
    socketio.emit('newData', {'data': json_string}, namespace='/test')


if __name__ == "__main__":
    app.config['SESSION_TYPE'] = 'filesystem'
    sess = Session()
    sess.init_app(app)
    socketio.run(app)