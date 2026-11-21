import csv
from pathlib import Path
from bbpssw import ocisti

zvestobe = [0.55, 0.60, 0.65, 0.70, 0.75, 0.80, 0.85, 0.90, 0.95]

rezultati = []

for f in zvestobe:
    spodnja = 0.0
    zgornja = 0.1

    for _ in range(22):
        sredina = (spodnja + zgornja) / 2
        f_izhod, uspeh = ocisti(f, sredina)

        if f_izhod > f:
            spodnja = sredina
        else:
            zgornja = sredina

    prag = (spodnja + zgornja) / 2
    f_izhod, uspeh = ocisti(f, prag)

    rezultati.append({
        "f_vhod": f,
        "prag_suma": prag,
        "p_uspeha": uspeh,
        "parov_na_izhod": 2 / uspeh
    })

    print(f"F = {f:.2f}, prag = {prag:.6f}")

pot = Path(__file__).resolve().parent.parent / "results"

with open(pot / "pragi.csv", "w", newline="", encoding="utf-8") as datoteka:
    zapis = csv.DictWriter(datoteka, fieldnames=rezultati[0].keys())
    zapis.writeheader()
    zapis.writerows(rezultati)