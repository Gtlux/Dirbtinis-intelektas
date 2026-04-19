# Užduotis 3: Tikimybės ir mokymasis iš pavyzdžių – Ataskaita

## Turinys

1. [3.1a Tikimybių lentelė](#31a-tikimybių-lentelė)
2. [3.1b Bajeso tinklas](#31b-bajeso-tinklas-su-6-kintamaisiais)
3. [3.2.1 scikit-learn k-NN](#321-scikit-learn-k-nn-analizė)
4. [3.2.2 TensorFlow/PyTorch MNIST](#322-tensorflowpytorch-mnist-analizė)
5. [3.3 pgmpy pavyzdys](#33-pgmpy-bajeso-tinklo-pavyzdys)

---

## 3.1a Tikimybių lentelė

**Failas:** `3_1a_tikimybes.py`

### Dalykinė sritis: Studentų egzaminų rezultatai

Pasirinkti 3 loginiai kintamieji:
- **M (Mokėsi)** – ar studentas mokėsi prieš egzaminą (True/False)
- **S (Sveikas)** – ar studentas buvo sveikas egzamino dieną (True/False)
- **I (Išlaikė)** – ar studentas išlaikė egzaminą (True/False)

### Pilna jungtinė tikimybių pasiskirstymo lentelė P(M, S, I)

| Mokėsi | Sveikas | Išlaikė | P(M, S, I) |
|--------|---------|---------|------------|
| T      | T       | T       | 0.360      |
| T      | T       | F       | 0.040      |
| T      | F       | T       | 0.100      |
| T      | F       | F       | 0.050      |
| F      | T       | T       | 0.080      |
| F      | T       | F       | 0.150      |
| F      | F       | T       | 0.020      |
| F      | F       | F       | 0.200      |
| **SUMA** |       |         | **1.000**  |

### Nesąlyginė tikimybė: P(Išlaikė = True)

Marginalizuojame (sumuojame) visas eilutes, kur I=True:

```
P(I=T) = P(T,T,T) + P(T,F,T) + P(F,T,T) + P(F,F,T)
       = 0.360 + 0.100 + 0.080 + 0.020
       = 0.56
```

**Atsakymas: P(Išlaikė=T) = 0.56 (56% studentų išlaiko egzaminą)**

### Sąlyginė tikimybė: P(Išlaikė = T | Mokėsi = T)

Naudojame formulę: P(I=T | M=T) = P(I=T, M=T) / P(M=T)

**Skaitiklis:**
```
P(I=T, M=T) = P(T,T,T) + P(T,F,T) = 0.360 + 0.100 = 0.460
```

**Vardiklis:**
```
P(M=T) = P(T,T,T) + P(T,T,F) + P(T,F,T) + P(T,F,F) 
       = 0.360 + 0.040 + 0.100 + 0.050 = 0.550
```

**Rezultatas:**
```
P(I=T | M=T) = 0.460 / 0.550 = 0.8364 (83.6%)
```

**Interpretacija:** Jei studentas mokėsi, tikimybė išlaikyti egzaminą = 83.6%.
Palyginimui, bendra tikimybė išlaikyti = 56.0%. Mokymasis padidina tikimybę 1.5 karto.

### Papildoma: Bajeso teorema P(Mokėsi = T | Išlaikė = T)

```
P(M=T | I=T) = P(I=T | M=T) × P(M=T) / P(I=T)
             = 0.8364 × 0.550 / 0.56 = 0.8214 (82.1%)
```

---

## 3.1b Bajeso tinklas su 6 kintamaisiais

**Failas:** `3_1b_bajeso_tinklas.md`  
**Įrankis:** https://profgavinbrown.github.io/projects/bayes_nets/

### Kintamieji

1. Motyvacija, 2. GeriDėstytojai, 3. Mokymasis, 4. DalyvavimasPaskaitose, 5. GerasEgzaminas, 6. Diplomas

### Tinklo struktūra

```
Motyvacija ──────→ Mokymasis ──────────→ GerasEgzaminas ──→ Diplomas
     │                                        ↑
     └──────→ DalyvavimasPaskaitose ──────────┘
                                              ↑
GeriDėstytojai ───────────────────────────────┘
```

### Klausimai ir atsakymai

**1 kl.:** P(Diplomas=Taip | Motyvacija=Taip, GeriDėstytojai=Taip) ≈ **0.82 (82%)**  
Motyvuotas studentas su gerais dėstytojais turi 82% tikimybę gauti diplomą.

**2 kl.:** P(Mokymasis=Taip | Diplomas=Taip) ≈ **0.84 (84%)**  
Jei žinome, kad studentas gavo diplomą, 84% tikimybė, kad jis mokėsi.

---

## 3.2.1 scikit-learn k-NN analizė

**Failas:** `3_2_1_sklearn_knn.py`

### Duomenų rinkinys: Iris (Vilkdalgiai)

- 150 imčių, 4 požymiai (taurėlapio/vainiklapio ilgis ir plotis)
- 3 klasės: Setosa, Versicolor, Virginica (po 50 kiekvienoje)

### Algoritmas: k-Nearest Neighbors (k-NN)

k-NN klasifikuoja naują tašką pagal k artimiausių kaimynų balsavimą.

### Veiksmai:
1. Duomenys padalinti: 70% mokymas, 30% testavimas
2. Požymiai standartizuoti (StandardScaler) – būtina k-NN algoritmui
3. Modelis treniruotas su k=5
4. Prognozuota ir įvertinta

### Rezultatai:

| k reikšmė | Tikslumas |
|-----------|-----------|
| 1         | 93.3%     |
| 3         | 91.1%     |
| 5         | 91.1%     |
| 7         | 93.3%     |
| 9         | 95.6%     |
| 11        | 95.6%     |

**Geriausias tikslumas: 95.6% su k=9 arba k=11**

---

## 3.2.2 TensorFlow/PyTorch MNIST analizė

**Failas:** `3_2_2_tensorflow_mnist.py`

> **Pastaba:** Kadangi TensorFlow nepalaiko Python 3.14, naudotas PyTorch – 
> antra pagal populiarumą giluminio mokymosi biblioteka. Architektūra identiška TensorFlow pavyzdžiui.

### Duomenų rinkinys: MNIST

- 60,000 mokymo + 10,000 testavimo paveikslėlių
- 28×28 pikselių pilkos spalvos skaitmenų (0-9) atpažinimas

### Neuroninio tinklo architektūra:

```
Flatten(28×28 → 784) → Dense(128, ReLU) → Dropout(0.2) → Dense(10, Softmax)
```

Parametrų skaičius: 101,770

### Mokymosi eiga (5 epochos):

| Epocha | Nuostolis | Tikslumas |
|--------|-----------|-----------|
| 1      | 0.3022    | 91.0%     |
| 2      | 0.1508    | 95.5%     |
| 3      | 0.1164    | 96.5%     |
| 4      | 0.0972    | 97.0%     |
| 5      | 0.0862    | 97.3%     |

### Testavimo rezultatai:

- **Tikslumas: 97.5%**
- Visos 5 pirmosios prognozės teisingos su >99% tikimybe

---

## 3.3 pgmpy Bajeso tinklo pavyzdys

**Failas:** `3_3_pgmpy_pavyzdys.py`  
**Paketas:** pgmpy (Probabilistic Graphical Models using Python)

### Bajeso tinklo modelis: Studento egzamino sėkmė

6 kintamieji su ryšiais:
```
Motyvacija → Mokymasis → GerasEgzaminas → Diplomas
Motyvacija → Dalyvavimas → GerasEgzaminas
Stresas → GerasEgzaminas
```

### Tikslaus tikimybinio išvedimo rezultatai (VariableElimination):

**1 kl.:** P(Diplomas=Taip | Motyvacija=Taip, Stresas=Ne) = **0.7636 (76.4%)**

**2 kl.:** P(Mokymasis=Taip | Diplomas=Taip) = **0.8377 (83.8%)**

**3 kl.:** P(GerasEgzaminas=Taip | Mokymasis=Ne, Dalyvavimas=Ne) = **0.0410 (4.1%)**
→ Nesimokant ir nelankant paskaitų, tikimybė gerai išlaikyti egzaminą tik 4.1%!

**4 kl.:** P(Diplomas=Taip | Motyvacija=Ne, Stresas=Taip) = **0.2175 (21.8%)**
→ Nemotyvuotas ir stresuojantis studentas turi tik 21.8% tikimybę gauti diplomą.

---

## Failų sąrašas

| Failas | Paskirtis |
|--------|-----------|
| `3_1a_tikimybes.py` | Tikimybių lentelė ir skaičiavimai |
| `3_1b_bajeso_tinklas.md` | Bajeso tinklo aprašymas su 6 kintamaisiais |
| `3_2_1_sklearn_knn.py` | scikit-learn k-NN analizė su Iris |
| `3_2_2_tensorflow_mnist.py` | PyTorch MNIST neuroninio tinklo analizė |
| `3_3_pgmpy_pavyzdys.py` | pgmpy Bajeso tinklo pavyzdys |
| `ataskaita.md` | Ši ataskaita |
