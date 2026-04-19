# 3.2.1 – scikit-learn k-NN – Paaiškinimas

## Kas čia vyksta paprastais žodžiais?

Įsivaizduok, kad turi parduotuvę su gėlėmis ir gauni naują gėlę, bet nežinai, 
kokia ji. Tu turi seną katalogą su 150 gėlių, kur kiekviena yra išmatuota 
(lapelių ilgis, plotis ir t.t.) ir pažymėta kokiai rūšiai priklauso.

**k-NN algoritmas daro būtent tai** – pažiūri į savo "katalogą" ir sako: 
"Ši nauja gėlė labiausiai panaši į šitas 5 gėles iš katalogo, ir 4 iš jų 
yra rožės, tai greičiausiai ir ši yra rožė!"

## Iris duomenų rinkinys

Mes naudojame garsų "Iris" (Vilkdalgių) duomenų rinkinį:
- **150 gėlių** iš viso
- **3 rūšys**: Setosa, Versicolor, Virginica (po 50 kiekvienoje)
- **4 matavimai** kiekvienai gėlei: taurėlapio ilgis/plotis ir vainiklapio ilgis/plotis

## Kas vyksta kode žingsnis po žingsnio?

### 1. Užkrauname duomenis
Tiesiog pasiimame tą gėlių katalogą su visais matavimais ir pavadinimais.

### 2. Padalijame duomenis
Paimame 150 gėlių ir daliname:
- **105 gėles (70%)** – tai mūsų "katalogas", iš kurio mokysimės
- **45 gėles (30%)** – tai "naujos gėlės", kuriomis patikrinsime, ar algoritmas veikia

Kodėl taip? Nes jei tikrintume tais pačiais duomenimis, kuriais mokėmės – 
tai būtų kaip nusirašyti nuo savęs. Reikia tikrinti su naujais, nematytais duomenimis.

### 3. Standartizuojame (lyginame matavimus)
Įsivaizduok, kad vienas matavimas yra centimetrais (pvz., 5.1 cm), 
o kitas – milimetrais (pvz., 35 mm). Tada milimetrai "užgožtų" centimetrus, 
nes skaičiai didesni.

Standartizacija padaro taip, kad visi matavimai būtų "vienodai svarbūs" – 
kiekvieną paverčia į tokį skaičių, kur 0 reiškia "vidutinis", +1 reiškia 
"vienas žingsnis aukščiau vidutinio" ir t.t.

### 4. Treniruojame modelį
k-NN atveju "treniravimas" yra labai paprastas – tiesiog **įsimena visas 
105 gėles**. Nieko neskaičiuoja, nieko neoptimizuoja. Todėl sakoma, kad 
k-NN yra "tingus" (lazy) algoritmas.

### 5. Prognozuojame
Kiekvienai iš 45 "naujų" gėlių algoritmas:
1. Apskaičiuoja atstumą iki visų 105 gėlių kataloge
2. Pasirenka **5 artimiausias** (k=5)
3. Pažiūri, kokiai rūšiai dauguma iš tų 5 priklauso
4. Priskiria tą rūšį

### 6. Tikriname tikslumą
Palyginame algoritmo spėjimus su tikrosiomis rūšimis. 
Rezultatas: **91.1% tikslumas** su k=5. Tai reiškia, kad iš 45 gėlių 
algoritmas teisingai atpažino 41.

### 7. Eksperimentuojame su k
Bandėme skirtingas k reikšmes (kiek kaimynų žiūrėti):
- k=1 (žiūri tik artimiausią) → 93.3%
- k=5 (žiūri 5 artimiausius) → 91.1%
- k=9 (žiūri 9 artimiausius) → **95.6%** ← geriausias!

Mažas k = jautrus klaidoms (vienas neteisingas kaimynas viską sugadina).
Didelis k = stabilesnis, bet gali "suglotninti" ribas tarp rūšių.

## Ko galime iš to pasimokyti?

k-NN yra vienas paprasčiausių mašininio mokymosi algoritmų, bet jis parodo 
pagrindinę idėją: **panašūs dalykai turėtų turėti panašias savybes**. 
Jei gėlė panaši į rožę – greičiausiai tai yra rožė. Ta pati logika taikoma 
rekomenduojant filmus, atpažįstant ligų simptomus ar prognozuojant orus.
