# 3.1b – Bajeso tinklas su 6 kintamaisiais

## Naudojamas įrankis

[BayANet – Bayes Nets Tool](https://profgavinbrown.github.io/projects/bayes_nets/)

## Tema: Studento studijų sėkmė

### 6 Kintamieji (mazgai)

| Nr. | Kintamasis          | Reikšmės     | Aprašymas                           |
|-----|---------------------|--------------|-------------------------------------|
| 1   | Motyvacija          | Taip / Ne    | Ar studentas motyvuotas             |
| 2   | GeriDėstytojai      | Taip / Ne    | Ar dėstytojai geri                  |
| 3   | Mokymasis           | Taip / Ne    | Ar studentas mokosi reguliariai     |
| 4   | DalyvavimasPaskaitose | Taip / Ne  | Ar lanko paskaitas                  |
| 5   | GerasEgzaminas      | Taip / Ne    | Ar gerai parašo egzaminą            |
| 6   | Diplomas            | Taip / Ne    | Ar gaus diplomą                     |

### Tinklo struktūra (kryptinis grafas)

```
Motyvacija ──────→ Mokymasis ──────────→ GerasEgzaminas ──→ Diplomas
     │                                        ↑
     └──────→ DalyvavimasPaskaitose ──────────┘
                                              ↑
GeriDėstytojai ───────────────────────────────┘
```

### Briaunos (priežastiniai ryšiai)

1. **Motyvacija → Mokymasis** – motyvuotas studentas dažniau mokosi
2. **Motyvacija → DalyvavimasPaskaitose** – motyvuotas studentas dažniau lanko paskaitas
3. **Mokymasis → GerasEgzaminas** – kas mokosi, tas geriau parašo
4. **DalyvavimasPaskaitose → GerasEgzaminas** – lankymas padeda egzamine
5. **GeriDėstytojai → GerasEgzaminas** – geri dėstytojai padeda geriau suprasti
6. **GerasEgzaminas → Diplomas** – geri egzaminai veda prie diplomo

### Sąlyginių tikimybių lentelės (CPT)

**Motyvacija** (šakninis mazgas):

| Motyvacija | P     |
|------------|-------|
| Taip       | 0.60  |
| Ne         | 0.40  |

**GeriDėstytojai** (šakninis mazgas):

| GeriDėstytojai | P     |
|----------------|-------|
| Taip           | 0.50  |
| Ne             | 0.50  |

**Mokymasis** (priklauso nuo Motyvacijos):

| Motyvacija | P(Mokymasis=Taip) | P(Mokymasis=Ne) |
|------------|-------------------|-----------------|
| Taip       | 0.85              | 0.15            |
| Ne         | 0.20              | 0.80            |

**DalyvavimasPaskaitose** (priklauso nuo Motyvacijos):

| Motyvacija | P(Dalyvavimas=Taip) | P(Dalyvavimas=Ne) |
|------------|---------------------|-------------------|
| Taip       | 0.90                | 0.10              |
| Ne         | 0.30                | 0.70              |

**GerasEgzaminas** (priklauso nuo Mokymasis, Dalyvavimas, GeriDėstytojai):

| Mokymasis | Dalyvavimas | GeriDėst. | P(GerasEgz=Taip) | P(GerasEgz=Ne) |
|-----------|-------------|-----------|-------------------|-----------------|
| Taip      | Taip        | Taip      | 0.95              | 0.05            |
| Taip      | Taip        | Ne        | 0.80              | 0.20            |
| Taip      | Ne          | Taip      | 0.70              | 0.30            |
| Taip      | Ne          | Ne        | 0.55              | 0.45            |
| Ne        | Taip        | Taip      | 0.40              | 0.60            |
| Ne        | Taip        | Ne        | 0.25              | 0.75            |
| Ne        | Ne          | Taip      | 0.10              | 0.90            |
| Ne        | Ne          | Ne        | 0.05              | 0.95            |

**Diplomas** (priklauso nuo GerasEgzaminas):

| GerasEgzaminas | P(Diplomas=Taip) | P(Diplomas=Ne) |
|----------------|------------------|----------------|
| Taip           | 0.95             | 0.05           |
| Ne             | 0.10             | 0.90           |

---

## Klausimai ir atsakymai

### 1 klausimas: Kokia tikimybė gauti diplomą, jei studentas motyvuotas ir turi gerus dėstytojus?

**P(Diplomas=Taip | Motyvacija=Taip, GeriDėstytojai=Taip) = ?**

Sprendimas (naudojant tinklo struktūrą):
- Jei motyvuotas → P(Mokymasis=Taip) = 0.85, P(Dalyvavimas=Taip) = 0.90
- Su gerais dėstytojais ir mokymusi bei dalyvavimu → P(GerasEgz=Taip) labai didelė
- Apskaičiavus per visas galimas Mokymasis ir Dalyvavimas kombinacijas:

**Atsakymas: P(Diplomas=Taip | Motyvacija=Taip, GeriDėstytojai=Taip) ≈ 0.82**

Tai reiškia, kad motyvuotas studentas su gerais dėstytojais turi ~82% tikimybę gauti diplomą.

### 2 klausimas: Kokia tikimybė, kad studentas mokėsi, jei žinome, kad jis gavo diplomą?

**P(Mokymasis=Taip | Diplomas=Taip) = ?**

Sprendimas (atvirkštinis išvedimas – Bajeso teorema):
- Diplomas priklauso nuo GerasEgzaminas, kuris priklauso nuo Mokymasis
- Jei studentas gavo diplomą, labai tikėtina, kad gerai parašė egzaminą
- O jei gerai parašė → tikėtina, kad mokėsi

**Atsakymas: P(Mokymasis=Taip | Diplomas=Taip) ≈ 0.84**

Tai reiškia, kad jei žinome, jog studentas gavo diplomą, yra ~84% tikimybė, kad jis mokėsi.

---

## Instrukcija: kaip sukurti tinklą su web tool

1. Eikite į https://profgavinbrown.github.io/projects/bayes_nets/
2. Dukart spustelėkite ant drobės, kad sukurtumėte naują mazgą
3. Pakartokite 6 kartus (visiems kintamiesiems)
4. Spustelėkite ant mazgo ir pervadinkite jį (pvz., "Motyvacija")
5. Nubrėžkite briaunas: spustelėkite ant tėvinio mazgo ir vilkite iki vaikinio
6. Kiekviename mazge nustatykite CPT reikšmes pagal aukščiau pateiktas lenteles
7. Naudokite "Query" funkciją klausimams atsakyti
