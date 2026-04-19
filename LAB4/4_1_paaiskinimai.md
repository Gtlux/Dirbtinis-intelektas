# 4.1 Webots pavyzdžio analizė ir modifikacija

## Kas yra šis pavyzdys?

Iš Webots programos paėmiau paruoštą pavyzdį – **keturių ratų robotą**, kuris moka vengti kliūčių. Šis pavyzdys yra Webots aplinkoje čia:
- `projects/samples/tutorials/worlds/4_wheels_robot.wbt`
- `projects/samples/tutorials/controllers/four_wheels_collision_avoidance/four_wheels_collision_avoidance.c`

Tai yra paprastas robotukas, kuris važinėja po tam tikrą aikštelę ant grindų ir kai priartėja prie sienos ar kliūties – pasisuka ir važiuoja kita kryptimi.

---

## Kas yra sensoriai ir aktuatoriai šiame robote?

### Sensoriai (tai, kuo robotas „jaučia" aplinką)

Robote yra **2 atstumo sensoriai** (`DistanceSensor`) – jie veikia kaip roboto „akys". Sensoriai sumontuoti roboto priekyje – vienas žiūri šiek tiek į kairę, kitas šiek tiek į dešinę. Jie nuolat matuoja atstumą iki artimiausio objekto priešais:
- Jei sensorius rodo **~1000** – priešais nieko nėra, kelias laisvas.
- Jei sensorius rodo **mažiau nei 950** – vadinasi, priešais yra kažkas (siena, objektas).
- Kuo mažesnė reikšmė – tuo arčiau kliūtis.

Kadangi vienas sensorius žiūri kairėn, o kitas dešinėn, robotas gali nustatyti iš kurios pusės artėja kliūtis ir pasukti priešinga kryptimi.

### Aktuatoriai (tai, kuo robotas „veikia" – juda, šviečia ir t.t.)

Robote yra **4 varikliai** (`RotationalMotor`) – po vieną kiekvienam ratui. Varikliai suka ratus ir taip robotas juda. Robotas naudoja **diferencialinį valdymą** – tai reiškia, kad kairieji ratai (wheel1 ir wheel3) ir dešinieji ratai (wheel2 ir wheel4) gali suktis skirtingais greičiais:
- Jei visi ratai sukasi vienodai – robotas važiuoja **tiesiai**.
- Jei kairieji sukasi greičiau – robotas sukasi **dešinėn**.
- Jei dešinieji sukasi greičiau – robotas sukasi **kairėn**.
- Jei viena pusė sukasi pirmyn, o kita atgal – robotas **sukasi vietoje**.

### Santrauka

| Tipas | Kas tai? | Kiekis | Ką daro? |
|-------|----------|--------|----------|
| **DistanceSensor** (sensorius) | Atstumo sensorius | 2 vnt. | Matuoja atstumą iki kliūties priešais |
| **RotationalMotor** (aktuatorius) | Rato variklis | 4 vnt. | Suka ratus, kad robotas judėtų |

---

## Kaip veikia originalus kontroleris?

Originalus kontroleris parašytas C programavimo kalba. Jo logika labai paprasta:

1. **Paleisties metu:** robotas inicializuoja sensorius ir variklius.
2. **Kiekvieną kadrą (kas 64 ms):**
   - Robotas pradeda su numatytuoju greičiu – abu pusės juda pirmyn (greitis = 1.0).
   - Jei kliūties vengimo skaitliukas aktyvus (>0) – robotas sukasi vietoje (kairė pusė pirmyn, dešinė atgal).
   - Jei skaitliukas = 0, tai robotas nuskaito sensorius. Jei bet kuris rodo mažiau nei 950 – reiškia kliūtis, ir skaitliukas nustatomas į 100 (t.y. robotas suktis 100 kadrų = 6.4 sekundes).

**Paprasčiau tariant:** robotas važiuoja tiesiai, kol pajunta kliūtį. Tada 6 sekundes sukasi vietoje ir vėl bando važiuoti tiesiai.

---

## Ką aš pakeičiau? (Modifikacijos)

### 1. Perrašiau iš C į Python

Python kodas yra paprastesnis ir trumpesnis. Vietoj sudėtingų C masyvų ir ciklų – paprastos Python eilutės:

```python
# C buvo: WbDeviceTag ds[2]; ... for loop ...
# Python:
ds_left = robot.getDevice("ds_left")
ds_left.enable(TIME_STEP)
```

### 2. Pridėjau proporcingą greičio valdymą

**Originalas:** robotas reaguoja kaip jungiklis – arba juda, arba sukasi. Jokio tarpinio varianto.

**Mano versija:** robotas reaguoja **proporcingai** – kuo arčiau kliūtis, tuo stipriau ir greičiau sukasi, o kuo toliau – tuo švelniau:

```python
# Artumas: 0.0 = toli, 1.0 = labai arti
left_proximity = max(0.0, (THRESHOLD - left_val) / THRESHOLD)
# Greitis mažėja proporcingai artumui
base_speed = MAX_SPEED * (1.0 - max(left_proximity, right_proximity) * 0.7)
```

Tai panašiau į tai, kaip važiuotų tikras robotas – ne staigiai sustoja ir sukasi, o palaipsniui lėtina ir švelniai pasuka.

### 3. Pridėjau atsitiktinį klaidžiojimą

**Originalas:** robotas visada juda tiesiai, kol atsitrenkia į sieną. Tada sukasi ir vėl tiesiai. Jis „tyrinėja" tik labai mažą arenos dalį.

**Mano versija:** kai robotas nemato kliūčių, jis kas 30-80 žingsnių atsitiktinai šiek tiek keičia kryptį. Taip jis tyrinėja didesnę teritoriją, o ne tik važiuoja pirmyn-atgal.

### 4. Pridėjau sensorių reikšmių spausdinimą

Dabar konsolėje matosi, ką robotas „mato":
```
[Žingsnis 100] Kairys: 987.3, Dešinys: 654.2
  >> Kliūties vengimas! L:0.00 R:0.31
```

### 5. Pakeičiau areną

- Roboto spalva pakeista iš raudonos į **mėlyną**.
- Arenoje pridėti **3 nauji objektai** (oranžinė dėžutė, žalias cilindras, geltonas stačiakampis) ir **kamuolys**, kurį robotas gali pastumti.

---

## Failų struktūra

```
uzd2/
└── 4_1_pavyzdys/
    ├── controllers/
    │   └── four_wheels_modified/
    │       └── four_wheels_modified.py    ← Modifikuotas kontroleris (Python)
    └── worlds/
        └── collision_avoidance_modified.wbt ← Modifikuotas pasaulio failas
```

## Kaip paleisti

1. Atidaryti Webots
2. `File → Open World...`
3. Pasirinkti `uzd2/4_1_pavyzdys/worlds/collision_avoidance_modified.wbt`
4. Paspausti ▶ (Play) simuliacijos paleidimui
5. Stebėti robotą ir konsolės pranešimus Webots lange
