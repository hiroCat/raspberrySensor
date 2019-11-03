# raspberrySensor
a python program to use a existing module to log temperature into a db 

# content
It has different modules:
- bme280 => slightly modified from https://bitbucket.org/MattHawkinsUK/rpispy-misc code (https://www.raspberrypi-spy.co.uk/2016/07/using-bme280-i2c-temperature-pressure-sensor-in-python/)
- main => soon to have all the logic , right now only a sleep and calling the bme280 module
- classes => different data structures , right now only the main one 

# additional config
For the db I choose postgresql so the config is as :
- postgres=# create database meteo;
The setup.py script can also be used to create the main table.

# run it 
To run you need to specify the table name.(make sure you have the dependencies installed pip install...)
If you want to run it as a service you need to copy the service to /lib/systemd/system/and also run :
- sudo chmod 644 /lib/systemd/system/meteo.service 
- sudo systemctl daemon-reload  
- sudo systemctl enable meteo.service 