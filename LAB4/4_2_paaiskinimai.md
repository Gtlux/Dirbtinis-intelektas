# 4.2 Sukurtas robotas – „Explorer Robot" (Tyrinėtojo robotas)

## Kas tai?

Sukūriau savo robotą Webots simuliacijos aplinkoje. Tai **autonominis tyrinėtojo robotas** – jis pats važinėja po areną, vengia kliūčių, ieško šviesos šaltinio, piešia savo kelią ant grindų ir rodo savo būseną per šviesiukus (LED). Robotas turi **3 skirtingų tipų sensorius** (kurie leidžia jam „jausti" aplinką) ir **3 skirtingų tipų aktuatorius** (kurie leidžia jam „veikti").

---

## Sensoriai – kaip robotas „mato" ir „jaučia" aplinką

### 1. Atstumo sensoriai (DistanceSensor) – 2 vienetai

Tai roboto „akys". Du maži sensoriai pritvirtinti roboto priekyje – vienas žiūri šiek tiek kairėn, kitas šiek tiek dešinėn. Jie nuolat matuoja, ar priešais yra kokia nors kliūtis (siena, dėžutė ir pan.).

**Kaip veikia:** sensorius siunčia nematomas spindulius ir matuoja, per kiek laiko jie atsimuša nuo objekto. Kuo arčiau objektas – tuo didesnė grąžinta reikšmė:
- **0** = nieko nematau (kelias laisvas 40 cm pirmyn)
- **600** = kažkas yra maždaug 16 cm atstumu
- **1000** = kliūtis visai šalia (beveik liečiu)

Kadangi vienas sensorius žiūri kairiau, o kitas – dešiniau, robotas gali suprasti iš kurios pusės artėja kliūtis ir apsisukti priešinga kryptimi.

### 2. Šviesos sensorius (LightSensor) – 1 vienetas

Tai lyg roboto „fotoelementas". Jis sumontuotas roboto priekyje ant viršaus ir matuoja, kiek šviesos jis gauna. Arenoje yra geltonas šviesos šaltinis (lemputė), ir kai robotas prie jos priartėja – šviesos reikšmė didėja.

**Kaip veikia:** sensorius tiesiog matuoja aplinkos apšvietimo intensyvumą. Programoje nustatytas slenkstis – jei reikšmė viršija 5, robotas pereina į „šviesos sekimo" režimą ir bando judėti link stipresnės šviesos.

### 3. GPS – 1 vienetas

Tai roboto „navigatorius". GPS modulis kiekvieną akimirką praneša, kur tiksliai robotas yra arenoje – X ir Y koordinates.

**Kam naudojamas:**
- Konsolėje rodoma dabartinė roboto pozicija (pvz. X=0.152, Y=-0.034)
- Programa skaičiuoja, kiek metrų robotas iš viso nuvažiavo – kiekvieną kadrą matuojamas atstumas nuo ankstesnės pozicijos ir pridedamas prie bendro atstumo

---

## Aktuatoriai – kaip robotas „veikia"

### 1. Ratų varikliai (RotationalMotor) – 4 vienetai

Tai „raumenys" roboto, kurie suka ratus. Kiekvienas iš 4 ratų turi savo variklį. Robotas naudoja **diferencialinį valdymą**:
- Kai visi ratai sukasi **vienodai** – robotas važiuoja tiesiai
- Kai **kairieji sukasi greičiau** nei dešinieji – robotas sukasi dešinėn
- Kai **dešinieji sukasi greičiau** nei kairieji – robotas sukasi kairėn
- Kai viena pusė sukasi **pirmyn**, o kita **atgal** – robotas sukasi vietoje

Programa nustato kiekvieno rato greitį pagal tai, ką robotas tuo metu daro (vengia kliūties, seka šviesą ar tiesiog patruliuoja).

### 2. LED šviesiukai – 2 vienetai

Du maži šviesiukai ant roboto viršuje – kairysis (žalias) ir dešinysis (raudonas). Jie rodo, ką robotas šiuo metu daro:

| Ką robotas daro | Kas vyksta su LED |
|-----------------|-------------------|
| **Patruliuoja** (važinėja aplink) | Šviesiukai lėtai kaitaliojasi – vienas šviečia, kitas ne, ir atvirkščiai |
| **Vengia kliūties** | Abu šviesiukai greitai mirksi – kaip pavojaus signalas |
| **Seka šviesą** | Abu šviesiukai nuolat šviečia – robotas rado taikinį |

### 3. Pen (rašiklis) – 1 vienetas

Tai kažkas panašaus į flomasterį roboto apačioje. Kai robotas važiuoja – jis **palieka spalvotą liniją ant grindų**, taip piešdamas savo kelią. Tai leidžia vizualiai pamatyti, kur robotas lankėsi.

**Spalvos keičiasi pagal būseną:**
- **Mėlyna** linija = robotas ramiai patruliuoja
- **Raudona** linija = robotas vengia kliūties
- **Geltona** linija = robotas seka šviesą

---

## Santraukos lentelė

| Komponentas | Tipas | Kiekis | Paprastas paaiškinimas |
|-------------|-------|--------|----------------------|
| DistanceSensor | Sensorius | 2 | „Akys" – mato kliūtis priekyje |
| LightSensor | Sensorius | 1 | „Fotoelementas" – jaučia šviesą |
| GPS | Sensorius | 1 | „Navigatorius" – žino savo poziciją |
| RotationalMotor | Aktuatorius | 4 | „Raumenys" – suka ratus |
| LED | Aktuatorius | 2 | „Šviesiukai" – rodo būseną |
| Pen | Aktuatorius | 1 | „Flomasteris" – piešia kelią ant grindų |

---

## Kaip robotas „galvoja"? (Kontrolerio logika)

Robotas veikia pagal **prioritetų sistemą**. Kiekvieną kadrą (kas 16 ms) jis patikrina situaciją ir nusprendžia, ką daryti:

### Prioritetai (nuo svarbiausio):

1. **REVERSE (atbulinė eiga)** – jei robotas jau važiuoja atbuline (patenka į kampą, kur iš abiejų pusių sienos), jis tęsia atbulinę eigą 30 kadrų (~0.5 sek.), po to pasuka atsitiktine kryptimi. Tai padeda jam neužstrigti kampuose.

2. **AVOID (kliūties vengimas)** – jei kuris nors atstumo sensorius rodo, kad kliūtis arti (~16 cm):
   - Kliūtis kairėje? → suka dešinėn
   - Kliūtis dešinėje? → suka kairėn
   - Kliūtis iš abiejų pusių? → REVERSE (atbulinė)

3. **LIGHT (šviesos sekimas)** – jei šviesos sensorius rodo reikšmę virš slenksčio:
   - Jei šviesa stiprėja (lyginant su praeitu kadru) – robotas juda tiesiai, nes juda teisinga kryptimi
   - Jei šviesa silpnėja – robotas šiek tiek sukasi, ieškodamas stipresnės šviesos

4. **PATROL (patruliavimas)** – jei nėra nei kliūčių, nei šviesos:
   - Robotas važiuoja pirmyn vidutinių greičiu
   - Kas 50-120 kadrų atsitiktinai keičia kryptį (šiek tiek pasuka kairėn arba dešinėn)
   - Taip jis tyrinėja visą areną, o ne važiuoja tik tiesiai

---

## Simuliacijos aplinka

Robotas važinėja po **1.5×1.5 metro areną** (RectangleArena), kurioje yra:
- **Sienos** aplink visą perimetrą (robotas nuo jų atsimuša)
- **4 kliūtys** skirtingose vietose: raudona dėžutė, žalias cilindras, mėlyna dėžutė, geltonas stačiakampis
- **Rožinis kamuolys** – fizikinis objektas, kurį robotas gali pastumti
- **Geltonas šviesos šaltinis** – lemputė, kurią aptinka šviesos sensorius

---

## Konsolinis išvedimas

Kas 50 kadrų programa spausdina informaciją:
```
--- Žingsnis 200 | Būsena: PATROL ---
  Atstumo sensoriai: L=0  R=350
  Šviesos sensorius: 3.2
  GPS: X=0.152  Y=-0.034
  Atstumas: 0.487 m
  Greitis: L=3.14  R=2.86
```

Iš šio išvedimo galima suprasti:
- **Būsena** – ką robotas šiuo metu daro
- **Atstumo sensoriai** – ar mato kliūtis (L=kairys, R=dešinys)
- **Šviesos sensorius** – ar jaučia šviesą
- **GPS** – kur robotas yra arenoje
- **Atstumas** – kiek metrų iš viso nuvažiavo
- **Greitis** – kairių ir dešinių ratų greitis

---

## Failų struktūra

```
uzd2/
└── 4_2_custom_robot/
    ├── controllers/
    │   └── explorer_controller/
    │       └── explorer_controller.py   ← Kontrolerio programa (Python)
    └── worlds/
        └── explorer_robot.wbt          ← Pasaulio ir roboto aprašymas
```

## Kaip paleisti

1. Atidaryti Webots
2. `File → Open World...`
3. Pasirinkti `uzd2/4_2_custom_robot/worlds/explorer_robot.wbt`
4. Paspausti ▶ (Play)
5. Stebėti:
   - Kaip robotas važinėja po areną
   - Spalvotas linijas ant grindų (piešia Pen)
   - LED šviesiukų mirksėjimą
   - Konsolės pranešimus su sensorių duomenimis
