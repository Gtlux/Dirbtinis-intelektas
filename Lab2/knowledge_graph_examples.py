# =============================================================================
# 2.2 — Žinių grafai ir žinių bazės (Knowledge Graphs & Knowledge Bases)
# =============================================================================
# Šis failas demonstruoja RDF žinių grafų kūrimą naudojant Python 'rdflib'.
#
# ===== Kas yra žinių grafas? =====
# Žinių grafas (Knowledge Graph) — tai duomenų struktūra, kurioje informacija
# saugoma kaip trejetas (triple): SUBJEKTAS → PREDIKATAS → OBJEKTAS.
# Pvz.: "Vilnius" → "yra_sostinė" → "Lietuva"
#
# ===== RDF (Resource Description Framework) =====
# RDF yra W3C standartas žinių grafams aprašyti. Kiekvienas elementas
# identifikuojamas URI (Uniform Resource Identifier).
#
# ===== SPARQL =====
# SPARQL — tai užklausų kalba RDF grafams, panaši į SQL duomenų bazėms.
# Ji leidžia ieškoti šablonų grafe ir gauti rezultatus.
#
# ===== Ontologijos =====
# Ontologija — tai formali žinių srities aprašymo schema, apibrėžianti
# klases, savybes ir jų tarpusavio ryšius. Pvz., FOAF (Friend of a Friend)
# ontologija aprašo žmonių ir jų santykių struktūrą.
# =============================================================================

from rdflib import Graph, Literal, Namespace, URIRef, RDF, RDFS, XSD
from rdflib.namespace import FOAF

print("=" * 70)
print("ŽINIŲ GRAFAI IR ŽINIŲ BAZĖS — RDFLIB PAVYZDŽIAI")
print("=" * 70)

# ─────────────────────────────────────────────────────────────────────
# 1 PAVYZDYS: Paprastas RDF grafas — žmonės ir jų ryšiai
# ─────────────────────────────────────────────────────────────────────
print("\n─── 1. Paprastas RDF grafas: žmonės ───")

g = Graph()

# Sukuriame savo vardų erdvę (namespace)
EX = Namespace("http://example.org/")
g.bind("ex", EX)
g.bind("foaf", FOAF)

# Pridedame trejetukus (triples): subjektas - predikatas - objektas
g.add((EX.Jonas, RDF.type, FOAF.Person))
g.add((EX.Jonas, FOAF.name, Literal("Jonas Jonaitis")))
g.add((EX.Jonas, FOAF.age, Literal(30, datatype=XSD.integer)))
g.add((EX.Jonas, FOAF.knows, EX.Ona))

g.add((EX.Ona, RDF.type, FOAF.Person))
g.add((EX.Ona, FOAF.name, Literal("Ona Onaitė")))
g.add((EX.Ona, FOAF.age, Literal(25, datatype=XSD.integer)))
g.add((EX.Ona, FOAF.knows, EX.Petras))

g.add((EX.Petras, RDF.type, FOAF.Person))
g.add((EX.Petras, FOAF.name, Literal("Petras Petraitis")))
g.add((EX.Petras, FOAF.age, Literal(35, datatype=XSD.integer)))

# Atspausdiname visus trejetukus
print("  Visi trejetukai grafe:")
for s, p, o in g:
    print(f"    {s.split('/')[-1]} → {p.split('/')[-1]} → {o}")

# ─────────────────────────────────────────────────────────────────────
# 2 PAVYZDYS: Serializacija — grafas įvairiais formatais
# ─────────────────────────────────────────────────────────────────────
print("\n─── 2. Serializacija: Turtle formatas ───")

turtle_output = g.serialize(format="turtle")
print(turtle_output)

print("\n─── 2b. Serializacija: JSON-LD formatas ───")
jsonld_output = g.serialize(format="json-ld", indent=2)
print(jsonld_output[:500] + "\n  ...")

# ─────────────────────────────────────────────────────────────────────
# 3 PAVYZDYS: SPARQL užklausos
# ─────────────────────────────────────────────────────────────────────
print("\n─── 3. SPARQL užklausa: visi žmonės vyresni nei 28 ───")

query = """
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

    SELECT ?name ?age
    WHERE {
        ?person a foaf:Person .
        ?person foaf:name ?name .
        ?person foaf:age ?age .
        FILTER (?age > 28)
    }
    ORDER BY ?age
"""

results = g.query(query)
for row in results:
    print(f"  Vardas: {row.name}, Amžius: {row.age}")

# ─────────────────────────────────────────────────────────────────────
# 4 PAVYZDYS: SPARQL — kas ką pažįsta?
# ─────────────────────────────────────────────────────────────────────
print("\n─── 4. SPARQL: kas ką pažįsta? ───")

knows_query = """
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
    PREFIX ex: <http://example.org/>

    SELECT ?person_name ?knows_name
    WHERE {
        ?person foaf:knows ?friend .
        ?person foaf:name ?person_name .
        ?friend foaf:name ?knows_name .
    }
"""

results = g.query(knows_query)
for row in results:
    print(f"  {row.person_name} pažįsta → {row.knows_name}")

# ═════════════════════════════════════════════════════════════════════
# 5 PAVYZDYS (AI sugeneruotas): Lietuvos miestų žinių grafas
# ═════════════════════════════════════════════════════════════════════
print("\n" + "=" * 70)
print("SAVARANKIŠKAS PAVYZDYS: LIETUVOS MIESTŲ ŽINIŲ GRAFAS")
print("=" * 70)

# Sukuriame naują grafą
cities_graph = Graph()

# Apibrėžiame savo ontologiją (vardų erdvę)
LT = Namespace("http://lietuvos-zinios.lt/ontology/")
GEO = Namespace("http://lietuvos-zinios.lt/geo/")
cities_graph.bind("lt", LT)
cities_graph.bind("geo", GEO)

# Apibrėžiame klases
cities_graph.add((LT.Miestas, RDF.type, RDFS.Class))
cities_graph.add((LT.Upe, RDF.type, RDFS.Class))
cities_graph.add((LT.Lankytina_Vieta, RDF.type, RDFS.Class))

# ── Vilnius ──
cities_graph.add((GEO.Vilnius, RDF.type, LT.Miestas))
cities_graph.add((GEO.Vilnius, LT.pavadinimas, Literal("Vilnius")))
cities_graph.add((GEO.Vilnius, LT.gyventoju_skaicius, Literal(592389, datatype=XSD.integer)))
cities_graph.add((GEO.Vilnius, LT.yra_sostine, Literal(True, datatype=XSD.boolean)))
cities_graph.add((GEO.Vilnius, LT.teka_upe, GEO.Neris))
cities_graph.add((GEO.Vilnius, LT.turi_lankytina_vieta, GEO.Gedimino_Pilis))
cities_graph.add((GEO.Vilnius, LT.turi_lankytina_vieta, GEO.Katedra))

# ── Kaunas ──
cities_graph.add((GEO.Kaunas, RDF.type, LT.Miestas))
cities_graph.add((GEO.Kaunas, LT.pavadinimas, Literal("Kaunas")))
cities_graph.add((GEO.Kaunas, LT.gyventoju_skaicius, Literal(315000, datatype=XSD.integer)))
cities_graph.add((GEO.Kaunas, LT.yra_sostine, Literal(False, datatype=XSD.boolean)))
cities_graph.add((GEO.Kaunas, LT.teka_upe, GEO.Nemunas))
cities_graph.add((GEO.Kaunas, LT.teka_upe, GEO.Neris))
cities_graph.add((GEO.Kaunas, LT.turi_lankytina_vieta, GEO.Kauno_Pilis))

# ── Klaipėda ──
cities_graph.add((GEO.Klaipeda, RDF.type, LT.Miestas))
cities_graph.add((GEO.Klaipeda, LT.pavadinimas, Literal("Klaipėda")))
cities_graph.add((GEO.Klaipeda, LT.gyventoju_skaicius, Literal(149000, datatype=XSD.integer)))
cities_graph.add((GEO.Klaipeda, LT.yra_sostine, Literal(False, datatype=XSD.boolean)))
cities_graph.add((GEO.Klaipeda, LT.teka_upe, GEO.Dane))
cities_graph.add((GEO.Klaipeda, LT.turi_lankytina_vieta, GEO.Smiltyne))

# ── Šiauliai ──
cities_graph.add((GEO.Siauliai, RDF.type, LT.Miestas))
cities_graph.add((GEO.Siauliai, LT.pavadinimas, Literal("Šiauliai")))
cities_graph.add((GEO.Siauliai, LT.gyventoju_skaicius, Literal(101000, datatype=XSD.integer)))
cities_graph.add((GEO.Siauliai, LT.yra_sostine, Literal(False, datatype=XSD.boolean)))
cities_graph.add((GEO.Siauliai, LT.turi_lankytina_vieta, GEO.Kryziu_Kalnas))

# ── Upės ──
cities_graph.add((GEO.Neris, RDF.type, LT.Upe))
cities_graph.add((GEO.Neris, LT.pavadinimas, Literal("Neris")))
cities_graph.add((GEO.Neris, LT.ilgis_km, Literal(510, datatype=XSD.integer)))

cities_graph.add((GEO.Nemunas, RDF.type, LT.Upe))
cities_graph.add((GEO.Nemunas, LT.pavadinimas, Literal("Nemunas")))
cities_graph.add((GEO.Nemunas, LT.ilgis_km, Literal(937, datatype=XSD.integer)))

cities_graph.add((GEO.Dane, RDF.type, LT.Upe))
cities_graph.add((GEO.Dane, LT.pavadinimas, Literal("Danė")))
cities_graph.add((GEO.Dane, LT.ilgis_km, Literal(62, datatype=XSD.integer)))

# ── Lankytinos vietos ──
for place, name in [(GEO.Gedimino_Pilis, "Gedimino pilis"),
                     (GEO.Katedra, "Vilniaus katedra"),
                     (GEO.Kauno_Pilis, "Kauno pilis"),
                     (GEO.Smiltyne, "Smiltynė"),
                     (GEO.Kryziu_Kalnas, "Kryžių kalnas")]:
    cities_graph.add((place, RDF.type, LT.Lankytina_Vieta))
    cities_graph.add((place, LT.pavadinimas, Literal(name)))

# ── Serializacija Turtle formatu ──
print("\n─── Lietuvos miestų grafas (Turtle formatas) ───")
print(cities_graph.serialize(format="turtle"))

# ── SPARQL užklausos ──
print("─── SPARQL: Miestai su > 200 000 gyventojų ───")

big_cities_query = """
    PREFIX lt: <http://lietuvos-zinios.lt/ontology/>
    SELECT ?pavadinimas ?gyventojai
    WHERE {
        ?miestas a lt:Miestas .
        ?miestas lt:pavadinimas ?pavadinimas .
        ?miestas lt:gyventoju_skaicius ?gyventojai .
        FILTER (?gyventojai > 200000)
    }
    ORDER BY DESC(?gyventojai)
"""

results = cities_graph.query(big_cities_query)
for row in results:
    print(f"  {row.pavadinimas}: {row.gyventojai} gyventojų")

print("\n─── SPARQL: Kokie miestai stovi prie Neries? ───")

neris_query = """
    PREFIX lt: <http://lietuvos-zinios.lt/ontology/>
    PREFIX geo: <http://lietuvos-zinios.lt/geo/>
    SELECT ?pavadinimas
    WHERE {
        ?miestas a lt:Miestas .
        ?miestas lt:pavadinimas ?pavadinimas .
        ?miestas lt:teka_upe geo:Neris .
    }
"""

results = cities_graph.query(neris_query)
for row in results:
    print(f"  {row.pavadinimas}")

print("\n─── SPARQL: Lankytinos vietos kiekviename mieste ───")

landmarks_query = """
    PREFIX lt: <http://lietuvos-zinios.lt/ontology/>
    SELECT ?miestas_pav ?vieta_pav
    WHERE {
        ?miestas a lt:Miestas .
        ?miestas lt:pavadinimas ?miestas_pav .
        ?miestas lt:turi_lankytina_vieta ?vieta .
        ?vieta lt:pavadinimas ?vieta_pav .
    }
    ORDER BY ?miestas_pav
"""

results = cities_graph.query(landmarks_query)
for row in results:
    print(f"  {row.miestas_pav}: {row.vieta_pav}")

print("\n─── SPARQL: Upės ilgesnės nei 100 km ───")

rivers_query = """
    PREFIX lt: <http://lietuvos-zinios.lt/ontology/>
    SELECT ?pavadinimas ?ilgis
    WHERE {
        ?upe a lt:Upe .
        ?upe lt:pavadinimas ?pavadinimas .
        ?upe lt:ilgis_km ?ilgis .
        FILTER (?ilgis > 100)
    }
    ORDER BY DESC(?ilgis)
"""

results = cities_graph.query(rivers_query)
for row in results:
    print(f"  {row.pavadinimas}: {row.ilgis} km")

# ─────────────────────────────────────────────────────────────────────
# SANTRAUKA
# ─────────────────────────────────────────────────────────────────────
print("\n" + "=" * 70)
print("SANTRAUKA:")
print("  • RDF grafas saugo žinias kaip trejetukus (subject-predicate-object)")
print("  • rdflib leidžia kurti, serializuoti ir užklausti RDF grafus")
print("  • SPARQL — SQL-tipo užklausų kalba RDF grafams")
print("  • Ontologijos apibrėžia klases ir ryšius tarp jų")
print("  • Žinių grafai naudojami Google, Wikipedia (Wikidata), biomedicinoje")
print("=" * 70)
