import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import numpy as np

pot = Path(__file__).resolve().parent.parent
podatki = pd.read_csv(pot / "results" / "poskusi.csv")

f = 0.8
rezultati = podatki[podatki["f_vhod"] == f].sort_values("sum_cnot")

plt.figure(figsize=(7, 4.5))

plt.plot(rezultati["sum_cnot"], rezultati["f_izhod"],
         marker="o", label="Po ociscevanju")

plt.axhline(f, linestyle="--", color="gray", label="Zacetna zvestoba")

plt.xlabel("Sum CNOT (lambda)")
plt.ylabel("Zvestoba")
plt.title("Vpliv suma CNOT pri F = 0.80")
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()

slike = pot / "Skupina24" / "img"
slike.mkdir(parents=True, exist_ok=True)

plt.savefig(slike / "zvestoba_sum.pdf")
plt.savefig(slike / "zvestoba_sum.png", dpi=200)


plt.figure(figsize=(9, 5))

for f in sorted(podatki["f_vhod"].unique()):
    rezultati = podatki[podatki["f_vhod"] == f].sort_values("sum_cnot")

    plt.plot(rezultati["sum_cnot"], rezultati["sprememba_f"],
             marker="o", label=f"F = {f:.2f}")

plt.axhline(0, linestyle="--", color="gray")

plt.xlabel("Sum CNOT (lambda)")
plt.ylabel("Sprememba zvestobe")
plt.title("Izboljsanje zvestobe pri razlicnih vhodnih stanjih")
plt.legend(bbox_to_anchor=(1.02, 1), loc="upper left")
plt.grid(alpha=0.3)
plt.tight_layout()

plt.savefig(slike / "izboljsanje_sum.pdf")
plt.savefig(slike / "izboljsanje_sum.png", dpi=200)



pragi = pd.read_csv(pot / "results" / "pragi.csv")

plt.figure(figsize=(7, 4.5))

plt.scatter(pragi["f_vhod"], pragi["prag_suma"],
            label="Numericna simulacija", zorder=3)

f_vrednosti = np.linspace(0.55, 0.95, 200)
pragi_teorija = 1 - 3 / np.sqrt(10 - 16 * (f_vrednosti - 0.75)**2)

plt.plot(f_vrednosti, pragi_teorija, label="Analiticna formula")

plt.xlabel("Zacetna zvestoba")
plt.ylabel("Mejni sum CNOT (lambda)")
plt.title("Mejna stopnja suma za uspesno ociscevanje")
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()

plt.savefig(slike / "pragi_suma.pdf")
plt.savefig(slike / "pragi_suma.png", dpi=200)

plt.show()