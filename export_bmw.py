import sqlite3
import csv

conn = sqlite3.connect("autoverso.db")
conn.row_factory = sqlite3.Row

rows = conn.execute("""
SELECT *
FROM cars
WHERE lower(brand)='bmw'
ORDER BY name
""").fetchall()

with open("bmw_review.csv","w",newline="",encoding="utf-8-sig") as f:
    writer = csv.writer(f)

    writer.writerow([
        "id","name","years","power","torque",
        "zero100","speed_max","fuel",
        "data_quality"
    ])

    for r in rows:
        writer.writerow([
            r["id"],
            r["name"],
            r["years"],
            r["power"],
            r["torque"],
            r["zero100"],
            r["speed_max"],
            r["fuel"],
            r["data_quality"]
        ])

print("Creato bmw_review.csv")
