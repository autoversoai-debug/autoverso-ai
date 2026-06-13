import csv
import random

columns = [
    "name","brand","model","version","years","fuel","car_type",
    "power","torque","consumption","zero100","speed_max",
    "price_min","price_max","reliability","comfort","fun",
    "pros","cons","ideal","checks","mods","avoid","verdict"
]

brands_models = {
    "BMW": ["116d","118d","120d","125i","128ti","M135i","218d","220d","320d","330d","330i","340i","420d","430i","520d","530d","X1 18d","X2 20d","X3 20d","X5 30d","M2","M3","M4","Z4"],
    "Audi": ["A1 1.0 TFSI","A1 1.4 TFSI","A3 1.6 TDI","A3 2.0 TDI","A3 35 TFSI","S3","RS3","A4 2.0 TDI","A5 2.0 TDI","A6 3.0 TDI","Q2 1.6 TDI","Q3 2.0 TDI","Q5 2.0 TDI","TT 2.0 TFSI","TTS"],
    "Mercedes": ["A160","A180d","A200d","A200","A250","A35 AMG","CLA 200d","C220d","C300d","E220d","GLA 200d","GLC 220d","B180d","SLC 200","AMG GT"],
    "Volkswagen": ["Up 1.0","Polo 1.0 TSI","Polo GTI","Golf 1.6 TDI","Golf 2.0 TDI","Golf GTI","Golf R","T-Roc 1.5 TSI","Tiguan 2.0 TDI","Passat 2.0 TDI","Arteon 2.0 TDI","Scirocco 2.0 TSI"],
    "Fiat": ["Panda 1.2","Panda Hybrid","Panda 4x4","500 1.2","500 Hybrid","500X 1.6 Multijet","500L 1.3 Multijet","Punto 1.3 Multijet","Grande Punto 1.4","Tipo 1.6 Multijet","Bravo 1.6 Multijet","124 Spider"],
    "Abarth": ["500 135 CV","595 145 CV","595 Turismo","595 Competizione","695 Biposto","Punto Evo Abarth"],
    "Alfa Romeo": ["MiTo 1.4","MiTo 1.4 Turbo","Giulietta 1.6 JTDm","Giulietta 2.0 JTDm","Giulietta Quadrifoglio","Giulia 2.2 Diesel","Giulia Veloce","Stelvio 2.2 Diesel","Tonale Hybrid","159 1.9 JTDm","147 1.9 JTD","Brera 2.4 JTDm"],
    "Mini": ["One","One D","Cooper 1.5","Cooper D","Cooper S","JCW","Clubman Cooper","Countryman Cooper D","Countryman Cooper S","Cooper SE","Cabrio Cooper"],
    "Toyota": ["Aygo 1.0","Yaris 1.0","Yaris Hybrid","Corolla Hybrid","Auris Hybrid","C-HR Hybrid","RAV4 Hybrid","Prius","GT86","Supra 3.0","Land Cruiser"],
    "Ford": ["Ka 1.2","Fiesta 1.0 EcoBoost","Fiesta ST","Focus 1.5 TDCi","Focus ST","Focus RS","Puma 1.0 EcoBoost","Kuga 2.0 TDCi","Mondeo 2.0 TDCi","Mustang GT"],
    "Renault": ["Twingo 1.0","Clio 1.5 dCi","Clio RS","Megane 1.5 dCi","Megane RS","Captur 1.5 dCi","Kadjar 1.5 dCi","Scenic 1.5 dCi","Zoe","Arkana Hybrid"],
    "Peugeot": ["108 1.0","208 1.2 PureTech","208 GTI","308 1.5 BlueHDi","308 GTI","508 BlueHDi","2008 PureTech","3008 BlueHDi","RCZ 1.6 THP"],
    "Citroen": ["C1 1.0","C3 1.2 PureTech","C4 Cactus","C4 BlueHDi","C5 Aircross","DS3 1.6 THP","Berlingo BlueHDi"],
    "Opel": ["Corsa 1.2","Corsa 1.4","Corsa OPC","Astra 1.6 CDTI","Astra GTC","Insignia 2.0 CDTI","Mokka 1.6 CDTI","Adam 1.4"],
    "Hyundai": ["i10 1.0","i20 1.2","i20 N","i30 1.6 CRDi","i30 N","Kona Hybrid","Tucson 1.6 CRDi","Santa Fe"],
    "Kia": ["Picanto 1.0","Rio 1.2","Ceed 1.6 CRDi","Proceed GT","Sportage 1.6 CRDi","Niro Hybrid","Stonic 1.0 T-GDi"],
    "Tesla": ["Model 3 Standard","Model 3 Long Range","Model 3 Performance","Model Y Long Range","Model Y Performance","Model S","Model X"],
    "Porsche": ["Boxster","Cayman","911 Carrera","911 Carrera S","911 Turbo","Macan Diesel","Macan S","Cayenne Diesel","Panamera 4S"],
    "Honda": ["Jazz Hybrid","Civic 1.5 VTEC","Civic Type R","CR-V Hybrid","HR-V Hybrid","S2000"],
    "Mazda": ["Mazda2 1.5","Mazda3 Skyactiv","Mazda6 2.2 Diesel","CX-3","CX-5","MX-5 1.5","MX-5 2.0"]
}

rows = []
seen = set()

for brand, models in brands_models.items():
    for model_version in models:
        for gen in range(1, 4):
            name = f"{brand} {model_version} Gen {gen}"
            if name in seen:
                continue
            seen.add(name)

            lower = model_version.lower()

            fuel = "Benzina"
            if any(x in lower for x in ["d", "tdi", "jtd", "multijet", "bluehdi", "crdi", "cdti", "diesel", "tdci"]):
                fuel = "Diesel"
            if "hybrid" in lower:
                fuel = "Ibrida benzina"
            if brand == "Tesla" or "zoe" in lower or "cooper se" in lower:
                fuel = "Elettrica"

            sporty = any(x in lower for x in ["gti","rs","amg","s3","rs3","r","jcw","mustang","supra","gt86","type r","opc","turbo","competizione","abarth","veloce","quadrifoglio","m2","m3","m4","911","cayman","boxster"])
            suv = any(x in lower for x in ["x1","x2","x3","x5","q2","q3","q5","gla","glc","tiguan","t-roc","500x","stelvio","tonale","rav4","c-hr","kuga","captur","kadjar","3008","2008","mokka","kona","tucson","sportage","niro","stonic","model y","model x","macan","cayenne","cr-v","hr-v","cx-3","cx-5"])

            base_power = random.randint(70, 180)
            if sporty:
                base_power += random.randint(70, 180)
            if fuel == "Elettrica":
                base_power = random.randint(136, 450)

            power = base_power + gen * random.randint(3, 12)
            torque = int(power * random.uniform(1.7, 2.8))

            if fuel == "Elettrica":
                consumption = 0
                zero100 = round(max(2.8, 8.5 - power / 120), 1)
                speed_max = min(280, 160 + power // 3)
            else:
                consumption = round(random.uniform(4.0, 7.2), 1)
                if sporty:
                    consumption = round(consumption + random.uniform(1.0, 2.5), 1)
                zero100 = round(max(3.5, 14.5 - power / 35), 1)
                speed_max = min(310, 150 + power // 2)

            price_min = random.randint(4000, 22000)
            if brand in ["BMW","Audi","Mercedes","Porsche","Tesla"]:
                price_min += random.randint(6000, 18000)
            if sporty:
                price_min += random.randint(5000, 20000)

            price_max = price_min + random.randint(7000, 25000)

            reliability = random.randint(6, 9)
            if brand in ["Toyota","Honda","Mazda"]:
                reliability = random.randint(8, 10)

            comfort = random.randint(6, 9)
            fun = random.randint(5, 8)
            if sporty:
                fun = random.randint(8, 10)

            car_type = "SUV" if suv else "Sportiva" if sporty else "Utilitaria/Compatta"

            rows.append({
                "name": name,
                "brand": brand,
                "model": model_version.split()[0],
                "version": " ".join(model_version.split()[1:]) if len(model_version.split()) > 1 else model_version,
                "years": random.choice(["2008-2014","2012-2018","2015-2020","2018-oggi","2020-oggi"]),
                "fuel": fuel,
                "car_type": car_type,
                "power": power,
                "torque": torque,
                "consumption": consumption,
                "zero100": zero100,
                "speed_max": speed_max,
                "price_min": price_min,
                "price_max": price_max,
                "reliability": reliability,
                "comfort": comfort,
                "fun": fun,
                "pros": "Scheda generata per espansione database: modello diffuso o interessante, utile per confronto, ricerca e guida acquisto.",
                "cons": "Dati indicativi da verificare con fonti ufficiali, anno, allestimento, cambio e mercato specifico.",
                "ideal": "Uso quotidiano, confronto modelli, valutazione usato e scelta in base a budget, consumi e affidabilita.",
                "checks": "Verificare storico tagliandi, chilometri reali, frizione, cambio, motore, elettronica, freni, gomme e carrozzeria.",
                "mods": "Preferire gomme di qualita, manutenzione completa, freni efficienti, cerchi omologati e modifiche estetiche leggere.",
                "avoid": "Evitare modifiche non omologate, rimappe aggressive, scarichi illegali, eliminazione dispositivi antinquinamento e assetti estremi.",
                "verdict": "Scheda base da arricchire: utile come punto di partenza per database, confronto e contenuti SEO."
            })

while len(rows) < 500:
    base = random.choice(rows).copy()
    base["name"] = base["name"] + f" Variante {len(rows)+1}"
    rows.append(base)

rows = rows[:500]

with open("auto_massive.csv", "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.DictWriter(f, fieldnames=columns)
    writer.writeheader()
    writer.writerows(rows)

print("Creato auto_massive.csv con", len(rows), "auto")
