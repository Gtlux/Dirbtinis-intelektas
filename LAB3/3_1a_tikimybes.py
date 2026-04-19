# -*- coding: utf-8 -*-
"""
3.1a Tikimybės – Sąlyginės ir nesąlyginės tikimybės
=====================================================
Dalykinė sritis: Studentų egzaminų rezultatai

Kintamieji (loginiai, True/False):
  M – Mokėsi (ar studentas mokėsi prieš egzaminą)
  S – Sveikas (ar studentas buvo sveikas egzamino dieną)
  I – Išlaikė (ar studentas išlaikė egzaminą)

Analogija su Gripo pavyzdžiu iš skaidrių (AIBookSkaidresLect7):
  Skaidrėse buvo kintamieji: Lietus, Epidemija, Gripas, GalvosSkausmas, Temperatūra
  Ir pilna tikimybių pasiskirstymo lentelė su 8 eilutėmis.
  
  Mes naudojame panašų principą: sudarome pilną jungtinę tikimybių lentelę
  P(M, S, I) visiems 2³ = 8 deriniams ir iš jos skaičiuojame
  nesąlygines bei sąlygines tikimybes.
"""

# ============================================================
# 1. PILNA JUNGTINĖ TIKIMYBIŲ PASISKIRSTYMO LENTELĖ
# ============================================================
# Kiekviena eilutė: (Mokėsi, Sveikas, Išlaikė, Tikimybė)
# Visos tikimybės turi sudaryti 1.0

pilna_lentele = [
    # Mokėsi  Sveikas  Išlaikė  P(M, S, I)
    (True,    True,    True,    0.36),   # mokėsi + sveikas + išlaikė – dažniausias geras atvejis
    (True,    True,    False,   0.04),   # mokėsi + sveikas, bet neišlaikė – reta
    (True,    False,   True,    0.10),   # mokėsi + sirgo, bet vis tiek išlaikė
    (True,    False,   False,   0.05),   # mokėsi + sirgo + neišlaikė
    (False,   True,    True,    0.08),   # nesimokė + sveikas, bet išlaikė (pasisekė)
    (False,   True,    False,   0.15),   # nesimokė + sveikas + neišlaikė
    (False,   False,   True,    0.02),   # nesimokė + sirgo + išlaikė (labai reta)
    (False,   False,   False,   0.20),   # nesimokė + sirgo + neišlaikė
]

# ============================================================
# 2. TIKRINIMAS – ar tikimybės sudaro 1.0
# ============================================================
suma = sum(p for _, _, _, p in pilna_lentele)
print("=" * 65)
print("PILNA JUNGTINĖ TIKIMYBIŲ PASISKIRSTYMO LENTELĖ P(M, S, I)")
print("=" * 65)
print(f"{'Mokėsi':<10} {'Sveikas':<10} {'Išlaikė':<10} {'P(M,S,I)':<10}")
print("-" * 65)
for m, s, i, p in pilna_lentele:
    print(f"{'T' if m else 'F':<10} {'T' if s else 'F':<10} {'T' if i else 'F':<10} {p:<10.3f}")
print("-" * 65)
print(f"{'SUMA:':<30} {'':<10} {suma:<10.3f}")
assert abs(suma - 1.0) < 1e-9, "Klaida: tikimybės nesudaro 1.0!"
print("✓ Tikimybės teisingos (suma = 1.0)\n")

# ============================================================
# 3. NESĄLYGINĖ TIKIMYBĖ: P(Išlaikė = True)
# ============================================================
# P(I=T) = Σ P(M, S, I=T) per visas M ir S reikšmes
# Tai yra marginalizacija – sumuojame visas eilutes, kur I=True

print("=" * 65)
print("NESĄLYGINĖ TIKIMYBĖ: P(Išlaikė = True)")
print("=" * 65)

p_islaikę = 0.0
print("Sumuojame visas eilutes, kur Išlaikė = True:")
for m, s, i, p in pilna_lentele:
    if i == True:
        print(f"  P(M={'T' if m else 'F'}, S={'T' if s else 'F'}, I=T) = {p:.3f}")
        p_islaikę += p

print(f"\n  P(Išlaikė = T) = {p_islaikę:.2f}")
print(f"  Interpretacija: {p_islaikę*100:.0f}% studentų išlaiko egzaminą.\n")

# ============================================================
# 4. SĄLYGINĖ TIKIMYBĖ: P(Išlaikė = True | Mokėsi = True) 
# ============================================================
# Pagal Bajeso formulę:
# P(I=T | M=T) = P(I=T, M=T) / P(M=T)
#
# P(I=T, M=T) = Σ P(M=T, S, I=T) per visas S reikšmes
# P(M=T)      = Σ P(M=T, S, I) per visas S ir I reikšmes

print("=" * 65)
print("SĄLYGINĖ TIKIMYBĖ: P(Išlaikė = T | Mokėsi = T)")
print("=" * 65)

# Skaitiklis: P(I=T ir M=T)
p_islaikę_ir_mokesi = 0.0
print("Skaitiklis P(I=T, M=T):")
for m, s, i, p in pilna_lentele:
    if i == True and m == True:
        print(f"  P(M=T, S={'T' if s else 'F'}, I=T) = {p:.3f}")
        p_islaikę_ir_mokesi += p
print(f"  P(I=T, M=T) = {p_islaikę_ir_mokesi:.3f}\n")

# Vardiklis: P(M=T)
p_mokesi = 0.0
print("Vardiklis P(M=T):")
for m, s, i, p in pilna_lentele:
    if m == True:
        print(f"  P(M=T, S={'T' if s else 'F'}, I={'T' if i else 'F'}) = {p:.3f}")
        p_mokesi += p
print(f"  P(M=T) = {p_mokesi:.3f}\n")

# Rezultatas
p_salygine = p_islaikę_ir_mokesi / p_mokesi
print(f"P(Išlaikė=T | Mokėsi=T) = P(I=T, M=T) / P(M=T)")
print(f"                        = {p_islaikę_ir_mokesi:.3f} / {p_mokesi:.3f}")
print(f"                        = {p_salygine:.4f}")
print(f"\nInterpretacija: Jei studentas mokėsi, tikimybė išlaikyti = {p_salygine*100:.1f}%")
print(f"Palyginkime su bendra tikimybe išlaikyti: {p_islaikę*100:.1f}%")
print(f"Mokymasis padidina tikimybę išlaikyti {p_salygine/p_islaikę:.1f} karto.\n")

# ============================================================
# 5. PAPILDOMA: P(Mokėsi = True | Išlaikė = True) – Bajeso teorema
# ============================================================
# P(M=T | I=T) = P(I=T | M=T) * P(M=T) / P(I=T)

print("=" * 65)
print("PAPILDOMA (Bajeso teorema): P(Mokėsi = T | Išlaikė = T)")
print("=" * 65)

p_mokesi_jei_islaikę = (p_salygine * p_mokesi) / p_islaikę
print(f"P(M=T | I=T) = P(I=T | M=T) × P(M=T) / P(I=T)")
print(f"             = {p_salygine:.4f} × {p_mokesi:.3f} / {p_islaikę:.2f}")
print(f"             = {p_mokesi_jei_islaikę:.4f}")
print(f"\nInterpretacija: Jei žinome, kad studentas išlaikė egzaminą,")
print(f"tikimybė, kad jis mokėsi = {p_mokesi_jei_islaikę*100:.1f}%")
