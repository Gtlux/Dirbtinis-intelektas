# 3.1b – Bajeso tinklas – Paaiškinimas

## Kas yra Bajeso tinklas?

Bajeso tinklas – tai **schema (grafas), kuri parodo, kas nuo ko priklauso**. 
Įsivaizduok šeimos medį, tik vietoj žmonių yra įvairūs faktai, o rodyklės rodo 
"kas ką veikia".

Pavyzdžiui, jei lauke lyja → tu gali susirgti gripu → tada turėsi temperatūrą. 
Lietus veikia gripą, gripas veikia temperatūrą. Bet lietus tiesiogiai neveikia 
temperatūros – tik per gripą.

## Ką mes padarėme?

Sukūrėme Bajeso tinklą apie **studento kelią iki diplomo**. Tinkle yra 6 mazgai 
(kintamieji), sujungti rodyklėmis:

```
Motyvacija ──→ Mokymasis ──→ Geras Egzaminas ──→ Diplomas
    │                              ↑
    └──→ Dalyvavimas Paskaitose ───┘
                                   ↑
Geri Dėstytojai ───────────────────┘
```

### Ką reiškia kiekviena rodyklė?

- **Motyvacija → Mokymasis**: Jei studentas motyvuotas, jis greičiausiai mokysis. 
  Nemotyvuotas – greičiausiai ne.
- **Motyvacija → Dalyvavimas**: Motyvuotas studentas dažniau eis į paskaitas.
- **Mokymasis → Geras Egzaminas**: Kas mokosi, tas geriau parašo.
- **Dalyvavimas → Geras Egzaminas**: Kas lanko paskaitas, irgi geriau parašo.
- **Geri Dėstytojai → Geras Egzaminas**: Geri dėstytojai padeda studentams.
- **Geras Egzaminas → Diplomas**: Geri egzaminai veda prie diplomo.

### Tikimybių lentelės (CPT)

Prie kiekvieno mazgo yra **tikimybių lentelė**, kuri nurodo, kokia tikimybė, 
kad kazkas atsitiks, priklausomai nuo tėvinių mazgų.

Pavyzdžiui, lentelė prie "Mokymasis":
- Jei motyvuotas → 85% tikimybė, kad mokysis
- Jei nemotyvuotas → tik 20% tikimybė, kad mokysis

## Kaip atsakome į klausimus?

Bajeso tinklas leidžia užduoti klausimus tipo "kas būtų, jei...":

### 1 klausimas: "Kokia tikimybė gauti diplomą, jei motyvuotas ir nėra streso?"

Kompiuteris "praeina" per visą tinklą nuo Motyvacijos iki Diplomo, apskaičiuodamas 
tikimybes kiekviename žingsnyje. Atsakymas: **76.4%** – gana gera tikimybė!

### 2 klausimas: "Jei žinau, kad gavo diplomą – ar jis mokėsi?"

Tai atvirkštinis klausimas – žinome pabaigą ir norime atspėti pradžią. 
Bajeso tinklas sugeba tai padaryti! Atsakymas: **83.8%** – labai tikėtina, kad mokėsi.

### 3 klausimas: "Nesimokė ir nelankė paskaitų – kokios tikimybės?"

Tikimybė gerai parašyti egzaminą: tik **4.1%**. Beveik neįmanoma.

### 4 klausimas: "Nemotyvuotas ir stresuojantis – ar gaus diplomą?"

Tikimybė gauti diplomą: tik **21.8%**. Liūdna, bet logiška.

## Kur tai naudojama?

Bajeso tinklai naudojami visur:
- **Medicinoje**: pagal simptomus nustatyti ligą
- **Spam filtruose**: ar laiškas yra spam, ar ne
- **Autonominiuose automobiliuose**: ar priekyje yra pėsčiasis, ar ne
- **Orų prognozėse**: ar rytoj lis, atsižvelgiant į dabartinius duomenis
