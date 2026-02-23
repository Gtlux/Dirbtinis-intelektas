# Chat Conversation

Note: _This is purely the output of the chat conversation and does not contain any raw data, codebase snippets, etc. used to generate the output._

### User Input

pilnai perskaityk visa musu aplankalo struktura ir padaryk sita uzduoti
1.2 Paleisti 2 paieškos uždavinius , suprasti ką jie daro ir (atsiskaitymo metu) pakomentuoti dėstytojui t.y. paaiškinti kas yra pirminė būsena, galinė būsena ir kokius kintamuosius reikia naudoti šių būsenų aprašymui. Atsiskaitymo metu turėti nubraižytą schemą (ranka ant lapo), kurioje būtų pavaizduotos bent 5 būsenos su kintamųjų reikšmėmis. 

 Atsiskaitymo metu mokėti paaiškinti dėstytojui: Kaip dirbant su "eile" realizuojama paieška į gylį ir į plotį. Mokėti paaiškinti kokias euristikas galima naudoti siekiant pagreitinti paiešką. Paaiškinkite dėstytojui algoritmo veikimo principus naudodami savo pavyzdžius. Kad būtų aiškiau pažiūrėkite šias video paskaitas: Search Algorithm  

uzduotims analizuoti paimk eighpuzzle ir graphmapproblem, tiksliai paaiskink paeskos i gylius ir plocius kaip jie veikia irgi.

*Listed directory [Artificial-Intelligence-Course-main](file:///c:/Users/jarek/Desktop/dirbt%20intelekt%202/Artificial-Intelligence-Course-main) *

*Viewed [EightPuzzle.py](file:///c:/Users/jarek/Desktop/dirbt%20intelekt%202/Artificial-Intelligence-Course-main/EightPuzzle.py) *

*Viewed [GraphMapProblem.py](file:///c:/Users/jarek/Desktop/dirbt%20intelekt%202/Artificial-Intelligence-Course-main/GraphMapProblem.py) *

*Analyzed [search.py](file:///c:/Users/jarek/Desktop/dirbt%20intelekt%202/Artificial-Intelligence-Course-main/search.py) *

### Planner Response

Now let me read the key search algorithms and the EightPuzzle/GraphProblem classes from [search.py](cci:7://file:///c:/Users/jarek/Desktop/dirbt%20intelekt%202/Artificial-Intelligence-Course-main/search.py:0:0-0:0):

*Viewed code item*

*Analyzed [search.py](file:///c:/Users/jarek/Desktop/dirbt%20intelekt%202/Artificial-Intelligence-Course-main/search.py) *

### Planner Response

Now let me also read the [maps.py](cci:7://file:///c:/Users/jarek/Desktop/dirbt%20intelekt%202/Artificial-Intelligence-Course-main/maps.py:0:0-0:0) and [notebook.py](cci:7://file:///c:/Users/jarek/Desktop/dirbt%20intelekt%202/Artificial-Intelligence-Course-main/notebook.py:0:0-0:0) for the `switch_country_map` and `show_map` functions, plus the Node class:

*Viewed [maps.py](file:///c:/Users/jarek/Desktop/dirbt%20intelekt%202/Artificial-Intelligence-Course-main/maps.py) *

*Viewed code item*

### Planner Response

Now let me look at the [notebook.py](cci:7://file:///c:/Users/jarek/Desktop/dirbt%20intelekt%202/Artificial-Intelligence-Course-main/notebook.py:0:0-0:0) for `switch_country_map` and `show_map`:

*Grep searched codebase*

*Grep searched codebase*

### Planner Response

Let me find where the Romania map data is actually defined:

*Grep searched codebase*

*Grep searched codebase*

### Planner Response

Now let me read the Romania map data to understand the graph structure:

### Planner Response

Let me read the Romania map graph data to provide concrete examples:

*Viewed [search.py](file:///c:/Users/jarek/Desktop/dirbt%20intelekt%202/Artificial-Intelligence-Course-main/search.py) *

### Planner Response

Now I have all the information needed. Let me create the comprehensive analysis document.

*Edited relevant file*

*Edited relevant file*

### User Input

This is a system-generated message that is sent due to the user's review policy. Proceed with the decision that you think is the most optimal here.

### Planner Response

Puiku! Dokumentas patvirtintas ✅ Sėkmės atsiskaityme! Jei reikės papildomų paaiškinimų ar pagalbos ruošiantis – kreipkis drąsiai.

### User Input

5+ būsenų schema (EightPuzzle) sita neturi jokios prasmes, geriau padaryk busenu schema su veiksmais kur galine turetu buti 12345678

### Planner Response

Supratau – reikia tikros sprendimo sekos nuo pradinės iki galinės būsenos. Pirma paleisiu programą, kad gaučiau tikslią veiksmų seką:

*User accepted the command `python EightPuzzle.py`*

### Planner Response

Sprendimas yra `['UP', 'LEFT', 'UP', 'LEFT', 'DOWN', 'RIGHT', 'RIGHT', 'DOWN']` – 8 žingsniai. Dabar sukursiu tikrą būsenų seką nuo pradžios iki galo:

*Viewed [walkthrough.md](file:///C:/Users/jarek/.gemini/antigravity/brain/738d38b3-357d-4317-8d81-c55830a76ba1/walkthrough.md) *

### Planner Response

Now let me trace through the solution manually. Starting state: [(2,4,3,1,5,6,7,8,0)](cci:1://file:///c:/Users/jarek/Desktop/dirbt%20intelekt%202/Artificial-Intelligence-Course-main/search.py:591:4-595:67), blank at index 8. Actions: `UP, LEFT, UP, LEFT, DOWN, RIGHT, RIGHT, DOWN`.

Let me compute each step and replace the section:

*Edited relevant file*

### Planner Response

Paruošta! Dabar būsenų schema rodo **tikrą sprendimo kelią** nuo pradžios iki galo:

```
(2,4,3,1,5,6,7,8,0) → UP → LEFT → UP → LEFT → DOWN → RIGHT → RIGHT → DOWN → (1,2,3,4,5,6,7,8,0) ✅
```

9 būsenos (0–8), kiekvienoje matosi [state](cci:1://file:///c:/Users/jarek/Desktop/dirbt%20intelekt%202/Artificial-Intelligence-Course-main/search.py:949:4-950:33), [depth](cci:1://file:///c:/Users/jarek/Desktop/dirbt%20intelekt%202/Artificial-Intelligence-Course-main/search.py:334:0-353:63), [cost](cci:1://file:///c:/Users/jarek/Desktop/dirbt%20intelekt%202/Artificial-Intelligence-Course-main/search.py:2240:4-2241:64) ir lentelės vizualizacija. Dabar galėsi lengvai perpiešti ant lapo – kiekviena būsena eina viena po kitos su rodyklėmis ir veiksmų pavadinimais.

### User Input

tavo schemos lakeliai kur paisyta siek tiek suvalgyti, pataisyk

*Viewed [walkthrough.md](file:///C:/Users/jarek/.gemini/antigravity/brain/738d38b3-357d-4317-8d81-c55830a76ba1/walkthrough.md) *

### Planner Response

Suprantu – dviejų stulpelių layout'as gali būti sunkiai skaitomas. Perrašysiu schemą vertikaliai – viena būsena po kitos, aiškiai ir tvarkingai:

*Edited relevant file*

### User Input

continue

### Planner Response

Viskas jau paruošta! Dokumentas [walkthrough.md](cci:7://file:///C:/Users/jarek/.gemini/antigravity/brain/738d38b3-357d-4317-8d81-c55830a76ba1/walkthrough.md:0:0-0:0) yra pilnai baigtas su visomis dalimis:

1. ✅ **EightPuzzle** – pradinė/galinė būsena, kintamieji, **9 būsenų schema** (vertikali, tvarkinga) nuo [(2,4,3,1,5,6,7,8,0)](cci:1://file:///c:/Users/jarek/Desktop/dirbt%20intelekt%202/Artificial-Intelligence-Course-main/search.py:507:4-511:16) iki [(1,2,3,4,5,6,7,8,0)](cci:1://file:///c:/Users/jarek/Desktop/dirbt%20intelekt%202/Artificial-Intelligence-Course-main/search.py:507:4-511:16)
2. ✅ **GraphMapProblem** – Arad→Bucharest, 7+ būsenų schema
3. ✅ **BFS** – FIFO eilė, `popleft()`, žingsnis po žingsnio lentelė
4. ✅ **DFS** – LIFO stekas, [pop()](cci:1://file:///c:/Users/jarek/Desktop/dirbt%20intelekt%202/Artificial-Intelligence-Course-main/search.py:1051:0-1062:21), žingsnis po žingsnio
5. ✅ **BFS vs DFS palyginimas** – lentelė
6. ✅ **Euristikos** – misplaced tiles, straight-line distance, Greedy/A*/Uniform
7. ✅ **Kaip paleisti** – komandos

Ar dar kažką norėtum papildyti ar pakeisti?

### User Input

kokie uzdaviniai musu faile naudoja dfs

*Grep searched codebase*

### Planner Response

**Nė vienas iš pagrindinių uždavinių** ([EightPuzzle.py](cci:7://file:///c:/Users/jarek/Desktop/dirbt%20intelekt%202/Artificial-Intelligence-Course-main/EightPuzzle.py:0:0-0:0), [GraphMapProblem.py](cci:7://file:///c:/Users/jarek/Desktop/dirbt%20intelekt%202/Artificial-Intelligence-Course-main/GraphMapProblem.py:0:0-0:0)) **nenaudoja DFS** tiesiogiai. Štai ką radau:

| Failas | DFS naudojimas |
|---|---|
| [EightPuzzle.py](cci:7://file:///c:/Users/jarek/Desktop/dirbt%20intelekt%202/Artificial-Intelligence-Course-main/EightPuzzle.py:0:0-0:0) | ❌ Naudoja tik [breadth_first_graph_search](cci:1://file:///c:/Users/jarek/Desktop/dirbt%20intelekt%202/Artificial-Intelligence-Course-main/search.py:272:0-296:15) (BFS) |
| [GraphMapProblem.py](cci:7://file:///c:/Users/jarek/Desktop/dirbt%20intelekt%202/Artificial-Intelligence-Course-main/GraphMapProblem.py:0:0-0:0) | ❌ Naudoja [breadth_first](cci:1://file:///c:/Users/jarek/Desktop/dirbt%20intelekt%202/Artificial-Intelligence-Course-main/search.py:183:0-199:15), [best_first](cci:1://file:///c:/Users/jarek/Desktop/dirbt%20intelekt%202/Artificial-Intelligence-Course-main/search.py:299:0-326:15), [uniform](cci:1://file:///c:/Users/jarek/Desktop/dirbt%20intelekt%202/Artificial-Intelligence-Course-main/search.py:1077:0-1085:42), [astar](cci:1://file:///c:/Users/jarek/Desktop/dirbt%20intelekt%202/Artificial-Intelligence-Course-main/search.py:454:0-459:82), [random](cci:1://file:///c:/Users/jarek/Desktop/dirbt%20intelekt%202/Artificial-Intelligence-Course-main/search.py:248:0-267:15) – **bet ne DFS** |
| [gui/eight_puzzle.py](cci:7://file:///c:/Users/jarek/Desktop/dirbt%20intelekt%202/Artificial-Intelligence-Course-main/gui/eight_puzzle.py:0:0-0:0) | ⚠️ Turi **užkomentuotas** DFS eilutes ([depth_first_tree_search](cci:1://file:///c:/Users/jarek/Desktop/dirbt%20intelekt%202/Artificial-Intelligence-Course-main/search.py:202:0-218:15) ir [depth_first_graph_search](cci:1://file:///c:/Users/jarek/Desktop/dirbt%20intelekt%202/Artificial-Intelligence-Course-main/search.py:221:0-240:15)), bet nenaudoja |
| [csp.py](cci:7://file:///c:/Users/jarek/Desktop/dirbt%20intelekt%202/Artificial-Intelligence-Course-main/csp.py:0:0-0:0) | ✅ Naudoja [depth_first_tree_search](cci:1://file:///c:/Users/jarek/Desktop/dirbt%20intelekt%202/Artificial-Intelligence-Course-main/search.py:202:0-218:15) CSP (Constraint Satisfaction Problem) sprendimui |
| [NQueensProblem](cci:2://file:///c:/Users/jarek/Desktop/dirbt%20intelekt%202/Artificial-Intelligence-Course-main/search.py:1937:0-1994:28) (search.py) | ✅ Docstringe parodyta, kad [depth_first_tree_search(NQueensProblem(8))](cci:1://file:///c:/Users/jarek/Desktop/dirbt%20intelekt%202/Artificial-Intelligence-Course-main/search.py:202:0-218:15) veikia |

**Trumpai**: DFS iš tikrųjų naudoja tik [csp.py](cci:7://file:///c:/Users/jarek/Desktop/dirbt%20intelekt%202/Artificial-Intelligence-Course-main/csp.py:0:0-0:0) ir [NQueensProblem](cci:2://file:///c:/Users/jarek/Desktop/dirbt%20intelekt%202/Artificial-Intelligence-Course-main/search.py:1937:0-1994:28). Tavo du pagrindiniai uždaviniai ([EightPuzzle.py](cci:7://file:///c:/Users/jarek/Desktop/dirbt%20intelekt%202/Artificial-Intelligence-Course-main/EightPuzzle.py:0:0-0:0) ir [GraphMapProblem.py](cci:7://file:///c:/Users/jarek/Desktop/dirbt%20intelekt%202/Artificial-Intelligence-Course-main/GraphMapProblem.py:0:0-0:0)) naudoja **BFS** ir kitus informuotus algoritmus.

### User Input

gerai padaryk dabar sita uzduoti 
1.3 Paaiškinti paieškos uždavinio architektūrą trasuojant (debug) kodą.
 
Debug rėžimu praeiname visus skaičiavimus ir išsiaiškiname tipinę dirbtinio intelekto agento architektūrą bei šio pavyzdžio algoritmą. Atsiskaitant studentas turi paaiškinti dėstytojui pagrindinius architektūrinius komponentus (klasės) bei algoritmo veikimo principus.
abiems musu nagrinetams uzdaviniams

*Viewed code item*

*Edited relevant file*

### User Input

This is a system-generated message that is sent due to the user's review policy. Proceed with the decision that you think is the most optimal here.

### Planner Response

Puiku, dokumentas patvirtintas ✅ Abu dokumentai paruošti:

- **1.2** – [walkthrough.md](cci:7://file:///C:/Users/jarek/.gemini/antigravity/brain/738d38b3-357d-4317-8d81-c55830a76ba1/walkthrough.md:0:0-0:0) (būsenos, BFS/DFS, euristikos)
- **1.3** – [debug_walkthrough.md](cci:7://file:///C:/Users/jarek/.gemini/antigravity/brain/738d38b3-357d-4317-8d81-c55830a76ba1/debug_walkthrough.md:0:0-0:0) (architektūra, trasavimas, breakpointai)

Sėkmės atsiskaityme! Jei reikės dar ko – kreipkis.

### User Input

kas yra cps ir nqueensproblem?

### Planner Response

## CSP (Constraint Satisfaction Problem)

**CSP** – tai **apribojimų tenkinimo uždavinys**. Tai specialus AI uždavinių tipas, kur reikia rasti kintamųjų reikšmes, kurios tenkina visus nurodytus apribojimus.

CSP sudaro:
- **Kintamieji** – ką reikia nustatyti
- **Domenai** – galimos reikšmės kiekvienam kintamajam
- **Apribojimai** – taisyklės, kurias turi tenkinti kintamųjų reikšmės

**Pavyzdys**: žemėlapio spalvinimas ([coloring_map.py](cci:7://file:///c:/Users/jarek/Desktop/dirbt%20intelekt%202/Artificial-Intelligence-Course-main/coloring_map.py:0:0-0:0) tavo projekte) – kiekvienai šaliai priskirti spalvą, kad kaimyninės šalys turėtų skirtingas spalvas.

---

## NQueensProblem

**N karalienių uždavinys** – klasikinis CSP pavyzdys. Reikia sudėlioti **N karalienių** ant N×N šachmatų lentos taip, kad **jokios dvi karalienės viena kitos nekirsdintų** (nei horizontaliai, nei vertikaliai, nei įstrižai).

**Pavyzdys su 4 karalienėmis:**
```
┌───┬───┬───┬───┐
│   │ ♛ │   │   │
├───┼───┼───┼───┤
│   │   │   │ ♛ │
├───┼───┼───┼───┤
│ ♛ │   │   │   │
├───┼───┼───┼───┤
│   │   │ ♛ │   │
└───┴───┴───┴───┘
```

Tavo projekte [NQueensProblem](cci:2://file:///c:/Users/jarek/Desktop/dirbt%20intelekt%202/Artificial-Intelligence-Course-main/search.py:1937:0-1994:28) yra [search.py](cci:7://file:///c:/Users/jarek/Desktop/dirbt%20intelekt%202/Artificial-Intelligence-Course-main/search.py:0:0-0:0) faile ir sprendžiamas su [depth_first_tree_search](cci:1://file:///c:/Users/jarek/Desktop/dirbt%20intelekt%202/Artificial-Intelligence-Course-main/search.py:202:0-218:15) – būtent **šis uždavinys naudoja DFS**, nes medis yra gilus, bet siauras (kiekviename lygyje dedame vieną karalienę į eilutę).

---

**Trumpai**: abu šie uždaviniai yra tavo projekte, bet jie **nesusiję** su tavo 1.2/1.3 atsiskaitymo užduotimis (EightPuzzle ir GraphMapProblem).

### User Input

gerai, padaryk dabar sita dali
1.4 Sukurti savo paieškos uždavinio sistemą naudojant aima architektūrą bei VC Copilot AI arba Google Antigravity (neredaguoti koda , parodyti atsiskaitymo metu tik Prompt'us).  Atsiskaitymo metu kiekvienas turi sugebėti paaiškinti ką daro kodas.


*Edited relevant file*

*User accepted the command `python WaterJugProblem.py`*

### Planner Response

Unicode issue with the console. Let me fix the print statements:

*Edited relevant file*

*User accepted the command `python WaterJugProblem.py`*

### Planner Response

Veikia puikiai! Dabar sukuriu prompt'ų dokumentaciją:

*Edited relevant file*

### User Input

This is a system-generated message that is sent due to the user's review policy. Proceed with the decision that you think is the most optimal here.

### Planner Response

Viskas patvirtinta ✅ Visos užduotys baigtos:

- **1.2** – [walkthrough.md](cci:7://file:///C:/Users/jarek/.gemini/antigravity/brain/738d38b3-357d-4317-8d81-c55830a76ba1/walkthrough.md:0:0-0:0) (būsenos, BFS/DFS, euristikos)
- **1.3** – [debug_walkthrough.md](cci:7://file:///C:/Users/jarek/.gemini/antigravity/brain/738d38b3-357d-4317-8d81-c55830a76ba1/debug_walkthrough.md:0:0-0:0) (architektūra, trasavimas, breakpointai)
- **1.4** – [WaterJugProblem.py](cci:7://file:///c:/Users/jarek/Desktop/dirbt%20intelekt%202/Artificial-Intelligence-Course-main/WaterJugProblem.py:0:0-0:0) + [custom_problem.md](cci:7://file:///C:/Users/jarek/.gemini/antigravity/brain/738d38b3-357d-4317-8d81-c55830a76ba1/custom_problem.md:0:0-0:0) (savo uždavinys + prompt'ai)

Sėkmės atsiskaityme! 🎓

### User Input

gal padaryk geriau kita, kokia fermerio lapes vistos ir grudu per upe uzdaviny. Tik koda kiekviena eilute aprasyk ka daro, ir geriau kad koda galima butu pasileist

*Edited relevant file*

*User accepted the command `python WaterJugProblem.py`*

### Planner Response

Veikia puikiai! 🎉 Failas perrašytas su fermerio uždaviniu. Štai rezultatas:

**Sprendimas per 7 žingsnius:**
```
0: Visi KAIRĖJE          → VEZTI_VISTA
1: Višta DEŠINĖJE        → PLAUKTI_VIENAM (grįžta tuščias)
2: Fermeris KAIRĖJE      → VEZTI_LAPE
3: Lapė+Višta DEŠINĖJE   → VEZTI_VISTA (grąžina vištą atgal!)
4: Višta KAIRĖJE         → VEZTI_GRUDUS
5: Grūdai+Lapė DEŠINĖJE  → PLAUKTI_VIENAM (grįžta tuščias)
6: Fermeris KAIRĖJE      → VEZTI_VISTA
7: Visi DEŠINĖJE         → TIKSLAS! ✅
```

Kiekviena kodo eilutė yra pakomentuota lietuviškai. Failas: [WaterJugProblem.py](cci:7://file:///c:/Users/jarek/Desktop/dirbt%20intelekt%202/Artificial-Intelligence-Course-main/WaterJugProblem.py:0:0-0:0) (galima pervadinti į `FarmerProblem.py` jei nori).

### User Input

pamirsai redatuoti custom_problem.md pagal nauja uzdavini

*Edited relevant file*

### Planner Response

Paruošta ✅ [custom_problem.md](cci:7://file:///C:/Users/jarek/.gemini/antigravity/brain/738d38b3-357d-4317-8d81-c55830a76ba1/custom_problem.md:0:0-0:0) atnaujintas su fermerio uždaviniu – prompt'ai, kodo paaiškinimas, rezultatų lentelė.

### User Input

gerai, padaryk dabar sita dali
1.4 Sukurti savo paieškos uždavinio sistemą naudojant aima architektūrą bei VC Copilot AI arba Google Antigravity (neredaguoti koda , parodyti atsiskaitymo metu tik Prompt'us).  Atsiskaitymo metu kiekvienas turi sugebėti paaiškinti ką daro kodas.

gal padaryk geriau kita, kokia fermerio lapes vistos ir grudu per upe uzdaviny. Tik koda kiekviena eilute aprasyk ka daro, ir geriau kad koda galima butu pasileist
tokie buvo promptai, tai juos ir dek


*Edited relevant file*

### Planner Response

Paruošta ✅ Prompt'ai dabar tiksliai tokie, kokius rašei. Pirmas – pilna užduoties formuluotė, antras – fermerio uždavinio prašymas su komentarais.

*Edited relevant file*

### User Input

gerai, kitas klausimas, ar yra koks nors antigravity extension kuris tau leistu kurti skaidres?

### Planner Response

Ne, Antigravity neturi specialaus extension'o skaidrėms kurti. Bet yra keli variantai:

1. **HTML skaidrės su reveal.js** – galiu sukurti `.html` failą, kuris veikia kaip prezentacija naršyklėje. Atrodytų profesionaliai, su animacijomis, ir nereikia jokio PowerPoint.

2. **Markdown → skaidrės** – jei naudoji VS Code, yra extension'as **Marp** (`marp-team.marp-vscode`), kuris leidžia rašyti skaidres Markdown formatu ir eksportuoti į PDF/PPTX. Aš galiu parašyti tą Markdown.

3. **Python-pptx** – galiu sugeneruoti tikrą `.pptx` PowerPoint failą per Python kodą.

Kuris variantas labiausiai tiktų? Ar tiesiog reikia skaidrių atsiskaitymui?

### User Input

3, jo, reikia dabar is visu tu musu aprasymu sudaryti skaidres

*User accepted the command `pip install python-pptx`*

*User accepted the command `python -m pip install python-pptx`*

### Planner Response

Jau suinstaliuota. Dabar kuriu skaidrių generavimo skriptą:

*Edited relevant file*

*User accepted the command `python create_slides.py`*

### User Input

paaiskink kaip veikia bfs ir dfs kuo detaliau su pavyzdziais

### Planner Response

## BFS (Breadth-First Search) – Paieška į plotį

### Principas

BFS naudoja **FIFO eilę** (First In, First Out) – kaip eilė parduotuvėje: **kas pirmas atėjo, tas pirmas aptarnaujamas**.

### Kaip veikia žingsnis po žingsnio

Įsivaizduok tokį medį:

```
            A
          / | \
         B  C  D
        /|     |
       E  F    G
       |
       H
```

**BFS eina LYGIAIS – visus vieno lygio mazgus pirma, tik tada kitą lygį:**

| Žingsnis | Eilė (frontier) | Išimame | Vaikai | Kas vyksta |
|---|---|---|---|---|
| 0 | `[A]` | – | – | Pradžia |
| 1 | `[B, C, D]` | `A` (popleft) | B, C, D | Ištyrėme A, jo vaikus dedame į GALĄ |
| 2 | `[C, D, E, F]` | `B` (popleft) | E, F | Ištyrėme B (pirmas eilėje!), vaikus į galą |
| 3 | `[D, E, F]` | `C` (popleft) | – | C neturi vaikų |
| 4 | `[E, F, G]` | `D` (popleft) | G | Ištyrėme D |
| 5 | `[F, G, H]` | `E` (popleft) | H | Ištyrėme E |
| 6 | `[G, H]` | `F` (popleft) | – | F neturi vaikų |
| 7 | `[H]` | `G` (popleft) | – | – |
| 8 | `[]` | `H` (popleft) | – | Medis ištirtas! |

**Aplankyta tvarka: `A → B → C → D → E → F → G → H`** (lygis po lygio)

### Kodas

```python
frontier = deque([pradinis_mazgas])  # FIFO eilė
explored = set()

while frontier:
    node = frontier.popleft()        # ← ima IŠ PRIEKIO (pirmas atėjo)
    explored.add(node.state)
    
    for child in node.expand():      # vaikų mazgai
        if child not in explored:
            frontier.append(child)   # ← deda Į GALĄ
```

**Esmė**: `popleft()` = ima seniausią mazgą. Todėl BFS **visada pirmiau aplanko arčiau šaknies esančius mazgus**.

---

## DFS (Depth-First Search) – Paieška į gylį

### Principas

DFS naudoja **LIFO steką** (Last In, First Out) – kaip krūva lėkščių: **kas paskutinis padėtas ant viršaus, tą pirma paimi**.

### Kaip veikia žingsnis po žingsnio

Tas pats medis:

```
            A
          / | \
         B  C  D
        /|     |
       E  F    G
       |
       H
```

**DFS eina GILYN – kuo giliau, kol gali, tada grįžta:**

| Žingsnis | Stekas (frontier) | Išimame | Vaikai | Kas vyksta |
|---|---|---|---|---|
| 0 | `[A]` | – | – | Pradžia |
| 1 | `[B, C, D]` | `A` (pop) | B, C, D | Ištyrėme A, vaikus dedame į galą |
| 2 | `[B, C, G]` | `D` (pop) | G | **D paskutinis, todėl jį ima!** Eina gilyn |
| 3 | `[B, C]` | `G` (pop) | – | G neturi vaikų, grįžta |
| 4 | `[B]` | `C` (pop) | – | C neturi vaikų |
| 5 | `[E, F]` | `B` (pop) | E, F | Ištyrėme B |
| 6 | `[E]` | `F` (pop) | – | F paskutinis – ima jį |
| 7 | `[H]` | `E` (pop) | H | Eina gilyn per E |
| 8 | `[]` | `H` (pop) | – | Medis ištirtas! |

**Aplankyta tvarka: `A → D → G → C → B → F → E → H`** (gilyn pirma!)

### Kodas

```python
frontier = [pradinis_mazgas]  # LIFO stekas (paprastas list)
explored = set()

while frontier:
    node = frontier.pop()            # ← ima IŠ GALO (paskutinis atėjo!)
    explored.add(node.state)
    
    for child in node.expand():
        if child not in explored:
            frontier.append(child)   # ← deda Į GALĄ (ant viršaus)
```

**Esmė**: [pop()](cci:1://file:///c:/Users/jarek/Desktop/dirbt%20intelekt%202/Artificial-Intelligence-Course-main/search.py:1051:0-1062:21) = ima naujausią mazgą. Todėl DFS **visada eina kuo giliau** – pirma ištirs visą šaką, tik tada grįš.

---

## Vizualus palyginimas

```
Medis:      A
          / | \
         B  C  D
        /|     |
       E  F    G
       |
       H

BFS tvarka: A → B → C → D → E → F → G → H
            ▔▔▔   ▔▔▔▔▔▔▔   ▔▔▔▔▔▔▔   ▔
            lygis0  lygis1    lygis2   lygis3

DFS tvarka: A → D → G → C → B → F → E → H
            │   └──gilyn    │   └──gilyn──┘
            └──────────────grįžta atgal
```

## Esminis skirtumas viena eilute

| | BFS | DFS |
|---|---|---|
| **Kodas** | `frontier.popleft()` | `frontier.pop()` |
| **Kas vyksta** | Ima **seniausią** (pirmas atėjo) | Ima **naujausią** (paskutinis atėjo) |
| **Rezultatas** | Eina **lygiais** (plotis) | Eina **gilyn** (gylis) |

Tai **vienintelis skirtumas kode** – `popleft()` vs [pop()](cci:1://file:///c:/Users/jarek/Desktop/dirbt%20intelekt%202/Artificial-Intelligence-Course-main/search.py:1051:0-1062:21). Viskas kita (expand, explored, append) – identišku! 🎯

### User Input

1.2 walkthrough.md, as ji idejau i ataskaitos faila, paaiskink man tiksliai kaip veikia grapmapproblem tam faile

### Planner Response

Žiūrėk, paaiškinu tiksliai kas vyksta [GraphMapProblem.py](cci:7://file:///c:/Users/jarek/Desktop/dirbt%20intelekt%202/Artificial-Intelligence-Course-main/GraphMapProblem.py:0:0-0:0) kode eilutė po eilutės:

## GraphMapProblem.py – kaip veikia

### 1. Importai ir žemėlapio pasirinkimas (1-6 eil.)

```python
from search import *       # Importuoja VISKĄ iš search.py: Problem, Node, BFS, DFS, A*, GraphProblem...
from notebook import *     # Importuoja vizualizacijos funkciją show_map()

country = "Romania"        # Pasirenkame šalį (galima keisti į "Lithuania", "India"...)
switch_country_map(country) # Ši funkcija užpildo maps.py kintamuosius:
                           #   maps.romania_map_start = "Arad"
                           #   maps.romania_map_goal = "Bucharest"  
                           #   maps.romania_map = UndirectedGraph({Arad:{Zerind:75, Sibiu:140,...}})
```

### 2. Uždavinio sukūrimas (8 eil.)

```python
romania_problem = GraphProblem(maps.romania_map_start, maps.romania_map_goal, maps.romania_map)
```

Tai sukuria [GraphProblem](cci:2://file:///c:/Users/jarek/Desktop/dirbt%20intelekt%202/Artificial-Intelligence-Course-main/search.py:1879:0-1915:25) objektą su:
- `self.initial = "Arad"` – **pradinė būsena** (iš kurio miesto pradedame)
- `self.goal = "Bucharest"` – **galinė būsena** (kur norime patekti)
- `self.graph = romania_map` – **grafas** (žemėlapis su miestais ir atstumais)

### 3. Paieškos metodo pasirinkimas (10-21 eil.)

```python
search_method = "breadth_first"   # Čia pasirenkame algoritmą
```

Pagal `search_method` reikšmę paleidžiamas vienas iš algoritmų:
- `"breadth_first"` → [breadth_first_graph_search()](cci:1://file:///c:/Users/jarek/Desktop/dirbt%20intelekt%202/Artificial-Intelligence-Course-main/search.py:272:0-296:15) – BFS, FIFO eilė
- `"best_first"` → euristinė paieška su [h(n)](cci:1://file:///c:/Users/jarek/Desktop/dirbt%20intelekt%202/Artificial-Intelligence-Course-main/search.py:941:4-943:44) (tiesioginis atstumas iki tikslo)
- `"uniform"` → pagal mažiausią kelionės kainą [g(n)](cci:1://file:///c:/Users/jarek/Desktop/dirbt%20intelekt%202/Artificial-Intelligence-Course-main/search.py:1145:4-1153:31)
- `"astar"` → A* algoritmas [f(n) = g(n) + h(n)](cci:1://file:///c:/Users/jarek/Desktop/dirbt%20intelekt%202/Artificial-Intelligence-Course-main/search.py:2146:4-2163:25) (optimalus!)
- `"random"` → atsitiktinė paieška

### 4. Kas vyksta viduje kai paleidi BFS?

```python
solution = breadth_first_graph_search(romania_problem).solution()
```

**Žingsnis po žingsnio:**

```
1) Sukuria Node(state="Arad", depth=0, cost=0)
2) Deda jį į frontier (FIFO eilę)

3) Ima "Arad" iš eilės, klausia: problem.actions("Arad")
   → graph.get("Arad").keys() → ["Zerind", "Sibiu", "Timisoara"]
   
   Kiekvienam kaimynui sukuria vaikinį mazgą:
   - Node("Zerind",    parent=Arad, cost=75)
   - Node("Sibiu",     parent=Arad, cost=140)
   - Node("Timisoara", parent=Arad, cost=118)
   
   Deda visus į eilės GALĄ

4) Ima "Zerind" (pirmą eilėje) → kaimynai: Oradea
5) Ima "Sibiu" → kaimynai: Fagaras, Rimnicu, Oradea
6) Ima "Timisoara" → kaimynai: Lugoj
...
N) Expand("Fagaras") → vaikas "Bucharest" → goal_test("Bucharest") = TRUE!
   → return Node("Bucharest")
```

**`.solution()`** eina per `parent` grandinę atgal:
```
Bucharest.parent = Fagaras
Fagaras.parent = Sibiu  
Sibiu.parent = Arad (šaknis, parent=None)

→ Surenka veiksmus: ["Sibiu", "Fagaras", "Bucharest"]
```

### 5. Sprendimo atvaizdavimas (23-43 eil.)

```python
solution.insert(0, maps.romania_map_start)  # Prideda "Arad" į pradžią
# Dabar: ["Arad", "Sibiu", "Fagaras", "Bucharest"]

print(f'solution size is {len(solution)} and solution : {solution}')
```

Tada kodas:
- Nuspalvina sprendimo kelio miestus **žaliai** (`node_colors`)
- Paima miestų koordinates iš `maps.romania_map.locations` 
- Paima kelių svoriuose (`edge_weights`)
- Iškviečia `show_map()` – atidaro langą su Rumunijos žemėlapiu, kur kelias pažymėtas žaliai

### Trumpai visas procesas

```
GraphMapProblem.py
    │
    ├─ switch_country_map("Romania")     ← užkrauna grafą
    ├─ GraphProblem("Arad","Bucharest")  ← sukuria uždavinį
    ├─ breadth_first_graph_search()      ← ieško kelio BFS
    │     └─ Node.expand() → actions() → result() → child_node() (ciklas)
    ├─ .solution()                       ← grąžina veiksmų seką
    └─ show_map()                        ← vizualizacija
```

Ar reikia dar kažką patikslinti? 🙂

### User Input

taip, 1.3 debug_walkthrough.md man rodo ne diagrama o koda tiesiog

### Planner Response

A, mermaid diagrama neveikia jų peržiūroje. Pakeisiu ją į tekstinę diagramą, kuri veiks visur:

*Viewed [debug_walkthrough.md](file:///C:/Users/jarek/.gemini/antigravity/brain/738d38b3-357d-4317-8d81-c55830a76ba1/debug_walkthrough.md) *

### Planner Response

Pakeisiu mermaid diagramą į tekstinę, kuri veiks visur:

*Edited relevant file*

### Planner Response

Paruošta ✅ Mermaid diagrama pakeista į tekstinę ASCII diagramą – dabar turėtų teisingai rodytis bet kokioje peržiūroje. Reikės iš naujo nukopijuoti [debug_walkthrough.md](cci:7://file:///C:/Users/jarek/.gemini/antigravity/brain/738d38b3-357d-4317-8d81-c55830a76ba1/debug_walkthrough.md:0:0-0:0) į savo `ataskaitos` aplanką.

### User Input

gali grazinti kaip buvo?

*Edited relevant file*

### Planner Response

Grąžinta ✅ Mermaid diagrama vėl kaip buvo originaliai.