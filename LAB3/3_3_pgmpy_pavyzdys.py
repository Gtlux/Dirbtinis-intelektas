# -*- coding: utf-8 -*-
"""
3.3 pgmpy pavyzdys – Bajeso tinklas su pgmpy paketu
=====================================================

Šis skriptas demonstruoja Bajeso tinklo kūrimą ir tikimybinį išvedimą
naudojant Python pgmpy (Probabilistic Graphical Models using Python) paketą.

Tema: Studento egzamino sėkmė
Kintamieji:
  1. Motyvacija (M) – ar studentas motyvuotas {0: Ne, 1: Taip}
  2. Mokymasis (K) – ar studentas mokosi reguliariai {0: Ne, 1: Taip}
  3. Dalyvavimas (D) – ar lanko paskaitas {0: Ne, 1: Taip}
  4. GerasEgzaminas (E) – ar gerai parašo egzaminą {0: Ne, 1: Taip}
  5. Stresas (S) – ar studentas patiria stresą {0: Ne, 1: Taip}
  6. Diplomas (P) – ar gaus diplomą {0: Ne, 1: Taip}

Tinklo struktūra (kryptinis grafas):
  Motyvacija → Mokymasis
  Motyvacija → Dalyvavimas
  Mokymasis → GerasEgzaminas
  Dalyvavimas → GerasEgzaminas
  Stresas → GerasEgzaminas
  GerasEgzaminas → Diplomas
"""

# ============================================================
# 1 ŽINGSNIS: Importuojame bibliotekas
# ============================================================

# DiscreteBayesianNetwork – klasė Bajeso tinklo struktūrai apibrėžti
# (ankstesnėse versijose buvo BayesianNetwork, dabar DiscreteBayesianNetwork)
from pgmpy.models import DiscreteBayesianNetwork

# TabularCPD – klasė sąlyginėms tikimybių lentelėms (CPD) sukurti
from pgmpy.factors.discrete import TabularCPD

# VariableElimination – tikimybinio išvedimo algoritmas
from pgmpy.inference import VariableElimination

print("=" * 70)
print("BAJESO TINKLAS SU PGMPY PAKETU")
print("=" * 70)

# ============================================================
# 2 ŽINGSNIS: Apibrėžiame tinklo struktūrą
# ============================================================

# Kuriame Bajeso tinklą nurodydami briaunas (parent → child)
# Kiekviena briauna reiškia priežastinį ryšį
model = DiscreteBayesianNetwork([
    ('Motyvacija', 'Mokymasis'),        # Motyvacija veikia mokymąsi
    ('Motyvacija', 'Dalyvavimas'),      # Motyvacija veikia dalyvavimą paskaitose
    ('Mokymasis', 'GerasEgzaminas'),    # Mokymasis veikia egzamino rezultatą
    ('Dalyvavimas', 'GerasEgzaminas'),  # Dalyvavimas veikia egzamino rezultatą
    ('Stresas', 'GerasEgzaminas'),      # Stresas veikia egzamino rezultatą
    ('GerasEgzaminas', 'Diplomas'),     # Egzamino rezultatas veikia diplomo gavimą
])

print("\nTinklo struktūra (briaunos):")
for edge in model.edges():
    print(f"  {edge[0]} → {edge[1]}")

# ============================================================
# 3 ŽINGSNIS: Apibrėžiame sąlyginių tikimybių lenteles (CPD)
# ============================================================

# --- Motyvacija: šakninis mazgas (neturi tėvų) ---
# P(Motyvacija=Ne) = 0.4, P(Motyvacija=Taip) = 0.6
cpd_motyvacija = TabularCPD(
    variable='Motyvacija',      # kintamojo pavadinimas
    variable_card=2,            # kintamojo kardinalumas (2 reikšmės: 0 ir 1)
    values=[[0.4], [0.6]]       # tikimybės: [P(0), P(1)]
)

# --- Stresas: šakninis mazgas (neturi tėvų) ---
# P(Stresas=Ne) = 0.7, P(Stresas=Taip) = 0.3
cpd_stresas = TabularCPD(
    variable='Stresas',
    variable_card=2,
    values=[[0.7], [0.3]]
)

# --- Mokymasis: priklauso nuo Motyvacijos ---
# Stulpeliai: Motyvacija=0, Motyvacija=1
# P(Mokymasis=Ne | Motyvacija=Ne) = 0.8  P(Mokymasis=Ne | Motyvacija=Taip) = 0.15
# P(Mokymasis=Taip | Motyvacija=Ne) = 0.2  P(Mokymasis=Taip | Motyvacija=Taip) = 0.85
cpd_mokymasis = TabularCPD(
    variable='Mokymasis',
    variable_card=2,
    values=[
        [0.8, 0.15],   # P(Mokymasis=Ne | Motyvacija)
        [0.2, 0.85]    # P(Mokymasis=Taip | Motyvacija)
    ],
    evidence=['Motyvacija'],    # tėvinis mazgas
    evidence_card=[2]           # tėvinio mazgo kardinalumas
)

# --- Dalyvavimas: priklauso nuo Motyvacijos ---
# P(Dalyvavimas=Ne | Motyvacija=Ne) = 0.7  P(Dalyvavimas=Ne | Motyvacija=Taip) = 0.1
# P(Dalyvavimas=Taip | Motyvacija=Ne) = 0.3  P(Dalyvavimas=Taip | Motyvacija=Taip) = 0.9
cpd_dalyvavimas = TabularCPD(
    variable='Dalyvavimas',
    variable_card=2,
    values=[
        [0.7, 0.1],    # P(Dalyvavimas=Ne | Motyvacija)
        [0.3, 0.9]     # P(Dalyvavimas=Taip | Motyvacija)
    ],
    evidence=['Motyvacija'],
    evidence_card=[2]
)

# --- GerasEgzaminas: priklauso nuo Mokymasis, Dalyvavimas, Stresas ---
# 3 tėvai × 2 reikšmės = 2³ = 8 stulpeliai
# Stulpelių tvarka: (Mok=0,Dal=0,Str=0), (Mok=0,Dal=0,Str=1), (Mok=0,Dal=1,Str=0), ...
cpd_egzaminas = TabularCPD(
    variable='GerasEgzaminas',
    variable_card=2,
    values=[
        # Tikimybė, kad blogas egzaminas:
        [0.95, 0.98, 0.70, 0.85, 0.40, 0.65, 0.10, 0.30],
        # Tikimybė, kad geras egzaminas:
        [0.05, 0.02, 0.30, 0.15, 0.60, 0.35, 0.90, 0.70]
    ],
    evidence=['Mokymasis', 'Dalyvavimas', 'Stresas'],
    evidence_card=[2, 2, 2]
)

# --- Diplomas: priklauso nuo GerasEgzaminas ---
# P(Diplomas=Ne | GerasEgz=Ne) = 0.9   P(Diplomas=Ne | GerasEgz=Taip) = 0.05
# P(Diplomas=Taip | GerasEgz=Ne) = 0.1    P(Diplomas=Taip | GerasEgz=Taip) = 0.95
cpd_diplomas = TabularCPD(
    variable='Diplomas',
    variable_card=2,
    values=[
        [0.9, 0.05],   # P(Diplomas=Ne | GerasEgzaminas)
        [0.1, 0.95]    # P(Diplomas=Taip | GerasEgzaminas)
    ],
    evidence=['GerasEgzaminas'],
    evidence_card=[2]
)

# ============================================================
# 4 ŽINGSNIS: Pridedame CPD lenteles prie modelio
# ============================================================

model.add_cpds(
    cpd_motyvacija, cpd_stresas, cpd_mokymasis,
    cpd_dalyvavimas, cpd_egzaminas, cpd_diplomas
)

# ============================================================
# 5 ŽINGSNIS: Tikriname ar modelis teisingas
# ============================================================

# check_model() tikrina:
# - Ar visos CPD lentelės nuoseklios su tinklo struktūra
# - Ar tikimybės sumuoja į 1.0 kiekviename stulpelyje
is_valid = model.check_model()
print(f"\nModelis teisingas: {is_valid}")

# ============================================================
# 6 ŽINGSNIS: Atspausdiname CPD lenteles
# ============================================================

print("\n" + "=" * 70)
print("SĄLYGINIŲ TIKIMYBIŲ LENTELĖS (CPD)")
print("=" * 70)

for cpd in model.get_cpds():
    print(f"\n{cpd}")

# ============================================================
# 7 ŽINGSNIS: Sukuriame tikimybinio išvedimo objektą
# ============================================================

# VariableElimination – tikslus tikimybinio išvedimo algoritmas
# Jis naudoja kintamųjų eliminavimo metodą sąlyginėms tikimybėms apskaičiuoti
infer = VariableElimination(model)

# ============================================================
# 8 ŽINGSNIS: Atsakome į klausimus
# ============================================================

print("\n" + "=" * 70)
print("TIKIMYBINIS IŠVEDIMAS – KLAUSIMAI IR ATSAKYMAI")
print("=" * 70)

# --- 1 KLAUSIMAS ---
# Kokia tikimybė gauti diplomą, jei studentas motyvuotas ir nėra streso?
print("\n--- 1 KLAUSIMAS ---")
print("Kokia tikimybė gauti diplomą, jei studentas motyvuotas ir nėra streso?")
print("P(Diplomas | Motyvacija=Taip, Stresas=Ne)")

result1 = infer.query(
    variables=['Diplomas'],                     # klausiame apie Diplomą
    evidence={'Motyvacija': 1, 'Stresas': 0}    # žinome: motyvuotas, nėra streso
)
print(result1)

# --- 2 KLAUSIMAS ---
# Kokia tikimybė, kad studentas mokėsi, jei žinome, kad jis gavo diplomą?
print("\n--- 2 KLAUSIMAS ---")
print("Kokia tikimybė, kad studentas mokėsi, jei žinome, kad jis gavo diplomą?")
print("P(Mokymasis | Diplomas=Taip)")

result2 = infer.query(
    variables=['Mokymasis'],        # klausiame apie Mokymąsi
    evidence={'Diplomas': 1}        # žinome: gavo diplomą
)
print(result2)

# --- 3 KLAUSIMAS (papildomas) ---
# Kokia tikimybė gerai parašyti egzaminą, jei studentas nesimoko ir nelanko paskaitų?
print("\n--- 3 KLAUSIMAS (papildomas) ---")
print("Kokia tikimybė gerai išlaikyti egzaminą, jei nesimokė ir nelankė paskaitų?")
print("P(GerasEgzaminas | Mokymasis=Ne, Dalyvavimas=Ne)")

result3 = infer.query(
    variables=['GerasEgzaminas'],
    evidence={'Mokymasis': 0, 'Dalyvavimas': 0}
)
print(result3)

# --- 4 KLAUSIMAS (papildomas) ---
# Kokia tikimybė gauti diplomą jei nesimokei?
print("\n--- 4 KLAUSIMAS (papildomas) ---")
print("Kokia tikimybė gauti diplomą, jei studentas nesimotyvuotas ir patiria stresą?")
print("P(Diplomas | Motyvacija=Ne, Stresas=Taip)")

result4 = infer.query(
    variables=['Diplomas'],
    evidence={'Motyvacija': 0, 'Stresas': 1}
)
print(result4)

print("\n✓ pgmpy Bajeso tinklo analizė baigta!")
