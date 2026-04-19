# Ekspertinė sistema: Medicininė simptomų diagnostika

## Specifikacija natūralia kalba

### Sistemos paskirtis
Ši ekspertinė sistema yra skirta preliminariai medicininei diagnostikai pagal paciento simptomus. Sistema veikia kaip pagalbinis įrankis, padedantis identifikuoti galimas ligas remiantis IF-THEN taisyklėmis.

### Įvesties duomenys (Faktai)
Paciento informacija:
- **Vardas** (string) — paciento vardas
- **Amžius** (integer) — paciento amžius
- **Temperatūra** (float) — kūno temperatūra °C
- **Simptomai** — boolean laukai:
  - `fever` — karščiavimas (temperatūra > 37.5)
  - `cough` — kosulys
  - `sore_throat` — gerklės skausmas
  - `runny_nose` — sloga
  - `headache` — galvos skausmas
  - `body_aches` — kūno skausmai
  - `fatigue` — nuovargis
  - `nausea` — pykinimas
  - `rash` — bėrimas
  - `shortness_of_breath` — dusulys

### Taisyklės (IF-THEN)

1. **Gripas (Flu)**
   JEI karščiavimas IR kosulys IR kūno_skausmai IR nuovargis
   TAI diagnozė = "Gripas" (tikimybė: aukšta)

2. **Peršalimas (Common Cold)**
   JEI sloga IR gerklės_skausmas IR kosulys IR NE karščiavimas
   TAI diagnozė = "Peršalimas" (tikimybė: aukšta)

3. **COVID-19**
   JEI karščiavimas IR kosulys IR nuovargis IR dusulys
   TAI diagnozė = "COVID-19 įtarimas" (tikimybė: vidutinė)

4. **Angina (Strep Throat)**
   JEI gerklės_skausmas IR karščiavimas IR NE kosulys IR NE sloga
   TAI diagnozė = "Angina" (tikimybė: vidutinė)

5. **Bronchitas (Bronchitis)**
   JEI kosulys IR nuovargis IR NE karščiavimas
   TAI diagnozė = "Bronchitas" (tikimybė: vidutinė)

6. **Migrena (Migraine)**
   JEI galvos_skausmas IR pykinimas IR NE karščiavimas IR NE kosulys
   TAI diagnozė = "Migrena" (tikimybė: aukšta)

7. **Alerginė reakcija (Allergic Reaction)**
   JEI bėrimas IR sloga IR NE karščiavimas
   TAI diagnozė = "Alerginė reakcija" (tikimybė: vidutinė)

8. **Pneumonija (Pneumonia)**
   JEI karščiavimas IR kosulys IR dusulys IR kūno_skausmai
   TAI diagnozė = "Pneumonija" (tikimybė: aukšta, SKUBU)

9. **Virškinimo infekcija (Gastroenteritis)**
   JEI pykinimas IR karščiavimas IR NE kosulys
   TAI diagnozė = "Virškinimo infekcija" (tikimybė: vidutinė)

10. **Dehidratacija (Dehydration)**
    JEI nuovargis IR galvos_skausmas IR NE karščiavimas IR NE kosulys
    TAI diagnozė = "Dehidratacija" (tikimybė: žema)

### Išvesties duomenys
- Paciento vardas ir simptomai
- Galimos diagnozės su tikimybės lygiu
- Rekomendacijos (pvz., "kreipkitės į gydytoją", "pailsėkite")

### Taisyklių prioritetai
1. Pirmenybė teikiama skubioms diagnozėms (Pneumonija, COVID-19)
2. Jei keli simptomai tinka kelioms diagnozėms — pateikiamos visos galimos
3. Jei joks simptomų rinkinys neatitinka taisyklių — pateikiamas pranešimas "Neįmanoma nustatyti diagnozės"

### Sistemos apribojimai
- Sistema NEpakeičia profesionalios medicininės konsultacijos
- Diagnozės yra tik preliminarios ir skirtos informavimui
- Sistema naudoja supaprastintas taisykles mokymosi tikslais
