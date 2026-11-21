# Vpliv napak vrat CNOT na učinkovitost očiščevanja Bellovih parov

Seminarska naloga pri predmetu Nekonvencionalne platforme in metode procesiranja (NPMP).

Raziskujemo, kako napake dvokubitnih vrat CNOT vplivajo na delovanje protokola BBPSSW za očiščevanje Bellovih parov.

## Opis

Za vhodna stanja uporabljamo Wernerjeva stanja z različnimi začetnimi zvestobami. Simulacija poteka na štirih kubitih in vključuje dve vrati CNOT, meritve ter pogojno ohranjanje izhodnega para.

Na vrata CNOT dodamo depolarizacijski šum in spremljamo:
- izhodno zvestobo očiščenega para,
- verjetnost uspeha protokola,
- povprečno število porabljenih vhodnih parov,
- mejno stopnjo šuma, pri kateri očiščevanje ne izboljša več zvestobe.

Rezultate primerjamo z analitičnimi formulami. Dodatno preverimo vpliv končnega števila meritev na oceno verjetnosti uspeha.

## Namestitev

Potrebujemo Python in knjižnice iz datoteke `requirements.txt`.

V PowerShellu iz korenske mape projekta:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## Zagon

Posamezen primer protokola BBPSSW:

```powershell
.\.venv\Scripts\python.exe .\code\bbpssw.py 0.8 0.05
```

Prvi argument je začetna zvestoba, drugi pa parameter šuma CNOT.

Za ponovno izvedbo vseh eksperimentov zaženemo skripte v naslednjem vrstnem redu:

```powershell
.\.venv\Scripts\python.exe .\code\poskusi.py
.\.venv\Scripts\python.exe .\code\pragi.py
.\.venv\Scripts\python.exe .\code\meritve.py
.\.venv\Scripts\python.exe .\code\grafi.py
```

Analiza zahtevnosti vezja:

```powershell
.\.venv\Scripts\python.exe .\code\vezje.py
```

## Datoteke

- `code/bell.py` - priprava Bellovega para.
- `code/werner.py` - priprava Wernerjevih stanj.
- `code/pari.py` - priprava in preverjanje dveh vhodnih parov.
- `code/bbpssw.py` - idealni in šumni protokol BBPSSW.
- `code/poskusi.py` - simulacije pri različnih začetnih zvestobah in stopnjah šuma.
- `code/pragi.py` - numerični izračun pragov šuma in primerjava s teorijo.
- `code/meritve.py` - simulacije s končnim številom meritev.
- `code/grafi.py` - izdelava grafov.
- `code/vezje.py` - analiza števila kubitov, globine in vrat.

Podatki se shranijo v mapo `results`, grafi pa v `Skupina24/img`.

## Omejitve

Glavni eksperimenti uporabljajo simulator Qiskit Aer z gostotnimi matrikami. Vhodna Wernerjeva stanja pripravimo neposredno, brez simulacije fizičnega vezja za njihovo pripravo.

Šum modeliramo z dvokubitnim depolarizacijskim kanalom na vratih CNOT. Ne gre za meritve na resnični kvantni napravi.

Pri eksperimentu s končnim številom meritev ocenjujemo verjetnost uspeha protokola. Izhodno zvestobo računamo iz gostotne matrike.