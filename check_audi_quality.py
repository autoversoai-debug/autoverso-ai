import sqlite3

conn = sqlite3.connect("autoverso.db")
cur = conn.cursor()

cur.execute("SELECT COUNT(*) FROM cars WHERE lower(brand)='audi' AND data_quality='verified'")
print("AUDI VERIFIED:", cur.fetchone()[0])

cur.execute("SELECT COUNT(*) FROM cars WHERE lower(brand)='audi' AND data_quality='legacy_generated'")
print("AUDI LEGACY:", cur.fetchone()[0])

cur.execute("SELECT COUNT(*) FROM cars")
print("AUTO TOTALI:", cur.fetchone()[0])

conn.close()
