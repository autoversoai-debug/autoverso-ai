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
WHERE lower(brand)='alfa romeo'
""")

alfa = [
    ("Alfa Romeo MiTo 1.4 Turbo","Alfa Romeo","MiTo","1.4 Turbo","2008-2018","Benzina","Utilitaria sportiva",155,230,6.5,8.0,215,6000,14000,7,6,8),
    ("Alfa Romeo MiTo Quadrifoglio Verde","Alfa Romeo","MiTo","Quadrifoglio Verde","2009-2016","Benzina","Utilitaria sportiva",170,250,6.0,7.5,219,9000,18000,7,6,9),

    ("Alfa Romeo Giulietta 1.6 JTDm","Alfa Romeo","Giulietta","1.6 JTDm","2010-2020","Diesel","Compatta",120,320,4.0,10.0,195,7000,17000,8,7,6),
    ("Alfa Romeo Giulietta 2.0 JTDm","Alfa Romeo","Giulietta","2.0 JTDm","2010-2020","Diesel","Compatta",150,380,4.2,8.8,210,9000,19000,8,7,7),
    ("Alfa Romeo Giulietta Quadrifoglio Verde 1750 TBi","Alfa Romeo","Giulietta","Quadrifoglio Verde 1750 TBi","2010-2016","Benzina","Compatta sportiva",235,340,7.6,6.8,242,13000,26000,7,6,9),
    ("Alfa Romeo Giulietta Veloce 1750 TBi TCT","Alfa Romeo","Giulietta","Veloce 1750 TBi TCT","2016-2020","Benzina","Compatta sportiva",240,340,6.8,6.0,244,16000,30000,7,6,9),

    ("Alfa Romeo 147 1.9 JTD 150","Alfa Romeo","147","1.9 JTD 150","2004-2010","Diesel","Compatta",150,305,5.8,8.8,208,3000,9000,7,6,7),
    ("Alfa Romeo 159 1.9 JTDm 150","Alfa Romeo","159","1.9 JTDm 150","2005-2011","Diesel","Berlina",150,320,6.0,9.4,210,4000,10000,7,7,7),
    ("Alfa Romeo Brera 2.4 JTDm","Alfa Romeo","Brera","2.4 JTDm","2006-2010","Diesel","Coupe",210,400,6.8,7.9,231,9000,22000,7,7,8),

    ("Alfa Romeo Giulia 2.2 Diesel 150","Alfa Romeo","Giulia","2.2 Diesel 150","2016-2022","Diesel","Berlina sportiva",150,380,4.2,8.4,220,18000,32000,8,8,8),
    ("Alfa Romeo Giulia 2.2 Diesel 180","Alfa Romeo","Giulia","2.2 Diesel 180","2016-2022","Diesel","Berlina sportiva",180,450,4.2,7.1,230,21000,36000,8,8,8),
    ("Alfa Romeo Giulia 2.2 Diesel 210 Q4","Alfa Romeo","Giulia","2.2 Diesel 210 Q4","2016-2022","Diesel","Berlina sportiva",210,470,4.7,6.8,235,26000,42000,8,8,8),
    ("Alfa Romeo Giulia 2.0 Turbo 200","Alfa Romeo","Giulia","2.0 Turbo 200","2016-oggi","Benzina","Berlina sportiva",200,330,6.0,6.6,235,25000,43000,8,8,8),
    ("Alfa Romeo Giulia Veloce 2.0 Turbo 280 Q4","Alfa Romeo","Giulia","Veloce 2.0 Turbo 280 Q4","2016-oggi","Benzina","Berlina sportiva",280,400,7.0,5.2,240,33000,56000,8,8,9),
    ("Alfa Romeo Giulia Quadrifoglio 2.9 V6","Alfa Romeo","Giulia","Quadrifoglio 2.9 V6","2016-oggi","Benzina","Berlina sportiva",510,600,10.4,3.9,307,65000,120000,7,7,10),

    ("Alfa Romeo Stelvio 2.2 Diesel 180","Alfa Romeo","Stelvio","2.2 Diesel 180","2017-2022","Diesel","SUV",180,450,5.0,7.6,210,25000,42000,8,8,7),
    ("Alfa Romeo Stelvio 2.2 Diesel 210 Q4","Alfa Romeo","Stelvio","2.2 Diesel 210 Q4","2017-oggi","Diesel","SUV",210,470,5.5,6.6,215,30000,52000,8,8,8),
    ("Alfa Romeo Stelvio 2.0 Turbo 280 Q4","Alfa Romeo","Stelvio","2.0 Turbo 280 Q4","2017-oggi","Benzina","SUV sportivo",280,400,7.0,5.7,230,35000,60000,8,8,9),
    ("Alfa Romeo Stelvio Quadrifoglio 2.9 V6","Alfa Romeo","Stelvio","Quadrifoglio 2.9 V6","2017-oggi","Benzina","SUV sportivo",510,600,9.0,3.8,283,70000,130000,7,8,10),

    ("Alfa Romeo Tonale Hybrid 130","Alfa Romeo","Tonale","Hybrid 130","2022-oggi","Ibrida benzina","SUV compatto",130,240,5.6,9.6,200,30000,43000,8,8,6),
    ("Alfa Romeo Tonale Plug-in Hybrid Q4","Alfa Romeo","Tonale","Plug-in Hybrid Q4","2022-oggi","Ibrida plug-in","SUV compatto",280,270,1.5,6.2,206,42000,60000,8,8,8)
]

for car in alfa:
    name = car[0]
    cur.execute("DELETE FROM cars WHERE lower(name)=lower(?)", (name,))

for car in alfa:
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
        "Scheda Alfa Romeo reale per generazione/versione, utile per confronto, acquisto usato e valutazione tecnica.",
        "Controllare sempre storico manutenzione, chilometri reali, elettronica, sospensioni, freni, gomme e modifiche.",
        "Guida emozionale, uso quotidiano, confronto usato e scelta in base a budget e piacere di guida.",
        "Verificare tagliandi, cambio automatico/manuale, turbo, frizione, gomme, freni, sospensioni, incidenti e modifiche precedenti.",
        "Gomme premium, freni efficienti, manutenzione completa, assetto solo se di qualita e omologato.",
        "Evitare rimappe aggressive, scarichi non omologati, auto senza storico e modifiche economiche.",
        "Scheda Alfa Romeo verificata nella struttura generazione/motore. Controllare sempre dati specifici dell'esemplare.",
        "verified"
    ))

conn.commit()
conn.close()

print("Alfa Romeo reali inserite e Alfa generate marcate legacy_generated")
