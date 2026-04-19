# Importuojame viską iš search.py – ten yra Problem, Node, BFS, DFS, A* klasės ir funkcijos
from search import *

# Importuojame sys ir io – reikės sutvarkyti lietuviškų raidžių atvaizdavimą Windows konsolėje
import sys
import io

# Nustatome UTF-8 kodavimą, kad Windows konsolėje veiktų lietuviškos raidės
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


# === Sukuriame savo uždavinio klasę, kuri paveldi iš Problem (AIMA architektūra) ===
class FarmerProblem(Problem):
    """
    Fermerio, lapės, vištos ir grūdų uždavinys.

    Fermeris turi pervežti per upę: lapę, vištą ir grūdus.
    Valtyje telpa tik fermeris + vienas daiktas.
    Negalima palikti:
      - Lapės su višta (lapė suės vištą)
      - Vištos su grūdais (višta suės grūdus)

    Būsena: tuple iš 4 elementų (fermeris, lapė, višta, grūdai)
    Kiekvienas elementas yra 'L' (kairysis krantas) arba 'R' (dešinysis krantas).
    """

    def __init__(self):
        # Pradinė būsena: visi kairėje ('L' = left)
        initial = ('L', 'L', 'L', 'L')
        # Galinė būsena: visi dešinėje ('R' = right)
        goal = ('R', 'R', 'R', 'R')
        # Kviečiame tėvinės klasės Problem konstruktorių
        super().__init__(initial, goal)

    def actions(self, state):
        """Grąžina sąrašą galimų veiksmų iš dabartinės būsenos."""
        # Išpakuojame būseną į atskirus kintamuosius
        fermeris, lape, vista, grudai = state
        # Sukuriame tuščią galimų veiksmų sąrašą
        galimi_veiksmai = []

        # Fermeris visada gali plaukti vienas (be nieko)
        galimi_veiksmai.append('PLAUKTI_VIENAM')

        # Fermeris gali vežti lapę tik jei jie tame pačiame krante
        if fermeris == lape:
            galimi_veiksmai.append('VEZTI_LAPE')

        # Fermeris gali vežti vištą tik jei jie tame pačiame krante
        if fermeris == vista:
            galimi_veiksmai.append('VEZTI_VISTA')

        # Fermeris gali vežti grūdus tik jei jie tame pačiame krante
        if fermeris == grudai:
            galimi_veiksmai.append('VEZTI_GRUDUS')

        # Filtruojame – paliekame tik tuos veiksmus, kurie veda į saugią būseną
        saugi_veiksmai = []
        for veiksmas in galimi_veiksmai:
            # Gauname naują būseną po veiksmo
            nauja_busena = self.result(state, veiksmas)
            # Tikriname ar nauja būsena yra saugi
            if self.ar_saugu(nauja_busena):
                # Jei saugi – pridedame prie galimų veiksmų
                saugi_veiksmai.append(veiksmas)

        # Grąžiname tik saugius veiksmus
        return saugi_veiksmai

    def result(self, state, action):
        """Grąžina naują būseną po nurodyto veiksmo."""
        # Paverčiame tuple į sąrašą, nes tuple negalima keisti
        nauja = list(state)

        # Nustatome kur fermeris plauks (priešingas krantas)
        # Jei buvo 'L' – plauks į 'R', ir atvirkščiai
        naujas_krantas = 'R' if state[0] == 'L' else 'L'

        # Fermeris visada persikelia (indeksas 0)
        nauja[0] = naujas_krantas

        # Jei veža lapę – lapė irgi persikelia (indeksas 1)
        if action == 'VEZTI_LAPE':
            nauja[1] = naujas_krantas

        # Jei veža vištą – višta irgi persikelia (indeksas 2)
        elif action == 'VEZTI_VISTA':
            nauja[2] = naujas_krantas

        # Jei veža grūdus – grūdai irgi persikelia (indeksas 3)
        elif action == 'VEZTI_GRUDUS':
            nauja[3] = naujas_krantas

        # PLAUKTI_VIENAM – niekas daugiau nekeičiama, tik fermeris persikėlė

        # Grąžiname kaip tuple (nekintamą tipą, reikalingą set() ir palyginimams)
        return tuple(nauja)

    def ar_saugu(self, state):
        """Tikrina ar būsena yra saugi (niekas nebus suėstas)."""
        # Išpakuojame būseną
        fermeris, lape, vista, grudai = state

        # Jei lapė ir višta tame pačiame krante, BET fermeris kitame – PAVOJUS!
        if lape == vista and fermeris != lape:
            return False  # Lapė suės vištą

        # Jei višta ir grūdai tame pačiame krante, BET fermeris kitame – PAVOJUS!
        if vista == grudai and fermeris != vista:
            return False  # Višta suės grūdus

        # Jei nė viena pavojinga situacija – saugu
        return True

    def goal_test(self, state):
        """Tikrina ar pasiektas tikslas (visi dešiniame krante)."""
        # Palygina dabartinę būseną su tiksline
        return state == self.goal

    def h(self, node):
        """Euristika A* algoritmui – skaičiuoja kiek objektų dar ne dešiniame krante."""
        # Skaičiuojame kiek elementų dar yra 'L' (kairiame krante)
        return sum(1 for x in node.state if x == 'L')


# ============================================================================
# PROGRAMOS PALEIDIMAS
# ============================================================================

# Sukuriame uždavinį
print("=" * 55)
print("FERMERIO, LAPES, VISTOS IR GRUDU UZDAVINYS")
print("=" * 55)
print("Tikslas: pervezti visus per upe.")
print("Negalima palikti: lapes su vista, vistos su grudais.")
print()

# Sukuriame FarmerProblem objektą
problema = FarmerProblem()

# === 1) BFS – paieška į plotį ===
print("--- BFS (paieska i ploti) ---")
# Paleidžiame BFS algoritmą iš search.py
rezultatas_bfs = breadth_first_graph_search(problema)
# Gauname veiksmų seką
sprendimas_bfs = rezultatas_bfs.solution()
# Atspausdiname veiksmų skaičių ir pačius veiksmus
print(f"Sprendimas ({len(sprendimas_bfs)} zingsniai): {sprendimas_bfs}")

# Einame per visą kelią nuo tikslo iki pradžios per parent grandine
mazgas = rezultatas_bfs
busenos = []
while mazgas:
    busenos.append(mazgas.state)
    mazgas = mazgas.parent
# Apverčiame sąrašą, nes ėjome nuo galo
busenos.reverse()

# Atspausdiname kiekvieną žingsnį suprantamai
print("\nZingsnis po zingsnio:")
# Stulpelių pavadinimai
print(f"  {'Zingsnis':<12} {'Fermeris':<10} {'Lape':<8} {'Vista':<8} {'Grudai':<8} {'Veiksmas'}")
print(f"  {'-'*12} {'-'*10} {'-'*8} {'-'*8} {'-'*8} {'-'*20}")

# Einame per kiekvieną būseną
for i, busena in enumerate(busenos):
    # Paverčiame 'L'/'R' į suprantamus pavadinimus
    krantas = lambda k: "KAIRE" if k == 'L' else "DESINE"
    # Nustatome kokį veiksmą atlikome (pirmai būsenai – PRADZIA)
    if i < len(sprendimas_bfs):
        veiksmas = sprendimas_bfs[i]
    else:
        veiksmas = "TIKSLAS!"
    # Atspausdiname eilutę
    print(f"  {i:<12} {krantas(busena[0]):<10} {krantas(busena[1]):<8} {krantas(busena[2]):<8} {krantas(busena[3]):<8} {veiksmas}")

print()

# === 2) DFS – paieška į gylį ===
print("--- DFS (paieska i gyli) ---")
rezultatas_dfs = depth_first_graph_search(problema)
sprendimas_dfs = rezultatas_dfs.solution()
print(f"Sprendimas ({len(sprendimas_dfs)} zingsniai): {sprendimas_dfs}")
print()

# === 3) A* – su euristika ===
print("--- A* (su euristika) ---")
rezultatas_astar = astar_search(problema)
sprendimas_astar = rezultatas_astar.solution()
print(f"Sprendimas ({len(sprendimas_astar)} zingsniai): {sprendimas_astar}")
