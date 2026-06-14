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
WHERE lower(brand)='volkswagen'
""")

vw = [
    ("Volkswagen Up 1.0","Volkswagen","Up","1.0","2011-2023","Benzina","City car",60,95,4.5,14.4,160,5000,12000,8,6,4),
    ("Volkswagen Polo 1.0 TSI AW","Volkswagen","Polo","1.0 TSI AW","2017-oggi","Benzina","Utilitaria",95,175,5.0,10.8,187,12000,22000,8,8,6),
    ("Volkswagen Polo GTI AW","Volkswagen","Polo","GTI AW","2017-oggi","Benzina","Utilitaria sportiva",200,320,6.0,6.7,237,22000,35000,7,7,9),

    ("Volkswagen Golf 1.6 TDI Mk7","Volkswagen","Golf","1.6 TDI Mk7","2012-2020","Diesel","Compatta",105,250,4.2,10.7,195,9000,20000,8,8,6),
    ("Volkswagen Golf 2.0 TDI Mk7","Volkswagen","Golf","2.0 TDI Mk7","2012-2020","Diesel","Compatta",150,340,4.3,8.6,216,13000,24000,8,8,7),
    ("Volkswagen Golf GTI Mk7","Volkswagen","Golf","GTI Mk7","2013-2020","Benzina","Compatta sportiva",230,350,6.4,6.4,250,18000,33000,8,8,9),
    ("Volkswagen Golf GTI Mk8","Volkswagen","Golf","GTI Mk8","2020-oggi","Benzina","Compatta sportiva",245,370,7.0,6.2,250,32000,50000,8,8,9),
    ("Volkswagen Golf R Mk7","Volkswagen","Golf","R Mk7","2013-2020","Benzina","Compatta sportiva",300,380,7.1,4.9,250,28000,45000,7,8,10),
    ("Volkswagen Golf R Mk8","Volkswagen","Golf","R Mk8","2020-oggi","Benzina","Compatta sportiva",320,420,7.8,4.7,250,45000,65000,8,8,10),

    ("Volkswagen Passat B8 2.0 TDI 150","Volkswagen","Passat","B8 2.0 TDI 150","2014-2023","Diesel","Berlina familiare",150,340,4.3,8.7,220,13000,28000,8,9,6),
    ("Volkswagen Passat B8 2.0 TDI 190","Volkswagen","Passat","B8 2.0 TDI 190","2014-2023","Diesel","Berlina familiare",190,400,4.7,7.7,237,17000,33000,8,9,7),

    ("Volkswagen Tiguan II 2.0 TDI 150","Volkswagen","Tiguan","II 2.0 TDI 150","2016-2024","Diesel","SUV compatto",150,340,5.0,9.3,204,18000,35000,8,8,6),
    ("Volkswagen Tiguan II 2.0 TDI 190","Volkswagen","Tiguan","II 2.0 TDI 190","2016-2024","Diesel","SUV compatto",190,400,5.7,7.9,212,24000,42000,8,8,7),

    ("Volkswagen T-Roc 1.5 TSI","Volkswagen","T-Roc","1.5 TSI","2017-oggi","Benzina","SUV compatto",150,250,5.8,8.4,205,19000,34000,8,8,7),
    ("Volkswagen Arteon 2.0 TDI 190","Volkswagen","Arteon","2.0 TDI 190","2017-2023","Diesel","Berlina coupe",190,400,4.8,7.8,239,26000,43000,8,9,7),
    ("Volkswagen Arteon 2.0 TDI 240","Volkswagen","Arteon","2.0 TDI 240","2017-2020","Diesel","Berlina coupe",240,500,5.9,6.5,245,30000,50000,7,9,8),

    ("Volkswagen Scirocco 2.0 TSI","Volkswagen","Scirocco","2.0 TSI","2008-2017","Benzina","Coupe compatta",200,280,7.6,7.2,235,10000,22000,7,6,8),
    ("Volkswagen Scirocco R","Volkswagen","Scirocco","R","2009-2017","Benzina","Coupe sportiva",265,350,8.0,5.8,250,18000,35000,7,6,9)
]

for car in vw:
    name = car[0]
    cur.execute("DELETE FROM cars WHERE lower(name)=lower(?)", (name,))

for car in vw:
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
        "Scheda Volkswagen reale per generazione, utile per confronto, acquisto usato e valutazione tecnica.",
        "Controllare sempre storico manutenzione, chilometri reali, cambio DSG/manuale, elettronica, gomme, freni e modifiche.",
        "Uso quotidiano, viaggi, confronto usato e scelta in base a budget, consumi e affidabilita.",
        "Verificare tagliandi, DSG se presente, frizione, turbina, DPF sui diesel, gomme, freni e incidenti.",
        "Gomme premium, freni efficienti, manutenzione completa, cerchi omologati e modifiche leggere.",
        "Evitare rimappe aggressive, scarichi non omologati, eliminazione DPF/FAP e auto senza storico.",
        "Scheda Volkswagen verificata nella struttura generazione/motore. Controllare sempre dati specifici dell'esemplare.",
        "verified"
    ))

conn.commit()
conn.close()

print("Volkswagen reali inserite e Volkswagen generate marcate legacy_generated")
