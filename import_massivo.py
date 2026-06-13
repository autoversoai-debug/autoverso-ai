import csv
import sqlite3
from pathlib import Path

DB_PATH = Path("autoverso.db")
CSV_PATH = Path("auto_massive.csv")

COLUMNS = [
    "name", "brand", "model", "version", "years", "fuel", "car_type",
    "power", "torque", "consumption", "zero100", "speed_max",
    "price_min", "price_max", "reliability", "comfort", "fun",
    "pros", "cons", "ideal", "checks", "mods", "avoid", "verdict"
]

if not CSV_PATH.exists():
    with CSV_PATH.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS)
        writer.writeheader()
        writer.writerow({
            "name": "BMW 320d",
            "brand": "BMW",
            "model": "Serie 3",
            "version": "320d",
            "years": "2019-oggi",
            "fuel": "Diesel",
            "car_type": "Berlina premium",
            "power": 190,
            "torque": 400,
            "consumption": 4.8,
            "zero100": 6.8,
            "speed_max": 240,
            "price_min": 25000,
            "price_max": 42000,
            "reliability": 8,
            "comfort": 8,
            "fun": 8,
            "pros": "Ottima per viaggi, consumi bassi, guida piacevole.",
            "cons": "Costi premium, manutenzione non economica.",
            "ideal": "Autostrada, viaggi, uso quotidiano premium.",
            "checks": "Tagliandi, cambio, turbina, DPF, gomme, freni.",
            "mods": "Gomme buone, assetto moderato, estetica sobria.",
            "avoid": "Mappe aggressive, eliminazione DPF, assetti estremi.",
            "verdict": "Ottima berlina diesel se mantenuta bene."
        })

    print("Creato template auto_massive.csv. Compilalo e riesegui questo script.")
    raise SystemExit

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

inserted = 0
skipped = 0
errors = []

with CSV_PATH.open("r", encoding="utf-8-sig", newline="") as f:
    reader = csv.DictReader(f)

    for index, row in enumerate(reader, start=2):
        try:
            name = row.get("name", "").strip()

            if not name:
                skipped += 1
                continue

            exists = cur.execute(
                "SELECT id FROM cars WHERE lower(name) = lower(?)",
                (name,)
            ).fetchone()

            if exists:
                skipped += 1
                continue

            values = []
            for col in COLUMNS:
                value = row.get(col, "")

                if col in [
                    "power", "torque", "speed_max", "price_min", "price_max",
                    "reliability", "comfort", "fun"
                ]:
                    value = int(float(value or 0))

                elif col in ["consumption", "zero100"]:
                    value = float(value or 0)

                else:
                    value = str(value or "").strip()

                values.append(value)

            cur.execute("""
                INSERT INTO cars (
                    name, brand, model, version, years, fuel, car_type,
                    power, torque, consumption, zero100, speed_max,
                    price_min, price_max, reliability, comfort, fun,
                    pros, cons, ideal, checks, mods, avoid, verdict
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, values)

            inserted += 1

        except Exception as e:
            errors.append(f"Riga {index}: {e}")

conn.commit()
conn.close()

print("Import completato")
print("Inserite:", inserted)
print("Saltate:", skipped)
print("Errori:", len(errors))

if errors:
    for error in errors[:20]:
        print(error)
