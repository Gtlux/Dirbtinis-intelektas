# 3.2.2 – PyTorch MNIST – Paaiškinimas

## Kas čia vyksta paprastais žodžiais?

Įsivaizduok, kad mokai mažą vaiką atpažinti skaitmenis. Rodai jam tūkstančius 
kortelių su ranka parašytais skaitmenimis (0, 1, 2, ... 9) ir kiekvieną kartą 
sakai: "Tai yra 7", "Tai yra 3" ir t.t. Po kurio laiko vaikas išmoksta ir 
gali pats atpažinti naujus skaitmenis, kurių niekada nematė.

**Neuroninis tinklas daro lygiai tą patį** – žiūri į 60,000 paveikslėlių, 
mokosi juos atpažinti, ir paskui gali atpažinti naujus, nematytus skaitmenis.

## MNIST duomenys

MNIST – tai garsus duomenų rinkinys, kuriame yra:
- **60,000 paveikslėlių mokymui** (kaip vadovėlis)
- **10,000 paveikslėlių testavimui** (kaip egzaminas)
- Kiekvienas paveikslėlis yra **28×28 pikselių** mažas pilkas kvadratėlis
- Kiekviename nupieštas vienas **skaitmuo nuo 0 iki 9**

## Kas yra neuroninis tinklas?

Neuroninis tinklas – tai programa, kuri imituoja, kaip veikia smegenys. 
Ji susideda iš "neuronų" – mažų skaičiuotuvų, sujungtų tarpusavyje.

Mūsų tinklas atrodo taip:

```
Paveikslėlis (28×28 = 784 pikseliai)
         ↓
    [Ištiesinimas]     ← Paverčia 2D paveikslėlį į vieną ilgą eilutę
         ↓
   [128 neuronai]      ← "Smegenys" – ieško raštų (linijų, kreivių)
         ↓
     [Dropout]         ← Atsitiktinai "išjungia" 20% neuronų (kad nepersimoktų)
         ↓
    [10 neuronų]       ← Kiekvienas atsako už vieną skaitmenį (0-9)
         ↓
    ATSAKYMAS: "Tai yra 7!"
```

### Kaip tai veikia?

1. **Ištiesinimas**: 28×28 pikselių tinklelis paverčiamas į 784 skaičių eilutę. 
   Kiekvienas skaičius reiškia, kiek tamsus yra vienas pikselis (0 = baltas, 1 = juodas).

2. **128 neuronų sluoksnis**: Kiekvienas iš 128 neuronų gauna visus 784 pikselius 
   ir "ieško" kažkokio rašto. Vienas gal atpažįsta horizontalią liniją, kitas – 
   apvalią kilpą, trečias – kampą. Šie raštai padeda atskirti skaitmenis.

3. **Dropout**: Mokymosi metu atsitiktinai "išjungiame" 20% neuronų. 
   Kodėl? Kad tinklas neišmoktų atsakymų "mintinai" (kaip studentas, kuris 
   išmoksta tik konkrečius klausimus, o ne supranta temą). Tai priverčia 
   kiekvieną neuroną būti naudingą savarankiškai.

4. **10 išėjimo neuronų**: Kiekvienas atsako už savo skaitmenį. 
   Jei rodome "7", tai 7-asis neuronas turėtų "sužibėti" labiausiai.

## Kaip tinklas mokosi?

Mokymasis vyksta **5 epochomis** (5 kartus peržiūri visus 60,000 paveikslėlių):

| Epocha | Ką daro | Tikslumas |
|--------|---------|-----------|
| 1 | Pirmas praėjimas – dar daug klysta | 91.4% |
| 2 | Pradeda geriau matyti raštus | 95.6% |
| 3 | Tobulėja toliau | 96.5% |
| 4 | Jau labai gerai | 97.2% |
| 5 | Beveik tobulas | 97.4% |

Kiekvieną epochą vyksta toks ciklas:
1. **Pirmyn**: Parodome paveikslėlį → tinklas spėja atsakymą
2. **Klaida**: Palyginame su teisingu atsakymu → apskaičiuojame klaidą
3. **Atgal**: "Pasakome" kiekvienam neuronui, kiek jis prisidėjo prie klaidos
4. **Taisymas**: Kiekvienas neuronas truputį pasikeičia, kad kitą kartą klystų mažiau

Šis procesas kartojamas 60,000 × 5 = **300,000 kartų**!

## Galutinis tikslumas

Po 5 epochų mokymosi, patikriname su 10,000 **naujų, nematytų** paveikslėlių:

**Tikslumas: 97.7%** – iš 10,000 skaitmenų tinklas teisingai atpažino 9,770!

Pirmos 5 prognozės:
- Paveikslėlis #1: Tinklas sako "7" → Tikrai yra 7 ✓ (100% tikras)
- Paveikslėlis #2: Tinklas sako "2" → Tikrai yra 2 ✓ (98.7% tikras)
- Paveikslėlis #3: Tinklas sako "1" → Tikrai yra 1 ✓ (99.8% tikras)

## Kodėl tai yra svarbu?

Šis paprastas pavyzdys yra **"Hello World" giluminio mokymosi pasaulyje**. 
Ta pati technologija, tik daug sudėtingesnė, naudojama:
- **Veido atpažinime** (telefonų atrakinimas)
- **Autonominiuose automobiliuose** (kelio ženklų skaitymas)
- **ChatGPT ir panašiuose AI** (teksto supratimas ir generavimas)
- **Medicinoje** (vėžio ląstelių atpažinimas nuotraukose)

## Pastaba apie TensorFlow vs PyTorch

Užduotyje prašoma naudoti TensorFlow, bet jis nepalaiko mūsų Python versijos (3.14). 
Todėl naudojome **PyTorch** – tai antra pagal populiarumą giluminio mokymosi biblioteka. 
Abi daro tą patį dalyką – kuria ir treniruoja neuroninius tinklus. 
Architektūra (Flatten → Dense → Dropout → Dense) yra **visiškai tokia pati** 
kaip būtų TensorFlow versijoje.
