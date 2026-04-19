# 3.3 – pgmpy Bajeso tinklas – Paaiškinimas

## Kas čia vyksta paprastais žodžiais?

Šioje dalyje mes paėmėme tą patį Bajeso tinklą, kurį sukūrėme web tool'e (3.1b dalis), 
ir užprogramavome jį Python kalba naudodami **pgmpy** biblioteką. 

Privalumas: web tool'as yra tik vizualizacijai, o pgmpy sugeba **tiksliai 
apskaičiuoti tikimybes** ir atsakyti į sudėtingus klausimus.

## Ką daro pgmpy programa?

### 1. Sukuria tinklo struktūrą

Pirma nurodome, kas nuo ko priklauso (rodyklėmis):

```
Motyvacija → Mokymasis        (motyvuotas studentas dažniau mokosi)
Motyvacija → Dalyvavimas      (motyvuotas dažniau eina į paskaitas)
Mokymasis → GerasEgzaminas    (kas mokosi – geriau rašo)
Dalyvavimas → GerasEgzaminas  (kas lanko – geriau rašo)
Stresas → GerasEgzaminas      (stresas trukdo parašyti)
GerasEgzaminas → Diplomas     (geri egzaminai → diplomas)
```

### 2. Užpildo tikimybių lenteles

Kiekvienam mazgui nurodome tikimybes. Pavyzdžiui:

**Motyvacija** – 60% studentų yra motyvuoti, 40% – ne.

**Mokymasis** – priklauso nuo motyvacijos:
- Jei motyvuotas → 85% mokysis
- Jei nemotyvuotas → tik 20% mokysis

**GerasEgzaminas** – priklauso nuo trijų dalykų vienu metu 
(mokymosi, dalyvavimo IR streso). Tai reiškia, kad yra 8 skirtingi deriniai.
Pavyzdžiui:
- Mokėsi + Lankė + Nėra streso → 90% tikimybė gerai parašyti
- Nesimokė + Nelankė + Yra stresas → tik 2% tikimybė (beveik neįmanoma)

### 3. Patikrina ar viskas teisinga

Programa patikrina:
- Ar visos tikimybės sumuoja į 1.0?
- Ar tinklo struktūra logiška (nėra ciklų)?
- Ar visi mazgai turi savo lenteles?

Mūsų atveju: **"Modelis teisingas: True"** ✓

### 4. Atsako į klausimus

Čia yra pati įdomiausia dalis. Naudojamas **VariableElimination** algoritmas – 
tai matematinis metodas, kuris "praeina" per visą tinklą ir tiksliai apskaičiuoja 
tikimybes.

## Klausimai ir atsakymai (suprantama kalba)

### 1 klausimas: "Motyvuotas studentas be streso – ar gaus diplomą?"

Mes sakome kompiuteriui: "Žinau, kad studentas motyvuotas ir nestresuoja. 
Kokia tikimybė, kad jis gaus diplomą?"

Kompiuteris galvoja taip:
- Motyvuotas → greičiausiai mokysis (85%) ir lankys paskaitas (90%)
- Mokosi + lanko + nėra streso → greičiausiai gerai parašys egzaminą
- Gerai parašys → greičiausiai gaus diplomą

**Atsakymas: 76.4%** – gana geri šansai!

### 2 klausimas: "Gavo diplomą – ar jis mokėsi?"

Čia klausimas atvirkščias – žinome rezultatą (diplomas) ir norime atspėti priežastį.

Kompiuteris "samprotauja atgal":
- Diplomas → greičiausiai gerai parašė egzaminą
- Gerai parašė → greičiausiai mokėsi
- Arba gal buvo pasisekimas? Bet tai reta...

**Atsakymas: 83.8%** – labai tikėtina, kad mokėsi.

### 3 klausimas: "Nesimokė ir nelankė – ar parašys?"

**Atsakymas: tik 4.1%** – beveik neįmanoma gerai parašyti be mokymosi ir paskaitų!

### 4 klausimas: "Nemotyvuotas + stresas – ar gaus diplomą?"

**Atsakymas: tik 21.8%** – mažiau nei ketvirtadalis šansų. Los nuo motyvacijos 
ir streso labai jaučiasi.

## Kuo pgmpy skiriasi nuo web tool?

| | Web tool (3.1b) | pgmpy (3.3) |
|---|---|---|
| **Kas tai?** | Interneto puslapio įrankis | Python biblioteka |
| **Vizualizacija** | ✅ Graži schema | ❌ Tik tekstas |
| **Tikimybių skaičiavimas** | ❌ Nėra query funkcijos | ✅ Tikslus skaičiavimas |
| **Automatizacija** | ❌ Viskas rankomis | ✅ Galima programuoti |
| **Kam tinka?** | Mokymui, demonstracijai | Realiam darbui, tyrimams |

## Išvada

pgmpy leidžia ne tik sukurti Bajeso tinklą, bet ir **užduoti jam klausimus** 
ir gauti tikslius atsakymus. Tai yra vienas pagrindinių dirbtinio intelekto 
metodų, naudojamas medicinoje, versle, saugumo sistemose ir kitur.
