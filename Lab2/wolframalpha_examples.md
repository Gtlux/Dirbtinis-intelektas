# 2.3 — WolframAlpha: 5 pavyzdžių aprašymas

## Kas yra WolframAlpha?

WolframAlpha (https://www.wolframalpha.com/) — tai **skaičiuojamasis žinių variklis** (computational knowledge engine), sukurtas Stephen Wolfram. Skirtingai nuo paieškos sistemų (pvz., Google), kurios pateikia nuorodas į puslapius, WolframAlpha **tiesiogiai apskaičiuoja atsakymą** naudodamas savo struktūrizuotą žinių bazę, ontologijas ir algoritmus.

WolframAlpha yra ryškiausias pavyzdys technologijų, kurios aprašomos **vadovėlio 7–11 skyriuose**: loginės sistemos, žinių vaizdavimas, ontologijos. Sistema naudoja formalias žinių struktūras ir logiką, kad iš faktų ir taisyklių gautų atsakymus.

---

## 5 pavyzdžiai

### 1. Matematika: `solve x^2 - 5x + 6 = 0`

**Paaiškinimas:** WolframAlpha priima algebrinę lygtį natūralia kalba ir apskaičiuoja jos šaknis (x=2 ir x=3). Sistema naudoja simbolinės matematikos algoritmų žinių bazę — ji „žino" kvadratinės lygties sprendimo formulę, faktorizacijos metodus ir gali pavaizduoti sprendinius grafiškai. Tai demonstruoja, kaip žinių bazė su taisyklėmis (matematikos dėsniais) leidžia automatiškai spręsti problemas.

### 2. Chemija: `caffeine molecule`

**Paaiškinimas:** Įvedus „caffeine molecule", WolframAlpha pateikia kofeino cheminę formulę (C₈H₁₀N₄O₂), molekulinę masę, 2D/3D struktūrą, fizikines savybes ir farmakologinę informaciją. Tai veikia dėl to, kad sistema turi ontologiją — struktūrizuotą cheminių medžiagų žinių bazę, kurioje kiekviena medžiaga aprašyta savybių rinkiniu (formulė, masė, struktūra ir t.t.). Tai tiesioginis **žinių vaizdavimo** (knowledge representation) pavyzdys.

### 3. Geografija: `population Vilnius vs Kaunas`

**Paaiškinimas:** WolframAlpha palygina dviejų miestų gyventojų skaičius, pateikia grafikus ir statistinius duomenis. Sistema naudoja geografinę ontologiją, kurioje miestai susieti su atributais (gyventojai, plotas, koordinatės). Užklausa apdorojama natūralios kalbos analizatoriumi (NLP), kuris atpažįsta, kad „population" yra atributas, o „Vilnius" ir „Kaunas" — objektai. Tai rodo, kaip **ontologijos** leidžia struktūrizuoti ir palyginti realaus pasaulio žinias.

### 4. Astronomija: `distance from Earth to Mars`

**Paaiškinimas:** Sistema apskaičiuoja atstumą tarp Žemės ir Marso konkrečiu laiko momentu (nes atstumas nuolat kinta). WolframAlpha naudoja astronominę žinių bazę su planetų orbitų parametrais ir realiu laiku skaičiuoja pozicijas. Tai demonstruoja skirtumą tarp **statinių žinių** (orbitų parametrai) ir **dinaminių skaičiavimų** (dabartinis atstumas) — sistema ne tik saugo faktus, bet ir taiko matematines taisykles jiems apdoroti.

### 5. Mityba: `calories in 100g of banana`

**Paaiškinimas:** WolframAlpha pateikia išsamią maistinę informaciją: kalorijas (~89 kcal), maistines medžiagas (angliavandeniai, baltymai, riebalai, vitaminai). Duomenys gaunami iš struktūrizuotos mitybos ontologijos, kurioje kiekvienas maisto produktas aprašytas standartizuotu atributų rinkiniu. Tai pavyzdys, kaip **ekspertinė sistema** gali pateikti specialisto lygio informaciją konkrečioje srityje (dietologija), naudodama žinių bazę vietoj paieškos internete.

---

## Apibendrinimas

WolframAlpha demonstruoja praktinį **žinių vaizdavimo ir ontologijų** pritaikymą:
- **Žinių bazė** — struktūrizuoti duomenys apie pasaulį (chemija, geografija, astronomija...)
- **Ontologijos** — formalios schemos, apibrėžiančios objektų klases ir jų savybes
- **Inference engine** — taisyklių ir algoritmų sistema, kuri iš žinomų faktų apskaičiuoja naujus
- **NLP** — natūralios kalbos supratimas, leidžiantis pateikti užklausas žmogiškai
