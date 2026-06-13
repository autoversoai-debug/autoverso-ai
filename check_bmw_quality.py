import sqlite3

conn = sqlite3.connect("autoverso.db")
cur = conn.cursor()

cur.execute("SELECT COUNT(*) FROM cars WHERE lower(brand)='bmw' AND data_quality='verified'")
print("BMW VERIFIED:", cur.fetchone()[0])

cur.execute("SELECT COUNT(*) FROM cars WHERE data_quality='legacy_generated'")
print("LEGACY GENERATED:", cur.fetchone()[0])

cur.execute("SELECT COUNT(*) FROM cars")
print("AUTO TOTALI:", cur.fetchone()[0])

conn.close()
