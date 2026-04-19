"""
Modifikuotas four_wheels_collision_avoidance kontroleris.
Originalus pavyzdys paimtas iš Webots tutorials.

Pakeitimai lyginant su originalu:
1. Perrašyta iš C į Python kalbą
2. Pridėtas proporcinis greičio valdymas (vietoj binarinio)
3. Pridėtas atsitiktinis klaidžiojimo (wander) elgesys
4. Pridėtas konsolinis sensorių reikšmių atvaizdavimas
5. Pridėtas adaptyvus posūkio kampas pagal atstumo sensorių reikšmes
"""

from controller import Robot, DistanceSensor, Motor
import random
import math

# Sukuriame roboto objektą
robot = Robot()

# Simuliacijos žingsnis milisekundėmis
TIME_STEP = 64

# Maksimalus ratų greitis (rad/s)
MAX_SPEED = 6.28

# --- Sensorių inicializacija ---
# Gauname kairiojo ir dešiniojo atstumo sensorius
ds_left = robot.getDevice("ds_left")
ds_right = robot.getDevice("ds_right")
ds_left.enable(TIME_STEP)
ds_right.enable(TIME_STEP)

# --- Variklių (aktuatorių) inicializacija ---
# Gauname visus 4 ratų variklius
wheels = []
wheel_names = ["wheel1", "wheel2", "wheel3", "wheel4"]
for name in wheel_names:
    motor = robot.getDevice(name)
    motor.setPosition(float('inf'))  # Nustatome begalinę poziciją = greičio valdymo režimas
    motor.setVelocity(0.0)
    wheels.append(motor)

# Kintamieji klaidžiojimo elgesiui
wander_timer = 0         # Laikmatis atsitiktiniam posūkiui
wander_direction = 1.0   # Posūkio kryptis: 1.0 = kairėn, -1.0 = dešinėn
step_count = 0            # Žingsnių skaitliukas

print("=== Modifikuotas collision avoidance kontroleris paleistas ===")
print("Pakeitimai: proporcinis valdymas, atsitiktinis klaidžiojimas, adaptyvus posūkis")

# --- Pagrindinis valdymo ciklas ---
while robot.step(TIME_STEP) != -1:
    step_count += 1

    # Nuskaitome sensorių reikšmes
    left_val = ds_left.getValue()
    right_val = ds_right.getValue()

    # Kas 20 žingsnių spausdiname sensorių reikšmes į konsolę
    if step_count % 20 == 0:
        print(f"[Žingsnis {step_count}] Kairys: {left_val:.1f}, Dešinys: {right_val:.1f}")

    # --- MODIFIKACIJA: Proporcinis greičio valdymas ---
    # Vietoj binarinio "yra kliūtis / nėra kliūties" naudojame
    # proporcinį valdymą - kuo arčiau kliūtis, tuo greičiau sukame
    
    # Atstumo sensoriai grąžina mažesnę reikšmę kai kliūtis arčiau
    # Tipinės reikšmės: ~1000 = toli / tuščia, ~0-500 = arti kliūtis
    OBSTACLE_THRESHOLD = 950.0
    
    left_obstacle = left_val < OBSTACLE_THRESHOLD
    right_obstacle = right_val < OBSTACLE_THRESHOLD
    
    if left_obstacle or right_obstacle:
        # --- Proporcinis posūkio greitis ---
        # Apskaičiuojame kliūties artumą (0.0 = toli, 1.0 = labai arti)
        left_proximity = max(0.0, (OBSTACLE_THRESHOLD - left_val) / OBSTACLE_THRESHOLD)
        right_proximity = max(0.0, (OBSTACLE_THRESHOLD - right_val) / OBSTACLE_THRESHOLD)
        
        # Bazinis greitis mažinamas proporcingai kliūties artumui
        base_speed = MAX_SPEED * (1.0 - max(left_proximity, right_proximity) * 0.7)
        
        if left_proximity > right_proximity:
            # Kliūtis kairėje - sukame dešinėn
            left_speed = base_speed
            right_speed = -base_speed * left_proximity
        else:
            # Kliūtis dešinėje - sukame kairėn
            left_speed = -base_speed * right_proximity
            right_speed = base_speed
        
        # Atstatome klaidžiojimo laikmatį
        wander_timer = 0
        
        if step_count % 20 == 0:
            print(f"  >> Kliūties vengimas! L:{left_proximity:.2f} R:{right_proximity:.2f}")
    else:
        # --- MODIFIKACIJA: Atsitiktinis klaidžiojimas ---
        # Kai nėra kliūčių, robotas periodiškai keičia kryptį
        wander_timer += 1
        
        if wander_timer > random.randint(30, 80):
            # Pasirenkame naują atsitiktinę kryptį
            wander_direction = random.choice([-1.0, 1.0])
            wander_timer = 0
            
            if step_count % 20 == 0:
                kryptis = "kairėn" if wander_direction > 0 else "dešinėn"
                print(f"  >> Keičiu kryptį: {kryptis}")
        
        # Bazinis greitis su nedideliu nuokrypiu
        left_speed = 0.6 * MAX_SPEED + wander_direction * 0.15 * MAX_SPEED
        right_speed = 0.6 * MAX_SPEED - wander_direction * 0.15 * MAX_SPEED

    # Nustatome variklių greitį
    # wheels[0] ir wheels[2] = kairieji ratai
    # wheels[1] ir wheels[3] = dešinieji ratai
    wheels[0].setVelocity(left_speed)
    wheels[1].setVelocity(right_speed)
    wheels[2].setVelocity(left_speed)
    wheels[3].setVelocity(right_speed)
