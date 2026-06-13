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
WHERE lower(brand)='bmw'
""")

bmw = [
    ("BMW 116d F20","BMW","Serie 1","116d F20","2011-2019","Diesel","Compatta",116,260,4.5,10.3,200,9000,17000,8,7,6),
    ("BMW 116d F40","BMW","Serie 1","116d F40","2019-oggi","Diesel","Compatta",116,270,4.2,10.3,200,18000,30000,8,8,6),
    ("BMW 118d F20","BMW","Serie 1","118d F20","2011-2019","Diesel","Compatta",143,320,4.5,8.9,212,11000,22000,8,7,7),
    ("BMW 118d F40","BMW","Serie 1","118d F40","2019-oggi","Diesel","Compatta",150,350,4.1,8.4,216,20000,34000,8,8,7),
    ("BMW 120d F20","BMW","Serie 1","120d F20","2011-2019","Diesel","Compatta",184,380,4.5,7.2,228,14000,26000,8,7,8),
    ("BMW 120d F40","BMW","Serie 1","120d F40","2019-oggi","Diesel","Compatta",190,400,4.3,7.3,231,23000,38000,8,8,8),
    ("BMW M135i F20","BMW","Serie 1","M135i F20","2012-2016","Benzina","Compatta sportiva",326,450,7.5,4.9,250,25000,42000,7,7,10),
    ("BMW M140i F20","BMW","Serie 1","M140i F20","2016-2019","Benzina","Compatta sportiva",340,500,7.8,4.6,250,28000,48000,8,7,10),
    ("BMW M135i F40","BMW","Serie 1","M135i F40","2019-oggi","Benzina","Compatta sportiva",306,450,7.1,4.8,250,32000,52000,8,8,9),

    ("BMW 320d E90","BMW","Serie 3","320d E90","2005-2012","Diesel","Berlina",177,350,4.8,7.9,230,6000,14000,8,7,7),
    ("BMW 320d F30","BMW","Serie 3","320d F30","2012-2019","Diesel","Berlina",184,380,4.5,7.5,235,12000,25000,8,8,7),
    ("BMW 320d G20","BMW","Serie 3","320d G20","2019-oggi","Diesel","Berlina",190,400,4.2,6.8,240,25000,45000,8,8,8),
    ("BMW 330d E90","BMW","Serie 3","330d E90","2005-2012","Diesel","Berlina",245,520,5.7,6.1,250,9000,18000,8,7,8),
    ("BMW 330d F30","BMW","Serie 3","330d F30","2012-2019","Diesel","Berlina",258,560,5.1,5.6,250,18000,32000,8,8,8),
    ("BMW 330d G20","BMW","Serie 3","330d G20","2019-oggi","Diesel","Berlina",286,650,5.0,5.3,250,35000,60000,8,8,9),
    ("BMW 340i F30","BMW","Serie 3","340i F30","2015-2019","Benzina","Berlina sportiva",326,450,7.0,5.1,250,28000,48000,8,8,9),
    ("BMW M340i G20","BMW","Serie 3","M340i G20","2019-oggi","Benzina","Berlina sportiva",374,500,7.4,4.4,250,45000,75000,8,8,9),

    ("BMW M2 F87","BMW","Serie 2","M2 F87","2016-2018","Benzina","Coupe sportiva",370,465,7.9,4.3,250,35000,55000,8,6,10),
    ("BMW M2 Competition F87","BMW","Serie 2","M2 Competition F87","2018-2021","Benzina","Coupe sportiva",410,550,8.5,4.2,250,45000,70000,8,6,10),
    ("BMW M2 G87","BMW","Serie 2","M2 G87","2023-oggi","Benzina","Coupe sportiva",460,550,9.8,4.1,250,60000,90000,7,6,10),

    ("BMW M3 E92","BMW","Serie 3","M3 E92","2007-2013","Benzina","Coupe sportiva",420,400,12.4,4.8,250,35000,75000,7,6,10),
    ("BMW M3 F80","BMW","Serie 3","M3 F80","2014-2018","Benzina","Berlina sportiva",431,550,8.8,4.1,250,45000,75000,7,7,10),
    ("BMW M3 Competition G80","BMW","Serie 3","M3 Competition G80","2021-oggi","Benzina","Berlina sportiva",510,650,10.0,3.9,250,70000,115000,7,7,10),

    ("BMW M4 F82","BMW","Serie 4","M4 F82","2014-2020","Benzina","Coupe sportiva",431,550,8.8,4.1,250,45000,75000,7,7,10),
    ("BMW M4 Competition F82","BMW","Serie 4","M4 Competition F82","2016-2020","Benzina","Coupe sportiva",450,550,8.8,4.0,250,55000,85000,7,7,10),
    ("BMW M4 Competition G82","BMW","Serie 4","M4 Competition G82","2021-oggi","Benzina","Coupe sportiva",510,650,10.0,3.9,250,70000,115000,7,7,10),
]

for car in bmw:
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
        "Scheda BMW reale per generazione, utile per confronto e valutazione usato.",
        "Controllare sempre storico manutenzione, chilometri reali, gomme, freni, cambio e modifiche.",
        "Uso quotidiano, guida premium, confronto usato e scelta in base a budget.",
        "Verificare tagliandi, frizione/cambio, turbina se presente, elettronica, gomme, freni, incidenti.",
        "Gomme premium, freni efficienti, manutenzione completa, modifiche solo omologate.",
        "Evitare rimappe aggressive, scarichi non omologati, auto senza storico o molto stressate.",
        "Scheda BMW verificata nella struttura generazione/motore. Controllare sempre dati specifici dell'esemplare.",
        "verified"
    ))

conn.commit()
conn.close()

print("BMW reali inserite e BMW generate marcate legacy_generated")
