from flask import Flask, request, render_template
app = Flask(__name__)
app.debug = True # Make this False if you are no longer debugging

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

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
