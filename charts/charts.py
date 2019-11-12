# library & dataset
from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
import psycopg2
from datetime import datetime
from dateutil import tz

from_zone = tz.gettz('UTC')
to_zone = tz.gettz('Europe/Madrid')

def getInCurrentT(t):
    utc = t.replace(tzinfo=from_zone)
    return utc.astimezone(to_zone)

def saveGrafic(tableName):
    d = []
    v = []
    with psycopg2.connect('dbname=meteo') as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT * FROM '+ tableName + ';')
            a = cur.fetchall()
            for i in a:
                t = getInCurrentT(i[0])
                d.append(str(t))
                v.append(i[1])
    data = {'date': d, 'temp': v}
    df = pd.DataFrame(data, columns=['date', 'temp'])
    df['datetime'] = pd.to_datetime(df['date'])
    df = df.set_index('datetime')
    df.drop(['date'], axis=1, inplace=True)
    plt.plot( 'temp' , data=df, marker='o', color='green', label ='baseS')
    plt.rcParams["figure.figsize"] = (100,50)
    plt.legend(loc='upper left')
    plt.xlabel('Time')
    plt.ylabel('temp')
    plt.grid(True)
    plt.savefig(tableName+'.png')
    

for t in ['difference', 'sensorbase', 'sensormodified']:
    saveGrafic(t)

