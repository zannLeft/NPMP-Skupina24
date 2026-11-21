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
         marker="o", label="Po očiščevanju")

plt.axhline(f, linestyle="--", color="gray", label="Začetna zvestoba")

plt.xlabel("Šum CNOT (λ)")
plt.ylabel("Zvestoba")
plt.title("Vpliv šuma CNOT pri F = 0,80")
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

plt.xlabel("Šum CNOT (λ)")
plt.ylabel("Sprememba zvestobe")
plt.title("Izboljšanje zvestobe pri različnih vhodnih stanjih")
plt.legend(bbox_to_anchor=(1.02, 1), loc="upper left")
plt.grid(alpha=0.3)
plt.tight_layout()

plt.savefig(slike / "izboljsanje_sum.pdf")
plt.savefig(slike / "izboljsanje_sum.png", dpi=200)



pragi = pd.read_csv(pot / "results" / "pragi.csv")

plt.figure(figsize=(7, 4.5))

plt.scatter(pragi["f_vhod"], pragi["prag_suma"],
            label="Numerična simulacija", zorder=3)

f_vrednosti = np.linspace(0.55, 0.95, 200)
pragi_teorija = 1 - 3 / np.sqrt(10 - 16 * (f_vrednosti - 0.75)**2)

plt.plot(f_vrednosti, pragi_teorija, label="Analitična formula")

plt.xlabel("Začetna zvestoba")
plt.ylabel("Mejni šum CNOT (λ)")
plt.title("Mejna stopnja šuma za uspešno očiščevanje")
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()

plt.savefig(slike / "pragi_suma.pdf")
plt.savefig(slike / "pragi_suma.png", dpi=200)


meritve = pd.read_csv(pot / "results" / "meritve.csv")

stevila = sorted(meritve["shots"].unique())
odkloni = []
odkloni_teorija = []

for n in stevila:
    izbrane = meritve[meritve["shots"] == n]

    odkloni.append(izbrane["p_ocena"].std(ddof=1))

    p = izbrane["p_natancno"].iloc[0]
    odkloni_teorija.append(np.sqrt(p * (1 - p) / n))

plt.figure(figsize=(7, 4.5))

plt.plot(stevila, odkloni, marker="o", label="Simulacija")
plt.plot(stevila, odkloni_teorija, marker="s", linestyle="--", label="Teorija")

plt.xscale("log", base=2)
plt.xticks(stevila, [str(n) for n in stevila])

plt.xlabel("Število meritev")
plt.ylabel("Standardni odklon ocene P")
plt.title("Statistična negotovost meritev")
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()

plt.savefig(slike / "odklon_meritev.pdf")
plt.savefig(slike / "odklon_meritev.png", dpi=200)

plt.show()