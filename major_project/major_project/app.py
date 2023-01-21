from flask import Flask, request, render_template
app = Flask(__name__)
app.debug = True # Make this False if you are no longer debugging

moisture_level = ""
water_pump = ""

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/temp_hum")
def temp_hum():
	import sys
	import Adafruit_DHT
	humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, 17)
	if humidity is not None and temperature is not None:
		return render_template("temp_hum.html",temp=temperature,hum=humidity)
	else:
		return render_template("no_sensor.html")

@app.route("/temp_hum_db")
def temp_hum_db():
	import sqlite3
	conn=sqlite3.connect('/var/www/major_project/app.db')
	curs=conn.cursor()
	curs.execute("SELECT * FROM temperatures")
	temperatures = curs.fetchall()
	curs.execute("SELECT * FROM humidities")
	humidities = curs.fetchall()
	conn.close()
	return render_template("temp_hum_db.html",temp=temperatures,hum=humidities)

@app.route("/home")
def temp_hum_ui_home():
    import sys
    import Adafruit_DHT
    humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, 17)
    if humidity is not None and temperature is not None:
        return render_template("dashboard.html",temp=temperature,hum=humidity,moisture=moisture_level, change=change_of_var)
    else:
        return render_template("no_sensor.html")

@app.route("/home/dashboard")
def temp_hum_ui_home_dashboard():
    import sys
    import Adafruit_DHT
    humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, 17)
    if humidity is not None and temperature is not None:
        return render_template("dashboard.html",temp=temperature,hum=humidity,moisture=moisture_level,pump=water_pump)
    else:
        return render_template("no_sensor.html")

@app.route("/home/crop_recommendation")
def crop_recommendation():
    return render_template("crop_recommendation.html")

@app.route("/home/tables")
def tables():
    import sqlite3
    conn=sqlite3.connect('/var/www/major_project/app.db')
    curs=conn.cursor()
    curs.execute("SELECT * FROM temperatures ORDER BY rDatetime DESC LIMIT 5")
    temperatures = curs.fetchall()
    curs.execute("SELECT * FROM humidities ORDER BY rDatetime DESC LIMIT 5")
    humidities = curs.fetchall()
    conn.close()
    return render_template("tables.html",temp=temperatures,hum=humidities)

import RPi.GPIO as GPIO

#GPIO SETUP
channel = 21
GPIO.setmode(GPIO.BCM)
GPIO.setup(channel, GPIO.IN)
GPIO.setup(26, GPIO.OUT)

def callback(channel):
        global moisture_level, water_pump
        if GPIO.input(channel):
                # print("no Water Detected!")
                moisture_level = "Not Adequate"
                GPIO.output(26, GPIO.HIGH)
                water_pump = "ON"
        else:
                # print("Water Detected!")
                moisture_level = "Adequate"
                GPIO.output(26, GPIO.LOW)
                water_pump = "OFF"

GPIO.add_event_detect(channel, GPIO.BOTH, bouncetime=300)  # let us know when the pin goes HIGH or LOW
GPIO.add_event_callback(channel, callback)  # assign function to GPIO PIN, Run function on change

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
