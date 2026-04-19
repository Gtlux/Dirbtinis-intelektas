# =============================================================================
# 2.4 — Ekspertinė sistema: Medicininė simptomų diagnostika
# =============================================================================
# Ši ekspertinė sistema naudoja Python 'rule-engine' biblioteką.
# Ji analizuoja paciento simptomus ir pateikia galimas diagnozes
# naudodama IF-THEN taisykles.
#
# Specifikacija: žr. expert_system_spec.md
# =============================================================================

import rule_engine

# ─────────────────────────────────────────────────────────────────────
# 1. DUOMENŲ MODELIS — Paciento simptomai aprašomi kaip žodynas (dict)
# ─────────────────────────────────────────────────────────────────────

def create_patient(name, age, temperature,
                   cough=False, sore_throat=False, runny_nose=False,
                   headache=False, body_aches=False, fatigue=False,
                   nausea=False, rash=False, shortness_of_breath=False):
    """Sukuria paciento duomenu zodynas su visais simptomais."""
    return {
        "name": name,
        "age": age,
        "temperature": temperature,
        "fever": temperature > 37.5,
        "cough": cough,
        "sore_throat": sore_throat,
        "runny_nose": runny_nose,
        "headache": headache,
        "body_aches": body_aches,
        "fatigue": fatigue,
        "nausea": nausea,
        "rash": rash,
        "shortness_of_breath": shortness_of_breath,
    }

# ─────────────────────────────────────────────────────────────────────
# 2. TAISYKLIŲ BAZĖ — IF-THEN taisyklės kaip rule-engine objektai
# ─────────────────────────────────────────────────────────────────────

# Kiekviena taisykle: (diagnozės pavadinimas, tikimybe, rule-engine taisykle, rekomendacija)
RULES = [
    {
        "diagnosis": "Pneumonija",
        "confidence": "AUKSTA (SKUBU!)",
        "rule": rule_engine.Rule(
            "fever == true and cough == true and shortness_of_breath == true and body_aches == true"
        ),
        "recommendation": "SKUBIAI kreipkites i gydytoja arba kvieskite greitaja pagalba!",
    },
    {
        "diagnosis": "COVID-19 itarimas",
        "confidence": "VIDUTINE",
        "rule": rule_engine.Rule(
            "fever == true and cough == true and fatigue == true and shortness_of_breath == true"
        ),
        "recommendation": "Atlikite COVID-19 testa ir izoliuokites. Kreipkites i gydytoja.",
    },
    {
        "diagnosis": "Gripas",
        "confidence": "AUKSTA",
        "rule": rule_engine.Rule(
            "fever == true and cough == true and body_aches == true and fatigue == true"
        ),
        "recommendation": "Likite namie, gerkite daug skysciu, vartokite antipiretinius vaistus.",
    },
    {
        "diagnosis": "Persalimas",
        "confidence": "AUKSTA",
        "rule": rule_engine.Rule(
            "runny_nose == true and sore_throat == true and cough == true and fever == false"
        ),
        "recommendation": "Pailsekite, gerkite siltus gerimu, naudokite nosies lasukus.",
    },
    {
        "diagnosis": "Angina",
        "confidence": "VIDUTINE",
        "rule": rule_engine.Rule(
            "sore_throat == true and fever == true and cough == false and runny_nose == false"
        ),
        "recommendation": "Kreipkites i gydytoja del antibiotiku skyrimo.",
    },
    {
        "diagnosis": "Bronchitas",
        "confidence": "VIDUTINE",
        "rule": rule_engine.Rule(
            "cough == true and fatigue == true and fever == false"
        ),
        "recommendation": "Venkite salto oro, gerkite daug skysciu. Jei nepraeina per 2 savaites — kreipkites i gydytoja.",
    },
    {
        "diagnosis": "Migrena",
        "confidence": "AUKSTA",
        "rule": rule_engine.Rule(
            "headache == true and nausea == true and fever == false and cough == false"
        ),
        "recommendation": "Pailsekite tamsioje patalpo, vartokite skausmoldzius.",
    },
    {
        "diagnosis": "Alergine reakcija",
        "confidence": "VIDUTINE",
        "rule": rule_engine.Rule(
            "rash == true and runny_nose == true and fever == false"
        ),
        "recommendation": "Vartokite antihistamininius vaistus. Jei sunku kveputoti — skubiai kreipkites i gydytoja.",
    },
    {
        "diagnosis": "Virskinimo infekcija",
        "confidence": "VIDUTINE",
        "rule": rule_engine.Rule(
            "nausea == true and fever == true and cough == false"
        ),
        "recommendation": "Gerkite daug skysciu, laikykites dietos. Jei nepraeina per 3 dienas — kreipkites i gydytoja.",
    },
    {
        "diagnosis": "Dehidratacija",
        "confidence": "ZEMA",
        "rule": rule_engine.Rule(
            "fatigue == true and headache == true and fever == false and cough == false"
        ),
        "recommendation": "Gerkite daugiau vandens ir elektrolitiniu gerimu.",
    },
]

# ─────────────────────────────────────────────────────────────────────
# 3. EKSPERTINĖS SISTEMOS VARIKLIS (Inference Engine)
# ─────────────────────────────────────────────────────────────────────

class ExpertSystem:
    """Ekspertine sistema, kuri priima paciento duomenis ir grazina diagnozes."""

    def __init__(self, rules):
        self.rules = rules

    def diagnose(self, patient):
        """Ivertina visas taisykles ir grazina atitinkancias diagnozes."""
        diagnoses = []
        for rule_entry in self.rules:
            if rule_entry["rule"].matches(patient):
                diagnoses.append({
                    "diagnosis": rule_entry["diagnosis"],
                    "confidence": rule_entry["confidence"],
                    "recommendation": rule_entry["recommendation"],
                })
        return diagnoses

    def print_report(self, patient):
        """Atspausdina pilna diagnostikos ataskaita."""
        print(f"\n{'='*60}")
        print(f"PACIENTAS: {patient['name']}")
        print(f"Amzius: {patient['age']} m.")
        print(f"Temperatura: {patient['temperature']} C")
        print(f"{'='*60}")

        # Atspausdiname aktyvius simptomus
        symptoms = []
        symptom_names = {
            "fever": "Karsciavimas",
            "cough": "Kosulys",
            "sore_throat": "Gerkles skausmas",
            "runny_nose": "Sloga",
            "headache": "Galvos skausmas",
            "body_aches": "Kuno skausmai",
            "fatigue": "Nuovargis",
            "nausea": "Pykinimas",
            "rash": "Berimas",
            "shortness_of_breath": "Dusulys",
        }
        for key, label in symptom_names.items():
            if patient.get(key, False):
                symptoms.append(label)

        print(f"Simptomai: {', '.join(symptoms) if symptoms else 'Nera'}")
        print("-" * 60)

        # Atliekame diagnostika
        diagnoses = self.diagnose(patient)

        if diagnoses:
            print(f"RASTOS DIAGNOZĖS ({len(diagnoses)}):")
            for i, d in enumerate(diagnoses, 1):
                print(f"\n  {i}. {d['diagnosis']}")
                print(f"     Tikimybe: {d['confidence']}")
                print(f"     Rekomendacija: {d['recommendation']}")
        else:
            print("Neimanoma nustatyti diagnozes pagal pateiktus simptomus.")
            print("Rekomendacija: kreipkites i gydytoja detalesniems tyrimams.")

        print("=" * 60)
        return diagnoses


# ─────────────────────────────────────────────────────────────────────
# 4. TESTAVIMAS — Pavyzdziai su skirtingais pacientais
# ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("*" * 60)
    print("  EKSPERTINE SISTEMA: MEDICININE SIMPTOMU DIAGNOSTIKA")
    print("  Naudojama biblioteka: Python rule-engine")
    print("*" * 60)

    # Sukuriame ekspertines sistemos objekta
    expert = ExpertSystem(RULES)

    # --- Pacientas 1: Gripas ---
    patient1 = create_patient(
        name="Jonas Jonaitis", age=35, temperature=38.5,
        cough=True, body_aches=True, fatigue=True, headache=True
    )
    expert.print_report(patient1)

    # --- Pacientas 2: Persalimas ---
    patient2 = create_patient(
        name="Ona Onaite", age=28, temperature=36.8,
        runny_nose=True, sore_throat=True, cough=True
    )
    expert.print_report(patient2)

    # --- Pacientas 3: Pneumonija (SKUBU!) ---
    patient3 = create_patient(
        name="Petras Petraitis", age=65, temperature=39.2,
        cough=True, body_aches=True, fatigue=True,
        shortness_of_breath=True
    )
    expert.print_report(patient3)

    # --- Pacientas 4: Migrena ---
    patient4 = create_patient(
        name="Birute Birutiene", age=42, temperature=36.6,
        headache=True, nausea=True
    )
    expert.print_report(patient4)

    # --- Pacientas 5: Alergine reakcija ---
    patient5 = create_patient(
        name="Antanas Antanaitis", age=22, temperature=36.9,
        rash=True, runny_nose=True
    )
    expert.print_report(patient5)

    # --- Pacientas 6: COVID-19 itarimas ---
    patient6 = create_patient(
        name="Ieva Ievaite", age=50, temperature=38.8,
        cough=True, fatigue=True, shortness_of_breath=True
    )
    expert.print_report(patient6)

    # --- Pacientas 7: Be aisku diagnozes ---
    patient7 = create_patient(
        name="Dainius Dainauskas", age=30, temperature=36.5,
        headache=True
    )
    expert.print_report(patient7)

    print("\n" + "*" * 60)
    print("  PASTABA: Si sistema yra skirta mokymosi tikslams.")
    print("  Ji NEPAKEICIA profesionalios medicinos konsultacijos!")
    print("*" * 60)
