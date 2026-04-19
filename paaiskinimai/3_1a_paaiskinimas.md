# 3.1a – Tikimybių lentelė – Paaiškinimas

## Kas čia vyksta?

Įsivaizduok, kad esi mokyklos direktorius ir nori suprasti, nuo ko priklauso, 
ar studentas išlaikys egzaminą. Tu žinai du dalykus apie kiekvieną studentą:
ar jis **mokėsi** ir ar jis buvo **sveikas** egzamino dieną.

## Ką mes padarėme?

Mes sukūrėme lentelę, kurioje surašėme VISUS įmanomus variantus. Kadangi turime 
3 dalykus (Mokėsi, Sveikas, Išlaikė) ir kiekvienas gali būti arba TAIP, arba NE, 
tai gauname 2 × 2 × 2 = **8 galimus variantus**.

Kiekvienam variantui priskyrėme tikimybę – kiek dažnai toks atvejis pasitaiko. 
Pavyzdžiui:
- Mokėsi + Sveikas + Išlaikė = **0.36** (36%) – tai dažniausias geras atvejis
- Nesimokė + Sirgo + Neišlaikė = **0.20** (20%) – irgi dažnas, bet blogas atvejis
- Nesimokė + Sirgo + Išlaikė = **0.02** (2%) – labai retas stebuklas

Visos tikimybės sudėjus turi duoti lygiai **1.0** (100%), nes tai yra visi įmanomi variantai.

## Ką paskaičiavome?

### 1. Nesąlyginė tikimybė: "Kokia tikimybė, kad studentas išlaikys?"

Čia mes tiesiog paklausėme: neatsižvelgiant į nieką kitą, kiek procentų studentų 
išlaiko egzaminą? 

Atsakyti paprasta – tiesiog **sudėjome visas eilutes, kur Išlaikė = Taip**:
```
0.360 + 0.100 + 0.080 + 0.020 = 0.56
```

**Atsakymas: 56% studentų išlaiko egzaminą.** Tai yra "nesąlyginė" tikimybė, 
nes mes neklausėme jokių papildomų sąlygų.

### 2. Sąlyginė tikimybė: "Kokia tikimybė išlaikyti, JEI studentas mokėsi?"

Čia jau yra sąlyga – mes žinome, kad studentas mokėsi, ir norime sužinoti, 
kiek tai padidina jo šansus.

Skaičiuojame dviem žingsniais:

**Žingsnis 1:** Randame P(Išlaikė IR Mokėsi) – kiek studentų ir mokėsi, ir išlaikė:
```
0.360 + 0.100 = 0.460 (46%)
```

**Žingsnis 2:** Randame P(Mokėsi) – kiek iš viso studentų mokėsi:
```
0.360 + 0.040 + 0.100 + 0.050 = 0.550 (55%)
```

**Žingsnis 3:** Daliname: 0.460 ÷ 0.550 = **0.836 (83.6%)**

**Atsakymas: Jei studentas mokėsi, jo tikimybė išlaikyti yra 83.6%!**

Palyginkime: bendra tikimybė buvo 56%, o mokiusiems – 83.6%. 
Tai reiškia, kad **mokymasis padidina šansus 1.5 karto**.

### 3. Bajeso teorema: "Jei žinau, kad išlaikė – ar jis mokėsi?"

Tai atvirkštinis klausimas. Dažnai gyvenime matome rezultatą (išlaikė!) 
ir norime spėti priežastį (ar mokėsi?).

Bajeso teorema leidžia "apversti" sąlyginę tikimybę:
```
P(Mokėsi | Išlaikė) = 0.8214 (82.1%)
```

**Tai reiškia: jei studentas išlaikė egzaminą, yra 82% tikimybė, kad jis mokėsi.**
Logiškai atrodo – dauguma išlaikiusių būna mokęsi, bet ne visi (kai kurie turi sėkmės).

## Kodėl tai svarbu?

Tikimybių lentelės ir sąlyginės tikimybės yra pagrindas dirbtiniam intelektui. 
Kai kompiuteris mato simptomus (pvz., temperatūra, kosulys), jis naudoja būtent 
tokius skaičiavimus, kad nuspręstų, kokia liga labiausiai tikėtina.
