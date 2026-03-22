# =============================================================================
# 2.1 — Taisyklių mašina (Rule Engine) Python pavyzdžiai
# =============================================================================
# Šis failas demonstruoja kaip naudoti Python 'rule-engine' biblioteką —
# lengvą taisyklių variklį, leidžiantį apibrėžti IF-THEN taisykles kaip
# tekstines išraiškas ir taikyti jas Python objektams (žodynams).
#
# ===== Kas yra Business Rules Engine (taisyklių mašina)? =====
# Taisyklių mašina — tai programinė sistema, kuri leidžia atskirti verslo
# logiką (taisykles) nuo programos kodo. Taisyklės apibrėžiamos deklaratyviai
# (pvz., "jei amžius >= 18 IR pajamos > 1000, tada patvirtinti"), o taisyklių
# variklis jas automatiškai įvertina pagal pateiktus duomenis.
#
# Privalumai:
#   - Taisykles gali keisti net ne-programuotojai
#   - Lengva pridėti naujas taisykles be kodo pakeitimų
#   - Centralizuota verslo logika
#
# ===== Kas yra Semantic Reasoner? =====
# Semantinis protavimo variklis (Semantic Reasoner) — tai sistema, kuri
# naudoja formalią logiką ir ontologijas (žinių struktūras) naujoms žinioms
# išvesti iš esamų faktų. Pvz., jei žinome "A yra B poklasis" ir
# "C priklauso A", tai reasoneris išves "C priklauso B".
#
# ===== Veikimo principas (rule-engine) =====
# 1. Sukuriame taisyklę (Rule) iš tekstinės išraiškos
# 2. Taisyklė kompiliuojama į vidinę struktūrą
# 3. Duomenys (Python dict) pateikiami taisyklei
# 4. Metodas matches() grąžina True/False — ar duomenys atitinka taisyklę
# 5. Metodas filter() filtruoja duomenų sąrašą pagal taisyklę
# =============================================================================

# Įdiegimas: pip install rule-engine
import rule_engine

print("=" * 70)
print("PYTHON RULE-ENGINE PAVYZDŽIAI")
print("=" * 70)

# ─────────────────────────────────────────────────────────────────────
# 1 PAVYZDYS: Paprasta taisyklė — amžiaus tikrinimas
# ─────────────────────────────────────────────────────────────────────
print("\n─── 1. Paprasta taisyklė: amžius >= 18 ───")

# Sukuriame taisyklę kaip tekstinę išraišką
rule = rule_engine.Rule("age >= 18")

# Tikriname ar konkretus žmogus atitinka taisyklę
person1 = {"name": "Jonas", "age": 25}
person2 = {"name": "Ona", "age": 16}

print(f"  {person1['name']} (amžius {person1['age']}): atitinka = {rule.matches(person1)}")
print(f"  {person2['name']} (amžius {person2['age']}): atitinka = {rule.matches(person2)}")

# ─────────────────────────────────────────────────────────────────────
# 2 PAVYZDYS: Sudėtingesnė taisyklė su AND/OR operatoriais
# ─────────────────────────────────────────────────────────────────────
print("\n─── 2. Sudėtinga taisyklė: paskolos patvirtinimas ───")

# Taisyklė: pajamos > 2000 IR kredito balas > 600 ARBA turi garantą
loan_rule = rule_engine.Rule(
    "salary > 2000 and (credit_score > 600 or has_guarantor == true)"
)

applicants = [
    {"name": "Petras", "salary": 3000, "credit_score": 750, "has_guarantor": False},
    {"name": "Marija", "salary": 1500, "credit_score": 800, "has_guarantor": True},
    {"name": "Antanas", "salary": 2500, "credit_score": 500, "has_guarantor": False},
    {"name": "Ieva", "salary": 2500, "credit_score": 500, "has_guarantor": True},
]

for a in applicants:
    result = loan_rule.matches(a)
    status = "✅ PATVIRTINTA" if result else "❌ ATMESTA"
    print(f"  {a['name']}: pajamos={a['salary']}, kreditas={a['credit_score']}, "
          f"garantas={a['has_guarantor']} → {status}")

# ─────────────────────────────────────────────────────────────────────
# 3 PAVYZDYS: filter() — filtravimas pagal taisyklę
# ─────────────────────────────────────────────────────────────────────
print("\n─── 3. Filtravimas: darbuotojai su patirtimi > 5 metų ───")

experience_rule = rule_engine.Rule("experience > 5")

employees = [
    {"name": "Algis", "experience": 10, "department": "IT"},
    {"name": "Birutė", "experience": 3, "department": "HR"},
    {"name": "Česlovas", "experience": 7, "department": "IT"},
    {"name": "Daiva", "experience": 2, "department": "Finance"},
    {"name": "Edmundas", "experience": 15, "department": "IT"},
]

# filter() grąžina iteratorių su atitinkančiais elementais
experienced = list(experience_rule.filter(employees))
print(f"  Patyrę darbuotojai (>5 m.):")
for emp in experienced:
    print(f"    - {emp['name']}: {emp['experience']} m. ({emp['department']})")

# ─────────────────────────────────────────────────────────────────────
# 4 PAVYZDYS: Teksto (string) taisyklės
# ─────────────────────────────────────────────────────────────────────
print("\n─── 4. Teksto taisyklės: el. pašto domeno tikrinimas ───")

# Taisyklė su string operacijomis
email_rule = rule_engine.Rule('email =~~ ".*@company\\.lt"')

users = [
    {"name": "Admin", "email": "admin@company.lt"},
    {"name": "Svečias", "email": "guest@gmail.com"},
    {"name": "Vadovas", "email": "boss@company.lt"},
]

for u in users:
    is_internal = email_rule.matches(u)
    label = "🏢 Vidinis" if is_internal else "🌐 Išorinis"
    print(f"  {u['name']} ({u['email']}): {label}")

# ─────────────────────────────────────────────────────────────────────
# 5 PAVYZDYS: Keletas taisyklių kartu — klasifikacija
# ─────────────────────────────────────────────────────────────────────
print("\n─── 5. Klasifikacija: produkto kategorija pagal kainą ───")

rules = [
    ("Premium", rule_engine.Rule("price >= 100")),
    ("Standartinis", rule_engine.Rule("price >= 30 and price < 100")),
    ("Ekonominis", rule_engine.Rule("price < 30")),
]

products = [
    {"name": "Telefonas", "price": 599},
    {"name": "Ausinės", "price": 45},
    {"name": "USB laidas", "price": 5},
    {"name": "Pelė", "price": 30},
]

for product in products:
    for category, r in rules:
        if r.matches(product):
            print(f"  {product['name']} ({product['price']}€) → {category}")
            break

# ─────────────────────────────────────────────────────────────────────
# 6 PAVYZDYS: Taisyklės su None/null reikšmėmis
# ─────────────────────────────────────────────────────────────────────
print("\n─── 6. Null tikrinimas: ar užpildytas profilis ───")

# Konteksto tipas nurodo kokius laukus tikėtis
context = rule_engine.Context(type_resolver=rule_engine.type_resolver_from_dict({
    "name": rule_engine.DataType.STRING,
    "phone": rule_engine.DataType.STRING,
    "email": rule_engine.DataType.STRING,
}))

complete_rule = rule_engine.Rule("name != null and phone != null and email != null", context=context)

profiles = [
    {"name": "Jonas", "phone": "+37061234567", "email": "jonas@mail.lt"},
    {"name": "Ona", "phone": None, "email": "ona@mail.lt"},
    {"name": None, "phone": "+37069876543", "email": None},
]

for p in profiles:
    complete = complete_rule.matches(p)
    status = "✅ Pilnas" if complete else "⚠️ Nepilnas"
    print(f"  Vardas={p['name']}, Tel={p['phone']}, El.p={p['email']} → {status}")

# ─────────────────────────────────────────────────────────────────────
# SANTRAUKA
# ─────────────────────────────────────────────────────────────────────
print("\n" + "=" * 70)
print("SANTRAUKA:")
print("  • rule-engine leidžia apibrėžti taisykles kaip tekstines išraiškas")
print("  • matches() tikrina ar vienas objektas atitinka taisyklę")
print("  • filter() filtruoja sąrašą pagal taisyklę")
print("  • Palaikomi operatoriai: ==, !=, >, <, >=, <=, and, or, not")
print("  • Palaikomos regex, null tikrinimas, aritmetika")
print("  • Tai veikia kaip supaprastinta Drools/CLIPS sistema Python'e")
print("=" * 70)
