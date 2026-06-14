import sqlite3

conn = sqlite3.connect("autoverso.db")
conn.row_factory = sqlite3.Row

rows = conn.execute("""
SELECT id,name,power,torque,zero100,data_quality
FROM cars
WHERE lower(brand)='audi'
ORDER BY name
""").fetchall()

for r in rows:
    print(f"{r['id']} - {r['name']} - {r['power']} CV - {r['torque']} Nm - 0-100 {r['zero100']} - {r['data_quality']}")

conn.close()
