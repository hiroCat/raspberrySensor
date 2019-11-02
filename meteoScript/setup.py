import psycopg2
import sys

def create_table(tName):
    with psycopg2.connect('dbname=meteo') as conn:
        with conn.cursor() as cur:
            cur.execute("CREATE TABLE "+tName+" (dtime timestamp, temp decimal, press double precision, hum double precision);")
            conn.commit()


def main():
    tName = sys.argv[1] if len(sys.argv) > 1 else "defaultTable"
    print ("Creating table "+tName)
    create_table(tName)

if __name__=="__main__":
    main()