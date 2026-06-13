import sqlite3

c=sqlite3.connect("autoverso.db")
c.row_factory=sqlite3.Row

for r in c.execute("""
SELECT id,name,years
FROM cars
WHERE lower(brand)='bmw'
ORDER BY name
"""):
    print(f"{r['id']};{r['name']};{r['years']}")
