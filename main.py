from fastapi import FastAPI
from fastapi.responses import HTMLResponse, RedirectResponse
from html import escape
import sqlite3
from pathlib import Path

app = FastAPI(title="AutoVerso AI")
DB_PATH = Path("autoverso.db")

SEED_CARS = [
    {
        "name": "Mini Cooper 1.5 136 CV",
        "brand": "Mini",
        "model": "Cooper",
        "version": "1.5 136 CV",
        "years": "2014-oggi",
        "fuel": "Benzina",
        "car_type": "Compatta premium",
        "power": 136,
        "torque": 220,
        "consumption": 5.5,
        "zero100": 7.9,
        "speed_max": 210,
        "price_min": 12000,
        "price_max": 22000,
        "reliability": 8,
        "comfort": 7,
        "fun": 9,
        "pros": "Bella, agile, divertente, interni curati, immagine premium.",
        "cons": "Spazio posteriore limitato, bagagliaio piccolo, costi non bassissimi.",
        "ideal": "Citta, uso quotidiano e guida divertente.",
        "checks": "Tagliandi, frizione, cambio, sospensioni, elettronica, gomme, eventuali perdite.",
        "mods": "Molle sportive moderate, cerchi leggeri, gomme di qualita, scarico omologato.",
        "avoid": "Assetto troppo basso, scarico non omologato, mappa aggressiva, cerchi troppo grandi.",
        "verdict": "Ottima scelta se vuoi una compatta bella, premium e divertente."
    },
    {
        "name": "Fiat Punto 1.3 Multijet",
        "brand": "Fiat",
        "model": "Punto",
        "version": "1.3 Multijet",
        "years": "2003-2018",
        "fuel": "Diesel",
        "car_type": "Utilitaria",
        "power": 95,
        "torque": 200,
        "consumption": 4.2,
        "zero100": 11.7,
        "speed_max": 178,
        "price_min": 2500,
        "price_max": 7500,
        "reliability": 8,
        "comfort": 6,
        "fun": 5,
        "pros": "Consuma poco, ricambi economici, motore molto diffuso.",
        "cons": "Interni semplici, prestazioni tranquille, attenzione a EGR e manutenzione.",
        "ideal": "Casa-lavoro, uso quotidiano economico e lunghi tragitti.",
        "checks": "Km reali, tagliandi, distribuzione, frizione, turbina, EGR, fumo allo scarico.",
        "mods": "Manutenzione completa, gomme buone, freni in ordine, cerchi sobri.",
        "avoid": "Eliminazione FAP, scarico non omologato, rimappa pesante, assetto estremo.",
        "verdict": "Scelta intelligente se vuoi spendere poco e consumare poco."
    },
    {
        "name": "Volkswagen Golf GTI 2.0 TSI",
        "brand": "Volkswagen",
        "model": "Golf",
        "version": "GTI 2.0 TSI",
        "years": "2013-2020",
        "fuel": "Benzina",
        "car_type": "Compatta sportiva",
        "power": 230,
        "torque": 350,
        "consumption": 7.5,
        "zero100": 6.4,
        "speed_max": 248,
        "price_min": 18000,
        "price_max": 32000,
        "reliability": 7,
        "comfort": 8,
        "fun": 9,
        "pros": "Veloce, equilibrata, comoda, qualita alta.",
        "cons": "Costo alto, manutenzione piu cara, attenzione a DSG e tagliandi.",
        "ideal": "Sportiva quotidiana, viaggi, guida brillante.",
        "checks": "Storico tagliandi, cambio DSG, turbina, freni, gomme, eventuali modifiche precedenti.",
        "mods": "Gomme sportive, freni migliori, assetto di qualita, scarico omologato.",
        "avoid": "Mappa senza controlli, preparazioni economiche, assetto estremo su uso quotidiano.",
        "verdict": "Una delle migliori compatte sportive per equilibrio generale."
    },
    {
        "name": "Toyota Yaris Hybrid",
        "brand": "Toyota",
        "model": "Yaris",
        "version": "Hybrid",
        "years": "2012-oggi",
        "fuel": "Ibrida benzina",
        "car_type": "Utilitaria ibrida",
        "power": 116,
        "torque": 120,
        "consumption": 3.8,
        "zero100": 9.7,
        "speed_max": 175,
        "price_min": 11000,
        "price_max": 24000,
        "reliability": 9,
        "comfort": 7,
        "fun": 6,
        "pros": "Affidabile, consuma poco, ottima in citta.",
        "cons": "Poco sportiva, bagagliaio medio, sound poco emozionante.",
        "ideal": "Citta, neopatentati, bassi consumi, affidabilita.",
        "checks": "Tagliandi, batteria ibrida, freni, gomme, stato carrozzeria, uso precedente.",
        "mods": "Gomme efficienti, manutenzione ufficiale, estetica leggera.",
        "avoid": "Scarico sportivo, assetto estremo, modifiche meccaniche pesanti.",
        "verdict": "Perfetta se cerchi risparmio, affidabilita e praticita."
    },
    {
        "name": "Fiat 500 Abarth",
        "brand": "Fiat",
        "model": "500 Abarth",
        "version": "Abarth",
        "years": "2008-oggi",
        "fuel": "Benzina",
        "car_type": "Piccola sportiva",
        "power": 145,
        "torque": 206,
        "consumption": 6.5,
        "zero100": 7.8,
        "speed_max": 210,
        "price_min": 13000,
        "price_max": 25000,
        "reliability": 7,
        "comfort": 5,
        "fun": 9,
        "pros": "Divertente, sound piacevole, estetica forte.",
        "cons": "Rigida, poco spaziosa, costi superiori a una 500 normale.",
        "ideal": "Divertimento, citta, appassionati.",
        "checks": "Modifiche precedenti, frizione, turbina, freni, assetto, gomme, storico tagliandi.",
        "mods": "Scarico omologato, gomme sportive, freni migliori, assetto di qualita.",
        "avoid": "Scarichi non omologati, assetti troppo rigidi, mappe spinte senza controlli.",
        "verdict": "Auto emozionale, perfetta se vuoi divertirti."
    }
]


def db():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    connection = db()
    cur = connection.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS cars (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            brand TEXT NOT NULL,
            model TEXT NOT NULL,
            version TEXT,
            years TEXT,
            fuel TEXT,
            car_type TEXT,
            power INTEGER,
            torque INTEGER,
            consumption REAL,
            zero100 REAL,
            speed_max INTEGER,
            price_min INTEGER,
            price_max INTEGER,
            reliability INTEGER,
            comfort INTEGER,
            fun INTEGER,
            pros TEXT,
            cons TEXT,
            ideal TEXT,
            checks TEXT,
            mods TEXT,
            avoid TEXT,
            verdict TEXT
        )
    """)

    total = cur.execute("SELECT COUNT(*) AS total FROM cars").fetchone()["total"]

    if total == 0:
        for car in SEED_CARS:
            cur.execute("""
                INSERT INTO cars (
                    name, brand, model, version, years, fuel, car_type, power, torque,
                    consumption, zero100, speed_max, price_min, price_max, reliability,
                    comfort, fun, pros, cons, ideal, checks, mods, avoid, verdict
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                car["name"], car["brand"], car["model"], car["version"], car["years"],
                car["fuel"], car["car_type"], car["power"], car["torque"],
                car["consumption"], car["zero100"], car["speed_max"], car["price_min"],
                car["price_max"], car["reliability"], car["comfort"], car["fun"],
                car["pros"], car["cons"], car["ideal"], car["checks"], car["mods"],
                car["avoid"], car["verdict"]
            ))

    connection.commit()
    connection.close()


def all_cars():
    connection = db()
    rows = connection.execute("SELECT * FROM cars ORDER BY brand, model, version").fetchall()
    connection.close()
    return rows


def get_car(car_id):
    connection = db()
    row = connection.execute("SELECT * FROM cars WHERE id = ?", (car_id,)).fetchone()
    connection.close()
    return row


init_db()

STYLE = """
body { margin: 0; font-family: Arial, sans-serif; background: #111318; color: white; }
header { background: #050609; padding: 24px 40px; border-bottom: 1px solid #333; }
header h1 { margin: 0; }
nav { margin-top: 12px; display: flex; gap: 16px; flex-wrap: wrap; }
nav a { color: #ddd; text-decoration: none; }
.hero { padding: 60px 40px; background: linear-gradient(135deg, #151821, #2a2f3d); }
.hero h2 { font-size: 42px; margin: 0 0 12px 0; }
.container { padding: 35px 40px; }
.grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 20px; }
.card { background: #1b1f2a; border: 1px solid #303747; border-radius: 16px; padding: 24px; margin-bottom: 20px; }
.button, button { display: inline-block; padding: 12px 18px; background: #e63946; color: white; text-decoration: none; border-radius: 10px; border: 0; font-weight: bold; cursor: pointer; margin: 4px; }
input, select, textarea { padding: 12px; border-radius: 10px; border: 1px solid #3a4254; background: #0d0f14; color: white; margin: 5px; min-width: 220px; }
textarea { width: 95%; min-height: 70px; }
table { width: 100%; border-collapse: collapse; margin-top: 15px; }
td, th { border-bottom: 1px solid #343b4d; padding: 12px; text-align: left; }
.muted { color: #b7bdc9; }
.number { font-size: 28px; font-weight: bold; color: #64d46e; }
.warning { background: #2a2114; color: #ffd699; border: 1px solid #6d4e1f; border-radius: 12px; padding: 18px; margin-top: 20px; }
"""


def page(title, body):
    return f"""<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <title>{escape(title)}</title>
    <style>{STYLE}</style>
</head>
<body>
    <header>
        <h1>AutoVerso AI</h1>
        <nav>
            <a href="/">Home</a>
            <a href="/auto">Schede auto</a>
            <a href="/cerca">Cerca</a>
            <a href="/confronta?id1=1&id2=2">Confronta</a>
            <a href="/consulente">Consulente</a>
            <a href="/tuning">Tuning</a>
            <a href="/aggiungi">Aggiungi</a>
            <a href="/api/auto">API</a>
        </nav>
    </header>
    {body}
</body>
</html>"""


def card(car):
    return f"""
<div class="card">
    <h3>{escape(car["name"])}</h3>
    <p class="muted">ID {car["id"]} - {escape(car["car_type"] or "")} - {escape(car["fuel"] or "")} - {car["power"]} CV</p>
    <p><strong>Pregi:</strong> {escape(car["pros"] or "")}</p>
    <p><strong>Difetti:</strong> {escape(car["cons"] or "")}</p>
    <a class="button" href="/auto/{car["id"]}">Apri scheda</a>
</div>"""


@app.get("/vecchia_home", response_class=HTMLResponse)
def home_old():
    total = len(all_cars())
    body = f"""
<section class="hero">
    <h2>Trova, confronta e conosci ogni auto.</h2>
    <p>Schede tecniche, prestazioni, consumi, pregi, difetti, consigli di acquisto e modifiche sensate.</p>
    <a class="button" href="/auto">Vai alle schede auto</a>
    <a class="button" href="/aggiungi">Aggiungi auto</a>
</section>
<main class="container">
    <div class="grid">
        <div class="card"><h3>Database reale</h3><p>Auto salvate: <strong>{total}</strong>. I dati restano nel file autoverso.db.</p></div>
        <div class="card"><h3>Confronto</h3><p>Confronta potenza, consumi, prezzo e punteggi.</p></div>
        <div class="card"><h3>Consulente</h3><p>Ricevi un consiglio in base a budget e priorita.</p></div>
        <div class="card"><h3>Tuning responsabile</h3><p>Modifiche consigliate e modifiche da evitare.</p></div>
    </div>
</main>"""
    return page("AutoVerso AI", body)


@app.get("/auto", response_class=HTMLResponse)
def car_list():
    body = '<main class="container"><h2>Schede auto disponibili</h2>'
    for car_row in all_cars():
        body += card(car_row)
    body += "</main>"
    return page("Schede auto", body)


@app.get("/auto/{car_id}", response_class=HTMLResponse)
def car_detail(car_id: int):
    car_row = get_car(car_id)

    if car_row is None:
        return page("Auto non trovata", '<main class="container"><h2>Auto non trovata</h2></main>')

    body = f"""
<main class="container">
    <div class="card">
        <h2>{escape(car_row["name"])}</h2>
        <p class="muted">{escape(car_row["car_type"] or "")} - {escape(car_row["fuel"] or "")} - {escape(car_row["years"] or "")}</p>
        <p>{escape(car_row["verdict"] or "")}</p>
    </div>

    <div class="grid">
        <div class="card"><p>Potenza</p><div class="number">{car_row["power"]} CV</div></div>
        <div class="card"><p>Coppia</p><div class="number">{car_row["torque"]} Nm</div></div>
        <div class="card"><p>Consumo</p><div class="number">{car_row["consumption"]} l/100 km</div></div>
        <div class="card"><p>0-100 km/h</p><div class="number">{car_row["zero100"]} s</div></div>
        <div class="card"><p>Velocita max</p><div class="number">{car_row["speed_max"]} km/h</div></div>
        <div class="card"><p>Prezzo usato</p><div class="number">{car_row["price_min"]} - {car_row["price_max"]} EUR</div></div>
    </div>

    <div class="grid">
        <div class="card"><h3>Affidabilita</h3><div class="number">{car_row["reliability"]}/10</div></div>
        <div class="card"><h3>Comfort</h3><div class="number">{car_row["comfort"]}/10</div></div>
        <div class="card"><h3>Piacere guida</h3><div class="number">{car_row["fun"]}/10</div></div>
    </div>

    <div class="card"><h3>Pregi</h3><p>{escape(car_row["pros"] or "")}</p></div>
    <div class="card"><h3>Difetti</h3><p>{escape(car_row["cons"] or "")}</p></div>
    <div class="card"><h3>Cosa controllare nell'usato</h3><p>{escape(car_row["checks"] or "")}</p></div>
    <div class="card"><h3>Uso ideale</h3><p>{escape(car_row["ideal"] or "")}</p></div>
    <div class="card"><h3>Modifiche consigliate</h3><p>{escape(car_row["mods"] or "")}</p></div>
    <div class="card"><h3>Da evitare</h3><p>{escape(car_row["avoid"] or "")}</p></div>

    <div class="warning">
        Prima di acquistare o modificare un'auto verifica sempre dati tecnici, libretto, omologazione, revisione, assicurazione e normativa vigente.
    </div>
</main>"""
    return page(car_row["name"], body)


@app.get("/cerca", response_class=HTMLResponse)
def search(q: str = ""):
    body = f"""
<main class="container">
    <h2>Cerca auto</h2>
    <form action="/cerca" method="get" class="card">
        <input name="q" value="{escape(q)}" placeholder="es. Mini, Fiat, Golf, diesel">
        <button type="submit">Cerca</button>
    </form>"""

    if q.strip() == "":
        body += '<p class="muted">Scrivi una marca, un modello o una versione.</p>'
    else:
        query = q.lower()
        found = []

        for car_row in all_cars():
            text = f"{car_row['name']} {car_row['brand']} {car_row['model']} {car_row['version']} {car_row['fuel']} {car_row['car_type']}".lower()

            if query in text:
                found.append(car_row)

        if not found:
            body += "<p>Nessuna auto trovata.</p>"
        else:
            for car_row in found:
                body += card(car_row)

    body += "</main>"
    return page("Cerca auto", body)


@app.get("/confronta", response_class=HTMLResponse)
def compare(id1: int = 1, id2: int = 2):
    car1 = get_car(id1)
    car2 = get_car(id2)

    if car1 is None or car2 is None:
        return page("Confronto", '<main class="container"><h2>Una delle due auto non esiste.</h2></main>')

    more_power = car1["name"] if car1["power"] > car2["power"] else car2["name"] if car2["power"] > car1["power"] else "Pareggio"
    less_consumption = car1["name"] if car1["consumption"] < car2["consumption"] else car2["name"] if car2["consumption"] < car1["consumption"] else "Pareggio"
    faster = car1["name"] if car1["zero100"] < car2["zero100"] else car2["name"] if car2["zero100"] < car1["zero100"] else "Pareggio"
    reliable = car1["name"] if car1["reliability"] > car2["reliability"] else car2["name"] if car2["reliability"] > car1["reliability"] else "Pareggio"

    body = f"""
<main class="container">
    <h2>Confronto auto</h2>

    <form action="/confronta" method="get" class="card">
        <input name="id1" value="{id1}" placeholder="ID prima auto">
        <input name="id2" value="{id2}" placeholder="ID seconda auto">
        <button type="submit">Confronta</button>
    </form>

    <table>
        <tr><th>Voce</th><th>{escape(car1["name"])}</th><th>{escape(car2["name"])}</th></tr>
        <tr><td>Tipo</td><td>{escape(car1["car_type"] or "")}</td><td>{escape(car2["car_type"] or "")}</td></tr>
        <tr><td>Alimentazione</td><td>{escape(car1["fuel"] or "")}</td><td>{escape(car2["fuel"] or "")}</td></tr>
        <tr><td>Potenza</td><td>{car1["power"]} CV</td><td>{car2["power"]} CV</td></tr>
        <tr><td>Coppia</td><td>{car1["torque"]} Nm</td><td>{car2["torque"]} Nm</td></tr>
        <tr><td>Consumo</td><td>{car1["consumption"]} l/100 km</td><td>{car2["consumption"]} l/100 km</td></tr>
        <tr><td>0-100</td><td>{car1["zero100"]} s</td><td>{car2["zero100"]} s</td></tr>
        <tr><td>Prezzo</td><td>{car1["price_min"]} - {car1["price_max"]} EUR</td><td>{car2["price_min"]} - {car2["price_max"]} EUR</td></tr>
    </table>

    <div class="grid">
        <div class="card"><h3>Piu potente</h3><p>{escape(more_power)}</p></div>
        <div class="card"><h3>Consuma meno</h3><p>{escape(less_consumption)}</p></div>
        <div class="card"><h3>Piu rapida</h3><p>{escape(faster)}</p></div>
        <div class="card"><h3>Piu affidabile</h3><p>{escape(reliable)}</p></div>
    </div>
</main>"""
    return page("Confronto auto", body)


@app.get("/consulente", response_class=HTMLResponse)
def advisor():
    body = """
<main class="container">
    <h2>Consulente auto</h2>

    <form action="/consiglio" method="get" class="card">
        <input name="budget" type="number" placeholder="Budget massimo, es. 10000">

        <select name="priority">
            <option value="risparmio">Risparmio e consumi bassi</option>
            <option value="sportiva">Piacere di guida</option>
            <option value="affidabilita">Affidabilita</option>
            <option value="comfort">Comfort</option>
        </select>

        <button type="submit">Ricevi consiglio</button>
    </form>
</main>"""
    return page("Consulente auto", body)


@app.get("/consiglio", response_class=HTMLResponse)
def advice(budget: int = 10000, priority: str = "risparmio"):
    available = [car_row for car_row in all_cars() if car_row["price_min"] <= budget]

    if not available:
        return page("Consiglio", '<main class="container"><h2>Nessuna auto trovata con questo budget.</h2></main>')

    if priority == "risparmio":
        chosen = sorted(available, key=lambda x: x["consumption"])[0]
    elif priority == "sportiva":
        chosen = sorted(available, key=lambda x: x["fun"], reverse=True)[0]
    elif priority == "affidabilita":
        chosen = sorted(available, key=lambda x: x["reliability"], reverse=True)[0]
    else:
        chosen = sorted(available, key=lambda x: x["comfort"], reverse=True)[0]

    body = f"""
<main class="container">
    <div class="card">
        <h2>Consiglio per budget {budget} EUR</h2>
        <h3>{escape(chosen["name"])}</h3>
        <p><strong>Uso ideale:</strong> {escape(chosen["ideal"] or "")}</p>
        <p><strong>Pregi:</strong> {escape(chosen["pros"] or "")}</p>
        <p><strong>Difetti:</strong> {escape(chosen["cons"] or "")}</p>
        <a class="button" href="/auto/{chosen["id"]}">Apri scheda completa</a>
    </div>
</main>"""
    return page("Consiglio auto", body)


@app.get("/tuning", response_class=HTMLResponse)
def tuning():
    body = """
<main class="container">
    <h2>Tuning responsabile</h2>

    <div class="grid">
        <div class="card">
            <h3>Molle sportive</h3>
            <p>Migliorano estetica e stabilita, ma possono ridurre il comfort. Verifica compatibilita e omologazione.</p>
        </div>

        <div class="card">
            <h3>Scarico</h3>
            <p>Scegli solo scarichi omologati e non troppo rumorosi. Evita modifiche che creano problemi a revisione e assicurazione.</p>
        </div>

        <div class="card">
            <h3>Cerchi e gomme</h3>
            <p>Controlla misure a libretto. Gomme buone migliorano piu di molte modifiche economiche.</p>
        </div>

        <div class="card">
            <h3>Rimappa</h3>
            <p>Da valutare con molta cautela: puo aumentare prestazioni ma anche stress meccanico e problemi legali.</p>
        </div>
    </div>

    <div class="warning">
        AutoVerso AI non invita a effettuare modifiche illegali, pericolose o non omologate.
    </div>
</main>"""
    return page("Tuning", body)


@app.get("/aggiungi", response_class=HTMLResponse)
def add_form():
    body = """
<main class="container">
    <h2>Aggiungi nuova auto</h2>

    <form action="/salva_auto" method="get" class="card">
        <input name="name" placeholder="Nome completo">
        <input name="brand" placeholder="Marca">
        <input name="model" placeholder="Modello">
        <input name="version" placeholder="Versione">
        <input name="years" placeholder="Anni produzione">
        <input name="fuel" placeholder="Alimentazione">
        <input name="car_type" placeholder="Tipo auto">

        <input name="power" type="number" placeholder="Potenza CV">
        <input name="torque" type="number" placeholder="Coppia Nm">
        <input name="consumption" type="number" step="0.1" placeholder="Consumo l/100 km">
        <input name="zero100" type="number" step="0.1" placeholder="0-100 km/h">
        <input name="speed_max" type="number" placeholder="Velocita max km/h">

        <input name="price_min" type="number" placeholder="Prezzo minimo EUR">
        <input name="price_max" type="number" placeholder="Prezzo massimo EUR">

        <input name="reliability" type="number" placeholder="Affidabilita 1-10">
        <input name="comfort" type="number" placeholder="Comfort 1-10">
        <input name="fun" type="number" placeholder="Piacere guida 1-10">

        <textarea name="pros" placeholder="Pregi"></textarea>
        <textarea name="cons" placeholder="Difetti"></textarea>
        <textarea name="ideal" placeholder="Uso ideale"></textarea>
        <textarea name="checks" placeholder="Cosa controllare nell'usato"></textarea>
        <textarea name="mods" placeholder="Modifiche consigliate"></textarea>
        <textarea name="avoid" placeholder="Da evitare"></textarea>
        <textarea name="verdict" placeholder="Verdetto finale"></textarea>

        <br>
        <button type="submit">Salva auto nel database</button>
    </form>
</main>"""
    return page("Aggiungi auto", body)


@app.get("/salva_auto")
def save_car(
    name: str = "Nuova auto",
    brand: str = "Marca",
    model: str = "Modello",
    version: str = "",
    years: str = "",
    fuel: str = "",
    car_type: str = "",
    power: int = 0,
    torque: int = 0,
    consumption: float = 0,
    zero100: float = 0,
    speed_max: int = 0,
    price_min: int = 0,
    price_max: int = 0,
    reliability: int = 5,
    comfort: int = 5,
    fun: int = 5,
    pros: str = "",
    cons: str = "",
    ideal: str = "",
    checks: str = "",
    mods: str = "",
    avoid: str = "",
    verdict: str = ""
):
    connection = db()

    connection.execute("""
        INSERT INTO cars (
            name, brand, model, version, years, fuel, car_type, power, torque,
            consumption, zero100, speed_max, price_min, price_max, reliability,
            comfort, fun, pros, cons, ideal, checks, mods, avoid, verdict
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        name, brand, model, version, years, fuel, car_type, power, torque,
        consumption, zero100, speed_max, price_min, price_max, reliability,
        comfort, fun, pros, cons, ideal, checks, mods, avoid, verdict
    ))

    connection.commit()
    connection.close()

    return RedirectResponse(url="/auto", status_code=302)


@app.get("/api/auto")
def api_cars():
    return [dict(car_row) for car_row in all_cars()]

from fastapi import File, UploadFile
from fastapi.responses import Response


CSV_COLUMNS = [
    "name",
    "brand",
    "model",
    "version",
    "years",
    "fuel",
    "car_type",
    "power",
    "torque",
    "consumption",
    "zero100",
    "speed_max",
    "price_min",
    "price_max",
    "reliability",
    "comfort",
    "fun",
    "pros",
    "cons",
    "ideal",
    "checks",
    "mods",
    "avoid",
    "verdict"
]


@app.get("/csv", response_class=HTMLResponse)
def csv_page():
    body = """
<main class="container">
    <h2>Importa auto da CSV</h2>

    <div class="card">
        <p>Usa questa sezione per caricare molte auto nel database senza inserirle una per una.</p>

        <a class="button" href="/template_csv">Scarica template CSV</a>
        <a class="button" href="/esporta_csv">Esporta database CSV</a>
    </div>

    <form action="/importa_csv" method="post" enctype="multipart/form-data" class="card">
        <h3>Carica file CSV</h3>
        <input type="file" name="file" accept=".csv">
        <br><br>
        <button type="submit">Importa nel database</button>
    </form>

    <div class="warning">
        Consiglio: scarica prima il template CSV, compilalo con Excel o Google Sheets, poi ricaricalo qui.
    </div>
</main>
"""
    return page("Importa CSV", body)


@app.get("/template_csv")
def template_csv():
    header = ",".join(CSV_COLUMNS)

    example = [
        "Audi A1 1.4 TFSI",
        "Audi",
        "A1",
        "1.4 TFSI",
        "2010-2018",
        "Benzina",
        "Compatta premium",
        "122",
        "200",
        "5.8",
        "8.9",
        "203",
        "8000",
        "16000",
        "7",
        "8",
        "7",
        "Buona qualita, compatta, piacevole da guidare",
        "Prezzi usato non sempre bassi, spazio limitato",
        "Uso quotidiano, citta, guida tranquilla",
        "Tagliandi, cambio, frizione, elettronica, gomme",
        "Cerchi leggeri, gomme buone, assetto moderato",
        "Assetto estremo, scarico non omologato, mappa aggressiva",
        "Buona scelta se vuoi una compatta premium usata"
    ]

    row = ",".join('"' + str(x).replace('"', '""') + '"' for x in example)

    csv_text = header + "\n" + row + "\n"

    return Response(
        content=csv_text,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=template_autoverso.csv"}
    )


@app.get("/esporta_csv")
def export_csv():
    lines = []
    lines.append(",".join(CSV_COLUMNS))

    for car_row in all_cars():
        values = []

        for col in CSV_COLUMNS:
            value = car_row[col]
            if value is None:
                value = ""
            value = str(value).replace('"', '""')
            values.append('"' + value + '"')

        lines.append(",".join(values))

    csv_text = "\n".join(lines)

    return Response(
        content=csv_text,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=database_autoverso.csv"}
    )


@app.post("/importa_csv", response_class=HTMLResponse)
async def import_csv(file: UploadFile = File(...)):
    import csv
    import io

    content = await file.read()
    text = content.decode("utf-8-sig")
    reader = csv.DictReader(io.StringIO(text))

    imported = 0
    errors = []

    connection = db()

    for index, row in enumerate(reader, start=2):
        try:
            data = {}

            for col in CSV_COLUMNS:
                data[col] = row.get(col, "")

            connection.execute("""
                INSERT INTO cars (
                    name, brand, model, version, years, fuel, car_type, power, torque,
                    consumption, zero100, speed_max, price_min, price_max, reliability,
                    comfort, fun, pros, cons, ideal, checks, mods, avoid, verdict
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                data["name"],
                data["brand"],
                data["model"],
                data["version"],
                data["years"],
                data["fuel"],
                data["car_type"],
                int(data["power"] or 0),
                int(data["torque"] or 0),
                float(data["consumption"] or 0),
                float(data["zero100"] or 0),
                int(data["speed_max"] or 0),
                int(data["price_min"] or 0),
                int(data["price_max"] or 0),
                int(data["reliability"] or 5),
                int(data["comfort"] or 5),
                int(data["fun"] or 5),
                data["pros"],
                data["cons"],
                data["ideal"],
                data["checks"],
                data["mods"],
                data["avoid"],
                data["verdict"]
            ))

            imported += 1

        except Exception as e:
            errors.append(f"Riga {index}: {str(e)}")

    connection.commit()
    connection.close()

    error_html = ""

    if errors:
        error_html = "<div class='card'><h3>Errori</h3><ul>"
        for err in errors:
            error_html += f"<li>{escape(err)}</li>"
        error_html += "</ul></div>"

    body = f"""
<main class="container">
    <div class="card">
        <h2>Importazione completata</h2>
        <p>Auto importate: <strong>{imported}</strong></p>
        <a class="button" href="/auto">Vai alle schede auto</a>
        <a class="button" href="/csv">Torna alla pagina CSV</a>
    </div>

    {error_html}
</main>
"""

    return page("Import CSV completato", body)

from fastapi.responses import FileResponse


def safe_value(row, key):
    value = row[key]
    if value is None:
        return ""
    return str(value)


@app.get("/admin", response_class=HTMLResponse)
def admin_panel():
    rows = all_cars()

    table_rows = ""

    for car_row in rows:
        table_rows += f"""
        <tr>
            <td>{car_row["id"]}</td>
            <td>{escape(car_row["brand"] or "")}</td>
            <td>{escape(car_row["model"] or "")}</td>
            <td>{escape(car_row["version"] or "")}</td>
            <td>{car_row["power"]} CV</td>
            <td>{car_row["price_min"]} - {car_row["price_max"]} EUR</td>
            <td>
                <a class="button" href="/auto/{car_row["id"]}">Apri</a>
                <a class="button" href="/modifica/{car_row["id"]}">Modifica</a>
                <a class="button" href="/elimina/{car_row["id"]}">Elimina</a>
            </td>
        </tr>
        """

    body = f"""
<main class="container">
    <h2>Pannello gestione auto</h2>

    <div class="grid">
        <div class="card">
            <h3>Auto nel database</h3>
            <div class="number">{len(rows)}</div>
        </div>

        <div class="card">
            <h3>Azioni rapide</h3>
            <a class="button" href="/aggiungi">Aggiungi auto</a>
            <a class="button" href="/csv">Importa CSV</a>
            <a class="button" href="/backup_db">Backup database</a>
        </div>
    </div>

    <div class="card">
        <h3>Lista auto</h3>
        <table>
            <tr>
                <th>ID</th>
                <th>Marca</th>
                <th>Modello</th>
                <th>Versione</th>
                <th>Potenza</th>
                <th>Prezzo</th>
                <th>Azioni</th>
            </tr>
            {table_rows}
        </table>
    </div>
</main>
"""
    return page("Admin AutoVerso AI", body)


@app.get("/modifica/{car_id}", response_class=HTMLResponse)
def edit_car_form(car_id: int):
    car_row = get_car(car_id)

    if car_row is None:
        return page("Auto non trovata", '<main class="container"><h2>Auto non trovata</h2></main>')

    body = f"""
<main class="container">
    <h2>Modifica auto</h2>

    <form action="/aggiorna_auto" method="get" class="card">
        <input name="car_id" type="hidden" value="{car_row["id"]}">

        <input name="name" value="{escape(safe_value(car_row, "name"))}" placeholder="Nome completo">
        <input name="brand" value="{escape(safe_value(car_row, "brand"))}" placeholder="Marca">
        <input name="model" value="{escape(safe_value(car_row, "model"))}" placeholder="Modello">
        <input name="version" value="{escape(safe_value(car_row, "version"))}" placeholder="Versione">
        <input name="years" value="{escape(safe_value(car_row, "years"))}" placeholder="Anni produzione">
        <input name="fuel" value="{escape(safe_value(car_row, "fuel"))}" placeholder="Alimentazione">
        <input name="car_type" value="{escape(safe_value(car_row, "car_type"))}" placeholder="Tipo auto">

        <input name="power" type="number" value="{car_row["power"]}" placeholder="Potenza CV">
        <input name="torque" type="number" value="{car_row["torque"]}" placeholder="Coppia Nm">
        <input name="consumption" type="number" step="0.1" value="{car_row["consumption"]}" placeholder="Consumo l/100 km">
        <input name="zero100" type="number" step="0.1" value="{car_row["zero100"]}" placeholder="0-100 km/h">
        <input name="speed_max" type="number" value="{car_row["speed_max"]}" placeholder="Velocita max km/h">

        <input name="price_min" type="number" value="{car_row["price_min"]}" placeholder="Prezzo minimo EUR">
        <input name="price_max" type="number" value="{car_row["price_max"]}" placeholder="Prezzo massimo EUR">

        <input name="reliability" type="number" value="{car_row["reliability"]}" placeholder="Affidabilita 1-10">
        <input name="comfort" type="number" value="{car_row["comfort"]}" placeholder="Comfort 1-10">
        <input name="fun" type="number" value="{car_row["fun"]}" placeholder="Piacere guida 1-10">

        <textarea name="pros" placeholder="Pregi">{escape(safe_value(car_row, "pros"))}</textarea>
        <textarea name="cons" placeholder="Difetti">{escape(safe_value(car_row, "cons"))}</textarea>
        <textarea name="ideal" placeholder="Uso ideale">{escape(safe_value(car_row, "ideal"))}</textarea>
        <textarea name="checks" placeholder="Cosa controllare nell'usato">{escape(safe_value(car_row, "checks"))}</textarea>
        <textarea name="mods" placeholder="Modifiche consigliate">{escape(safe_value(car_row, "mods"))}</textarea>
        <textarea name="avoid" placeholder="Da evitare">{escape(safe_value(car_row, "avoid"))}</textarea>
        <textarea name="verdict" placeholder="Verdetto finale">{escape(safe_value(car_row, "verdict"))}</textarea>

        <br>
        <button type="submit">Salva modifiche</button>
        <a class="button" href="/admin">Annulla</a>
    </form>
</main>
"""
    return page("Modifica auto", body)


@app.get("/aggiorna_auto")
def update_car(
    car_id: int,
    name: str = "",
    brand: str = "",
    model: str = "",
    version: str = "",
    years: str = "",
    fuel: str = "",
    car_type: str = "",
    power: int = 0,
    torque: int = 0,
    consumption: float = 0,
    zero100: float = 0,
    speed_max: int = 0,
    price_min: int = 0,
    price_max: int = 0,
    reliability: int = 5,
    comfort: int = 5,
    fun: int = 5,
    pros: str = "",
    cons: str = "",
    ideal: str = "",
    checks: str = "",
    mods: str = "",
    avoid: str = "",
    verdict: str = ""
):
    connection = db()

    connection.execute("""
        UPDATE cars SET
            name = ?,
            brand = ?,
            model = ?,
            version = ?,
            years = ?,
            fuel = ?,
            car_type = ?,
            power = ?,
            torque = ?,
            consumption = ?,
            zero100 = ?,
            speed_max = ?,
            price_min = ?,
            price_max = ?,
            reliability = ?,
            comfort = ?,
            fun = ?,
            pros = ?,
            cons = ?,
            ideal = ?,
            checks = ?,
            mods = ?,
            avoid = ?,
            verdict = ?
        WHERE id = ?
    """, (
        name, brand, model, version, years, fuel, car_type, power, torque,
        consumption, zero100, speed_max, price_min, price_max, reliability,
        comfort, fun, pros, cons, ideal, checks, mods, avoid, verdict, car_id
    ))

    connection.commit()
    connection.close()

    return RedirectResponse(url=f"/auto/{car_id}", status_code=302)


@app.get("/elimina/{car_id}", response_class=HTMLResponse)
def delete_confirm(car_id: int):
    car_row = get_car(car_id)

    if car_row is None:
        return page("Auto non trovata", '<main class="container"><h2>Auto non trovata</h2></main>')

    body = f"""
<main class="container">
    <div class="card">
        <h2>Conferma eliminazione</h2>
        <p>Stai per eliminare questa auto:</p>
        <h3>{escape(car_row["name"])}</h3>

        <div class="warning">
            Attenzione: questa azione elimina la scheda dal database.
        </div>

        <br>
        <a class="button" href="/conferma_elimina/{car_row["id"]}">Si, elimina</a>
        <a class="button" href="/admin">No, torna indietro</a>
    </div>
</main>
"""
    return page("Elimina auto", body)


@app.get("/conferma_elimina/{car_id}")
def delete_car(car_id: int):
    connection = db()
    connection.execute("DELETE FROM cars WHERE id = ?", (car_id,))
    connection.commit()
    connection.close()

    return RedirectResponse(url="/admin", status_code=302)


@app.get("/backup_db")
def backup_database():
    return FileResponse(
        path="autoverso.db",
        filename="backup_autoverso.db",
        media_type="application/octet-stream"
    )


@app.get("/statistiche", response_class=HTMLResponse)
def stats():
    rows = all_cars()

    total = len(rows)

    if total == 0:
        return page("Statistiche", '<main class="container"><h2>Nessuna auto nel database.</h2></main>')

    avg_power = round(sum([row["power"] for row in rows]) / total, 1)
    avg_consumption = round(sum([row["consumption"] for row in rows]) / total, 1)
    avg_price = round(sum([(row["price_min"] + row["price_max"]) / 2 for row in rows]) / total, 0)

    brands = {}

    for row in rows:
        brand = row["brand"] or "Sconosciuta"
        brands[brand] = brands.get(brand, 0) + 1

    brand_rows = ""

    for brand, count in sorted(brands.items()):
        brand_rows += f"<tr><td>{escape(brand)}</td><td>{count}</td></tr>"

    body = f"""
<main class="container">
    <h2>Statistiche database</h2>

    <div class="grid">
        <div class="card"><h3>Auto totali</h3><div class="number">{total}</div></div>
        <div class="card"><h3>Potenza media</h3><div class="number">{avg_power} CV</div></div>
        <div class="card"><h3>Consumo medio</h3><div class="number">{avg_consumption} l/100 km</div></div>
        <div class="card"><h3>Prezzo medio</h3><div class="number">{int(avg_price)} EUR</div></div>
    </div>

    <div class="card">
        <h3>Auto per marca</h3>
        <table>
            <tr><th>Marca</th><th>Numero auto</th></tr>
            {brand_rows}
        </table>
    </div>
</main>
"""
    return page("Statistiche", body)

@app.get("/filtri", response_class=HTMLResponse)
def advanced_filters(
    q: str = "",
    fuel: str = "",
    car_type: str = "",
    max_price: int = 0,
    min_power: int = 0,
    min_reliability: int = 0,
    sort: str = "name"
):
    rows = all_cars()
    results = []

    for row in rows:
        ok = True

        text = f"{row['name']} {row['brand']} {row['model']} {row['version']} {row['fuel']} {row['car_type']}".lower()

        if q.strip() != "" and q.lower() not in text:
            ok = False

        if fuel.strip() != "" and fuel.lower() not in str(row["fuel"]).lower():
            ok = False

        if car_type.strip() != "" and car_type.lower() not in str(row["car_type"]).lower():
            ok = False

        if max_price > 0 and row["price_min"] > max_price:
            ok = False

        if min_power > 0 and row["power"] < min_power:
            ok = False

        if min_reliability > 0 and row["reliability"] < min_reliability:
            ok = False

        if ok:
            results.append(row)

    if sort == "price":
        results = sorted(results, key=lambda x: x["price_min"])
    elif sort == "power":
        results = sorted(results, key=lambda x: x["power"], reverse=True)
    elif sort == "consumption":
        results = sorted(results, key=lambda x: x["consumption"])
    elif sort == "reliability":
        results = sorted(results, key=lambda x: x["reliability"], reverse=True)
    elif sort == "fun":
        results = sorted(results, key=lambda x: x["fun"], reverse=True)
    else:
        results = sorted(results, key=lambda x: x["name"])

    cards = ""

    if len(results) == 0:
        cards = "<p>Nessuna auto trovata con questi filtri.</p>"
    else:
        for row in results:
            cards += card(row)

    body = f"""
<main class="container">
    <h2>Filtri avanzati</h2>

    <form action="/filtri" method="get" class="card">
        <input name="q" value="{escape(q)}" placeholder="Cerca marca, modello o versione">

        <input name="fuel" value="{escape(fuel)}" placeholder="Alimentazione: Benzina, Diesel, Ibrida">

        <input name="car_type" value="{escape(car_type)}" placeholder="Tipo: Utilitaria, Sportiva, SUV">

        <input name="max_price" type="number" value="{max_price}" placeholder="Budget massimo EUR">

        <input name="min_power" type="number" value="{min_power}" placeholder="Potenza minima CV">

        <input name="min_reliability" type="number" value="{min_reliability}" placeholder="Affidabilita minima 1-10">

        <select name="sort">
            <option value="name">Ordina per nome</option>
            <option value="price">Prezzo piu basso</option>
            <option value="power">Potenza piu alta</option>
            <option value="consumption">Consumi piu bassi</option>
            <option value="reliability">Affidabilita piu alta</option>
            <option value="fun">Piacere di guida piu alto</option>
        </select>

        <br><br>
        <button type="submit">Applica filtri</button>
    </form>

    <div class="card">
        <h3>Risultati trovati: {len(results)}</h3>
    </div>

    {cards}
</main>
"""
    return page("Filtri avanzati", body)


@app.get("/classifiche", response_class=HTMLResponse)
def rankings():
    rows = all_cars()

    best_consumption = sorted(rows, key=lambda x: x["consumption"])[:5]
    best_power = sorted(rows, key=lambda x: x["power"], reverse=True)[:5]
    best_reliability = sorted(rows, key=lambda x: x["reliability"], reverse=True)[:5]
    best_fun = sorted(rows, key=lambda x: x["fun"], reverse=True)[:5]
    cheapest = sorted(rows, key=lambda x: x["price_min"])[:5]

    def mini_table(title, data, field, suffix):
        html = f"<div class='card'><h3>{title}</h3><table>"
        html += "<tr><th>Auto</th><th>Valore</th><th>Scheda</th></tr>"

        for row in data:
            html += f"""
            <tr>
                <td>{escape(row["name"])}</td>
                <td>{row[field]} {suffix}</td>
                <td><a class="button" href="/auto/{row["id"]}">Apri</a></td>
            </tr>
            """

        html += "</table></div>"
        return html

    body = """
<main class="container">
    <h2>Classifiche AutoVerso AI</h2>
    <p class="muted">Classifiche generate automaticamente dal database.</p>
"""

    body += mini_table("Auto che consumano meno", best_consumption, "consumption", "l/100 km")
    body += mini_table("Auto piu potenti", best_power, "power", "CV")
    body += mini_table("Auto piu affidabili", best_reliability, "reliability", "/10")
    body += mini_table("Auto piu divertenti", best_fun, "fun", "/10")
    body += mini_table("Auto piu economiche", cheapest, "price_min", "EUR")

    body += "</main>"

    return page("Classifiche", body)

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard():
    body = """
<main class="container">
    <h2>Dashboard AutoVerso AI</h2>
    <p class="muted">Centro di controllo del progetto.</p>

    <div class="grid">
        <div class="card">
            <h3>Schede auto</h3>
            <p>Visualizza tutte le auto presenti nel database.</p>
            <a class="button" href="/auto">Apri schede</a>
        </div>

        <div class="card">
            <h3>Filtri avanzati</h3>
            <p>Cerca auto per budget, alimentazione, potenza e affidabilita.</p>
            <a class="button" href="/filtri">Apri filtri</a>
        </div>

        <div class="card">
            <h3>Classifiche</h3>
            <p>Scopri auto piu economiche, affidabili, potenti e divertenti.</p>
            <a class="button" href="/classifiche">Apri classifiche</a>
        </div>

        <div class="card">
            <h3>Confronto auto</h3>
            <p>Confronta due auto tramite ID.</p>
            <a class="button" href="/confronta?id1=1&id2=2">Apri confronto</a>
        </div>

        <div class="card">
            <h3>Consulente auto</h3>
            <p>Ricevi un consiglio in base a budget e priorita.</p>
            <a class="button" href="/consulente">Apri consulente</a>
        </div>

        <div class="card">
            <h3>Tuning</h3>
            <p>Sezione dedicata a modifiche responsabili.</p>
            <a class="button" href="/tuning">Apri tuning</a>
        </div>

        <div class="card">
            <h3>Import CSV</h3>
            <p>Importa molte auto da file CSV.</p>
            <a class="button" href="/csv">Apri CSV</a>
        </div>

        <div class="card">
            <h3>Admin</h3>
            <p>Modifica, elimina e gestisci le auto.</p>
            <a class="button" href="/admin">Apri admin</a>
        </div>

        <div class="card">
            <h3>Statistiche</h3>
            <p>Vedi statistiche base del database.</p>
            <a class="button" href="/statistiche">Apri statistiche</a>
        </div>

        <div class="card">
            <h3>Aggiungi auto</h3>
            <p>Inserisci manualmente una nuova scheda.</p>
            <a class="button" href="/aggiungi">Aggiungi</a>
        </div>
    </div>
</main>
"""
    return page("Dashboard AutoVerso AI", body)


@app.get("/report/{car_id}", response_class=HTMLResponse)
def car_report(car_id: int):
    car_row = get_car(car_id)

    if car_row is None:
        return page("Report non trovato", '<main class="container"><h2>Auto non trovata</h2></main>')

    score = 0

    score += int(car_row["reliability"] or 0) * 2
    score += int(car_row["comfort"] or 0)
    score += int(car_row["fun"] or 0)

    if car_row["consumption"] <= 4.5:
        score += 10
    elif car_row["consumption"] <= 6.5:
        score += 7
    else:
        score += 4

    if car_row["price_min"] <= 8000:
        score += 10
    elif car_row["price_min"] <= 15000:
        score += 7
    else:
        score += 4

    if score >= 45:
        final_label = "Molto consigliata"
    elif score >= 35:
        final_label = "Consigliata con controlli"
    elif score >= 25:
        final_label = "Da valutare con attenzione"
    else:
        final_label = "Consigliata solo se il prezzo e molto conveniente"

    body = f"""
<main class="container">
    <div class="card">
        <h2>Report acquisto: {escape(car_row["name"])}</h2>
        <p class="muted">Report pratico per valutare acquisto, usato e modifiche sensate.</p>
        <div class="number">{escape(final_label)}</div>
    </div>

    <div class="grid">
        <div class="card">
            <h3>Dati principali</h3>
            <table>
                <tr><td>Marca</td><td>{escape(car_row["brand"] or "")}</td></tr>
                <tr><td>Modello</td><td>{escape(car_row["model"] or "")}</td></tr>
                <tr><td>Versione</td><td>{escape(car_row["version"] or "")}</td></tr>
                <tr><td>Anni</td><td>{escape(car_row["years"] or "")}</td></tr>
                <tr><td>Alimentazione</td><td>{escape(car_row["fuel"] or "")}</td></tr>
                <tr><td>Tipo</td><td>{escape(car_row["car_type"] or "")}</td></tr>
            </table>
        </div>

        <div class="card">
            <h3>Prestazioni e costi</h3>
            <table>
                <tr><td>Potenza</td><td>{car_row["power"]} CV</td></tr>
                <tr><td>Coppia</td><td>{car_row["torque"]} Nm</td></tr>
                <tr><td>0-100 km/h</td><td>{car_row["zero100"]} s</td></tr>
                <tr><td>Velocita massima</td><td>{car_row["speed_max"]} km/h</td></tr>
                <tr><td>Consumo</td><td>{car_row["consumption"]} l/100 km</td></tr>
                <tr><td>Prezzo usato</td><td>{car_row["price_min"]} - {car_row["price_max"]} EUR</td></tr>
            </table>
        </div>
    </div>

    <div class="grid">
        <div class="card"><h3>Affidabilita</h3><div class="number">{car_row["reliability"]}/10</div></div>
        <div class="card"><h3>Comfort</h3><div class="number">{car_row["comfort"]}/10</div></div>
        <div class="card"><h3>Piacere guida</h3><div class="number">{car_row["fun"]}/10</div></div>
        <div class="card"><h3>Punteggio report</h3><div class="number">{score}/50</div></div>
    </div>

    <div class="card">
        <h3>Perche comprarla</h3>
        <p>{escape(car_row["pros"] or "")}</p>
    </div>

    <div class="card">
        <h3>Perche evitarla o fare attenzione</h3>
        <p>{escape(car_row["cons"] or "")}</p>
    </div>

    <div class="card">
        <h3>Cosa controllare prima dell'acquisto</h3>
        <p>{escape(car_row["checks"] or "")}</p>
    </div>

    <div class="card">
        <h3>Uso ideale</h3>
        <p>{escape(car_row["ideal"] or "")}</p>
    </div>

    <div class="card">
        <h3>Modifiche consigliate</h3>
        <p>{escape(car_row["mods"] or "")}</p>
    </div>

    <div class="card">
        <h3>Modifiche da evitare</h3>
        <p>{escape(car_row["avoid"] or "")}</p>
    </div>

    <div class="warning">
        Questo report e indicativo. Prima di acquistare o modificare un'auto verifica sempre documenti, libretto, storico manutenzione, omologazione, revisione e assicurazione.
    </div>

    <br>
    <a class="button" href="/auto/{car_row["id"]}">Torna alla scheda</a>
    <a class="button" href="/confronta?id1={car_row["id"]}&id2=1">Confronta questa auto</a>
</main>
"""
    return page("Report acquisto", body)


@app.get("/report", response_class=HTMLResponse)
def report_list():
    body = '<main class="container"><h2>Report acquisto disponibili</h2>'

    for car_row in all_cars():
        body += f"""
        <div class="card">
            <h3>{escape(car_row["name"])}</h3>
            <p class="muted">{escape(car_row["car_type"] or "")} - {escape(car_row["fuel"] or "")} - {car_row["price_min"]} / {car_row["price_max"]} EUR</p>
            <a class="button" href="/report/{car_row["id"]}">Apri report</a>
            <a class="button" href="/auto/{car_row["id"]}">Apri scheda</a>
        </div>
        """

    body += "</main>"
    return page("Report acquisto", body)


@app.get("/", response_class=HTMLResponse)
def home_new():
    cars = all_cars()
    total = len(cars)

    if total > 0:
        avg_power = round(sum([car["power"] for car in cars]) / total, 1)
        avg_consumption = round(sum([car["consumption"] for car in cars]) / total, 1)
        cheapest = sorted(cars, key=lambda x: x["price_min"])[0]
        most_fun = sorted(cars, key=lambda x: x["fun"], reverse=True)[0]
        most_reliable = sorted(cars, key=lambda x: x["reliability"], reverse=True)[0]
    else:
        avg_power = 0
        avg_consumption = 0
        cheapest = None
        most_fun = None
        most_reliable = None

    def quick_car_box(title, car_row):
        if car_row is None:
            return "<div class='card'><h3>Nessuna auto</h3><p>Database vuoto.</p></div>"

        return f"""
        <div class="card">
            <h3>{escape(title)}</h3>
            <p><strong>{escape(car_row["name"])}</strong></p>
            <p class="muted">{escape(car_row["fuel"] or "")} - {car_row["power"]} CV - {car_row["price_min"]} / {car_row["price_max"]} EUR</p>
            <a class="button" href="/auto/{car_row["id"]}">Apri scheda</a>
            <a class="button" href="/report/{car_row["id"]}">Report</a>
        </div>
        """

    body = f"""
<section class="hero">
    <h2>La guida intelligente per scegliere, confrontare e migliorare la tua auto.</h2>
    <p>
        AutoVerso AI raccoglie schede tecniche, prestazioni, consumi, pregi, difetti,
        consigli di acquisto, confronti, report e modifiche responsabili.
    </p>

    <a class="button" href="/dashboard">Apri dashboard</a>
    <a class="button" href="/filtri">Trova auto</a>
    <a class="button" href="/confronta?id1=1&id2=2">Confronta</a>
    <a class="button" href="/report">Report acquisto</a>
</section>

<main class="container">

    <div class="grid">
        <div class="card">
            <h3>Auto nel database</h3>
            <div class="number">{total}</div>
            <p class="muted">Schede salvate nel database SQLite.</p>
        </div>

        <div class="card">
            <h3>Potenza media</h3>
            <div class="number">{avg_power} CV</div>
            <p class="muted">Calcolata sulle auto presenti.</p>
        </div>

        <div class="card">
            <h3>Consumo medio</h3>
            <div class="number">{avg_consumption} l/100 km</div>
            <p class="muted">Valore indicativo del database.</p>
        </div>

        <div class="card">
            <h3>Modalita sprint</h3>
            <div class="number">MVP</div>
            <p class="muted">Obiettivo: pubblicare velocemente una prima versione.</p>
        </div>
    </div>

    <div class="card">
        <h2>Cerca subito un'auto</h2>
        <form action="/filtri" method="get">
            <input name="q" placeholder="Cerca marca, modello o versione">
            <input name="max_price" type="number" placeholder="Budget massimo EUR">
            <input name="min_power" type="number" placeholder="Potenza minima CV">

            <select name="sort">
                <option value="price">Prezzo piu basso</option>
                <option value="reliability">Affidabilita piu alta</option>
                <option value="consumption">Consumi piu bassi</option>
                <option value="power">Potenza piu alta</option>
                <option value="fun">Piacere guida piu alto</option>
            </select>

            <button type="submit">Cerca</button>
        </form>
    </div>

    <h2>Scorciatoie principali</h2>

    <div class="grid">
        <div class="card">
            <h3>Schede auto</h3>
            <p>Consulta tutte le auto presenti nel database.</p>
            <a class="button" href="/auto">Apri schede</a>
        </div>

        <div class="card">
            <h3>Filtri avanzati</h3>
            <p>Trova auto per budget, alimentazione, potenza e affidabilita.</p>
            <a class="button" href="/filtri">Apri filtri</a>
        </div>

        <div class="card">
            <h3>Confronto</h3>
            <p>Confronta due auto tramite ID.</p>
            <a class="button" href="/confronta?id1=1&id2=2">Apri confronto</a>
        </div>

        <div class="card">
            <h3>Report acquisto</h3>
            <p>Genera una scheda pratica per valutare un acquisto usato.</p>
            <a class="button" href="/report">Apri report</a>
        </div>

        <div class="card">
            <h3>Classifiche</h3>
            <p>Vedi auto piu economiche, potenti, affidabili e divertenti.</p>
            <a class="button" href="/classifiche">Apri classifiche</a>
        </div>

        <div class="card">
            <h3>Consulente</h3>
            <p>Ricevi un consiglio in base a budget e priorita.</p>
            <a class="button" href="/consulente">Apri consulente</a>
        </div>

        <div class="card">
            <h3>Tuning responsabile</h3>
            <p>Consigli su molle, scarichi, cerchi, gomme e modifiche da evitare.</p>
            <a class="button" href="/tuning">Apri tuning</a>
        </div>

        <div class="card">
            <h3>Admin</h3>
            <p>Gestisci, modifica, elimina e fai backup delle schede auto.</p>
            <a class="button" href="/admin">Apri admin</a>
        </div>

        <div class="card">
            <h3>CSV</h3>
            <p>Importa o esporta tante auto velocemente.</p>
            <a class="button" href="/csv">Apri CSV</a>
        </div>

        <div class="card">
            <h3>Aggiungi auto</h3>
            <p>Inserisci manualmente una nuova scheda nel database.</p>
            <a class="button" href="/aggiungi">Aggiungi</a>
        </div>

        <div class="card">
            <h3>Statistiche</h3>
            <p>Controlla numeri, medie e distribuzione marche.</p>
            <a class="button" href="/statistiche">Apri statistiche</a>
        </div>

        <div class="card">
            <h3>Backup</h3>
            <p>Scarica una copia del database.</p>
            <a class="button" href="/backup_db">Scarica backup</a>
        </div>
    </div>

    <h2>Auto evidenziate</h2>

    <div class="grid">
        {quick_car_box("Piu economica", cheapest)}
        {quick_car_box("Piu divertente", most_fun)}
        {quick_car_box("Piu affidabile", most_reliable)}
    </div>

    <div class="warning">
        I dati sono indicativi. Prima di acquistare o modificare un'auto verifica sempre documenti, libretto,
        storico manutenzione, omologazione, revisione, assicurazione e normativa vigente.
    </div>

</main>
"""
    return page("AutoVerso AI", body)


@app.get("/menu", response_class=HTMLResponse)
def full_menu():
    body = """
<main class="container">
    <h2>Menu completo AutoVerso AI</h2>

    <div class="grid">
        <div class="card"><h3>Home</h3><a class="button" href="/">Apri</a></div>
        <div class="card"><h3>Dashboard</h3><a class="button" href="/dashboard">Apri</a></div>
        <div class="card"><h3>Schede auto</h3><a class="button" href="/auto">Apri</a></div>
        <div class="card"><h3>Cerca</h3><a class="button" href="/cerca">Apri</a></div>
        <div class="card"><h3>Filtri</h3><a class="button" href="/filtri">Apri</a></div>
        <div class="card"><h3>Classifiche</h3><a class="button" href="/classifiche">Apri</a></div>
        <div class="card"><h3>Confronto</h3><a class="button" href="/confronta?id1=1&id2=2">Apri</a></div>
        <div class="card"><h3>Consulente</h3><a class="button" href="/consulente">Apri</a></div>
        <div class="card"><h3>Report</h3><a class="button" href="/report">Apri</a></div>
        <div class="card"><h3>Tuning</h3><a class="button" href="/tuning">Apri</a></div>
        <div class="card"><h3>CSV</h3><a class="button" href="/csv">Apri</a></div>
        <div class="card"><h3>Admin</h3><a class="button" href="/admin">Apri</a></div>
        <div class="card"><h3>Statistiche</h3><a class="button" href="/statistiche">Apri</a></div>
        <div class="card"><h3>Aggiungi</h3><a class="button" href="/aggiungi">Apri</a></div>
        <div class="card"><h3>API</h3><a class="button" href="/api/auto">Apri</a></div>
        <div class="card"><h3>Documentazione tecnica</h3><a class="button" href="/docs">Apri</a></div>
    </div>
</main>
"""
    return page("Menu completo", body)

def report_score(car_row):
    score = 0

    score += int(car_row["reliability"] or 0) * 2
    score += int(car_row["comfort"] or 0)
    score += int(car_row["fun"] or 0)

    if car_row["consumption"] <= 4.5:
        score += 10
    elif car_row["consumption"] <= 6.5:
        score += 7
    else:
        score += 4

    if car_row["price_min"] <= 8000:
        score += 10
    elif car_row["price_min"] <= 15000:
        score += 7
    else:
        score += 4

    if score >= 45:
        label = "Molto consigliata"
    elif score >= 35:
        label = "Consigliata con controlli"
    elif score >= 25:
        label = "Da valutare con attenzione"
    else:
        label = "Solo se il prezzo e molto conveniente"

    return score, label


def pro_card(car_row):
    score, label = report_score(car_row)

    return f"""
    <div class="card">
        <h3>{escape(car_row["name"])}</h3>

        <p class="muted">
            ID {car_row["id"]} - {escape(car_row["brand"] or "")} - {escape(car_row["fuel"] or "")} -
            {escape(car_row["car_type"] or "")}
        </p>

        <div class="grid">
            <div><strong>{car_row["power"]} CV</strong><br><span class="muted">Potenza</span></div>
            <div><strong>{car_row["consumption"]} l/100 km</strong><br><span class="muted">Consumo</span></div>
            <div><strong>{car_row["zero100"]} s</strong><br><span class="muted">0-100 km/h</span></div>
            <div><strong>{car_row["price_min"]} - {car_row["price_max"]} EUR</strong><br><span class="muted">Prezzo usato</span></div>
        </div>

        <p><strong>Verdetto rapido:</strong> {escape(label)} - punteggio {score}/50</p>
        <p><strong>Pregi:</strong> {escape(car_row["pros"] or "")}</p>
        <p><strong>Difetti:</strong> {escape(car_row["cons"] or "")}</p>

        <a class="button" href="/scheda/{car_row["id"]}">Scheda PRO</a>
        <a class="button" href="/report/{car_row["id"]}">Report</a>
        <a class="button" href="/confronta?id1={car_row["id"]}&id2=1">Confronta</a>
        <a class="button" href="/modifica/{car_row["id"]}">Modifica</a>
    </div>
    """


@app.get("/schede", response_class=HTMLResponse)
def pro_cards_list():
    rows = all_cars()

    body = f"""
<main class="container">
    <h2>Schede AutoVerso AI PRO</h2>
    <p class="muted">Versione piu completa e leggibile delle schede auto. Auto nel database: {len(rows)}</p>

    <div class="card">
        <form action="/schede" method="get">
            <a class="button" href="/filtri">Filtri avanzati</a>
            <a class="button" href="/classifiche">Classifiche</a>
            <a class="button" href="/report">Report acquisto</a>
            <a class="button" href="/admin">Admin</a>
        </form>
    </div>
"""

    for car_row in rows:
        body += pro_card(car_row)

    body += "</main>"

    return page("Schede PRO", body)


@app.get("/scheda/{car_id}", response_class=HTMLResponse)
def pro_car_detail(car_id: int):
    car_row = get_car(car_id)

    if car_row is None:
        return page("Scheda non trovata", '<main class="container"><h2>Auto non trovata</h2></main>')

    score, label = report_score(car_row)

    body = f"""
<main class="container">

    <div class="card">
        <h2>{escape(car_row["name"])}</h2>
        <p class="muted">
            {escape(car_row["brand"] or "")} - {escape(car_row["model"] or "")} -
            {escape(car_row["version"] or "")} - {escape(car_row["years"] or "")}
        </p>

        <div class="number">{escape(label)}</div>
        <p>Punteggio AutoVerso AI: <strong>{score}/50</strong></p>

        <a class="button" href="/report/{car_row["id"]}">Apri report acquisto</a>
        <a class="button" href="/confronta?id1={car_row["id"]}&id2=1">Confronta</a>
        <a class="button" href="/modifica/{car_row["id"]}">Modifica</a>
        <a class="button" href="/schede">Torna alle schede</a>
    </div>

    <div class="grid">
        <div class="card"><h3>Potenza</h3><div class="number">{car_row["power"]} CV</div></div>
        <div class="card"><h3>Coppia</h3><div class="number">{car_row["torque"]} Nm</div></div>
        <div class="card"><h3>Consumo</h3><div class="number">{car_row["consumption"]} l/100 km</div></div>
        <div class="card"><h3>0-100 km/h</h3><div class="number">{car_row["zero100"]} s</div></div>
        <div class="card"><h3>Velocita max</h3><div class="number">{car_row["speed_max"]} km/h</div></div>
        <div class="card"><h3>Prezzo usato</h3><div class="number">{car_row["price_min"]} - {car_row["price_max"]} EUR</div></div>
    </div>

    <div class="grid">
        <div class="card"><h3>Affidabilita</h3><div class="number">{car_row["reliability"]}/10</div></div>
        <div class="card"><h3>Comfort</h3><div class="number">{car_row["comfort"]}/10</div></div>
        <div class="card"><h3>Piacere guida</h3><div class="number">{car_row["fun"]}/10</div></div>
    </div>

    <div class="card">
        <h3>Descrizione rapida</h3>
        <p>{escape(car_row["verdict"] or "")}</p>
    </div>

    <div class="grid">
        <div class="card">
            <h3>Perche comprarla</h3>
            <p>{escape(car_row["pros"] or "")}</p>
        </div>

        <div class="card">
            <h3>Perche fare attenzione</h3>
            <p>{escape(car_row["cons"] or "")}</p>
        </div>
    </div>

    <div class="card">
        <h3>Cosa controllare prima di comprarla usata</h3>
        <p>{escape(car_row["checks"] or "")}</p>
    </div>

    <div class="card">
        <h3>Uso ideale</h3>
        <p>{escape(car_row["ideal"] or "")}</p>
    </div>

    <div class="grid">
        <div class="card">
            <h3>Modifiche consigliate</h3>
            <p>{escape(car_row["mods"] or "")}</p>
        </div>

        <div class="card">
            <h3>Modifiche da evitare</h3>
            <p>{escape(car_row["avoid"] or "")}</p>
        </div>
    </div>

    <div class="warning">
        I dati sono indicativi. Prima di acquistare o modificare l'auto verifica sempre documenti,
        libretto, storico manutenzione, compatibilita, omologazione, revisione e assicurazione.
    </div>

</main>
"""
    return page("Scheda PRO", body)

def guide_card(car_row):
    return f"""
    <div class="card">
        <h3>{escape(car_row["name"])}</h3>
        <p class="muted">
            Guida acquisto, problemi comuni, consumi, difetti e modifiche consigliate.
        </p>
        <a class="button" href="/guida/{car_row["id"]}">Apri guida SEO</a>
        <a class="button" href="/scheda/{car_row["id"]}">Scheda PRO</a>
        <a class="button" href="/report/{car_row["id"]}">Report</a>
    </div>
    """


@app.get("/guide", response_class=HTMLResponse)
def guide_index():
    rows = all_cars()

    body = f"""
<main class="container">
    <h2>Guide acquisto AutoVerso AI</h2>
    <p class="muted">
        Guide automatiche per valutare auto usate, problemi comuni, consumi, difetti,
        costi indicativi e modifiche responsabili. Guide disponibili: {len(rows)}.
    </p>

    <div class="grid">
        <div class="card">
            <h3>Guida auto usata</h3>
            <p>Regole generali per controllare un'auto prima dell'acquisto.</p>
            <a class="button" href="/guida-usato">Apri guida</a>
        </div>

        <div class="card">
            <h3>Auto per neopatentati</h3>
            <p>Consigli pratici per scegliere una prima auto economica e sensata.</p>
            <a class="button" href="/guida-neopatentati">Apri guida</a>
        </div>

        <div class="card">
            <h3>Tuning leggero</h3>
            <p>Molle, scarichi, gomme, cerchi e modifiche da valutare con attenzione.</p>
            <a class="button" href="/guida-tuning">Apri guida</a>
        </div>
    </div>

    <h2>Guide per modello</h2>
"""

    for car_row in rows:
        body += guide_card(car_row)

    body += "</main>"

    return page("Guide acquisto", body)


@app.get("/guida/{car_id}", response_class=HTMLResponse)
def seo_car_guide(car_id: int):
    car_row = get_car(car_id)

    if car_row is None:
        return page("Guida non trovata", '<main class="container"><h2>Auto non trovata</h2></main>')

    score, label = report_score(car_row)

    if car_row["consumption"] <= 4.5:
        consumo_text = "molto interessante per chi cerca consumi bassi"
    elif car_row["consumption"] <= 6.5:
        consumo_text = "equilibrata nei consumi per la categoria"
    else:
        consumo_text = "piu orientata a prestazioni o piacere di guida che al risparmio"

    if car_row["price_min"] <= 8000:
        prezzo_text = "puo essere interessante per budget contenuti"
    elif car_row["price_min"] <= 15000:
        prezzo_text = "si posiziona in una fascia di prezzo media"
    else:
        prezzo_text = "richiede un budget piu alto e va scelta con attenzione"

    if car_row["fun"] >= 8:
        guida_text = "piacevole e divertente da guidare"
    elif car_row["comfort"] >= 8:
        guida_text = "piu orientata al comfort che alla sportivita"
    else:
        guida_text = "adatta soprattutto a un uso razionale e quotidiano"

    body = f"""
<main class="container">

    <div class="card">
        <h1>{escape(car_row["name"])}: problemi, consumi, difetti e consigli usato</h1>
        <p class="muted">
            Guida pratica AutoVerso AI per capire se conviene comprare questa auto usata,
            cosa controllare e quali modifiche valutare.
        </p>

        <a class="button" href="/scheda/{car_row["id"]}">Scheda PRO</a>
        <a class="button" href="/report/{car_row["id"]}">Report acquisto</a>
        <a class="button" href="/confronta?id1={car_row["id"]}&id2=1">Confronta</a>
    </div>

    <div class="card">
        <h2>Conviene comprare {escape(car_row["name"])} usata?</h2>
        <p>
            La {escape(car_row["name"])} e una {escape(car_row["car_type"] or "auto")} con alimentazione
            {escape(car_row["fuel"] or "")}. In base ai dati presenti nel database AutoVerso AI,
            questa auto risulta: <strong>{escape(label)}</strong>.
        </p>
        <p>
            Il punteggio complessivo e <strong>{score}/50</strong>. Questo valore considera
            affidabilita, comfort, piacere di guida, consumi e fascia di prezzo.
        </p>
        <p>
            In sintesi, e una scelta {escape(consumo_text)} e {escape(prezzo_text)}.
            Dal punto di vista della guida, risulta {escape(guida_text)}.
        </p>
    </div>

    <div class="grid">
        <div class="card">
            <h2>Dati principali</h2>
            <table>
                <tr><td>Marca</td><td>{escape(car_row["brand"] or "")}</td></tr>
                <tr><td>Modello</td><td>{escape(car_row["model"] or "")}</td></tr>
                <tr><td>Versione</td><td>{escape(car_row["version"] or "")}</td></tr>
                <tr><td>Anni</td><td>{escape(car_row["years"] or "")}</td></tr>
                <tr><td>Alimentazione</td><td>{escape(car_row["fuel"] or "")}</td></tr>
                <tr><td>Tipo auto</td><td>{escape(car_row["car_type"] or "")}</td></tr>
            </table>
        </div>

        <div class="card">
            <h2>Prestazioni e consumi</h2>
            <table>
                <tr><td>Potenza</td><td>{car_row["power"]} CV</td></tr>
                <tr><td>Coppia</td><td>{car_row["torque"]} Nm</td></tr>
                <tr><td>0-100 km/h</td><td>{car_row["zero100"]} s</td></tr>
                <tr><td>Velocita massima</td><td>{car_row["speed_max"]} km/h</td></tr>
                <tr><td>Consumo indicativo</td><td>{car_row["consumption"]} l/100 km</td></tr>
                <tr><td>Prezzo usato</td><td>{car_row["price_min"]} - {car_row["price_max"]} EUR</td></tr>
            </table>
        </div>
    </div>

    <div class="card">
        <h2>Pregi principali</h2>
        <p>{escape(car_row["pros"] or "")}</p>
    </div>

    <div class="card">
        <h2>Difetti e problemi da valutare</h2>
        <p>{escape(car_row["cons"] or "")}</p>
    </div>

    <div class="card">
        <h2>Cosa controllare prima dell'acquisto</h2>
        <p>{escape(car_row["checks"] or "")}</p>
        <p>
            Prima di comprare un esemplare usato e consigliabile verificare sempre storico tagliandi,
            eventuali incidenti, stato gomme, freni, frizione, elettronica e coerenza dei chilometri.
        </p>
    </div>

    <div class="card">
        <h2>Per chi e adatta</h2>
        <p>{escape(car_row["ideal"] or "")}</p>
    </div>

    <div class="grid">
        <div class="card">
            <h2>Modifiche consigliate</h2>
            <p>{escape(car_row["mods"] or "")}</p>
        </div>

        <div class="card">
            <h2>Modifiche da evitare</h2>
            <p>{escape(car_row["avoid"] or "")}</p>
        </div>
    </div>

    <div class="card">
        <h2>Verdetto finale</h2>
        <p>{escape(car_row["verdict"] or "")}</p>
        <p>
            Se il prezzo e corretto, la manutenzione e documentata e l'esemplare non presenta problemi evidenti,
            questa auto puo essere una scelta interessante nella sua categoria.
        </p>
    </div>

    <div class="warning">
        Guida indicativa. I dati possono variare in base ad anno, mercato, cambio, allestimento e condizioni reali.
        Prima di acquistare o modificare un'auto verifica sempre libretto, documenti, storico manutenzione,
        omologazione, revisione e assicurazione.
    </div>

</main>
"""
    return page(f"Guida {car_row['name']}", body)


@app.get("/guida-usato", response_class=HTMLResponse)
def used_car_guide():
    body = """
<main class="container">
    <h1>Come scegliere un'auto usata</h1>

    <div class="card">
        <h2>1. Parti dal budget reale</h2>
        <p>Non guardare solo il prezzo di acquisto. Considera passaggio, assicurazione, bollo, tagliando, gomme e possibili lavori iniziali.</p>
    </div>

    <div class="card">
        <h2>2. Controlla manutenzione e chilometri</h2>
        <p>Uno storico tagliandi chiaro vale piu di una macchina lucida ma senza documenti. Controlla fatture, revisioni e coerenza del chilometraggio.</p>
    </div>

    <div class="card">
        <h2>3. Guarda motore, cambio e frizione</h2>
        <p>Rumori strani, vibrazioni, fumo allo scarico, slittamento frizione o cambi automatici bruschi possono indicare spese importanti.</p>
    </div>

    <div class="card">
        <h2>4. Non sottovalutare gomme e freni</h2>
        <p>Gomme consumate, dischi rovinati e ammortizzatori stanchi possono aumentare subito il costo reale dell'auto.</p>
    </div>

    <div class="card">
        <h2>5. Evita auto troppo modificate</h2>
        <p>Modifiche non documentate, scarichi non omologati e rimappe aggressive possono creare problemi di affidabilita, revisione e assicurazione.</p>
    </div>

    <div class="warning">
        Prima di acquistare, fai controllare l'auto da un meccanico o da una persona competente.
    </div>
</main>
"""
    return page("Guida auto usata", body)


@app.get("/guida-neopatentati", response_class=HTMLResponse)
def beginner_guide():
    body = """
<main class="container">
    <h1>Auto per neopatentati: guida semplice</h1>

    <div class="card">
        <h2>Obiettivo</h2>
        <p>Una buona prima auto deve essere economica, affidabile, facile da guidare e non troppo costosa da mantenere.</p>
    </div>

    <div class="card">
        <h2>Cosa valutare</h2>
        <p>Consumi, assicurazione, bollo, gomme, manutenzione, visibilita, dimensioni e facilita di parcheggio.</p>
    </div>

    <div class="card">
        <h2>Auto sensate</h2>
        <p>City car e utilitarie come Panda, 500, Ypsilon, Corsa, Polo, Fiesta, Clio e Yaris possono essere scelte interessanti in base a budget e versione.</p>
    </div>

    <div class="card">
        <h2>Cosa evitare</h2>
        <p>Auto molto potenti, costose da mantenere, troppo modificate o con manutenzione incerta.</p>
    </div>

    <div class="warning">
        Verifica sempre i limiti di legge per neopatentati in base alla normativa vigente e ai dati riportati sul libretto.
    </div>
</main>
"""
    return page("Guida neopatentati", body)


@app.get("/guida-tuning", response_class=HTMLResponse)
def tuning_guide():
    body = """
<main class="container">
    <h1>Tuning leggero: cosa sapere prima di modificare un'auto</h1>

    <div class="card">
        <h2>Molle sportive</h2>
        <p>Possono migliorare estetica e stabilita, ma riducono il comfort. Scegli prodotti compatibili e verifica sempre omologazione.</p>
    </div>

    <div class="card">
        <h2>Scarico</h2>
        <p>Uno scarico omologato puo migliorare il sound. Evita scarichi troppo rumorosi o non omologati.</p>
    </div>

    <div class="card">
        <h2>Cerchi e gomme</h2>
        <p>Controlla sempre le misure a libretto. Gomme di qualita migliorano sicurezza e guida piu di molte modifiche economiche.</p>
    </div>

    <div class="card">
        <h2>Rimappatura</h2>
        <p>Puo aumentare prestazioni, ma anche stress meccanico. Da valutare solo con professionisti seri e senza compromettere affidabilita e legalita.</p>
    </div>

    <div class="warning">
        AutoVerso AI non invita a effettuare modifiche illegali, pericolose o non omologate.
    </div>
</main>
"""
    return page("Guida tuning", body)

from fastapi.responses import Response as AutoVersoResponse

@app.get("/health")
def health_check_autoverso():
    return {
        "status": "ok",
        "project": "AutoVerso AI",
        "database": "autoverso.db",
        "cars": len(all_cars())
    }


@app.get("/robots.txt")
def robots_txt_autoverso():
    return AutoVersoResponse(
        content="User-agent: *`nAllow: /`nSitemap: http://127.0.0.1:8000/sitemap.xml`n",
        media_type="text/plain"
    )


@app.get("/sitemap.xml")
def sitemap_xml_autoverso():
    base_url = "http://127.0.0.1:8000"

    urls = [
        "/",
        "/auto",
        "/schede",
        "/guide",
        "/filtri",
        "/classifiche",
        "/report",
        "/tuning",
        "/privacy",
        "/termini",
        "/disclaimer"
    ]

    for car_row in all_cars():
        urls.append(f"/auto/{car_row['id']}")
        urls.append(f"/scheda/{car_row['id']}")
        urls.append(f"/report/{car_row['id']}")
        urls.append(f"/guida/{car_row['id']}")

    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'

    for url in urls:
        xml += "  <url>\n"
        xml += f"    <loc>{base_url}{url}</loc>\n"
        xml += "  </url>\n"

    xml += "</urlset>"

    return AutoVersoResponse(content=xml, media_type="application/xml")

import re


def make_slug(text):
    text = text.lower()
    text = text.replace("+", " plus ")
    text = text.replace("&", " e ")
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = text.strip("-")
    return text


def find_car_by_slug(slug):
    for car_row in all_cars():
        if make_slug(car_row["name"]) == slug:
            return car_row
    return None


@app.get("/s/{slug}", response_class=HTMLResponse)
def seo_slug_page(slug: str):
    car_row = find_car_by_slug(slug)

    if car_row is None:
        return page("Scheda non trovata", '<main class="container"><h2>Auto non trovata</h2><a class="button" href="/schede">Torna alle schede</a></main>')

    return seo_car_guide(car_row["id"])


@app.get("/url-seo", response_class=HTMLResponse)
def seo_url_list():
    body = """
<main class="container">
    <h2>URL SEO AutoVerso AI</h2>
    <p class="muted">Lista delle pagine ottimizzate per Google.</p>
"""

    for car_row in all_cars():
        slug = make_slug(car_row["name"])
        body += f"""
        <div class="card">
            <h3>{escape(car_row["name"])}</h3>
            <p class="muted">/s/{slug}</p>
            <a class="button" href="/s/{slug}">Apri URL SEO</a>
            <a class="button" href="/scheda/{car_row["id"]}">Scheda PRO</a>
        </div>
        """

    body += "</main>"
    return page("URL SEO", body)


@app.get("/sitemap-seo.xml")
def sitemap_seo_xml():
    base_url = "https://autoverso-ai.onrender.com"

    urls = [
        "/",
        "/schede",
        "/guide",
        "/filtri",
        "/classifiche",
        "/report",
        "/tuning",
        "/privacy",
        "/termini",
        "/disclaimer"
    ]

    for car_row in all_cars():
        slug = make_slug(car_row["name"])
        urls.append(f"/s/{slug}")
        urls.append(f"/scheda/{car_row['id']}")
        urls.append(f"/report/{car_row['id']}")
        urls.append(f"/guida/{car_row['id']}")

    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'

    for url in urls:
        xml += "  <url>\n"
        xml += f"    <loc>{base_url}{url}</loc>\n"
        xml += "  </url>\n"

    xml += "</urlset>"

    return AutoVersoResponse(content=xml, media_type="application/xml")


def brand_slug(text):
    return make_slug(text)


def brand_list():
    brands = {}

    for car_row in all_cars():
        brand = car_row["brand"] or "Sconosciuta"
        brands[brand] = brands.get(brand, 0) + 1

    return sorted(brands.items(), key=lambda x: x[0].lower())


@app.get("/marche", response_class=HTMLResponse)
def brands_page():
    brands = brand_list()

    body = f"""
<main class="container">
    <h2>Marche auto</h2>
    <p class="muted">Esplora le auto presenti nel database AutoVerso AI divise per marca. Marche disponibili: {len(brands)}.</p>

    <div class="grid">
"""

    for brand, count in brands:
        slug = brand_slug(brand)

        body += f"""
        <div class="card">
            <h3>{escape(brand)}</h3>
            <div class="number">{count}</div>
            <p class="muted">Auto presenti nel database</p>
            <a class="button" href="/marca/{slug}">Apri marca</a>
        </div>
        """

    body += """
    </div>
</main>
"""
    return page("Marche auto", body)


@app.get("/marca/{slug}", response_class=HTMLResponse)
def brand_detail(slug: str):
    rows = []

    brand_name = None

    for car_row in all_cars():
        if brand_slug(car_row["brand"] or "") == slug:
            rows.append(car_row)
            brand_name = car_row["brand"]

    if not rows:
        return page("Marca non trovata", '<main class="container"><h2>Marca non trovata</h2><a class="button" href="/marche">Torna alle marche</a></main>')

    avg_power = round(sum([row["power"] for row in rows]) / len(rows), 1)
    avg_consumption = round(sum([row["consumption"] for row in rows]) / len(rows), 1)
    avg_price = round(sum([(row["price_min"] + row["price_max"]) / 2 for row in rows]) / len(rows), 0)

    most_powerful = sorted(rows, key=lambda x: x["power"], reverse=True)[0]
    cheapest = sorted(rows, key=lambda x: x["price_min"])[0]
    most_reliable = sorted(rows, key=lambda x: x["reliability"], reverse=True)[0]

    body = f"""
<main class="container">

    <div class="card">
        <h1>{escape(brand_name)}</h1>
        <p class="muted">Pagina marca AutoVerso AI con schede, report, guide e confronti.</p>

        <a class="button" href="/marche">Tutte le marche</a>
        <a class="button" href="/filtri?q={escape(brand_name)}">Filtra {escape(brand_name)}</a>
        <a class="button" href="/classifiche">Classifiche</a>
    </div>

    <div class="grid">
        <div class="card"><h3>Auto presenti</h3><div class="number">{len(rows)}</div></div>
        <div class="card"><h3>Potenza media</h3><div class="number">{avg_power} CV</div></div>
        <div class="card"><h3>Consumo medio</h3><div class="number">{avg_consumption} l/100 km</div></div>
        <div class="card"><h3>Prezzo medio</h3><div class="number">{int(avg_price)} EUR</div></div>
    </div>

    <h2>Auto evidenziate {escape(brand_name)}</h2>

    <div class="grid">
        <div class="card">
            <h3>Piu potente</h3>
            <p>{escape(most_powerful["name"])}</p>
            <p class="muted">{most_powerful["power"]} CV</p>
            <a class="button" href="/scheda/{most_powerful["id"]}">Apri scheda</a>
        </div>

        <div class="card">
            <h3>Piu economica</h3>
            <p>{escape(cheapest["name"])}</p>
            <p class="muted">Da {cheapest["price_min"]} EUR</p>
            <a class="button" href="/scheda/{cheapest["id"]}">Apri scheda</a>
        </div>

        <div class="card">
            <h3>Piu affidabile</h3>
            <p>{escape(most_reliable["name"])}</p>
            <p class="muted">{most_reliable["reliability"]}/10</p>
            <a class="button" href="/scheda/{most_reliable["id"]}">Apri scheda</a>
        </div>
    </div>

    <h2>Tutte le auto {escape(brand_name)}</h2>
"""

    for car_row in rows:
        body += pro_card(car_row)

    body += """
</main>
"""
    return page(f"Marca {brand_name}", body)


@app.get("/classifica-marche", response_class=HTMLResponse)
def brand_ranking():
    brands = brand_list()

    rows_html = ""

    for brand, count in sorted(brands, key=lambda x: x[1], reverse=True):
        rows_html += f"""
        <tr>
            <td>{escape(brand)}</td>
            <td>{count}</td>
            <td><a class="button" href="/marca/{brand_slug(brand)}">Apri</a></td>
        </tr>
        """

    body = f"""
<main class="container">
    <h2>Classifica marche</h2>
    <p class="muted">Marche ordinate per numero di auto presenti nel database.</p>

    <div class="card">
        <table>
            <tr>
                <th>Marca</th>
                <th>Auto presenti</th>
                <th>Pagina</th>
            </tr>
            {rows_html}
        </table>
    </div>
</main>
"""
    return page("Classifica marche", body)


@app.get("/sitemap-marche.xml")
def sitemap_brands_xml():
    base_url = "https://autoverso-ai.onrender.com"

    urls = ["/marche", "/classifica-marche"]

    for brand, count in brand_list():
        urls.append(f"/marca/{brand_slug(brand)}")

    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'

    for url in urls:
        xml += "  <url>\n"
        xml += f"    <loc>{base_url}{url}</loc>\n"
        xml += "  </url>\n"

    xml += "</urlset>"

    return AutoVersoResponse(content=xml, media_type="application/xml")


def model_key(car_row):
    brand = car_row["brand"] or "Sconosciuta"
    model = car_row["model"] or "Modello"
    return brand, model


def model_slug(brand, model):
    return make_slug(f"{brand} {model}")


def model_list():
    models = {}

    for car_row in all_cars():
        brand, model = model_key(car_row)
        key = (brand, model)
        models[key] = models.get(key, 0) + 1

    return sorted(models.items(), key=lambda x: (x[0][0].lower(), x[0][1].lower()))


@app.get("/modelli", response_class=HTMLResponse)
def models_page():
    models = model_list()

    body = f"""
<main class="container">
    <h2>Modelli auto</h2>
    <p class="muted">Esplora il database AutoVerso AI diviso per marca e modello. Modelli disponibili: {len(models)}.</p>

    <div class="grid">
"""

    for (brand, model), count in models:
        slug = model_slug(brand, model)

        body += f"""
        <div class="card">
            <h3>{escape(brand)} {escape(model)}</h3>
            <div class="number">{count}</div>
            <p class="muted">Versioni presenti nel database</p>
            <a class="button" href="/modello/{slug}">Apri modello</a>
            <a class="button" href="/marca/{brand_slug(brand)}">Marca</a>
        </div>
        """

    body += """
    </div>
</main>
"""
    return page("Modelli auto", body)


@app.get("/modello/{slug}", response_class=HTMLResponse)
def model_detail(slug: str):
    rows = []
    model_brand = None
    model_name = None

    for car_row in all_cars():
        brand, model = model_key(car_row)

        if model_slug(brand, model) == slug:
            rows.append(car_row)
            model_brand = brand
            model_name = model

    if not rows:
        return page("Modello non trovato", '<main class="container"><h2>Modello non trovato</h2><a class="button" href="/modelli">Torna ai modelli</a></main>')

    avg_power = round(sum([row["power"] for row in rows]) / len(rows), 1)
    avg_consumption = round(sum([row["consumption"] for row in rows]) / len(rows), 1)
    avg_price = round(sum([(row["price_min"] + row["price_max"]) / 2 for row in rows]) / len(rows), 0)

    most_powerful = sorted(rows, key=lambda x: x["power"], reverse=True)[0]
    cheapest = sorted(rows, key=lambda x: x["price_min"])[0]
    best_consumption = sorted(rows, key=lambda x: x["consumption"])[0]

    body = f"""
<main class="container">

    <div class="card">
        <h1>{escape(model_brand)} {escape(model_name)}</h1>
        <p class="muted">Pagina modello con versioni, schede, report e confronti.</p>

        <a class="button" href="/modelli">Tutti i modelli</a>
        <a class="button" href="/marca/{brand_slug(model_brand)}">Vai alla marca</a>
        <a class="button" href="/filtri?q={escape(model_brand)} {escape(model_name)}">Filtra modello</a>
    </div>

    <div class="grid">
        <div class="card"><h3>Versioni presenti</h3><div class="number">{len(rows)}</div></div>
        <div class="card"><h3>Potenza media</h3><div class="number">{avg_power} CV</div></div>
        <div class="card"><h3>Consumo medio</h3><div class="number">{avg_consumption} l/100 km</div></div>
        <div class="card"><h3>Prezzo medio</h3><div class="number">{int(avg_price)} EUR</div></div>
    </div>

    <h2>Versioni evidenziate</h2>

    <div class="grid">
        <div class="card">
            <h3>Piu potente</h3>
            <p>{escape(most_powerful["name"])}</p>
            <p class="muted">{most_powerful["power"]} CV</p>
            <a class="button" href="/scheda/{most_powerful["id"]}">Apri scheda</a>
        </div>

        <div class="card">
            <h3>Piu economica</h3>
            <p>{escape(cheapest["name"])}</p>
            <p class="muted">Da {cheapest["price_min"]} EUR</p>
            <a class="button" href="/scheda/{cheapest["id"]}">Apri scheda</a>
        </div>

        <div class="card">
            <h3>Consuma meno</h3>
            <p>{escape(best_consumption["name"])}</p>
            <p class="muted">{best_consumption["consumption"]} l/100 km</p>
            <a class="button" href="/scheda/{best_consumption["id"]}">Apri scheda</a>
        </div>
    </div>

    <h2>Tutte le versioni {escape(model_brand)} {escape(model_name)}</h2>
"""

    for car_row in rows:
        body += pro_card(car_row)

    body += """
</main>
"""
    return page(f"Modello {model_brand} {model_name}", body)


@app.get("/sitemap-modelli.xml")
def sitemap_models_xml():
    base_url = "https://autoverso-ai.onrender.com"

    urls = ["/modelli"]

    for (brand, model), count in model_list():
        urls.append(f"/modello/{model_slug(brand, model)}")

    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'

    for url in urls:
        xml += "  <url>\n"
        xml += f"    <loc>{base_url}{url}</loc>\n"
        xml += "  </url>\n"

    xml += "</urlset>"

    return AutoVersoResponse(content=xml, media_type="application/xml")

@app.get("/verify", response_class=HTMLResponse)
def verify_page():
    rows = all_cars()

    html = """
<main class="container">
    <h1>Verifica Database</h1>

    <div class="card">
        <p>Controllo qualità schede auto. Le auto generate automaticamente devono essere verificate prima di considerarle affidabili.</p>
    </div>
"""

    for car in rows:
        quality = car["data_quality"] if "data_quality" in car.keys() else "generated"

        color = "#e74c3c"

        if quality == "verified":
            color = "#f39c12"

        if quality == "premium_verified":
            color = "#27ae60"

        html += f"""
<div class="card">
    <h3>{escape(car["name"])}</h3>

    <p>
        Stato:
        <span style="background:{color}; color:white; padding:4px 8px; border-radius:8px;">
            {escape(quality)}
        </span>
    </p>

    <p>
        {car["power"]} CV |
        {car["torque"]} Nm |
        0-100 {car["zero100"]} s |
        {car["price_min"]} - {car["price_max"]} EUR
    </p>

    <a class="button" href="/scheda/{car["id"]}">Scheda</a>
    <a class="button" href="/modifica/{car["id"]}">Modifica</a>
    <a class="button" href="/report/{car["id"]}">Report</a>
</div>
"""

    html += "</main>"

    return page("Verifica Database", html)

@app.get("/set-quality/{car_id}/{quality}")
def set_quality(car_id: int, quality: str):
    allowed = ["generated", "verified", "premium_verified"]

    if quality not in allowed:
        return RedirectResponse(url="/verify", status_code=302)

    connection = db()
    connection.execute(
        "UPDATE cars SET data_quality = ? WHERE id = ?",
        (quality, car_id)
    )
    connection.commit()
    connection.close()

    return RedirectResponse(url="/verify", status_code=302)


@app.get("/verify-bmw", response_class=HTMLResponse)
def verify_bmw():
    rows = [car for car in all_cars() if (car["brand"] or "").lower() == "bmw"]

    html = """
<main class="container">
    <h1>Verifica BMW</h1>
    <a class="button" href="/verify">Tutte le auto</a>
"""

    for car in rows:
        quality = car["data_quality"] if "data_quality" in car.keys() else "generated"

        html += f"""
<div class="card">
    <h3>{escape(car["name"])}</h3>
    <p>{car["power"]} CV | {car["torque"]} Nm | 0-100 {car["zero100"]} s</p>
    <p>Qualità dato: <strong>{escape(quality)}</strong></p>

    <a class="button" href="/scheda/{car["id"]}">Scheda</a>
    <a class="button" href="/modifica/{car["id"]}">Modifica</a>
    <a class="button" href="/set-quality/{car["id"]}/generated">Generated</a>
    <a class="button" href="/set-quality/{car["id"]}/verified">Verified</a>
    <a class="button" href="/set-quality/{car["id"]}/premium_verified">Premium</a>
</div>
"""

    html += "</main>"
    return page("Verifica BMW", html)
