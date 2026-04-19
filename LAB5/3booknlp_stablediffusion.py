# -*- coding: utf-8 -*-
"""BookNLP_StableDiffusion.ipynb

Automatiškai sugeneruota iš Colab.

Originalus failas:
    https://colab.research.google.com/drive/1WhU5TzT_r84mf1feaYmsczQD-lcdqDws

## 🇱🇹 Kas yra šis sąsiuvinis?

Šis sąsiuvinis yra **trečiasis ir paskutinis žingsnis** iš trijų.
Jo užduotis – paversti knygos ar filmo scenas **paveikslėliais** naudojant
dirbtinį intelektą (Stable Diffusion), pridėti **garsą** (kompiuteris „perskaito"
tekstą balsu) ir viską sujungti į **vaizdo įrašą**.

**Paprasčiau:** Pirmasis failas paruošė knygos tekstą, antrasis jį analizavo
kaip kalbininkas, o šis – „nupiešia" scenas ir sukuria iš jų filmą su pasakojimo garsu.
Tai kaip animatorius, kuris perskaito scenarijų ir sukuria animacinę juostą.

### Ką gauname rezultate:
- Atskirus paveikslėlius kiekvienai scenai (JPEG)
- Garso failus su scenų aprašymais (MP3)
- Galutinį vaizdo įrašą su garsu (MP4)

# <img src="https://www.gutenberg.org/gutenberg/pg-logo-129x80.png" width=50 height=50>   <font color='Orange'>Book NLP 5 - <br> <b>Text</b>  to <b>Image</b> with Stable Diffusion</font>

---
"""

#@title Imports

from google.colab import files       # Failų valdymas Colab aplinkoje
import pandas as pd                   # Lentelių kūrimas
import os.path                         # Failų tikrinimas
import re                              # Teksto šablonų paieška

from google.colab.data_table import DataTable
DataTable.max_columns = 50             # Leisti rodyti daugiau stulpelių lentelėse

import numpy as np                     # Skaičiavimai su dideliais duomenų masyvais
import cv2                             # Paveikslėlių apdorojimas (saugojimas, konvertavimas)
import os                              # Failų sistemos operacijos
import requests                        # Duomenų gavimas iš interneto
import json                            # Struktūruotų duomenų skaitymas

# ============================================================
# PIEŠIMO STILIŲ SĄRAŠAS
# ============================================================
# Čia surašyti 50+ dailės stilių, kuriais galima piešti paveikslėlius.
# Galima pasirinkti bet kurį – nuo klasikinio Van Gogh iki anime ar pikselių meno.
style_list =["Colorful cartoon drawing style", "anime art style", "Line drawing", "Coloring book page", "Salvador Dali", "A digital painting with an anime-inspired art style",
    "Detailed Renaissance style", "Surrealist painting", "Impressionist", "Abstract painting", "Pop Art painting", "Baroque-style", "Cubist painting", "Romantic painting",
    "Art Nouveau painting", "Gothic painting", "Macro photography", "Aerial photography", "Underwater photography", "Vintage-style travel photography", "Long-exposure night photography",
    "Documentary-style photography", "Photography with a shallow depth of field and soft lighting", "Cyberpunk with neon signs", "Fantasy illustration",
    "Digital painting", "Concept art", "Isometric digital art" , "Digital illustration in manga style", "Minimalistic digital artwork",
    "Sci-fi digital painting", "Steampunk digital art","Yamato-e","Kanō school","Gongbi","Shuimo","Literary painting",
    "Caricature drawing",  "Figure drawing", "Gesture drawing", "Scratchboard drawing", "Perspective drawing",
    "Photorealism", "Pointillism", "Scientific illustrations", "Silhouette drawing" , "Sketch drawing", "Technical drawing",
    "Vincent van Gogh", "Gustave Klimt", "M.C. Escher", "Claude Monet", "René Magritte", "Pablo Picasso",
    "Leonardo da Vinci", "Edvard Munch", "Andy Warhol",  "Pixel art"]

"""

---

## 1. Google Drive prijungimas

Prijungiame Google Drive – ten saugomi ankstesnių sąsiuvinių rezultatai.

"""

from google.colab import drive

import os
if os.path.isdir('/content/drive/MyDrive'):
    print('Google Drive is mounted.')
else:
    drive.mount('/content/drive')

"""
---

## 2. Scenų aprašymų paruošimas

Čia ruošiame „piešimo užduotis" – aprašome scenas, kurias norime nupiešti.

### Stiliaus pasirinkimas
"""

# Pasirenkame piešimo stilių iš sąrašo (0 = „Colorful cartoon drawing style")
# Galima pakeisti skaičių ir gauti kitą stilių
style = style_list[0]

# Nurodome, ko NEREIKIA piešti – tai padeda išvengti bjaurių/iškraipytų paveikslėlių
negative_prompt='distorted, ugly, deformed, disfigured, poor details'

"""### Scenų aprašymų gavimas

Scenas galima sukurti keliais būdais:

**1 būdas:** Pateikti ChatGPT ar Gemini tokį užklausimą:
> „Esi scenarijų rašytojas. Aprašyk 10 svarbiausių filmo „Matrix" scenų JSON formatu
> su vieta, laiku, veikėjais, objektais ir aprašymu."

ChatGPT grąžins struktūruotą scenų sąrašą, kurį programa galės naudoti.

**2 būdas:** Atsisiųsti jau paruoštą scenų failą iš interneto.

**3 būdas:** Pačiam parašyti scenas žemiau esančiame JSON bloke.

Kiekvienoje scenoje yra:
- `scene_title` – scenos pavadinimas
- `description` – vizualinis aprašymas (ką piešti)
- `scene_date` – metai
- `location` – vieta
- `characters` – veikėjai
- `objects` – matomi daiktai
"""

prompt_response_json_text = """

[
    {
        "scene_title": "The Hacker's Lair",
        "dialog_summary": "Neo receives a mysterious message hinting that reality is an illusion and a hidden world awaits.",
        "description": "A dark, cramped room cluttered with computers, cables, and old monitors. Neo is immersed in a sea of code.",
        "scene_environment": "Dim room filled with humming servers and scattered computer equipment.",
        "scene_type": "INT",
        "scene_date": "1999",
        "location": "Abandoned Building",
        "time_of_day": "NIGHT",
        "characters": [
            "Neo",
            "Morpheus"
        ],
        "objects": [
            "computer",
            "monitor",
            "keyboard",
            "cables"
        ],
        "object_part_of_object": [
            "keyboard; computer",
            "cable; computer"
        ],
        "motion_sequence": [
            "typing",
            "scrolling"
        ],
        "constant_state_sequence": [
            "glowing",
            "idle"
        ]
    }
]

"""

# ============================================================
# SCENŲ APDOROJIMAS
# ============================================================
# Jei aukščiau įrašytas JSON tekstas – naudojame jį.
# Jei tuščias – atsisiunčiame paruoštą failą iš interneto.
#@title If the prompt_response_json_text variable is an empty string then the json file from the Internet must be submitted

if len(prompt_response_json_text)==0:
  book_code = '2852' # 84  244 2701 2852 42671
  url = "https://raw.githubusercontent.com/aalgirdas/novel-semantic-parsing/refs/heads/main/data/gpt4_scene_info_"+book_code+".json"
  response = requests.get(url)
  prompt_response_json_text = response.text
else:
  prompt_response_json_text = '{"1":'+prompt_response_json_text+'}'

data = json.loads(prompt_response_json_text)  # Paverčiame tekstą į struktūruotus duomenis
print("JSON data:", data)

number_of_prompts = 10 #+1000

# Surenkame piešimo užduotis iš kiekvienos scenos
scene_nr = 1
prompts = []              # Scenų aprašymai (ką piešti)
scene_dates = []          # Scenų datos (metai)
scene_locations = []      # Scenų vietos
scene_objects = []        # Scenų objektai (daiktai)
for key, value in data.items():
  for item in value:
    print(f"{scene_nr:>5} {item.get('description')}")
    prompts.append(item.get('description'))
    scene_dates.append(item.get('scene_date'))
    scene_locations.append(item.get('location'))
    scene_objects.append(item.get('objects'))
    scene_nr += 1

  if scene_nr > number_of_prompts:
    break

"""---

## 3. Paveikslėlių generavimas su Stable Diffusion

**Kas yra Stable Diffusion?**
Tai dirbtinio intelekto programa, kuri moka „piešti" paveikslėlius
pagal tekstinį aprašymą. Pvz., jei pasakysite „sena pilis naktyje su žaibais" –
ji sugeneruos tokį paveikslėlį.

**Kaip tai veikia?**
1. Programa gauna tekstinį aprašymą (pvz., „tamsi patalpa su kompiuteriais")
2. Prie jo pridedamas stilius (pvz., „spalvinga karikatūra") ir objektai
3. AI „nupiešia" paveikslėlį per 8-12 žingsnių
4. Taip pat nurodoma, ko NEPIEŠTI (negative_prompt) – pvz., „iškraipyta, bjauru"

**Hyper-SD** – tai pagreitinta versija, kuri piešia greičiau nei įprastai.
"""

# Commented out IPython magic to ensure Python compatibility.
# %pip install --quiet --upgrade diffusers transformers accelerate mediapy peft

# Commented out IPython magic to ensure Python compatibility.
# %%capture
# import mediapy as media
# import random
# import sys
# import torch
# 
# from diffusers import DiffusionPipeline, TCDScheduler
# from huggingface_hub import hf_hub_download
# 
# # Pasirenkame kiek žingsnių piešti (8 arba 12):
# num_inference_steps = 12
# 
# base_model_id = "stabilityai/stable-diffusion-xl-base-1.0"
# repo_name = "ByteDance/Hyper-SD"
# plural = "s" if num_inference_steps > 1 else ""
# ckpt_name = f"Hyper-SDXL-{num_inference_steps}step{plural}-CFG-lora.safetensors"
# device = "cuda"
# 
# pipe = DiffusionPipeline.from_pretrained(base_model_id, torch_dtype=torch.float16, variant="fp16").to(device)
# pipe.load_lora_weights(hf_hub_download(repo_name, ckpt_name))
# pipe.fuse_lora()
# pipe.scheduler = TCDScheduler.from_config(pipe.scheduler.config)

# ============================================================
# PAVEIKSLĖLIŲ GENERAVIMAS
# ============================================================
# Einame per kiekvieną sceną ir „prašome" AI nupiešti paveikslėlį.
# Kiekvienam paveikslėliui sukuriamas pilnas aprašymas:
# data + vieta + objektai + stilius + scenos aprašymas

seed = random.randint(0, sys.maxsize)  # Atsitiktinis skaičius (tam pačiam rezultatui atkurti)
guidance_scale = 5.0  # Kaip tiksliai sekti aprašymą (5-8 optimalus diapazonas)
eta = 0.1  # Detalumo parametras (mažesnis = daugiau detalių)


all_images_list = []  # Čia saugosime visus sugeneruotus paveikslėlius
for image_nr, prompt in enumerate(prompts):
        # Sukuriame pilną piešimo aprašymą su visa informacija apie sceną
        if 'scene_dates' in globals():
          prompt = scene_dates[image_nr]  + ". Location is "+scene_locations[image_nr]+". Objects: " + (", ".join(scene_objects[image_nr]))+ ". " + style + ". "  + prompt
        print(f'{image_nr}    {prompt} ')

        # AI piešia paveikslėlį pagal aprašymą
        images = pipe( prompt = prompt,  num_inference_steps = num_inference_steps ,  guidance_scale = guidance_scale,   eta = eta,    generator = torch.Generator(device).manual_seed(seed),  negative_prompt=negative_prompt   ).images
        image_info_tuple = (image_nr, prompt, images[0]  )
        all_images_list.append(image_info_tuple)

# Parodome pirmąjį sugeneruotą paveikslėlį
all_images_list[0][2]

# ============================================================
# PAVEIKSLĖLIŲ IŠSAUGOJIMAS
# ============================================================
# Kiekvieną paveikslėlį išsaugome kaip JPEG failą,
# tada viską supakuojame į ZIP archyvą ir nukopijuojame į Google Drive.

image_list = [np.array(img[2]) for img in all_images_list]

def save_images(image_list, directory):
    """Išsaugo paveikslėlių sąrašą į nurodytą aplanką kaip JPEG failus."""
    if not os.path.exists(directory):
        os.makedirs(directory)

    for i, image in enumerate(image_list):
        filename = f"image_{i}.jpg"
        filepath = os.path.join(directory, filename)
        cv2.imwrite(filepath, image)


directory = "saved_images"

save_images(image_list, directory)

!zip -r saved_images.zip saved_images
!cp saved_images.zip /content/drive/MyDrive/saved_images.zip

"""
---

## 4. Garso generavimas

Kiekvienai scenai sukuriame garso failą – kompiuteris „perskaito" scenos
aprašymą žmogaus balsu. Naudojame Google Text-to-Speech (gTTS) –
tai ta pati technologija, kurią naudoja Google Translate, kai paspaudžiate
garsiakalbio mygtuką. Pasirinktas britiškas akcentas.
"""

!pip install gTTS -q

'''
# Import the required module for text
# to speech conversion
from gtts import gTTS

# This module is imported so that we can
# play the converted audio
import os

# The text that you want to convert to audio
mytext = 'Welcome to geeksforgeeks Joe!'

# Language in which you want to convert
language = 'en'

# Passing the text and language to the engine,
# here we have marked slow=False. Which tells
# the module that the converted audio should
# have a high speed
myobj = gTTS(text=mytext, lang=language, slow=False)

# Saving the converted audio in a mp3 file named
# welcome
myobj.save("welcome.mp3")
'''

from gtts import gTTS

# Einame per kiekvieną sceną ir sukuriame garso failą
mp3_list = []
for image_nr, prompt in enumerate(prompts):
  mytext = prompt
  # Sukuriame garso failą su britišku akcentu
  myobj = gTTS(text=mytext, lang='en', slow=False, tld='co.uk')  # https://gtts.readthedocs.io/en/latest/module.html#gtts.tts.gTTS
  myobj.save("welcome"+str(image_nr)+".mp3")
  mp3_list.append("welcome"+str(image_nr)+".mp3")
  print(f'{image_nr} ', end='')

"""## 5. Vaizdo įrašo kūrimas

Čia sujungiame viską į galutinį vaizdo įrašą (MP4):
1. Paimame kiekvieną paveikslėlį
2. Prie jo pridedame atitinkamą garso failą
3. Paveikslėlis rodomas tol, kol baigiasi pasakojimas
4. Visus klipus sujungiame į vieną vaizdo įrašą

Rezultatas – MP4 failas su paveikslėliais ir garsiniu pasakojimu,
kurį galima žiūrėti kaip trumpą filmą.
"""

!pip install -q moviepy pillow

import numpy as np
from PIL import Image    # Paveikslėlių konvertavimas
from moviepy.editor import ImageSequenceClip, AudioFileClip, concatenate_videoclips

frames = [np.array(img) for img in image_list]  # Paveikslėliai → duomenų masyvai

# Kuriame vaizdo klipus – kiekvienam paveikslėliui su garsu
video_clips = []
for i, frame in enumerate(frames):
    audio_clip = AudioFileClip(mp3_list[i])  # Atitinkamas garso failas

    # Sukuriame vieno kadro klipą, kurio trukmė = garso trukmė
    img_clip = ImageSequenceClip([frame], durations=[audio_clip.duration])

    # Pridedame garsą prie paveikslėlio
    img_clip = img_clip.set_audio(audio_clip)

    video_clips.append(img_clip)

# Sujungiame visus klipus į vieną vaizdo įrašą
final_clip = concatenate_videoclips(video_clips)

# Eksportuojame kaip MP4 failą
final_clip.write_videofile("output_video_with_audio.mp4", codec="libx264",fps=1)

"""#

---

## ⛔ Senas kodas (nebenaudojamas)

Žemiau esantis kodas yra **senoji versija** – jis nebenaudojamas, bet paliktas
kaip pavyzdys ir atsarginė kopija. Čia buvo naudojama kita piešimo technologija
(Keras/TensorFlow vietoj HuggingFace Diffusers) ir automatinis scenų kūrimas
iš knygos žodžių (vietoj ChatGPT).
"""

#!pip install tensorflow keras_cv --upgrade --quiet

'''
import time
import keras_cv
from tensorflow import keras
import matplotlib.pyplot as plt
import numpy as np
'''

#model = keras_cv.models.StableDiffusion(    img_width=512, img_height=512, jit_compile=False )

'''

images = model.text_to_image("photograph of an astronaut riding a horse", batch_size=3)


def plot_images(images):
    plt.figure(figsize=(20, 20))
    for i in range(len(images)):
        ax = plt.subplot(1, len(images), i + 1)
        plt.imshow(images[i])
        plt.axis("off")


plot_images(images)

'''

'''

promt_text = "The detective watches from the top of the mountain. A flaming dog runs along the mountain"

images = []

for i, style in enumerate(style_list[:]):
    promt_text_final = promt_text + ", style of " + style   + ", high quality, highly detailed"
    print(f"{str(i):<3} {promt_text_final}")
    images_tmp = model.text_to_image(promt_text_final, batch_size=1)
    images.append(images_tmp[0])

'''

'''
n_rows = len(images) // 3 + (len(images) % 3 > 0)
n_cols = min(len(images), 3)

fig, axs = plt.subplots(n_rows, n_cols, figsize=(20, 100))


print(f"promt_text = {promt_text}")

axs = axs.flatten() # Flatten the subplots array to make it easier to iterate over
for i, img in enumerate(images):
    axs[i].imshow(img, aspect='auto')
    axs[i].axis('off')
    axs[i].set_title(f"{style_list[i]}", fontsize=12)

plt.show()
'''

"""
---

## ⛔ Senas knygos iliustravimo kodas (nebenaudojamas)

Šis kodas bandė automatiškai kurti piešimo užduotis iš knygos žodžių –
ieškojo fizinių objektų (daiktų) ir asmenų vardų ir iš jų sudarydavo scenas.
Dabar tai pakeista ChatGPT variantu, kuris kuria geresnius aprašymus.
"""

#@title We load the word and paragraph tables of the book
'''
wn_df_book_token_spacy = pd.read_csv('/content/drive/MyDrive/wn_df_book_token_spacy.tsv', sep='\t')
df_paragraphs = pd.read_csv('/content/drive/MyDrive/df_paragraphs.tsv', sep='\t')
df_chapters_info = pd.read_csv('/content/drive/MyDrive/df_chapters_info.tsv', sep='\t')

'''

#@title We collect words that represent a physical object into phrases that will be fed to the Stable Diffusion model
'''
prompts_dic = {}
number_of_prompts = 0

for index_ch, row_ch in df_chapters_info.iterrows():
    chapter = row_ch['chapter']
    chapter_name = row_ch['chapter_name']

    row_nr = -1
    prev_token_in_chunk = -1
    phrase = ''

    noun_chunk_has_artifact = False
    noun_chunk_has_PERSON = False

    prompt = ''
    prompts = []

    df_one_chapter = wn_df_book_token_spacy[(wn_df_book_token_spacy['chapter'] == chapter)  & (wn_df_book_token_spacy['is_quote'] == 0)]
    for index, row in df_one_chapter.iterrows():
        token = row['token']
        token_in_chunk = row['token_in_chunk']
        wn_lesk_lexname = row['wn_lesk_lexname']
        ent_type = row['ent_type']

        if wn_lesk_lexname == 'noun.artifact':
          noun_chunk_has_artifact = True
        if ent_type == 'PERSON':
          noun_chunk_has_PERSON = True


        if token_in_chunk == 1 :
            phrase += ' ' + token
            chunk_end_index = index
            if token_in_chunk != prev_token_in_chunk :
                chunk_start_index = index


        if token_in_chunk == 0:
            if prev_token_in_chunk == 1 :
              chunk_start_index = index
              if noun_chunk_has_PERSON or noun_chunk_has_artifact:
                if phrase not in prompt:
                  prompt += ' ; ' + phrase
            phrase = ''
            noun_chunk_has_artifact = False
            noun_chunk_has_PERSON = False


        if len(prompt)>100:
          prompts.append(prompt)
          print(f"chapter: {chapter:<2} prompt nr.: {len(prompts):<3}  ->  {prompt.strip()} ")
          #print(f"{prompt.strip()} ")
          prompt = ''

        prev_token_in_chunk = token_in_chunk


    prompts_dic[chapter] = prompts
    print(f"Chapter: {chapter:<2}  Number of prompts: {len(prompts):<2} \n\n ")
    number_of_prompts += len(prompts)

print(f"Number of prompts in the book:  {number_of_prompts}  ")
'''

'''
style =  " style of steampunk digital art ; "  # , high quality, highly detailed,
image_nr = 1
all_images_list = []
end_ganeration = False
for chapter in prompts_dic:
    prompts = prompts_dic[chapter]
    for prompt in prompts:
        print(f'{image_nr} {chapter}   {prompt} ')
        images = model.text_to_image(style  + ' ' +prompt, batch_size=1)
        image_info_tuple = (chapter, prompt, images[0]  )
        all_images_list.append(image_info_tuple)
        image_nr += 1

        if image_nr > 150:
          end_ganeration = True
          break

    if end_ganeration:
      break
'''

'''
import matplotlib.pyplot as plt
print(all_images_list[3][1])
plt.axis("off")
plt.imshow(all_images_list[3][2])
'''

"""
---

## ⛔ Senas vaizdo kūrimo kodas (nebenaudojamas)

Senesnė vaizdo įrašo kūrimo versija su OpenCV (be garso) ir paprastas
moviepy variantas. Pakeista naujesnė versija su garso palaikymu.
"""

'''
import cv2
import numpy as np

video_name = 'output_video3.mp4'  #

image_shape = (512, 512)

fourcc = cv2.VideoWriter_fourcc(*'mp4v')

video = cv2.VideoWriter(video_name, fourcc, 1, image_shape)


font = cv2.FONT_HERSHEY_SIMPLEX
font_scale = 0.3
font_color = (255, 255, 255)
font_thickness = 1


for image_tuple in all_images_list:
    text = image_tuple[1]
    print(text)
    image = image_tuple[2]

    image = np.array(image)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    image_with_text = image.copy()

    cv2.putText(image, text, (2, 20), font, font_scale, font_color, font_thickness)

    video.write(image)

cv2.destroyAllWindows()
video.release()
'''

#image_list = [np.array(img[2]) for img in all_images_list]

'''
import numpy as np
from PIL import Image
from moviepy.editor import ImageSequenceClip



# Convert images to numpy arrays
frames = [np.array(img) for img in image_list]

# Create the video clip
fps = 1
clip = ImageSequenceClip(frames, fps=fps)

# Write the video file
clip.write_videofile("output_video.mp4", codec="libx264")
'''