def temp_hum_db():
    import sqlite3
    conn=sqlite3.connect('/var/www/major_project/app.db')
    curs=conn.cursor()
    curs.execute("SELECT * FROM temperatures LIMIT 20")
    temperatures = curs.fetchall()
    curs.execute("SELECT * FROM humidities LIMIT 20")
    humidities = curs.fetchall()
    conn.close()
    
    # print("Temperature type: ", type(temperatures), "\n")
    # print("Temperature element type: ", type(temperatures[0]), "\n")
    # print("Humidity type: ", type(humidities), "\n")
    # print(temperatures)

    labels = [record[0] for record in temperatures]
    datapts = [record[2] for record in temperatures]

    print("Label type: ", type(labels), "\n")
    print(labels, "\n")
    print("Datapts type: ", type(datapts), "\n")
    print(datapts, "\n")

temp_hum_db()
