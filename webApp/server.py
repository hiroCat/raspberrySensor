from flask import Flask, render_template, session, request
from flask_session import Session
import jinja2
import psycopg2
from flask_socketio import SocketIO, emit
import json
from datetime import datetime , timedelta
from dateutil import tz
import psycopg2
import json
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

app = Flask(__name__)
SESSION_TYPE = config['other']['SESSION_TYPE'] 
app.secret_key = config['other']['secret_key'] 
app.config.from_object(__name__)
Session(app)
socketio = SocketIO(app, async_mode=None, logger=True, engineio_logger=True)
from_zone = tz.gettz(config['other']['from_zone'])
to_zone = tz.gettz(config['other']['to_zone'])

@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template('index.html')

@socketio.on('connect', namespace='/test')
def getConnect():
    print ("penislol")

@socketio.on('charts', namespace='/test')
def getData(message):
    # maybe switch to 5min / 10 min / 15min / 20 min / 30 min / 60 min 
    dateFrom = message[0]
    if not dateFrom:
        dateFrom = (datetime.now() - timedelta(1)).strftime("%d/%m/%Y")
    dateTo = message[1]
    if not dateTo:
        dateTo = datetime.now().strftime("%d/%m/%Y")
    print ("[TRACE] => selecting from date("+dateFrom+") to ("+dateTo+") with a "+message[2]+" min frequency")
    labelI,valuesI = getDataFromDb(dateFrom, dateTo, "inside")
    _,valuesO = getDataFromDb(dateFrom, dateTo, "outside")

    print ("[TRACE] => labels => ("+ str(labelI)+")")
    print ("[TRACE] => values => ("+ str(valuesI)+")")

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
          '''
    y = json.loads(json_string)  
    # junky as ... 
    y["labels"] = labelI  
    y["datasets"][0]["data"] = valuesI
    y["datasets"][1]["data"] = valuesO
    
    s = json.dumps(y)
    socketio.emit('newData', {'data': s}, namespace='/test')

def getInCurrentT(t):
    utc = t.replace(tzinfo=from_zone)
    return utc.astimezone(to_zone)

def getDataFromDb(dateFrom, dateTo, tableName):
    d = []
    v = []  
    with psycopg2.connect('dbname='+config['Postgresql']['dbname']+' host='+config['Postgresql']['host']+ ' user='+config['Postgresql']['user']+' password='+config['Postgresql']['password']) as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT * FROM '+ tableName + ' WHERE dtime between \''+dateFrom+'\' and \''+dateTo+'\';')
            a = cur.fetchall()
            for i in a:
                t = getInCurrentT(i[0]).strftime("%Y-%m-%d %H:%M")
                d.append(str(t))
                v.append(str(i[1]))
    return d, v


if __name__ == "__main__":
    app.config['SESSION_TYPE'] = config['other']['SESSION_TYPE'] 
    sess = Session()
    sess.init_app(app)
    socketio.run(app)