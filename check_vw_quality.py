import sqlite3

conn = sqlite3.connect("autoverso.db")
cur = conn.cursor()

cur.execute("SELECT COUNT(*) FROM cars WHERE lower(brand)='volkswagen' AND data_quality='verified'")
print("VW VERIFIED:", cur.fetchone()[0])

cur.execute("SELECT COUNT(*) FROM cars WHERE lower(brand)='volkswagen' AND data_quality='legacy_generated'")
print("VW LEGACY:", cur.fetchone()[0])

cur.execute("SELECT COUNT(*) FROM cars WHERE data_quality IN ('verified','premium_verified')")
print("TOTAL VERIFIED:", cur.fetchone()[0])

conn.close()
