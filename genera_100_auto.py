import csv

columns = [
    "name","brand","model","version","years","fuel","car_type",
    "power","torque","consumption","zero100","speed_max",
    "price_min","price_max","reliability","comfort","fun",
    "pros","cons","ideal","checks","mods","avoid","verdict"
]

brands = {
    "BMW": ["116d", "118d", "120d", "320d", "330d", "420d", "520d", "X1 18d", "X3 20d", "M140i"],
    "Audi": ["A1 1.4 TFSI", "A3 2.0 TDI", "A4 2.0 TDI", "A5 2.0 TDI", "Q2 1.6 TDI", "Q3 2.0 TDI", "TT 2.0 TFSI", "S3", "A6 3.0 TDI", "Q5 2.0 TDI"],
    "Mercedes": ["A180d", "A200d", "CLA 200d", "C220d", "E220d", "GLA 200d", "GLC 220d", "A35 AMG", "C300d", "B180d"],
    "Volkswagen": ["Polo 1.0 TSI", "Golf 1.6 TDI", "Golf GTI", "Golf R", "T-Roc 1.5 TSI", "Tiguan 2.0 TDI", "Passat 2.0 TDI", "Up 1.0", "Scirocco 2.0 TSI", "Arteon 2.0 TDI"],
    "Fiat": ["Panda 1.2", "500 1.2", "Punto 1.3 Multijet", "Tipo 1.6 Multijet", "Bravo 1.6 Multijet", "Grande Punto 1.4", "500X 1.6 Multijet", "Panda 4x4", "Doblo 1.6 Multijet", "124 Spider"],
    "Alfa Romeo": ["MiTo 1.4 Turbo", "Giulietta 1.6 JTDm", "Giulietta Quadrifoglio", "Giulia 2.2 Diesel", "Giulia Veloce", "Stelvio 2.2 Diesel", "159 1.9 JTDm", "147 1.9 JTD", "Brera 2.4 JTDm", "Tonale Hybrid"],
    "Mini": ["Cooper 1.5", "Cooper S", "One D", "Clubman Cooper", "Countryman Cooper D", "JCW", "Paceman Cooper S", "Cooper SE", "Cabrio Cooper", "Roadster Cooper S"],
    "Toyota": ["Yaris Hybrid", "Aygo 1.0", "Corolla Hybrid", "C-HR Hybrid", "RAV4 Hybrid", "Prius", "Auris Hybrid", "GT86", "Supra 3.0", "Land Cruiser"],
    "Ford": ["Fiesta 1.0 EcoBoost", "Focus 1.5 TDCi", "Focus ST", "Focus RS", "Puma 1.0 EcoBoost", "Kuga 2.0 TDCi", "Mondeo 2.0 TDCi", "Ka 1.2", "Mustang GT", "S-Max 2.0 TDCi"],
    "Renault": ["Clio 1.5 dCi", "Clio RS", "Megane 1.5 dCi", "Megane RS", "Captur 1.5 dCi", "Kadjar 1.5 dCi", "Twingo 1.0", "Scenic 1.5 dCi", "Zoe", "Arkana Hybrid"]
}

rows = []
i = 0

for brand, models in brands.items():
    for item in models:
        i += 1

        fuel = "Diesel" if any(x in item.lower() for x in ["d", "tdi", "jtd", "multijet", "diesel", "tdci"]) else "Benzina"
        if "Hybrid" in item or "hybrid" in item:
            fuel = "Ibrida benzina"
        if item in ["Zoe", "Cooper SE"]:
            fuel = "Elettrica"

        sporty = any(x in item.lower() for x in ["gti", "rs", "amg", "s3", "r", "jcw", "mustang", "supra", "gt86", "quadrifoglio", "veloce"])
        suv = any(x in item.lower() for x in ["x1", "x3", "q2", "q3", "q5", "gla", "glc", "tiguan", "t-roc", "500x", "stelvio", "rav4", "c-hr", "kuga", "captur", "kadjar", "puma", "land cruiser", "tonale"])

        power = 90 + (i % 12) * 12
        if sporty:
            power += 90
        if fuel == "Elettrica":
            power = 136 + (i % 4) * 20

        torque = power * 2
        consumption = round(4.0 + (i % 8) * 0.35, 1)
        if sporty:
            consumption += 1.8
        if fuel == "Elettrica":
            consumption = 0

        zero100 = round(max(4.2, 13.5 - power / 35), 1)
        speed = min(280, 160 + power // 2)

        price_min = 5000 + (i % 20) * 1200
        if brand in ["BMW", "Audi", "Mercedes"]:
            price_min += 7000
        if sporty:
            price_min += 8000
        price_max = price_min + 9000 + (i % 8) * 1000

        reliability = 7 + (i % 3)
        comfort = 6 + (i % 4)
        fun = 5 + (i % 5)
        if sporty:
            fun = 9
        if brand in ["Toyota"]:
            reliability = 9

        rows.append({
            "name": f"{brand} {item}",
            "brand": brand,
            "model": item.split()[0],
            "version": " ".join(item.split()[1:]) if len(item.split()) > 1 else item,
            "years": "2012-oggi",
            "fuel": fuel,
            "car_type": "SUV compatto" if suv else "Compatta sportiva" if sporty else "Utilitaria/Compatta",
            "power": power,
            "torque": torque,
            "consumption": consumption,
            "zero100": zero100,
            "speed_max": speed,
            "price_min": price_min,
            "price_max": price_max,
            "reliability": reliability,
            "comfort": comfort,
            "fun": fun,
            "pros": "Modello diffuso, buona disponibilita sul mercato usato, ricambi reperibili e buon equilibrio generale.",
            "cons": "Verificare sempre manutenzione, chilometri reali, stato meccanico, gomme, freni ed eventuali modifiche precedenti.",
            "ideal": "Uso quotidiano, acquisto usato, confronto con modelli simili e valutazione in base al budget.",
            "checks": "Controllare storico tagliandi, frizione, cambio, motore, elettronica, gomme, freni, sospensioni e carrozzeria.",
            "mods": "Gomme di qualita, manutenzione completa, freni in ordine, cerchi omologati e modifiche estetiche leggere.",
            "avoid": "Evitare modifiche non omologate, rimappe aggressive, scarichi illegali, eliminazione dispositivi antinquinamento e assetti estremi.",
            "verdict": "Scelta interessante se il prezzo e coerente, la manutenzione e documentata e l'esemplare e in buone condizioni."
        })

with open("auto_massive.csv", "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.DictWriter(f, fieldnames=columns)
    writer.writeheader()
    writer.writerows(rows)

print("Creato auto_massive.csv con", len(rows), "auto")
