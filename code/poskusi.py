import csv
from pathlib import Path
from bbpssw import ocisti

zvestobe = [0.55, 0.60, 0.65, 0.70, 0.75, 0.80, 0.85, 0.90, 0.95]
sumi = [0, 0.005, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.08, 0.10]

rezultati = []

for f in zvestobe:
    for s in sumi:
        f_izhod, uspeh = ocisti(f, s)

        rezultati.append({
            "f_vhod": f,
            "sum_cnot": s,
            "f_izhod": f_izhod,
            "sprememba_f": f_izhod - f,
            "p_uspeha": uspeh,
            "parov_na_izhod": 2 / uspeh
        })

pot = Path(__file__).resolve().parent.parent / "results"
pot.mkdir(exist_ok=True)

with open(pot / "poskusi.csv", "w", newline="", encoding="utf-8") as datoteka:
    zapis = csv.DictWriter(datoteka, fieldnames=rezultati[0].keys())
    zapis.writeheader()
    zapis.writerows(rezultati)

for r in rezultati:
    if r["f_vhod"] == 0.8 and r["sum_cnot"] == 0.05:
        print("Primer F=0.8, sum=0.05")
        print("Izhodna zvestoba:", round(r["f_izhod"], 6))
        print("Verjetnost uspeha:", round(r["p_uspeha"], 6))