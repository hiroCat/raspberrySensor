from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
from datetime import datetime
from dateutil import tz
import psycopg2
from decimal import *
import matplotlib.dates as mdates

from_zone = tz.gettz('UTC')
to_zone = tz.gettz('Europe/Madrid')

def getInCurrentT(t):
    utc = t.replace(tzinfo=from_zone)
    return utc.astimezone(to_zone)

def getPandas(tableName):
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
    df['temperature'] = df['temp'].astype(np.float64)
    df.drop(['date'], axis=1, inplace=True)
    df.drop(['temp'], axis=1, inplace=True)
    return df

def plotGrafic(pnd, tableName):
    plt.rcParams["figure.figsize"] = (150,50)
    fig, ax = plt.subplots()
    ax.plot('datetime','temperature', data=pnd, marker='o', color='green')
    plt.xlabel('time')
    plt.ylabel('temperature')
    minT = min(min(pnd['temperature']),min(pnd['temperature']))
    maxT = max(max(pnd['temperature']),max(pnd['temperature']))
    ax.yaxis.set_ticks(np.arange(minT, maxT+ float(1.0), float(0.1)))
    ax.xaxis.set_major_locator(mdates.MinuteLocator(interval=15)) 
    plt.draw()
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
    ax.grid(True)
    plt.savefig(tableName+'.png')
    plt.clf()

def plotTwoGrafic(pndOne, pndTwo, gName):
    plt.rcParams["figure.figsize"] = (150,50)
    fig, ax = plt.subplots()
    ax.plot('datetime','temperature', data=pndOne, marker='o', color='green', label ='baseS')
    ax.plot('datetime','temperature', data=pndTwo, marker='o', color='blue', label ='modifiedS')
    ax.legend(loc='upper left')
    plt.xlabel('time')
    plt.ylabel('temperature')
    minT = min(min(pndOne['temperature']),min(pndTwo['temperature']))
    maxT = max(max(pndOne['temperature']),max(pndTwo['temperature']))
    ax.yaxis.set_ticks(np.arange(minT, maxT+ float(1.0), float(0.1)))
    ax.xaxis.set_major_locator(mdates.MinuteLocator(interval=15)) 
    plt.draw()
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
    ax.grid(True)
    plt.savefig(gName+'.png')
    plt.clf()

def saveGrafic(tableName):
    pd = getPandas(tableName)
    plotGrafic(pd, tableName)        


# for t in ['difference', 'sensorbase', 'sensormodified']:
#     saveGrafic(t)

sB = getPandas('sensorbase')
sM = getPandas('sensormodified')
plotTwoGrafic(sB, sM, 'other')