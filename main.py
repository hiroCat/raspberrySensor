import time
import bme280
import classes

def main():
    while True:
        time.sleep(3)
        r = bme280.getReadings()
        print (r)

if __name__=="__main__":
    main()