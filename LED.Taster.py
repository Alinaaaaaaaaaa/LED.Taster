import sqlite3
import RPi.GPIO as GPIO
from datetime import datetime
import time

con = sqlite3.connect('LED.Taster.db')
cur = con.cursor()

o = open('LED.Taster.sql')
sql = o.read()
cur.executescript(sql)

GPIO.setmode(GPIO.BOARD)

class LED():
    def __init__ (self, pin):
        self.pin=pin
        self.an=False
        GPIO.setup(self.pin, GPIO.OUT)
        GPIO.output(self.pin, False)

    def LED_an (self):
        GPIO.output(self.pin, True)
        self.an=True

    def LED_aus (self):
        GPIO.output(self.pin, False)
        self.an=False

    def LED_ist_an(self):
        return self.an


class Taster():
    def __init__ (self,pin):
        self.pin=pin 
        GPIO.setup(self.pin, GPIO.IN)

    def betaetigt (self):
        return GPIO.input(self.pin)
 
 
led = LED (37)
taster = Taster (31)


try:
    while True:
        if led.LED_ist_an() == True and taster.betaetigt():
            zeit1 = time.time()
            
            while taster.betaetigt():
                zeit2 = time.time()
                   
            if zeit2 - zeit1 <= 0.5:
                led.LED_aus()
                cur.execute("INSERT INTO LED(led_an, led_zeit) VALUES(?,?)",(led.LED_ist_an(), str(datetime.now())))
                    
                
        if led.LED_ist_an() == False and taster.betaetigt():
            zeit1 = time.time()
               
            while taster.betaetigt():
                zeit2 = time.time()
                   
            if zeit2 - zeit1 <= 0.5:
                led.LED_an()
                cur.execute("INSERT INTO LED(led_an, led_zeit) VALUES(?,?)",(led.LED_ist_an(), str(datetime.now())))

except KeyboardInterrupt:
    GPIO.cleanup()
    cur.execute("SELECT * FROM LED;")
    print(cur.fetchall())
    