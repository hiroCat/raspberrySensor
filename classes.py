class reading(object):
    def __init__(self, temp, press, hum, dtime):
        self.temp = temp
        self.press = press
        self.hum = hum
        self.dtime = dtime

    def __str__(self):
        return "At t %s: temperature = %s pressure = %s humidity = %s" % (self.dtime, self.temp, self.press, self.hum)
