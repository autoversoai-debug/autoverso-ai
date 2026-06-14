import sqlite3

conn = sqlite3.connect("autoverso.db")
cur = conn.cursor()

try:
    cur.execute("ALTER TABLE cars ADD COLUMN data_quality TEXT DEFAULT 'generated'")
except:
    pass

cur.execute("""
UPDATE cars
SET data_quality='legacy_generated'
WHERE lower(brand)='audi'
""")

audi = [
    ("Audi A1 1.4 TFSI 8X","Audi","A1","1.4 TFSI 8X","2010-2018","Benzina","Utilitaria premium",122,200,5.3,8.9,203,8000,17000,7,7,7),
    ("Audi A1 30 TFSI GB","Audi","A1","30 TFSI GB","2018-oggi","Benzina","Utilitaria premium",116,200,5.1,9.4,203,16000,28000,8,8,7),

    ("Audi A3 1.6 TDI 8V","Audi","A3","1.6 TDI 8V","2012-2020","Diesel","Compatta premium",110,250,3.9,10.5,200,10000,22000,8,8,6),
    ("Audi A3 2.0 TDI 8V","Audi","A3","2.0 TDI 8V","2012-2020","Diesel","Compatta premium",150,340,4.1,8.4,218,13000,26000,8,8,7),
    ("Audi A3 35 TFSI 8Y","Audi","A3","35 TFSI 8Y","2020-oggi","Benzina","Compatta premium",150,250,5.5,8.4,224,23000,39000,8,8,7),

    ("Audi S3 8V","Audi","S3","8V","2013-2020","Benzina","Compatta sportiva",300,380,6.9,4.8,250,25000,42000,7,7,9),
    ("Audi S3 8Y","Audi","S3","8Y","2020-oggi","Benzina","Compatta sportiva",310,400,7.4,4.8,250,42000,65000,8,8,9),
    ("Audi RS3 8V","Audi","RS3","8V","2015-2020","Benzina","Compatta sportiva",400,480,8.3,4.1,250,42000,70000,7,7,10),
    ("Audi RS3 8Y","Audi","RS3","8Y","2021-oggi","Benzina","Compatta sportiva",400,500,8.8,3.8,250,60000,85000,8,8,10),

    ("Audi A4 2.0 TDI B8","Audi","A4","2.0 TDI B8","2008-2015","Diesel","Berlina premium",143,320,4.8,9.4,215,7000,17000,8,8,6),
    ("Audi A4 2.0 TDI B9","Audi","A4","2.0 TDI B9","2015-2023","Diesel","Berlina premium",150,320,4.0,8.9,219,16000,33000,8,8,7),
    ("Audi A4 40 TDI B9","Audi","A4","40 TDI B9","2015-2023","Diesel","Berlina premium",190,400,4.4,7.7,237,22000,42000,8,8,7),

    ("Audi A5 2.0 TDI F5","Audi","A5","2.0 TDI F5","2016-oggi","Diesel","Coupe premium",190,400,4.4,7.7,235,24000,46000,8,8,7),
    ("Audi A6 3.0 TDI C7","Audi","A6","3.0 TDI C7","2011-2018","Diesel","Berlina premium",272,580,5.1,5.5,250,18000,37000,8,9,8),

    ("Audi TT 2.0 TFSI 8J","Audi","TT","2.0 TFSI 8J","2006-2014","Benzina","Coupe sportiva",200,280,7.7,6.6,240,9000,22000,7,6,8),
    ("Audi TT 2.0 TFSI 8S","Audi","TT","2.0 TFSI 8S","2014-2023","Benzina","Coupe sportiva",230,370,6.0,5.3,250,22000,42000,8,7,8),
    ("Audi TTS 8S","Audi","TTS","8S","2014-2023","Benzina","Coupe sportiva",310,380,7.2,4.7,250,32000,55000,7,7,9),

    ("Audi Q2 1.6 TDI","Audi","Q2","1.6 TDI","2016-2020","Diesel","SUV compatto",116,250,4.4,10.5,197,16000,28000,8,8,6),
    ("Audi Q3 2.0 TDI 8U","Audi","Q3","2.0 TDI 8U","2011-2018","Diesel","SUV compatto",150,340,4.7,9.6,204,13000,27000,8,8,6),
    ("Audi Q5 2.0 TDI FY","Audi","Q5","2.0 TDI FY","2017-oggi","Diesel","SUV premium",190,400,5.0,7.9,218,28000,56000,8,9,7),
]

for car in audi:
    name = car[0]
    cur.execute("DELETE FROM cars WHERE lower(name)=lower(?)", (name,))

for car in audi:
    name, brand, model, version, years, fuel, car_type, power, torque, consumption, zero100, speed_max, price_min, price_max, reliability, comfort, fun = car

    cur.execute("""
    INSERT INTO cars (
        name, brand, model, version, years, fuel, car_type,
        power, torque, consumption, zero100, speed_max,
        price_min, price_max, reliability, comfort, fun,
        pros, cons, ideal, checks, mods, avoid, verdict, data_quality
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        name, brand, model, version, years, fuel, car_type,
        power, torque, consumption, zero100, speed_max,
        price_min, price_max, reliability, comfort, fun,
        "Scheda Audi reale per generazione, utile per confronto, acquisto usato e valutazione tecnica.",
        "Controllare sempre storico manutenzione, chilometri reali, cambio, elettronica, gomme, freni e modifiche.",
        "Uso quotidiano premium, viaggi, confronto usato e scelta in base a budget.",
        "Verificare tagliandi, S tronic/DSG se presente, frizione, turbina, DPF sui diesel, gomme, freni e incidenti.",
        "Gomme premium, freni efficienti, manutenzione completa, cerchi omologati e modifiche leggere.",
        "Evitare rimappe aggressive, scarichi non omologati, eliminazione DPF/FAP e auto senza storico.",
        "Scheda Audi verificata nella struttura generazione/motore. Controllare sempre dati specifici dell'esemplare.",
        "verified"
    ))

conn.commit()
conn.close()

print("Audi reali inserite e Audi generate marcate legacy_generated")
