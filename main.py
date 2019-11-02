import time
import bme280
import classes
# from dotenv import load_dotenv
# import os
import psycopg2

def add_log(reading):
    with psycopg2.connect('dbname=meteo') as conn:
        with conn.cursor() as cur:
            query = """
            INSERT INTO
                logData
            VALUES
                (%s, %s, %s, %s)
            """
            values = (reading.dtime, reading.temp, reading.press, reading.hum)
            cur.execute(query, values)
            conn.commit()

def main():
    while True:
        r = bme280.getReadings()
        add_log(r)
        time.sleep(300)

if __name__=="__main__":
    # load_dotenv()
    main()