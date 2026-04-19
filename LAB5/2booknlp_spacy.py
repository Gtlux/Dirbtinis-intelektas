# -*- coding: utf-8 -*-
"""BookNLP_spaCy.ipynb

Automatiškai sugeneruota iš Colab.

Originalus failas:
    https://colab.research.google.com/drive/1Ib0NVhiJ1McSlAmCoGXJGRCmK9wz3NDQ

## 🇱🇹 Kas yra šis sąsiuvinis?

Šis sąsiuvinis yra **antrasis žingsnis** iš trijų.
Jis paima pirmojo sąsiuvinio paruoštą lentelę su knygos pastraipomis
ir kiekvieną žodį „perleidžia" per kalbos analizės įrankius.

**Paprasčiau:** Pirmasis failas „nuskaitė" knygą ir suskaidė ją pastraipomis.
Šis failas kiekvieną žodį „perskaito kaip kalbininkas" – prie kiekvieno
parašo, kokia tai kalbos dalis (daiktavardis, veiksmažodis...), suranda
pamatinę formą (pvz., „bėgo" → „bėgti"), atpažįsta vardus, vietas, datas
ir ieško žodžio reikšmės žodyne.

### Ką gauname rezultate:
- `df_book_token_spacy` – lentelė, kur kiekviena eilutė = vienas žodis su ~20 pastabų
- `df_book_entity_spacy` – lentelė su atpažintais vardais, vietomis, datomis
- `df_book_noun_chunk_spacy` – lentelė su susijusių žodžių grupėmis (pvz., „senas medinis namas")
- TSV failas Google Drive – išsaugota žodžių lentelė

### Naudojami įrankiai:
- **spaCy** – „dirbtinis kalbininkas", kuris moka skaityti anglų kalbą
- **WordNet** – anglų kalbos žodynas-enciklopedija su žodžių reikšmėmis
- **Lesk algoritmas** – nustato, kurią reikšmę žodis turi šiame sakinyje
"""

# Pasirenkame tomą (turi atitikti pirmojo sąsiuvinio nustatymą)
Vol = 'Vol2'

"""## Įrankių prijungimas

Prijungiame visus reikalingus įrankius:
- `pandas` – lentelių kūrimas (kaip Excel)
- `nltk` ir `wordnet` – žodžių reikšmių žodynas
- `lesk` – įrankis nustatyti žodžio reikšmę pagal kontekstą
"""

#@title Imports

from google.colab import files       # Failų įkėlimas Colab aplinkoje
import pandas as pd                   # Lentelių kūrimo įrankis
import urllib.request                  # Failų atsisiuntimas
import os.path                         # Failų tikrinimas
import re                              # Teksto šablonų paieška
import requests                        # Duomenų gavimas iš interneto
import json                            # Struktūruotų duomenų apdorojimas

# NLTK – sena, bet labai galinga kalbos apdorojimo biblioteka
import nltk
from nltk.corpus import wordnet as wn  # WordNet – didžiulis anglų kalbos žodynas
nltk.download('wordnet')               # Atsisiunčiame žodyno duomenis
from nltk.wsd import lesk              # Lesk – algoritmas, kuris parenka teisingą žodžio reikšmę

"""---

## 1. Google Drive prijungimas

Prijungiame Google Drive – ten saugomi duomenys iš pirmojo sąsiuvinio.
"""

from google.colab import drive

import os
if os.path.isdir('/content/drive/MyDrive'):
    print('Google Drive is mounted.')
else:
    drive.mount('/content/drive')

"""---

## 2. Knygos duomenų įkėlimas

Atidarome lentelę su knygos pastraipomis, kurią paruošė pirmas sąsiuvinis.
Tai kaip atidaryti Excel failą, kurį kažkas jau sutvarkė.
"""

book_code = '2852' # 2852 244 wget_To_Kill_a_Mockingbird

book_corp_path = f'/content/drive/MyDrive/Book_Info/{Vol}/'
paragraphs_path = book_corp_path+'book_text/df_paragraphs_'+book_code+'.tsv'

df_paragraphs = pd.read_csv(paragraphs_path, sep='\t')  # Nuskaitome TSV lentelę

"""---

## 3. „Dirbtinio kalbininko" įjungimas

Įkeliame spaCy modelį – tai kompiuterinė programa, kuri „moka skaityti"
anglų kalbą. Ji sugeba:
- **Suskaidyti** tekstą į atskirus žodžius
- **Nustatyti kalbos dalį** – ar tai daiktavardis, veiksmažodis, būdvardis...
- **Rasti ryšius tarp žodžių** – pvz., „didelis" priklauso „namas"
- **Atpažinti vardus ir vietas** – pvz., „Šerlokas Holmsas" = žmogaus vardas
- **Grupuoti susijusius žodžius** – pvz., „senas medinis namas" yra viena frazė

Tai kaip pasamdyti kalbininką, kuris perskaitys visą knygą ir prie kiekvieno
žodžio parašys pastabas.
"""

import spacy
nlp = spacy.load("en_core_web_sm")  # Įkeliame mažą anglų kalbos modelį

"""## Žodžio reikšmės nustatymo funkcija

Ši funkcija kiekvienam žodžiui ieško informacijos žodyne (WordNet):

1. **Dažniausia reikšmė** – kokia reikšmė dažniausiai vartojama
   (pvz., „dog" → keturkojis gyvūnas)
2. **Kontekstinė reikšmė** – kokia reikšmė šiame sakinyje
   (pvz., „I went to the bank" → ar „bank" = bankas ar upės krantas?
   Lesk algoritmas pažiūri į visą sakinį ir nusprendžia)
3. **Žodžio „šeimos medis"** – kaip žodis susijęs su bendresnėmis sąvokomis
   (pvz.: šuo → šunų šeima → žinduoliai → gyvūnai → gyvos būtybės)
"""

#@title wordnet_info function
def wordnet_info(word, word_pos , sentence_str ):

  most_frequent_synset = None
  most_frequent_synset_key = ''
  hypernym_path = []
  hypernym_path_key = []

  # Ieškome žodžio žodyne pagal kalbos dalį
  synsets = []
  if word_pos == 'NOUN':       # Daiktavardis
    synsets = wn.synsets(word, pos=wn.NOUN)
  if word_pos == 'VERB':       # Veiksmažodis
    synsets = wn.synsets(word, pos=wn.VERB)
  if word_pos == 'ADJ':        # Būdvardis
    synsets = wn.synsets(word, pos=wn.ADJ)
  if word_pos == 'ADV':        # Prieveiksmis
    synsets = wn.synsets(word, pos=wn.ADV)

  # Jei radome žodį žodyne – imame dažniausią reikšmę
  if len(synsets)>0:
    most_frequent_synset = synsets[0]  # Pirmoji = dažniausia
    most_frequent_synset_key = most_frequent_synset.lemmas()[0].key()

    # Surandame žodžio „šeimos medį" – nuo konkrečios iki bendriausios sąvokos
    hypernym_paths = most_frequent_synset.hypernym_paths()
    if len(hypernym_paths)>0:
      hypernym_path = [synset for synset in  hypernym_paths[0]]
      hypernym_path_key = [synset.lemmas()[0].key() for synset in  hypernym_path]

  # Lesk algoritmas – nustato reikšmę pagal sakinio kontekstą
  # (pvz., „bank" sakinyje apie pinigus = bankas, ne upės krantas)
  lesk_synset = None
  lesk_synset_key = ''
  if len(sentence_str)>0 and len(most_frequent_synset_key)>0:
    sentence_str = re.sub(r'[^\w\s]','',sentence_str)  # Pašaliname skyrybos ženklus
    sentence = sentence_str.split()
    if  word_pos == 'NOUN':
      lesk_synset = lesk(sentence, word, pos='n')
    elif  word_pos == 'VERB':
      lesk_synset = lesk(sentence, word, pos='v')
    else:
      lesk_synset = lesk(sentence, word)

    if lesk_synset is not None:
      lesk_synset_key = lesk_synset.lemmas()[0].key()


  return most_frequent_synset_key, lesk_synset_key, hypernym_path_key

"""## Pagrindinė analizės dalis

Čia vyksta visa magija – programa eina per **kiekvieną knygos žodį** ir daro štai ką:

1. **Nustato kalbos dalį** – ar tai daiktavardis, veiksmažodis, būdvardis...
2. **Suranda pamatinę formą** – pvz., „running" → „run", „was" → „be"
3. **Nustato ryšius** – pvz., „didelis" priklauso „namas" (būdvardis apibūdina daiktavardį)
4. **Atpažįsta vardus, vietas, datas** – pvz., „Sherlock Holmes" = asmens vardas
5. **Ieško reikšmės žodyne** – ką žodis reiškia ir kokia jo reikšmė šiame sakinyje
6. **Pažymi dialogą** – ar žodis yra kabutėse (veikėjas kalba)
7. **Grupuoja frazes** – pvz., „the old wooden door" = viena daiktavardinė frazė

Rezultate gauname lentelę, kur kiekvienas žodis turi savo eilutę su visomis pastabomis.
Tai kaip kalbininko užrašų knygelė – labai detalūs pastebėjimai apie kiekvieną žodį.
"""

#@title We will put each annotation into separate python list. We will then combine these lists to create a dataframe table 'df_book_token_spacy'

# Paruošiame tuščius sąrašus – kiekvienas sąrašas surinks vieną tipo informaciją
# apie kiekvieną žodį. Galiausiai visa tai sujungsime į vieną lentelę.

token_text_list = []          # Pats žodis
token_lemma_list = []         # Pamatinė forma (pvz., „bėgo" → „bėgti")
token_pos_list = []           # Kalbos dalis (daiktavardis, veiksmažodis...)
token_tag_list = []           # Detali kalbos dalies žymė
token_dep_list = []           # Ryšys su kitu žodžiu (pvz., „priklauso veiksmažodžiui")
token_is_stop_list = []       # Ar tai „tuščias" žodis (a, the, is, in...)
token_head_list = []          # Nuo kurio žodžio priklauso
token_head_pos_list = []      # To žodžio kalbos dalis
token_head_i_list = []        # To žodžio pozicija sakinyje
token_ent_type_list = []      # Esinio tipas (PERSON, GPE, DATE...)
token_in_chunk_list = []      # Ar priklauso frazei
#token_is_speech_list = []
token_nr_list = []            # Žodžio numeris pastraipoje
token_idx_list = []           # Žodžio pozicija tekste (simbolių skaičius nuo pradžios)
token_sent_nr_list = []       # Sakinio numeris pastraipoje
token_id_in_sent_list = []    # Žodžio pozicija sakinyje
is_quote_list = []            # Ar žodis yra kabutėse (dialoge)
mf_synset_list = []           # Dažniausia žodžio reikšmė žodyne
lesk_synset_list = []         # Kontekstinė žodžio reikšmė (pagal sakinį)


chapter_nrs_list = []         # Skyriaus numeris
paragraph_nrs_list = []       # Pastraipos numeris
paragraph_type_list = []

# Atpažintų vardų/vietų/datų sąrašai
entity_text_list = []         # Esinio tekstas (pvz., „Sherlock Holmes")
entity_label_list = []        # Esinio tipas (pvz., „PERSON")
entity_chapter_nrs_list = []
entity_paragraph_nrs_list = []
entity_sentence_nrs_list = []
entity_start_list = []
entity_end_list = []

# Daiktavardinių frazių sąrašai (pvz., „the old wooden door")
noun_chunk_text_list = []         # Visa frazė
noun_chunk_root_text_list = []    # Pagrindinis frazės žodis (pvz., „door")
noun_chunk_start_list = []
noun_chunk_end_list = []
noun_chunk_root_i_list = []
noun_chapter_nrs_list = []
noun_paragraph_nrs_list = []
noun_chunk_sent_nr_list = []
noun_chunk_entity_list = []


# ============================================================
# PAGRINDINĖ ANALIZĖS KILPA
# ============================================================
# Einame per kiekvieną pastraipą → kiekvieną sakinį → kiekvieną žodį
# ir renkame informaciją apie kiekvieną žodį.
for index, row in df_paragraphs.iterrows():
    paragraph = row["paragraph"]

    is_quote = 0  # Sekame, ar esame kabutėse (dialoge)

    my_text = paragraph
    doc = nlp(my_text)  # „Dirbtinis kalbininkas" analizuoja visą pastraipą

    for sent_i, sent in enumerate(doc.sents):  # Kiekvienam sakiniui
         for token in sent:  # Kiekvienam žodžiui

          # spaCy kartais sukuria „tuščius" žodžius (tarpus) – juos praleidžiame
          if len(token.text.strip())==0:
            continue

          # Surenkame visą informaciją apie žodį
          token_text_list.append(token.text)            # Žodis
          token_lemma_list.append(token.lemma_)          # Pamatinė forma
          token_pos_list.append(token.pos_)              # Kalbos dalis
          token_tag_list.append(token.tag_)              # Detali žymė
          token_dep_list.append(token.dep_)              # Ryšys su kitu žodžiu
          token_is_stop_list.append(token.is_stop)       # Ar „tuščias" žodis?
          token_head_list.append(token.head.text)        # Nuo kurio žodžio priklauso
          token_head_i_list.append(token.head.i - sent.start)
          token_head_pos_list.append(token.head.pos_)
          token_ent_type_list.append(token.ent_type_)    # Esinio tipas (jei yra)
          token_nr_list.append(token.i)
          token_idx_list.append(token.idx)
          token_sent_nr_list.append(sent_i)              # Sakinio numeris
          token_id_in_sent_list.append(token.i - sent.start)

          # Kabučių sekimas – jei randame kabutę, „perjungiame" dialogo būseną
          # (kaip jungiklis: įjungta/išjungta)
          if token.is_quote:
            is_quote = 1 - is_quote
          is_quote_list.append(is_quote)

          # Ieškome žodžio reikšmės žodyne (WordNet)
          most_frequent_synset_key, lesk_synset_key, hypernym_path_key = wordnet_info(token.text, token.pos_, sent.text)
          mf_synset_list.append(most_frequent_synset_key)
          lesk_synset_list.append(lesk_synset_key)


          # Tikriname, ar žodis priklauso kokiai nors daiktavardinei frazei
          token_in_chunk = 0
          for chunk in doc.noun_chunks:
              if token in chunk:
                  token_in_chunk = 1
                  break


          token_in_chunk_list.append(token_in_chunk)


          chapter_nrs_list.append(row["chapter"])
          paragraph_nrs_list.append(index)

         # Surenkame visus atpažintus vardus, vietas, datas iš sakinio
         for entity in sent.ents:
              entity_text_list.append(entity.text)       # Pvz., „Sherlock Holmes"
              entity_label_list.append(entity.label_)     # Pvz., „PERSON"
              entity_chapter_nrs_list.append(row["chapter"])
              entity_paragraph_nrs_list.append(index)
              entity_sentence_nrs_list.append(sent_i)
              entity_start_list.append(entity.start)
              entity_end_list.append(entity.end)

         # Surenkame visas daiktavardines frazes
         # (pvz., „the old wooden door" – grupė susijusių žodžių apie vieną daiktą)
         for chunk in sent.noun_chunks:
            noun_chunk_text_list.append(chunk.text)               # Visa frazė
            noun_chunk_root_text_list.append(chunk.root.text)     # Pagrindinis žodis
            noun_chapter_nrs_list.append(row["chapter"])
            noun_paragraph_nrs_list.append(index)

            noun_chunk_sent_nr_list.append(sent_i)

            noun_chunk_start_list.append(chunk.start-chunk.sent.start)
            noun_chunk_end_list.append(chunk.end-chunk.sent.start-1)

            noun_chunk_root_i_list.append(chunk.root.i-chunk.sent.start)
            chunk_entity_label = ''
            if len(chunk.ents)>0:
              chunk_entity_label = chunk.ents[0].label_

            noun_chunk_entity_list.append(chunk_entity_label)

# Atspausdiname kiek žodžių, vardų/vietų ir frazių rasta
print(f"Book has {len(token_text_list)} words,  {len(entity_text_list)} entities and  {len(noun_chunk_text_list)} noun chunks")

"""## Lentelių sukūrimas iš surinktų duomenų

Visas pastabas, kurias „kalbininkas" parašė prie kiekvieno žodžio,
sudedame į tris tvarkingus lenteles:
1. **Žodžių lentelė** – kiekvienas žodis su visomis pastabomis
2. **Vardų/vietų lentelė** – visi atpažinti vardai, vietos, datos
3. **Frazių lentelė** – visos susijusių žodžių grupės
"""

#@title We combine annotation lists to create a dataframe table 'df_book_token_spacy'

# Žodžių lentelė – kiekvienas stulpelis = vienas sąrašas
df_book_token_spacy = pd.DataFrame({'token': token_text_list, 'lemma': token_lemma_list , 'pos': token_pos_list, 'tag': token_tag_list, 'dep': token_dep_list,   'is_stop': token_is_stop_list,'head': token_head_list,'head_i': token_head_i_list,'head_pos': token_head_pos_list,'ent_type': token_ent_type_list,'token_in_chunk': token_in_chunk_list,  'chapter': chapter_nrs_list, 'paragraph': paragraph_nrs_list, 'paragraph_token_id':  token_nr_list, 'paragraph_token_strpoz': token_idx_list, 'paragraph_sentence_id': token_sent_nr_list  ,'token_id_in_sent': token_id_in_sent_list, 'is_quote':is_quote_list, 'wn_mf_synset': mf_synset_list , 'wn_lesk_synset': lesk_synset_list   }  )

# Vardų/vietų/datų lentelė ir frazių lentelė
df_book_entity_spacy = pd.DataFrame({'entity': entity_text_list, 'label': entity_label_list , 'chapter': entity_chapter_nrs_list, 'paragraph': entity_paragraph_nrs_list   , 'paragraph_entity_start': entity_start_list, 'paragraph_entity_end': entity_end_list, 'sent_id': entity_sentence_nrs_list})
df_book_noun_chunk_spacy = pd.DataFrame({'chunk': noun_chunk_text_list, 'chapter': noun_chapter_nrs_list, 'paragraph': noun_paragraph_nrs_list ,'paragraph_sentence_id': noun_chunk_sent_nr_list ,  'chunk_start': noun_chunk_start_list ,'chunk_end': noun_chunk_end_list ,'root': noun_chunk_root_text_list ,'chunk_root_i': noun_chunk_root_i_list, 'noun_chunk_entity': noun_chunk_entity_list })

"""## Duomenų peržiūra

Parodome pirmas 50 eilučių iš žodžių lentelės – patikriname ar viskas gerai.
"""

df_book_token_spacy[:50]

"""---

## Rezultatų išsaugojimas

Išsaugome žodžių lentelę kaip TSV failą į Google Drive.
Ją vėliau galima toliau analizuoti arba naudoti kitose programose.
"""

import pandas as pd

token_spacy_path = book_corp_path+'tmp/df_book_token_spacy_'+book_code+'.tsv'

df_book_token_spacy.to_csv(token_spacy_path, sep='\t', index=False)

#df_book_token_spacy.to_csv('df_book_token_spacy.tsv', sep='\t', index=False)
#df_paragraphs.to_csv('df_paragraphs.tsv', sep='\t', index=False)
#df_chapters_info.to_csv('df_chapters_info.tsv', sep='\t', index=False)

#df_book_entity_spacy.to_csv('df_book_entity_spacy.tsv', sep='\t', index=False)
#df_book_noun_chunk_spacy.to_csv('df_book_noun_chunk_spacy.tsv', sep='\t', index=False)

"""## Alternatyvūs išsaugojimo keliai

Čia saugomi užkomentuoti eksportavimo variantai kitoms vietoms.
Atkomentuokite tik tuos, kuriuos norite išsaugoti.
"""

#df_book_token_spacy.to_csv('/content/drive/MyDrive/df_book_token_spacy_'+book_code+'.tsv', sep='\t', index=False)
#df_chapters_info.to_csv('/content/drive/MyDrive/df_chapters_info_'+book_code+'.tsv', sep='\t', index=False)
#df_book_entity_spacy.to_csv('/content/drive/MyDrive/df_book_entity_spacy_'+book_code+'.tsv', sep='\t', index=False)
#df_book_noun_chunk_spacy.to_csv('/content/drive/MyDrive/df_book_noun_chunk_spacy_'+book_code+'.tsv', sep='\t', index=False)

"""---

## Interaktyvi vizualizacija (neprivaloma)

Žemiau yra paruoštos interaktyvių diagramų konfigūracijos su PyGWalker įrankiu.
Tai leidžia vizualiai tyrinėti duomenis (pvz., kiek žodžių kiekviename skyriuje,
kokie vardai dažniausi ir pan.). Šiuo metu viskas išjungta – jei norite naudoti,
atkomentuokite eilutes.
"""

#!pip install pygwalker -q

"""### PyGWalker importavimas (neprivaloma)"""

#import pygwalker as pyg
#import pandas as pd

"""### Žodžių lentelės diagrama (neprivaloma)

Stulpelinė diagrama: žodžių skaičius pagal skyrius, spalvinta pagal tai,
ar žodis yra dialoge (kabutėse).
"""

#vis_spec = r"""{"config":[{"config":{"defaultAggregated":true,"geoms":["auto"],"coordSystem":"generic","limit":-1,"timezoneDisplayOffset":0},"encodings":{"dimensions":[{"fid":"token","name":"token","basename":"token","semanticType":"nominal","analyticType":"dimension","offset":0},{"fid":"lemma","name":"lemma","basename":"lemma","semanticType":"nominal","analyticType":"dimension","offset":0},{"fid":"pos","name":"pos","basename":"pos","semanticType":"nominal","analyticType":"dimension","offset":0},{"fid":"tag","name":"tag","basename":"tag","semanticType":"nominal","analyticType":"dimension","offset":0},{"fid":"dep","name":"dep","basename":"dep","semanticType":"nominal","analyticType":"dimension","offset":0},{"fid":"is_stop","name":"is_stop","basename":"is_stop","semanticType":"nominal","analyticType":"dimension","offset":0},{"fid":"head","name":"head","basename":"head","semanticType":"nominal","analyticType":"dimension","offset":0},{"fid":"head_pos","name":"head_pos","basename":"head_pos","semanticType":"nominal","analyticType":"dimension","offset":0},{"fid":"ent_type","name":"ent_type","basename":"ent_type","semanticType":"nominal","analyticType":"dimension","offset":0},{"fid":"token_in_chunk","name":"token_in_chunk","basename":"token_in_chunk","semanticType":"quantitative","analyticType":"dimension","offset":0},{"fid":"chapter","name":"chapter","basename":"chapter","semanticType":"nominal","analyticType":"dimension","offset":0},{"fid":"paragraph_sentence_id","name":"paragraph_sentence_id","basename":"paragraph_sentence_id","semanticType":"quantitative","analyticType":"dimension","offset":0},{"fid":"is_quote","name":"is_quote","basename":"is_quote","semanticType":"nominal","analyticType":"dimension","offset":0},{"fid":"gw_mea_key_fid","name":"Measure names","analyticType":"dimension","semanticType":"nominal"}],"measures":[{"fid":"paragraph","name":"paragraph","basename":"paragraph","analyticType":"measure","semanticType":"quantitative","aggName":"sum","offset":0},{"fid":"paragraph_token_id","name":"paragraph_token_id","basename":"paragraph_token_id","analyticType":"measure","semanticType":"quantitative","aggName":"sum","offset":0},{"fid":"paragraph_token_strpoz","name":"paragraph_token_strpoz","basename":"paragraph_token_strpoz","analyticType":"measure","semanticType":"quantitative","aggName":"sum","offset":0},{"fid":"token_id_in_sent","name":"token_id_in_sent","basename":"token_id_in_sent","analyticType":"measure","semanticType":"quantitative","aggName":"sum","offset":0},{"fid":"gw_count_fid","name":"Row count","analyticType":"measure","semanticType":"quantitative","aggName":"sum","computed":true,"expression":{"op":"one","params":[],"as":"gw_count_fid"}},{"fid":"gw_mea_val_fid","name":"Measure values","analyticType":"measure","semanticType":"quantitative","aggName":"sum"}],"rows":[{"fid":"gw_count_fid","name":"Row count","analyticType":"measure","semanticType":"quantitative","aggName":"sum","computed":true,"expression":{"op":"one","params":[],"as":"gw_count_fid"}}],"columns":[{"fid":"chapter","name":"chapter","basename":"chapter","semanticType":"nominal","analyticType":"dimension","offset":0}],"color":[{"fid":"is_quote","name":"is_quote","basename":"is_quote","semanticType":"quantitative","analyticType":"dimension","offset":0}],"opacity":[],"size":[],"shape":[],"radius":[],"theta":[],"longitude":[],"latitude":[],"geoId":[],"details":[],"filters":[],"text":[]},"layout":{"showActions":false,"showTableSummary":false,"stack":"stack","interactiveScale":false,"zeroScale":true,"size":{"mode":"auto","width":320,"height":200},"format":{},"geoKey":"name","resolve":{"x":false,"y":false,"color":false,"opacity":false,"shape":false,"size":false}},"visId":"gw_yXLc","name":"Chart 1"}],"chart_map":{},"workflow_list":[{"workflow":[{"type":"transform","transform":[{"key":"gw_count_fid","expression":{"op":"one","params":[],"as":"gw_count_fid"}}]},{"type":"view","query":[{"op":"aggregate","groupBy":["chapter","is_quote"],"measures":[{"field":"gw_count_fid","agg":"sum","asFieldKey":"gw_count_fid_sum"}]}]}]}],"version":"0.4.9.1"}"""
#pyg.walk(df_book_token_spacy, spec=vis_spec)

"""### Vardų/vietų diagrama (neprivaloma)

Diagrama: dažniausi atpažinti vardai ir vietos pagal skyrius.
"""

#vis_spec = r"""{"config":[{"config":{"defaultAggregated":true,"geoms":["auto"],"coordSystem":"generic","limit":-1,"timezoneDisplayOffset":0},"encodings":{"dimensions":[{"fid":"entity","name":"entity","basename":"entity","semanticType":"nominal","analyticType":"dimension","offset":0},{"fid":"label","name":"label","basename":"label","semanticType":"nominal","analyticType":"dimension","offset":0},{"fid":"chapter","name":"chapter","basename":"chapter","semanticType":"quantitative","analyticType":"dimension","offset":0},{"fid":"sent_id","name":"sent_id","basename":"sent_id","semanticType":"quantitative","analyticType":"dimension","offset":0},{"fid":"gw_mea_key_fid","name":"Measure names","analyticType":"dimension","semanticType":"nominal"}],"measures":[{"fid":"paragraph","name":"paragraph","basename":"paragraph","analyticType":"measure","semanticType":"quantitative","aggName":"sum","offset":0},{"fid":"paragraph_entity_start","name":"paragraph_entity_start","basename":"paragraph_entity_start","analyticType":"measure","semanticType":"quantitative","aggName":"sum","offset":0},{"fid":"paragraph_entity_end","name":"paragraph_entity_end","basename":"paragraph_entity_end","analyticType":"measure","semanticType":"quantitative","aggName":"sum","offset":0},{"fid":"gw_count_fid","name":"Row count","analyticType":"measure","semanticType":"quantitative","aggName":"sum","computed":true,"expression":{"op":"one","params":[],"as":"gw_count_fid"}},{"fid":"gw_mea_val_fid","name":"Measure values","analyticType":"measure","semanticType":"quantitative","aggName":"sum"}],"rows":[{"fid":"gw_count_fid","name":"Row count","analyticType":"measure","semanticType":"quantitative","aggName":"sum","computed":true,"expression":{"op":"one","params":[],"as":"gw_count_fid"}}],"columns":[{"fid":"entity","name":"entity","basename":"entity","semanticType":"nominal","analyticType":"dimension","offset":0,"sort":"descending"}],"color":[],"opacity":[],"size":[{"fid":"chapter","name":"chapter","basename":"chapter","semanticType":"quantitative","analyticType":"dimension","offset":0}],"shape":[],"radius":[],"theta":[],"longitude":[],"latitude":[],"geoId":[],"details":[],"filters":[],"text":[]},"layout":{"showActions":false,"showTableSummary":false,"stack":"stack","interactiveScale":false,"zeroScale":true,"size":{"mode":"auto","width":10009,"height":409},"format":{},"geoKey":"name","resolve":{"x":false,"y":false,"color":false,"opacity":false,"shape":false,"size":false},"scaleIncludeUnmatchedChoropleth":false,"showAllGeoshapeInChoropleth":false,"colorPalette":"","useSvg":false,"scale":{"opacity":{},"size":{}}},"visId":"gw_pZr6","name":"Chart 1"},{"config":{"defaultAggregated":true,"geoms":["auto"],"coordSystem":"generic","limit":-1,"timezoneDisplayOffset":0},"encodings":{"dimensions":[{"fid":"entity","name":"entity","basename":"entity","semanticType":"nominal","analyticType":"dimension","offset":0},{"fid":"label","name":"label","basename":"label","semanticType":"nominal","analyticType":"dimension","offset":0},{"fid":"chapter","name":"chapter","basename":"chapter","semanticType":"quantitative","analyticType":"dimension","offset":0},{"fid":"sent_id","name":"sent_id","basename":"sent_id","semanticType":"quantitative","analyticType":"dimension","offset":0},{"fid":"gw_mea_key_fid","name":"Measure names","analyticType":"dimension","semanticType":"nominal"}],"measures":[{"fid":"paragraph","name":"paragraph","basename":"paragraph","analyticType":"measure","semanticType":"quantitative","aggName":"sum","offset":0},{"fid":"paragraph_entity_start","name":"paragraph_entity_start","basename":"paragraph_entity_start","analyticType":"measure","semanticType":"quantitative","aggName":"sum","offset":0},{"fid":"paragraph_entity_end","name":"paragraph_entity_end","basename":"paragraph_entity_end","analyticType":"measure","semanticType":"quantitative","aggName":"sum","offset":0},{"fid":"gw_count_fid","name":"Row count","analyticType":"measure","semanticType":"quantitative","aggName":"sum","computed":true,"expression":{"op":"one","params":[],"as":"gw_count_fid"}},{"fid":"gw_mea_val_fid","name":"Measure values","analyticType":"measure","semanticType":"quantitative","aggName":"sum"}],"rows":[{"fid":"gw_count_fid","name":"Row count","analyticType":"measure","semanticType":"quantitative","aggName":"sum","computed":true,"expression":{"op":"one","params":[],"as":"gw_count_fid"}}],"columns":[{"fid":"label","name":"label","basename":"label","semanticType":"nominal","analyticType":"dimension","offset":0,"sort":"descending"}],"color":[],"opacity":[],"size":[],"shape":[],"radius":[],"theta":[],"longitude":[],"latitude":[],"geoId":[],"details":[],"filters":[{"fid":"chapter","name":"chapter","basename":"chapter","semanticType":"quantitative","analyticType":"dimension","offset":0,"rule":{"type":"one of","value":[1]}}],"text":[]},"layout":{"showActions":false,"showTableSummary":false,"stack":"stack","interactiveScale":false,"zeroScale":true,"size":{"mode":"auto","width":10009,"height":409},"format":{},"geoKey":"name","resolve":{"x":false,"y":false,"color":false,"opacity":false,"shape":false,"size":false}},"visId":"gw_cPgM","name":"Chart 2"}],"chart_map":{},"workflow_list":[{"workflow":[{"type":"transform","transform":[{"key":"gw_count_fid","expression":{"op":"one","params":[],"as":"gw_count_fid"}}]},{"type":"view","query":[{"op":"aggregate","groupBy":["entity","chapter"],"measures":[{"field":"gw_count_fid","agg":"sum","asFieldKey":"gw_count_fid_sum"}]}]}]},{"workflow":[{"type":"filter","filters":[{"fid":"chapter","rule":{"type":"one of","value":[1]}}]},{"type":"transform","transform":[{"key":"gw_count_fid","expression":{"op":"one","params":[],"as":"gw_count_fid"}}]},{"type":"view","query":[{"op":"aggregate","groupBy":["label"],"measures":[{"field":"gw_count_fid","agg":"sum","asFieldKey":"gw_count_fid_sum"}]}]}]}],"version":"0.4.9.1"}"""
#pyg.walk(df_book_entity_spacy, spec=vis_spec)

"""### Frazių diagrama (neprivaloma)

Diagrama: dažniausios daiktavardinės frazės pagal pagrindinį žodį.
"""

#vis_spec = r"""{"config":[{"config":{"defaultAggregated":true,"geoms":["auto"],"coordSystem":"generic","limit":-1,"timezoneDisplayOffset":0},"encodings":{"dimensions":[{"fid":"chunk","name":"chunk","basename":"chunk","semanticType":"nominal","analyticType":"dimension","offset":0},{"fid":"chapter","name":"chapter","basename":"chapter","semanticType":"nominal","analyticType":"dimension","offset":0},{"fid":"root","name":"root","basename":"root","semanticType":"nominal","analyticType":"dimension","offset":0},{"fid":"gw_mea_key_fid","name":"Measure names","analyticType":"dimension","semanticType":"nominal"}],"measures":[{"fid":"paragraph","name":"paragraph","basename":"paragraph","analyticType":"measure","semanticType":"quantitative","aggName":"sum","offset":0},{"fid":"chunk_start","name":"chunk_start","basename":"chunk_start","analyticType":"measure","semanticType":"quantitative","aggName":"sum","offset":0},{"fid":"chunk_end","name":"chunk_end","basename":"chunk_end","analyticType":"measure","semanticType":"quantitative","aggName":"sum","offset":0},{"fid":"chunk_root_i","name":"chunk_root_i","basename":"chunk_root_i","analyticType":"measure","semanticType":"quantitative","aggName":"sum","offset":0},{"fid":"gw_count_fid","name":"Row count","analyticType":"measure","semanticType":"quantitative","aggName":"sum","computed":true,"expression":{"op":"one","params":[],"as":"gw_count_fid"}},{"fid":"gw_mea_val_fid","name":"Measure values","analyticType":"measure","semanticType":"quantitative","aggName":"sum"}],"rows":[{"fid":"gw_count_fid","name":"Row count","analyticType":"measure","semanticType":"quantitative","aggName":"sum","computed":true,"expression":{"op":"one","params":[],"as":"gw_count_fid"}}],"columns":[{"fid":"root","name":"root","basename":"root","semanticType":"nominal","analyticType":"dimension","offset":0,"sort":"descending"}],"color":[{"fid":"root","name":"root","basename":"root","semanticType":"nominal","analyticType":"dimension","offset":0}],"opacity":[],"size":[],"shape":[],"radius":[],"theta":[],"longitude":[],"latitude":[],"geoId":[],"details":[],"filters":[{"fid":"chapter","name":"chapter","basename":"chapter","semanticType":"quantitative","analyticType":"dimension","offset":0,"sort":"ascending","rule":{"type":"one of","value":[1]}}],"text":[]},"layout":{"showActions":false,"showTableSummary":false,"stack":"stack","interactiveScale":false,"zeroScale":true,"size":{"mode":"auto","width":320,"height":200},"format":{},"geoKey":"name","resolve":{"x":false,"y":false,"color":false,"opacity":false,"shape":false,"size":false}},"visId":"gw_QYL0","name":"Chart 1"}],"chart_map":{},"workflow_list":[{"workflow":[{"type":"filter","filters":[{"fid":"chapter","rule":{"type":"one of","value":[1]}}]},{"type":"transform","transform":[{"key":"gw_count_fid","expression":{"op":"one","params":[],"as":"gw_count_fid"}}]},{"type":"view","query":[{"op":"aggregate","groupBy":["root"],"measures":[{"field":"gw_count_fid","agg":"sum","asFieldKey":"gw_count_fid_sum"}]}]}]}],"version":"0.4.9.1"}"""
#pyg.walk(df_book_noun_chunk_spacy, spec=vis_spec)

"""---

## Gutenberg katalogo atsisiuntimas (neprivaloma)

Jei norite pamatyti, kokios knygos yra prieinamos nemokamam skaitymui
Gutenberg projekte – įjunkite šią dalį ir gausite pilną sąrašą (~70 000 knygų).
"""

#@title 🗂️ Get catalog

get_catalog = False # @param ["False", "True"] {type:"raw"}

if get_catalog:
  df_books_catalog = pd.read_csv('https://www.gutenberg.org/cache/epub/feeds/pg_catalog.csv', keep_default_na=False)
  df_books_catalog = df_books_catalog[df_books_catalog['Language']=='en']
  df_books_catalog.reset_index(drop=True, inplace=True)
  print("df_books_catalog.shape: " ,df_books_catalog.shape)

"""---

## Sąsiuvinio santrauka

Šis sąsiuvinis atliko šiuos veiksmus:
1. Įkėlė paruoštą knygos tekstą iš pirmojo sąsiuvinio
2. Kiekvieną žodį analizavo su „dirbtiniu kalbininku" (spaCy)
3. Kiekvienam žodžiui ieškojo reikšmės žodyne (WordNet)
4. Surinko visas pastabas į lenteles ir jas išsaugojo

Rezultatas – detalus kiekvieno knygos žodžio aprašymas, kurį galima
naudoti tolesnei analizei, vizualizacijai ar kitų programų maitinimui.
"""