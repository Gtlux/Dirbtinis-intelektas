# -*- coding: utf-8 -*-
"""
3.2.1 scikit-learn pavyzdys – k-NN (k-Nearest Neighbors) su Iris duomenimis
=============================================================================

Šis skriptas demonstruoja k-NN (k artimiausių kaimynų) klasifikavimo algoritmą
naudojant scikit-learn biblioteką ir Iris (Vilkdalgių) duomenų rinkinį.

Iris duomenų rinkinys – tai klasikinis ML duomenų rinkinys su 150 gėlių matavimais:
  - 4 požymiai: taurėlapio ilgis/plotis, vainiklapio ilgis/plotis
  - 3 klasės: Setosa, Versicolor, Virginica

k-NN algoritmas: klasifikuoja naują tašką pagal k artimiausių kaimynų balsavimą.
"""

# ============================================================
# 1 ŽINGSNIS: Importuojame reikalingas bibliotekas
# ============================================================

# load_iris – funkcija, kuri užkrauna Iris (vilkdalgių) duomenų rinkinį
from sklearn.datasets import load_iris

# train_test_split – funkcija, kuri padalina duomenis į mokymo ir testavimo rinkinius
from sklearn.model_selection import train_test_split

# StandardScaler – standartizuoja požymius (atima vidurkį, dalina iš std)
# Tai svarbu k-NN algoritmui, nes jis naudoja atstumo metrikas
from sklearn.preprocessing import StandardScaler

# KNeighborsClassifier – k artimiausių kaimynų klasifikatorius
from sklearn.neighbors import KNeighborsClassifier

# accuracy_score – skaičiuoja klasifikavimo tikslumą (teisingų prognozių %)
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# numpy – skaitinių skaičiavimų biblioteka
import numpy as np

print("=" * 70)
print("k-NN KLASIFIKAVIMAS SU IRIS DUOMENIMIS (scikit-learn)")
print("=" * 70)

# ============================================================
# 2 ŽINGSNIS: Užkrauname duomenis
# ============================================================

# load_iris() grąžina Bunch objektą su .data (požymiai) ir .target (klasės)
iris = load_iris()

# X – požymių matrica (150 eilučių × 4 stulpeliai)
X = iris.data

# y – tikslinės klasės (150 reikšmių: 0=Setosa, 1=Versicolor, 2=Virginica)
y = iris.target

print(f"\n1. Duomenų rinkinys: Iris (Vilkdalgiai)")
print(f"   Imčių skaičius: {X.shape[0]}")       # 150
print(f"   Požymių skaičius: {X.shape[1]}")      # 4
print(f"   Požymių pavadinimai: {iris.feature_names}")
print(f"   Klasės: {list(iris.target_names)}")    # ['setosa', 'versicolor', 'virginica']
print(f"   Klasių pasiskirstymas: {np.bincount(y)}")  # [50, 50, 50]

# ============================================================
# 3 ŽINGSNIS: Padalijame duomenis į mokymo ir testavimo rinkinius
# ============================================================

# test_size=0.3 – 30% duomenų bus testavimui, 70% mokymui
# random_state=42 – fiksuotas atsitiktinumo generatorius (rezultatai atkartojami)
# stratify=y – užtikrina, kad kiekviena klasė proporcingai atstovaujama abiejuose rinkiniuose
X_train, X_test, y_train, y_test = train_test_split(
    X, y,                   # požymiai ir tikslinės klasės
    test_size=0.3,          # 30% testavimui
    random_state=42,        # atkartojamumui
    stratify=y              # proporcinis padalijimas pagal klases
)

print(f"\n2. Duomenų padalijimas:")
print(f"   Mokymo imčių: {X_train.shape[0]}")    # 105
print(f"   Testavimo imčių: {X_test.shape[0]}")   # 45

# ============================================================
# 4 ŽINGSNIS: Standartizuojame požymius (Feature Scaling)
# ============================================================

# k-NN naudoja Euklido atstumą, todėl būtina standartizuoti požymius.
# Be standartizacijos, požymiai su didesnėmis reikšmėmis dominuotų atstumą.
# StandardScaler transformuoja kiekvieną požymį: z = (x - vidurkis) / std

scaler = StandardScaler()

# fit_transform – apskaičiuoja vidurkį/std IŠ MOKYMO duomenų ir transformuoja
X_train_scaled = scaler.fit_transform(X_train)

# transform – naudoja TĄ PATĮ vidurkį/std (iš mokymo) testavimo duomenims
# SVARBU: negalima naudoti fit_transform testavimo duomenims!
X_test_scaled = scaler.transform(X_test)

print(f"\n3. Požymių standartizacija (StandardScaler):")
print(f"   Prieš: pirmoji mokymo imtis = {X_train[0]}")
print(f"   Po:    pirmoji mokymo imtis = {X_train_scaled[0].round(3)}")

# ============================================================
# 5 ŽINGSNIS: Kuriame ir treniruojame k-NN modelį
# ============================================================

# n_neighbors=5 – naudosime 5 artimiausius kaimynus balsavimui
# Tai yra hiperparametras – galime eksperimentuoti su skirtingomis k reikšmėmis
knn = KNeighborsClassifier(n_neighbors=5)

# fit() – "treniruoja" modelį (k-NN atveju tiesiog įsimena duomenis)
knn.fit(X_train_scaled, y_train)

print(f"\n4. k-NN modelis sukurtas su k={knn.n_neighbors}")

# ============================================================
# 6 ŽINGSNIS: Atliekame prognozes
# ============================================================

# predict() – prognozuoja klases testavimo duomenims
# Kiekvienam testavimo taškui randa 5 artimiausius mokymo taškus
# ir balsavimu priskiria dažniausią klasę
y_pred = knn.predict(X_test_scaled)

print(f"\n5. Prognozavimo rezultatai:")
print(f"   Pirmosios 10 prognozių: {y_pred[:10]}")
print(f"   Tikrosios reikšmės:     {y_test[:10]}")

# ============================================================
# 7 ŽINGSNIS: Įvertiname modelio tikslumą
# ============================================================

# accuracy_score – teisingų prognozių dalis (0.0 – 1.0)
accuracy = accuracy_score(y_test, y_pred)
print(f"\n6. Modelio tikslumas (accuracy): {accuracy:.4f} ({accuracy*100:.1f}%)")

# Confusion matrix – rodo, kiek kartų kiekviena klasė buvo teisingai/klaidingai klasifikuota
print(f"\n7. Painiavos matrica (Confusion Matrix):")
cm = confusion_matrix(y_test, y_pred)
print(f"   Klasės: {list(iris.target_names)}")
for i, row in enumerate(cm):
    print(f"   {iris.target_names[i]:>12}: {row}")

# Classification report – tikslumas, atkūrimas, F1 kiekvienai klasei
print(f"\n8. Klasifikavimo ataskaita:")
print(classification_report(y_test, y_pred, target_names=iris.target_names))

# ============================================================
# 8 ŽINGSNIS: Eksperimentuojame su skirtingomis k reikšmėmis
# ============================================================

print("9. Eksperimentas: tikslumas su skirtingomis k reikšmėmis:")
print(f"   {'k':<5} {'Tikslumas':<12}")
print(f"   {'-'*5} {'-'*12}")

for k in [1, 3, 5, 7, 9, 11]:
    # Kuriame naują modelį su kita k reikšme
    knn_temp = KNeighborsClassifier(n_neighbors=k)
    knn_temp.fit(X_train_scaled, y_train)
    y_pred_temp = knn_temp.predict(X_test_scaled)
    acc = accuracy_score(y_test, y_pred_temp)
    print(f"   {k:<5} {acc:.4f} ({acc*100:.1f}%)")

print("\n✓ Analizė baigta!")
