# -*- coding: utf-8 -*-
"""BookNLP.ipynb

Automatiškai sugeneruota iš Colab.

Originalus failas:
    https://colab.research.google.com/drive/1JTWPWybrq_TAUfHckIB0dTpeaC1cv_8K

🎧 **Garso įvadas**

> *Pirmą kartą čia? Garso gidas viską paaiškina prieš pradedant.*

<audio controls>
  <source src="https://raw.githubusercontent.com/aalgirdas/novel-semantic-parsing/main/assets/audio/BookNLP_1_book text corpus.wav" type="audio/wav">
</audio>

#  <img src="https://www.gutenberg.org/gutenberg/pg-logo-129x80.png" width=50 height=50> <font color='Green'>Book NLP </font>

<font color='Green'> Knygų tekstų paruošimas ir anotavimas iš tokių projektų kaip Gutenberg ir FadedPage. <br>
   [gutenberg ](https://www.gutenberg.org)     
   [fadedpage ](https://www.fadedpage.com)      <br>
   </font>

---

## 🇱🇹 Kas yra šis sąsiuvinis?

Šis sąsiuvinis yra **pirmasis žingsnis** iš trijų.
Jo užduotis – pasiimti knygos tekstą iš interneto, suskaidyti jį
į **pastraipas** ir **skyrius**, pažymėti, kur yra **dialogai** (kur veikėjai kalba),
ir viską išsaugoti kaip lentelę, kurią naudos kiti du sąsiuviniai.

**Paprasčiau:** Įsivaizduokite, kad turite popierinę knygą ir norite ją paruošti
kompiuteriui. Ši programa tą knygą „nuskenuoja", suskaido į dalis,
pažymi kur kas kalba, ir viską sudeda į tvarkingą lentelę (panašią į Excel).

### Ką gauname rezultate:
- `df_paragraphs` – lentelė, kur kiekviena eilutė = viena pastraipa su skyriaus numeriu
- `df_chapters_info` – lentelė su skyrių pavadinimais ir žodžių skaičiais
- TSV failas Google Drive – išsaugota lentelė, kurią naudos kiti sąsiuviniai

### Darbo eiga:
1. Pasirenkame knygą ir nustatome jos parametrus
2. Sukuriame aplankus Google Drive
3. Nuskaitome knygos tekstą ir suskaidome į pastraipas
4. Atpažįstame skyrių ribas
5. Pažymime, kur yra dialogai
6. Išsaugome rezultatus
"""

# ============================================================
# TOMO PASIRINKIMAS
# Pasirenkame „lentyną" (Vol2), kurioje saugosime knygos duomenis.
# Jei dirbame su keliomis knygomis, kiekvienai galime skirti atskirą tomą.
# ============================================================
Vol = 'Vol2'

"""## Pasiruošimas darbui

Čia prijungiame visus reikalingus įrankius ir prisijungiame prie Google Drive
(tai kaip debesies „kietas diskas", kur saugosime savo darbo rezultatus).
Taip pat atsisiunčiame knygų sąrašą iš interneto – tai žinynas, kuriame jau yra
informacija apie anksčiau apdorotas knygas.
"""

#@title Imports 🤝 Google Drive

from google.colab import files, drive  # Prisijungimas prie Google Colab ir Drive
import pandas as pd          # Lentelių kūrimo įrankis (panašu į Excel)
import urllib.request          # Failų atsisiuntimas iš interneto
import os.path                 # Failų ir aplankų tikrinimas
import re                      # Teksto šablonų paieška (pvz., rasti žodį „Chapter")
import requests                # Duomenų gavimas iš interneto puslapių
import json                    # Struktūruotų duomenų skaitymas/rašymas


# Tikriname, ar Google Drive jau prijungtas. Jei ne – prijungiame.
# Drive naudojame kaip saugyklą failams tarp sąsiuvinių.
if os.path.isdir('/content/drive/MyDrive'):
    print('Google Drive is mounted.')
else:
    drive.mount('/content/drive')




# Atsisiunčiame „knygų katalogą" iš interneto.
# Tai žinynas su visų anksčiau apdorotų knygų nustatymais
# (pavadinimas, kodas, kaip atpažinti skyrius ir t.t.).
response = requests.get("https://raw.githubusercontent.com/aalgirdas/novel-semantic-parsing/refs/heads/main/file_path_dic.json")
file_path_dic = json.loads(response.text)  # Paverčiame tekstą į Python žodyną
print("on github #books:", len(file_path_dic))


# Kur saugosime knygų žinynus Google Drive
file_path_for_json = f'/content/drive/MyDrive/Book_Info/file_path_dic.json'
file_path_rev_json = f'/content/drive/MyDrive/Book_Info/file_path_rev_dic.json'

# Jei jau turime ankstesnę žinyno kopiją Drive – sujungiame ją su interneto versija.
# Taip neprarandame savo anksčiau pridėtų knygų.
if os.path.exists(file_path_for_json):
    with open(file_path_for_json, 'r') as file:
        file_path_tmp = json.load(file)

    file_path_dic.update(file_path_tmp)  # Sujungiame žinynus
    print(f"file_path_dic updated. #books: {len(file_path_dic)}")

"""## Aplankų sukūrimas

Sukuriame tvarkingą aplankų struktūrą Google Drive – tai kaip spintelė
su atskirais stalčiais kiekvienam duomenų tipui.
Jei aplankai jau egzistuoja – nieko blogo neatsitiks.
"""

# Pagrindiniai aplankai
os.makedirs('/content/drive/MyDrive/Book_Info', exist_ok=True)              # Šakninis aplankas
os.makedirs(f'/content/drive/MyDrive/Book_Info/{Vol}', exist_ok=True)       # Tomo aplankas

# Aplankai konkretiems duomenų tipams
os.makedirs(f'/content/drive/MyDrive/Book_Info/{Vol}/book_words', exist_ok=True)       # Žodžių analizei
os.makedirs(f'/content/drive/MyDrive/Book_Info/{Vol}/cyborg_scene_info', exist_ok=True) # Scenų aprašymams
os.makedirs(f'/content/drive/MyDrive/Book_Info/{Vol}/book_text', exist_ok=True)        # Knygos tekstui
os.makedirs(f'/content/drive/MyDrive/Book_Info/{Vol}/gpt4_scene_info', exist_ok=True)  # GPT-4 scenoms
os.makedirs(f'/content/drive/MyDrive/Book_Info/{Vol}/ollama_scene_info', exist_ok=True) # Ollama scenoms

# Laikini aplankai tarpiniams rezultatams
os.makedirs(f'/content/drive/MyDrive/Book_Info/{Vol}/tmp', exist_ok=True)
os.makedirs(f'/content/drive/MyDrive/Book_Info/{Vol}/tmp/stanza', exist_ok=True)
os.makedirs(f'/content/drive/MyDrive/Book_Info/{Vol}/tmp/wordnet', exist_ok=True)
os.makedirs(f'/content/drive/MyDrive/Book_Info/{Vol}/tmp/webots', exist_ok=True)
os.makedirs(f'/content/drive/MyDrive/Book_Info/{Vol}/tmp/masked', exist_ok=True)

"""<br><br><br><br>

---

## 1. Knygos pasirinkimas

Pasirenkame, kurią knygą norime analizuoti.
- Kai `just_test = True` – naudojama testinė knyga „Baskervilių šuo" (Šerloko Holmso nuotykis)
- Kai `just_test = False` – galima įrašyti bet kurią kitą knygą

Taip pat tikrinama, ar ši knyga jau buvo anksčiau apdorota (ieškoma žinyne).
"""

#@title 1.1 📖 Choose a book and its attributes (chapter_regex). { run: "auto" }
'''
https://www.gutenberg.org/ebooks/bookshelf/645?start_index=76
https://en.wikipedia.org/wiki/The_Big_Read

'''

# just_test = True → naudojame testinę knygą „Baskervilių šuo"
# just_test = False → galime pasirinkti savo knygą
just_test = True # If you want just test

if just_test:
    # Testinis režimas – Šerloko Holmso knyga iš Gutenberg svetainės (kodas 2852)
    book_name = "THE HOUND OF THE BASKERVILLES"
    book_code = "2852"              # Unikalus knygos numeris Gutenberg svetainėje
    file_encoding_scheme = "utf-8"   # Teksto koduotė
else:
    # Čia galima įrašyti bet kurią kitą knygą
    book_name = "To Kill a Mockingbird"
    book_code = "wget_"+ book_name.replace(' ', '_')  # Sukuriamas kodas iš pavadinimo
    print(book_code)
    file_path = "file:///content/To Kill a Mockingbird.txt"  # Failo vieta
    file_encoding_scheme = "utf-8"  # utf-8  windows-1252

    # Sukuriame pagalbinį žinyną: kodas → pavadinimas
    bcode_bname_dict = {v['book_code']: {'book_name': k} for k, v in file_path_dic.items()}

    # Tikriname, ar knyga jau yra žinyne
    if book_name in file_path_dic :
        print(f"\033[91m book_name found: '{book_name}' {book_code}     {file_path_dic[book_name]}   \033[0m")
    if book_code in bcode_bname_dict:
        print(f"\033[38;5;208m book_code found: '{book_name}' {book_code}     {bcode_bname_dict[book_code]}  \033[0m")

    # Ieškome dalinio atitikmens (pvz., „Mockingbird" rastų „To Kill a Mockingbird")
    partial_matches = [    key for key in file_path_dic    if book_name.lower() in key.lower() ] # partial‐match lookup # collect all keys in which your book_name is a substring (case–insensitive)
    if partial_matches:
        for key in partial_matches:
            print(f"\033[38;5;170m Partial name match for {book_name}  →  key: {key!r}, value: {file_path_dic[key]} \033[0m")

"""## Knygos nustatymų konfigūracija

Čia nurodome programai „taisykles", kaip dirbti su konkrečia knyga:
- **Skyriaus šablonas** – kaip atpažinti skyriaus antraštę tekste (pvz., eilutė „Chapter 1...")
- **Pradžios/pabaigos žymės** – kur prasideda ir baigiasi tikrasis knygos tekstas
  (Gutenberg failuose prieš ir po knygos yra teisinė informacija, kurios mums nereikia)
- **Teksto pakeitimai** – pvz., pakeisti vienas kabutes dvigubomis

Tai kaip instrukcija programai: „skaityti nuo čia iki čia, skyrius atpažinti pagal šį šabloną".
"""

# if our book parameters are not described in the GitHub portal file file_path_dic.json then we can describe them here

if just_test:
    # Testinio režimo nustatymai
    # Skyriaus šablonas atpažįsta „Chapter 1. ..." tipo eilutes
    file_path_dic_tmp =  {
            book_name: {
            "book_code": book_code ,
            "chapter_regex": r'Chapter (\d+)\..*',  # Šablonas: „Chapter" + skaičius + taškas
            "Vol":Vol
        }
    }

else:
    # Pilno režimo nustatymai su daugiau galimybių
    file_path_dic_tmp =  {

        book_name: {
        #"useWget": True,
        #"wgetURL": r"https://lib.ru/ILFPETROV/ilf_petrov_12_chairs_engl.txt",  #
        "book_code": book_code ,
        #"stringReplaceDic": {  "^'": '"', "' ": '" ', "'$": '"' , " '": ' "' }, #  stringReplaceDic": { r"<.*?>": "" }     "stringReplaceDic": {  "^—": '"' },   #"stringReplaceDic": {   "\u201c":"'", "\u201d":"'" },        #"stringReplaceDic": {  "^'": '"', "' ": '" ', "'$": '"' , " '": ' "' , "\\[\\d{1,2}\\]":"" },      #"stringReplaceDic": { "—":" ",  "^'": "\u201c", "' ": "\u201c ", "'$": "\u201d" , " '": " \u201c" },
        "chapter_regex": r'^Chapter \d{1,3}$',  # CHAPTER [IVXLC]+ .*   \d{1,2}\.      [A-Za-z_★•—_'\u201c\u201d\u2018 \-:]{3,65}    [ivxl]+   ^[A-Za-z ]{23,65}$   ^NO CHAPTERS$
        #"start_line": r'0',    # r'0' It can be str or int .   If int then line number will be match if str then string match for first line start (it may be not the whole line).
        #"end_line": r'0' ,
        #"new_paragraph_str": r'     ',    #
        "file_path": file_path ,
        "Vol":Vol
        }

    }


# Atnaujiname knygų žinyną su mūsų knygos nustatymais
file_path_dic.update(file_path_dic_tmp)

# Ištraukiame konkrečios knygos nustatymus
book_dic = file_path_dic.get(book_name)
chapter_regex = book_dic.get("chapter_regex")  # Šablonas skyriams atpažinti

# Pradžios ir pabaigos žymės – programa skaitys tik tarp jų esantį tekstą
# (Gutenberg failuose prieš/po knygos teksto yra teisinė informacija)
start_line = book_dic.get('start_line', '*** START OF THE PROJECT GUTENBERG')
end_line = book_dic.get('end_line', '*** END OF THE PROJECT GUTENBERG EBOOK')
new_paragraph_str = book_dic.get('new_paragraph_str', '')

# Numatytasis knygos adresas internete (pagal Gutenberg kodą)
file_path_default = 'https://www.gutenberg.org/cache/epub/'+book_code+'/pg'+book_code+'.txt'
file_path = book_dic.get('file_path', file_path_default)

# Jei knyga turi būti atsisiųsta iš kito šaltinio
if book_dic.get('useWget', False):
    wgetURL = book_dic.get('wgetURL')
    #!wget $wgetURL

    from urllib.parse import urlparse
    import pathlib
    filename = os.path.basename(urlparse(wgetURL).path)
    full_path = os.path.abspath(filename)
    file_path = pathlib.Path(full_path).as_uri()

    print(f"from wget file name: {filename}     full path: {full_path}      file_path {file_path}" )


# Teksto pakeitimo taisyklės (jei reikia sutvarkyti kabutes ar kitus simbolius)
stringReplaceDic = book_dic.get("stringReplaceDic",{})

print(f'{book_name} {book_code}    {len(file_path_dic)}    chapter_regex={chapter_regex}   start_line={start_line}  stringReplaceDic={stringReplaceDic}    \nfile_path={file_path} \n')

"""## Žinynų išsaugojimas

Išsaugome knygų žinynus į Google Drive, kad kitą kartą paleidus programą
nereikėtų visko konfigūruoti iš naujo. Sukuriame ir atvirkštinį žinyną
(pagal kodą galima rasti knygos pavadinimą).
"""

# Atvirkštinis žinynas: kodas → pavadinimas (pvz., „2852" → „Baskervilių šuo")
bcode_bname_dict = {v['book_code']: {'book_name': k} for k, v in file_path_dic.items()}
with open(file_path_rev_json, 'w') as file:
    json.dump(bcode_bname_dict, file, indent=4)

# Pagrindinis žinynas – išsaugome atnaujintą versiją
with open(file_path_for_json, 'w') as file:
    json.dump(file_path_dic, file, indent=4)

"""## Pastraipų ir skyrių lentelių kūrimas

Čia yra šio sąsiuvinio **pagrindinė dalis** – keturios funkcijos, kurios:
1. Nuskaito knygos tekstą iš interneto
2. Praleidžia nereikalingą teisinę informaciją pradžioje ir pabaigoje
3. Sujungia eilutes į pastraipas (nauja pastraipa prasideda po tuščios eilutės)
4. Atpažįsta skyrių antraštes ir viską sudeda į lenteles
"""

#@title 1.2 Let's create a dataframe tables: df_paragraphs and df_chapters_info

# ============================================================
# FUNKCIJA 1: Knygos teksto nuskaitymas (testinis režimas)
# ============================================================
# Ši funkcija atidaro knygą internete ir skaito ją eilutė po eilutės.
# Ji praleidžia Gutenberg teisinę informaciją pradžioje (iki „*** START...")
# ir sustoja prieš pabaigos teisinę dalį (ties „*** END...").
# Tai kaip atversti knygą nuo pirmo skyriaus ir skaityti iki paskutinio,
# praleidžiant viršelio ir autoriaus teisių puslapius.
def get_book_good_lines_just_test(file_path, start_line, end_line, new_paragraph_str):

    good_lines = []             # Apkarpytos eilutės (be tarpų pradžioje/pabaigoje)
    good_lines_no_strip = []    # Originalios eilutės (su visais tarpais)
    b_add_line = False          # Ar jau radome teksto pradžią?
    file = urllib.request.urlopen(file_path)  # Atidarome knygą internete
    for index, line in enumerate(file):
      try:
        line_no_strip = line.decode('utf-8')  # Paverčiame kompiuterio baitus į skaitomą tekstą
      except:
        continue  # Jei nepavyksta perskaityti – praleidžiame tą eilutę

      # Jei nustatytas specialus naujos pastraipos ženklas – pridedame tuščią eilutę
      if len(new_paragraph_str)>0 and line_no_strip.startswith(new_paragraph_str):
        good_lines.append('')
        good_lines_no_strip.append('')

      line = line_no_strip.strip()  # Pašaliname tarpus iš eilutės pradžios ir pabaigos

      # Ieškome pradžios žymės (pvz., „*** START OF THE PROJECT GUTENBERG")
      if isinstance(start_line, str):
        if line.startswith(start_line) and (not b_add_line):
          b_add_line = True  # Radome pradžią! Nuo čia pradedame rinkti tekstą
          continue
      else:
        if index == start_line and (not b_add_line):
          b_add_line = True
          continue

      if (not b_add_line):
        continue  # Dar neradome pradžios – praleidžiame



      # Tikriname, ar pasiekėme pabaigos žymę
      if line.startswith(end_line) and (b_add_line):
           break  # Pabaiga – stabdome skaitymą

      good_lines.append(line)
      good_lines_no_strip.append(line_no_strip)


    file.close()

    return good_lines, good_lines_no_strip  # Grąžiname nuskaitytas eilutes



# ============================================================
# FUNKCIJA 2: Knygos teksto nuskaitymas (pilna versija)
# ============================================================
# Paprastesnė versija – tiesiog nuskaito VISAS eilutes be jokio filtravimo.
# Naudojama kai failas jau „švarus" (pvz., jūsų pačių įkeltas tekstas).
def get_book_good_lines(file_path ):

    good_lines = []
    good_lines_no_strip = []

    file = urllib.request.urlopen(file_path)
    for index, line in enumerate(file):
      try:
        line_no_strip = line.decode(file_encoding_scheme)
      except:
        continue

      line = line_no_strip.strip()

      good_lines.append(line)
      good_lines_no_strip.append(line_no_strip)


    file.close()

    return good_lines, good_lines_no_strip



# ============================================================
# FUNKCIJA 3: Eilučių sujungimas į pastraipas
# ============================================================
# Knygos tekstas yra suskaidytas į trumpas eilutes. Ši funkcija jas sujungia
# į prasmingus paragrafus/pastraipas. Nauja pastraipa prasideda po tuščios eilutės.
#
# Svarbi detalė: pastraipa ribojama iki 400 žodžių, kad vėliau dirbtinio
# intelekto modelis (BERT, kurio limitas 512 žodžių) galėtų ją pilnai apdoroti.
def get_book_paragraph_lines(good_lines, good_lines_no_strip, stringReplaceDic):
    paragraph_lines = []   # Galutinis pastraipų sąrašas
    joined_lines = ''      # Dabartinė kuriama pastraipa

    for line, line_no_strip in zip(good_lines, good_lines_no_strip):
      # Jei yra teksto pakeitimo taisyklės – pritaikome jas
      for old, new in stringReplaceDic.items():
        line = re.sub(old, new, line)

      # Jei eilutė ne tuščia IR pastraipa dar neviršija 400 žodžių – pridedame
      if len(line)>0 and len(joined_lines.split())<400:
        joined_lines += line + ' '
      else:
        # Tuščia eilutė arba viršytas žodžių limitas – baigiame pastraipą
        if len(joined_lines)>0:
          paragraph_lines.append(joined_lines.rstrip())
          joined_lines = ''  # Pradedame naują pastraipą

    # Pridedame paskutinę pastraipą, jei ji liko nepridėta
    if len(joined_lines.strip())>0:
      paragraph_lines.append(joined_lines.rstrip())
      joined_lines = ''

    return paragraph_lines


# ============================================================
# FUNKCIJA 4: Lentelių su pastraipomis ir skyriais sukūrimas
# ============================================================
# Eina per visas pastraipas ir kiekvienai tikrina: ar tai skyriaus pavadinimas?
# - Jei taip (pvz., „Chapter 1. ...") – padidina skyriaus numerį
# - Jei ne – prideda pastraipą į lentelę su atitinkamu skyriaus numeriu
def get_book_paragraphs_df(paragraph_lines, chapter_regex):
    chapter_nr = 0  # Dabartinis skyriaus numeris
    df_paragraphs = pd.DataFrame(columns=['paragraph','chapter', 'is_speech'])     # Pastraipų lentelė
    df_chapters_info = pd.DataFrame(columns=['chapter','chapter_name'])            # Skyrių lentelė

    for line in paragraph_lines:
      match = re.match(chapter_regex, line)  # Ar ši eilutė yra skyriaus antraštė?
      if match:
        chapter_nr += 1  # Naujas skyrius!
        df_chapters_info = pd.concat([df_chapters_info, pd.DataFrame({ 'chapter': [chapter_nr]  , 'chapter_name': [line]  }) ], ignore_index=True)
        continue  # Antraštė nėra pastraipa – praleidžiame

      # Paprasta pastraipa – įdedame į lentelę
      df_paragraphs = pd.concat([df_paragraphs, pd.DataFrame({ 'paragraph': [line] , 'chapter': [chapter_nr] , 'is_speech':0 })], ignore_index=True)


    return df_paragraphs, df_chapters_info


# ============================================================
# FUNKCIJŲ PALEIDIMAS
# ============================================================

# 1 žingsnis – nuskaitome knygos eilutes iš interneto
if just_test:
    good_lines, good_lines_no_strip = get_book_good_lines_just_test(file_path, start_line,end_line,new_paragraph_str) # old version
else:
    good_lines, good_lines_no_strip = get_book_good_lines(file_path)

# 2 žingsnis – sujungiame eilutes į pastraipas
paragraph_lines = get_book_paragraph_lines(good_lines, good_lines_no_strip,stringReplaceDic)

# 3 žingsnis – sukuriame lenteles su skyriais
df_paragraphs, df_chapters_info = get_book_paragraphs_df(paragraph_lines, chapter_regex)

# Atspausdiname kiek eilučių, pastraipų ir skyrių turi knyga
print(f'Book has {len(good_lines)} lines , {len(paragraph_lines)} paragraphs and {df_chapters_info.shape[0]} chapters')

"""## Žodžių skaičiavimas pagal skyrius

Suskaičiuojame, kiek žodžių yra kiekviename skyriuje, ir pridedame
tą informaciją prie skyrių lentelės. Tai naudinga sužinoti,
kurie skyriai ilgesni, o kurie trumpesni.
"""

# Skaičiuojame žodžius kiekviename skyriuje
word_count_per_chapter = df_paragraphs.groupby('chapter')['paragraph'].apply(lambda x: x.str.split().str.len().sum()).reset_index(name='word_count')
# Prijungiame žodžių skaičius prie skyrių lentelės
df_chapters_info = pd.merge(df_chapters_info, word_count_per_chapter, on='chapter', how='left')
df_chapters_info

"""## Duomenų peržiūra

Atspausdiname pirmas ir paskutines 5 pastraipas, kad patikrintume
ar viskas teisingai nuskaityta ir suskaidyta.
"""

print(df_paragraphs.head(5).to_markdown())  # Pirmos 5 pastraipos
print(df_paragraphs.tail(5).to_markdown())  # Paskutinės 5 pastraipos

"""## Dialogų aptikimas

Ši dalis yra labai svarbi – ji atpažįsta, kur knygoje veikėjai **kalba**
(tekstas kabutėse, pvz.: „Sveiki!" – tarė jis) ir kur yra **autoriaus pasakojimas**.

Kiekviena pastraipa gauna žymą:
- `is_speech = 0` → tik pasakojimas (autorius pasakoja kas vyksta)
- `is_speech = 1` → tik dialogas (veikėjas kalba)
- `is_speech = 2` → mišri pastraipa (ir veikėjas kalba, ir autorius pasakoja)

**Paprasčiau:** Tai kaip dramaturgas pažymi scenarijuje – kur aktorius turi kalbėti,
o kur yra sceninės pastabos.
"""

#@title Let's mark the paragraphs that contain dialogue language


# ============================================================
# Kabučių tvarkymo funkcija
# ============================================================
# Pakeičia paprastas kabutes (") į „gražias" kabutes – atidarančias „ ir uždarančias ".
# Tai būtina, kad programa suprastų, kur dialogas prasideda ir kur baigiasi.
# Veikia kaip perjungiklis: pirma kabutė = dialogas prasideda, antra = baigiasi.
def replace_quotes(input_string):
    new_string = ""
    quote_count = 0
    for char in input_string:
        if char == '"':
            quote_count += 1
            if quote_count % 2 == 1:  # Nelyginė kabutė = dialogo pradžia
                new_string += '\u201c'
            else:                     # Lyginė kabutė = dialogo pabaiga
                new_string += '\u201d'
        else:
            new_string += char
    return new_string


# ============================================================
# Dialogo ir pasakojimo atskyrimo funkcija
# ============================================================
# Paima pastraipą ir atskiria: kas yra kabutėse (dialogas) ir kas ne (pasakojimas).
# Pavyzdžiui:
#   „Labas!" – pasakė jis. →
#     1. „Labas!" (dialogas)
#     2. – pasakė jis. (pasakojimas)
def get_list_speech_or_not(paragraph):
    returnt_list = []

    # Šablonas, kuris randa tekstą tarp kabučių „..."
    position_regex = r'(\u201c[^\u201d]+\u201d|\u201c[^\u201d]+$|$)'

    # Suskaidome pastraipą į dalis pagal kabučių pozicijas
    parts = re.split(position_regex, paragraph)

    parts = [part for part in parts if part.strip()]  # Pašaliname tuščias dalis

    # Kiekvienai daliai nustatome: dialogas (1) ar pasakojimas (0)
    result = [(part, 1 if part.startswith("\u201c") else 0) for part in parts]

    for part, is_speech in result:
        returnt_list.append((part, is_speech))

    return returnt_list


# ============================================================
# Pagrindinis dialogo apdorojimas
# ============================================================
# Eina per kiekvieną knygos pastraipą ir:
# 1. Sutvarko kabutes (paprastas pakeičia tipografinėmis)
# 2. Atskiria dialogą nuo pasakojimo
# 3. Pažymi kiekvieną pastraipą: tik pasakojimas (0), tik dialogas (1), arba mišri (2)
# Sukuria papildomą lentelę, kur kiekviena dialogo/pasakojimo dalis yra atskira eilutė.
def get_splitted_speech_narrative(df_paragraphs):

  book_parts_df = pd.DataFrame(columns=["text", "chapter","paragraph_nr" , "is_speech"])
  book_parts_df['is_speech'] = book_parts_df['is_speech'].astype(int)

  for index, row in df_paragraphs.iterrows():
      paragraph = row["paragraph"]
      # Jei yra paprastų kabučių – pakeičiame tipografinėmis
      if '"' in paragraph:
        paragraph = replace_quotes(paragraph)
        df_paragraphs.at[index, "paragraph"] = paragraph

      speech_or_not_list = get_list_speech_or_not(paragraph)
      if len(speech_or_not_list)>1:
        # Mišri pastraipa – yra ir dialogas, ir pasakojimas
        df_paragraphs.at[index, 'is_speech'] = 2
        for tup_text_speech in speech_or_not_list:
          book_parts_df = pd.concat([book_parts_df, pd.DataFrame({ 'text': [tup_text_speech[0]] , 'chapter': [row["chapter"]], 'paragraph_nr': [index]  , 'is_speech': [tup_text_speech[1]]  })], ignore_index=True)

      if len(speech_or_not_list)==1:
        tup_text_speech = speech_or_not_list[0]
        book_parts_df = pd.concat([book_parts_df, pd.DataFrame({ 'text': [tup_text_speech[0]] , 'chapter': [row["chapter"]], 'paragraph_nr': [index]  , 'is_speech': [tup_text_speech[1]]  })], ignore_index=True)
        if tup_text_speech[1] == 1:
          df_paragraphs.at[index, 'is_speech'] = 1  # Visa pastraipa yra dialogas



  return book_parts_df

# Paleidžiame dialogo aptikimą
book_parts_df = get_splitted_speech_narrative(df_paragraphs)

# Kiek dialogo ir kiek pasakojimo eilučių rasta
print(f"Book has {book_parts_df[book_parts_df['is_speech']==1].shape[0]} lines of speech  and {book_parts_df[book_parts_df['is_speech']!=1].shape[0]} lines of narrative")

"""## Pasirinktiniai filtrai

Tai „įrankių dėžė" su paruoštais filtrais – jei knygoje yra šiukšlių
(pvz., „[Iliustracija]" ar dekoratyvūs ženklai), čia galima juos pašalinti.
Šiuo metu visi filtrai išjungti (užkomentuoti).
"""

#filtered_df = df_paragraphs[~df_paragraphs['paragraph'].str.match(r'^ *\* *\*.*')]
#filtered_df = df_paragraphs[~df_paragraphs['paragraph'].str.match(r'^_.*')]
#filtered_df = df_paragraphs[~df_paragraphs['paragraph'].str.match(r'^\[.*')]
#filtered_df = df_paragraphs[df_paragraphs['paragraph'].str.match(r'^\[[0-9]+\]')]
#filtered_df = df_paragraphs[~df_paragraphs['paragraph'].str.match(r'^\[[0-9]+\]')]
#filtered_df = df_paragraphs[df_paragraphs['chapter']==0]

"""## Galutinė pastraipų lentelė

Rodoma galutinė pastraipų lentelė po visų filtravimo ir dialogo žymėjimo veiksmų.
"""



#df_paragraphs = df_paragraphs[df_paragraphs['chapter']!=0]
#df_paragraphs = df_paragraphs.query("not  paragraph.str.startswith('[Illustration')")
#df_paragraphs = df_paragraphs[~df_paragraphs['paragraph'].str.match(r'^p.*\.jpg .*')]

df_paragraphs

"""<br><br><br><br>

---

## Išsaugojimas į Google Drive

Eksportuojame pastraipų lentelę kaip TSV failą į Google Drive.
TSV – tai lentelė, kur stulpeliai atskirti Tab ženklu (kaip Excel, tik paprastesnis).
Šį failą naudos kiti du sąsiuviniai tolesniam darbui.
"""

# @title Select True and confirm the connection to Google Drive; The data will be saved in your gdrive root directory { run: "auto", vertical-output: true }

from google.colab import drive

save_to_gdrive = True # @param ["False", "True"] {type:"raw"}

# Išsaugome lentelę kaip TSV failą
if save_to_gdrive:
  df_paragraphs.to_csv(f'/content/drive/MyDrive/Book_Info/{Vol}/book_text/df_paragraphs_'+book_code+'.tsv', sep='\t', index=False)
  print(f'{book_name}  {book_code} saved to Google Drive. It has {df_paragraphs.shape[0]} paragraphs  ')

"""## Ryšys su kitais sąsiuviniais

Šis sąsiuvinis yra **1-as iš 3** vamzdynyje:
1. **BookNLP.ipynb** (šis) → paruošia tekstą, skaido pastraipomis, žymi dialogus
2. **BookNLP_spaCy.ipynb** → analizuoja kiekvieną žodį (kalbos dalys, vardai, reikšmės)
3. **BookNLP_StableDiffusion.ipynb** → generuoja paveikslėlius ir vaizdo įrašą iš scenų

Abu kalbos analizės sąsiuviniai (spaCy ir Stanza) naudoja tą patį failą iš šio sąsiuvinio,
todėl jų rezultatai yra palyginami.

## Nuorodos į kitus sąsiuvinius
- [BookNLP_spaCy.ipynb](https://colab.research.google.com/drive/1Ib0NVhiJ1McSlAmCoGXJGRCmK9wz3NDQ)
- [BookNLP_stanza.ipynb](https://colab.research.google.com/drive/1_daF3cy_f2WIYNyx8CNOiOEBh6nOK-N4)
"""