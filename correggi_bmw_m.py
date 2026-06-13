import sqlite3

conn = sqlite3.connect("autoverso.db")
cur = conn.cursor()

updates = [
    {
        "id": 179,
        "name": "BMW M4 Competition G82",
        "model": "M4",
        "version": "Competition G82",
        "years": "2021-oggi",
        "fuel": "Benzina",
        "car_type": "Coupe sportiva",
        "power": 510,
        "torque": 650,
        "consumption": 10.0,
        "zero100": 3.9,
        "speed_max": 250,
        "price_min": 70000,
        "price_max": 115000,
        "reliability": 7,
        "comfort": 7,
        "fun": 10,
        "pros": "Prestazioni altissime, motore S58, telaio preciso, immagine M forte.",
        "cons": "Costi elevati, consumi alti, gomme e freni costosi, attenzione a uso pista.",
        "ideal": "Appassionati, guida sportiva, track day leggero, auto emozionale.",
        "checks": "Storico tagliandi, freni, gomme, uso pista, incidenti, manutenzione cambio e differenziale.",
        "mods": "Gomme premium, freni di qualita, manutenzione scrupolosa, assetto professionale solo se omologato.",
        "avoid": "Mappe aggressive, scarichi non omologati, auto incidentate o molto stressate in pista.",
        "verdict": "M4 G82 Competition e una coupe M molto prestazionale, da comprare solo con storico chiaro.",
        "data_quality": "verified"
    },
    {
        "id": 176,
        "name": "BMW M3 Competition G80",
        "model": "M3",
        "version": "Competition G80",
        "years": "2021-oggi",
        "fuel": "Benzina",
        "car_type": "Berlina sportiva",
        "power": 510,
        "torque": 650,
        "consumption": 10.0,
        "zero100": 3.9,
        "speed_max": 250,
        "price_min": 70000,
        "price_max": 115000,
        "reliability": 7,
        "comfort": 7,
        "fun": 10,
        "pros": "Prestazioni da supercar, quattro porte, motore S58, grande efficacia.",
        "cons": "Costi alti, consumi elevati, manutenzione costosa, attenzione a uso pista.",
        "ideal": "Chi vuole una sportiva vera ma piu pratica di una coupe.",
        "checks": "Storico tagliandi, gomme, freni, differenziale, uso pista, incidenti, modifiche precedenti.",
        "mods": "Gomme top, freni adeguati, manutenzione accurata, upgrade solo professionali e omologati.",
        "avoid": "Rimappe pesanti, scarichi illegali, esemplari senza storico o usati male.",
        "verdict": "M3 G80 Competition e una delle berline sportive piu complete, ma va controllata molto bene.",
        "data_quality": "verified"
    },
    {
        "id": 171,
        "name": "BMW M2 G87",
        "model": "M2",
        "version": "G87",
        "years": "2023-oggi",
        "fuel": "Benzina",
        "car_type": "Coupe sportiva",
        "power": 460,
        "torque": 550,
        "consumption": 9.8,
        "zero100": 4.1,
        "speed_max": 250,
        "price_min": 60000,
        "price_max": 90000,
        "reliability": 7,
        "comfort": 6,
        "fun": 10,
        "pros": "Molto divertente, motore S58, trazione posteriore, dimensioni compatte.",
        "cons": "Costi elevati, consumi alti, comfort rigido, attenzione a uso sportivo.",
        "ideal": "Appassionati che cercano una M compatta e molto guidabile.",
        "checks": "Tagliandi, gomme, freni, uso pista, incidenti, modifiche precedenti.",
        "mods": "Gomme premium, freni, manutenzione, assetto solo professionale.",
        "avoid": "Mappe aggressive, scarichi non omologati, esemplari maltrattati.",
        "verdict": "M2 G87 e una delle BMW M piu divertenti, ma va verificata con attenzione.",
        "data_quality": "verified"
    },
    {
        "id": 31,
        "name": "BMW M140i F20",
        "model": "Serie 1",
        "version": "M140i F20",
        "years": "2016-2019",
        "fuel": "Benzina",
        "car_type": "Compatta sportiva",
        "power": 340,
        "torque": 500,
        "consumption": 7.8,
        "zero100": 4.6,
        "speed_max": 250,
        "price_min": 28000,
        "price_max": 45000,
        "reliability": 8,
        "comfort": 7,
        "fun": 10,
        "pros": "Motore B58, trazione posteriore, prestazioni forti, grande potenziale.",
        "cons": "Prezzi alti, consumi, gomme posteriori, attenzione ad auto modificate.",
        "ideal": "Appassionati che vogliono una compatta molto potente e divertente.",
        "checks": "Tagliandi, modifiche, turbo, cambio ZF/manuale, gomme, differenziale, incidenti.",
        "mods": "Gomme ottime, freni, manutenzione, assetto di qualita.",
        "avoid": "Stage aggressivi senza controlli, drift, esemplari maltrattati.",
        "verdict": "M140i F20 e una compatta speciale, molto cercata e da verificare bene.",
        "data_quality": "verified"
    }
]

for u in updates:
    cur.execute("""
        UPDATE cars SET
            name=?, model=?, version=?, years=?, fuel=?, car_type=?,
            power=?, torque=?, consumption=?, zero100=?, speed_max=?,
            price_min=?, price_max=?, reliability=?, comfort=?, fun=?,
            pros=?, cons=?, ideal=?, checks=?, mods=?, avoid=?, verdict=?,
            data_quality=?
        WHERE id=?
    """, (
        u["name"], u["model"], u["version"], u["years"], u["fuel"], u["car_type"],
        u["power"], u["torque"], u["consumption"], u["zero100"], u["speed_max"],
        u["price_min"], u["price_max"], u["reliability"], u["comfort"], u["fun"],
        u["pros"], u["cons"], u["ideal"], u["checks"], u["mods"], u["avoid"], u["verdict"],
        u["data_quality"], u["id"]
    ))

conn.commit()
conn.close()

print("Correzioni BMW M applicate.")
