import time
import bme280
import classes
# from dotenv import load_dotenv
# import os
import psycopg2
import sys

def create_table(tName):
    with psycopg2.connect('dbname=meteo') as conn:
        with conn.cursor() as cur:
            cur.execute("CREATE TABLE "+tName+" (dtime timestamp, temp decimal, press double precision, hum double precision);")
            conn.commit()

def add_log(tName, reading):
    with psycopg2.connect('dbname=meteo') as conn:
        with conn.cursor() as cur:
            query = """
            INSERT INTO
                """+tName+"""
            VALUES
                (%s, %s, %s, %s)
            """
            values = (reading.dtime, reading.temp, reading.press, reading.hum)
            cur.execute(query, values)
            conn.commit()

def main():
    tName = sys.argv[1] if len(sys.argv) > 1 else "defaultTable"
    tName2 = sys.argv[2] if len(sys.argv) > 1 else "defaultTable2"
    print ("Using table "+tName)
    while True:
        r = bme280.getReadings(0x76)
        add_log(tName,r)
        r2 = bme280.getReadings(0x77)
        add_log(tName2,r2)
        time.sleep(300)

if __name__=="__main__":
    # load_dotenv()
    main()