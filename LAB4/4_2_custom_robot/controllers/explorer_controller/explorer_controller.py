"""
Explorer Robot - Tyrinėtojo roboto kontroleris
================================================
SENSORIAI (3 tipai):
  1. DistanceSensor (x2) - kliūčių aptikimas
  2. LightSensor (x1)    - šviesos sekimas
  3. GPS (x1)            - pozicijos sekimas

AKTUATORIAI (3 tipai):
  1. RotationalMotor (x4) - ratų varikliai
  2. LED (x2)             - būsenos indikatoriai
  3. Pen (x1)             - trajektorijos piešimas
"""

from controller import Robot
import math
import random

# ============================================================
# INICIALIZACIJA
# ============================================================

robot = Robot()
TIME_STEP = int(robot.getBasicTimeStep())
MAX_SPEED = 6.28

# --- Sensoriai ---
ds_left = robot.getDevice("ds_left")
ds_right = robot.getDevice("ds_right")
ds_left.enable(TIME_STEP)
ds_right.enable(TIME_STEP)

light_sensor = robot.getDevice("light_sensor")
light_sensor.enable(TIME_STEP)

gps = robot.getDevice("gps")
gps.enable(TIME_STEP)

# --- Aktuatoriai ---
wheels = []
for name in ["wheel1", "wheel2", "wheel3", "wheel4"]:
    motor = robot.getDevice(name)
    motor.setPosition(float('inf'))
    motor.setVelocity(0.0)
    wheels.append(motor)

led_left = robot.getDevice("led_left")
led_right = robot.getDevice("led_right")

pen = robot.getDevice("pen")
pen.write(True)
pen.setInkColor(0x0066FF, 1.0)  # Mėlyna spalva, pilnas intensyvumas

# ============================================================
# KINTAMIEJI
# ============================================================

prev_x, prev_y = 0.0, 0.0
total_distance = 0.0
step_count = 0

# Vengimas
avoid_counter = 0
avoid_dir = 1
reverse_counter = 0  # Atbulinės eigos skaitliukas

# Patruliavimas
wander_timer = 0
wander_turn = 0.0
wander_interval = random.randint(50, 120)

# Šviesos sekimas
prev_light = 0.0

LED_OFF = 0
LED_ON = 1

# lookupTable: 0m→1000, 0.4m→0
# DIDESNĖ reikšmė = ARČIAU kliūtis
NEAR = 600
BOTH_NEAR = 500  # Kai abu sensoriai > 500 = kampas
CLOSE = 850

# Šviesos slenkstis (attenuation=1, reikšmės bus ~5-50+)
LIGHT_THRESHOLD = 5

print("=" * 60)
print("  EXPLORER ROBOT paleistas!")
print("  Sensoriai: DistanceSensor, LightSensor, GPS")
print("  Aktuatoriai: RotationalMotor, LED, Pen")
print("=" * 60)

# ============================================================
# PAGRINDINIS CIKLAS
# ============================================================

while robot.step(TIME_STEP) != -1:
    step_count += 1

    # --- Sensoriai ---
    lv = ds_left.getValue()
    rv = ds_right.getValue()
    light = light_sensor.getValue()

    pos = gps.getValues()
    cx, cy = pos[0], pos[1]

    # --- GPS atstumas ---
    if step_count > 1:
        total_distance += math.sqrt((cx - prev_x)**2 + (cy - prev_y)**2)
    prev_x, prev_y = cx, cy

    # --- Greičių nustatymas ---
    left_speed = 0.5 * MAX_SPEED
    right_speed = 0.5 * MAX_SPEED
    state = "PATROL"

    # ======== PIRMENYBĖ 1: ATBULINĖ EIGA (išvažiavimas iš kampo) ========
    if reverse_counter > 0:
        reverse_counter -= 1
        state = "REVERSE"
        left_speed = -0.5 * MAX_SPEED
        right_speed = -0.4 * MAX_SPEED

    # ======== PIRMENYBĖ 2: POSŪKIS PO ATBULINĖS ========
    elif avoid_counter > 0:
        avoid_counter -= 1
        state = "AVOID"
        if avoid_dir == 1:
            left_speed = -0.3 * MAX_SPEED
            right_speed = 0.5 * MAX_SPEED
        else:
            left_speed = 0.5 * MAX_SPEED
            right_speed = -0.3 * MAX_SPEED

    # ======== ABU SENSORIAI MATO KLIŪTĮ (kampas/aklavietė) ========
    elif lv > BOTH_NEAR and rv > BOTH_NEAR:
        state = "REVERSE"
        reverse_counter = 30  # Ilga atbulinė
        avoid_counter = 20    # Po to - ilgas posūkis
        avoid_dir = random.choice([1, -1])
        left_speed = -0.5 * MAX_SPEED
        right_speed = -0.4 * MAX_SPEED

    # ======== VIENAS SENSORIUS MATO KLIŪTĮ ========
    elif lv > NEAR or rv > NEAR:
        state = "AVOID"
        if lv > rv:
            avoid_dir = -1  # kliūtis kairėje → dešinėn
        else:
            avoid_dir = 1   # kliūtis dešinėje → kairėn
        avoid_counter = 12

        if avoid_dir == 1:
            left_speed = -0.2 * MAX_SPEED
            right_speed = 0.5 * MAX_SPEED
        else:
            left_speed = 0.5 * MAX_SPEED
            right_speed = -0.2 * MAX_SPEED

    # ======== ŠVIESOS SEKIMAS ========
    elif light > LIGHT_THRESHOLD:
        state = "LIGHT"
        light_change = light - prev_light

        if light_change > 0.5:
            # Šviesa stiprėja - judame tiesiai, greitėjame
            intensity = min(light / 50.0, 1.0)
            base = 0.4 * MAX_SPEED * (1.0 + intensity * 0.3)
            left_speed = base
            right_speed = base
        else:
            # Šviesa silpsta arba nekinta - ieškome sukdamiesi
            base = 0.35 * MAX_SPEED
            turn = 0.25 * MAX_SPEED
            if step_count % 100 < 50:
                left_speed = base + turn
                right_speed = base - turn
            else:
                left_speed = base - turn
                right_speed = base + turn

    # ======== PATRULIAVIMAS ========
    else:
        state = "PATROL"
        wander_timer += 1

        if wander_timer >= wander_interval:
            wander_timer = 0
            wander_interval = random.randint(50, 120)
            wander_turn = random.uniform(-0.7, 0.7)

        wander_turn *= 0.998

        base = 0.5 * MAX_SPEED
        left_speed = base + wander_turn * 0.35 * MAX_SPEED
        right_speed = base - wander_turn * 0.35 * MAX_SPEED

    prev_light = light

    # --- LED ---
    if state == "AVOID" or state == "REVERSE":
        blink = step_count % 8 < 4
        led_left.set(LED_ON if blink else LED_OFF)
        led_right.set(LED_ON if blink else LED_OFF)
    elif state == "LIGHT":
        led_left.set(LED_ON)
        led_right.set(LED_ON)
    else:  # PATROL
        led_left.set(LED_ON if step_count % 30 < 15 else LED_OFF)
        led_right.set(LED_OFF if step_count % 30 < 15 else LED_ON)

    # --- Pen spalvos keitimas pagal būseną ---
    if state in ("AVOID", "REVERSE"):
        pen.setInkColor(0xFF0000, 1.0)   # Raudona - vengimas
    elif state == "LIGHT":
        pen.setInkColor(0xFFFF00, 1.0)   # Geltona - šviesos sekimas
    else:
        pen.setInkColor(0x0066FF, 1.0)   # Mėlyna - patruliavimas

    # --- Ratai ---
    left_speed = max(-MAX_SPEED, min(MAX_SPEED, left_speed))
    right_speed = max(-MAX_SPEED, min(MAX_SPEED, right_speed))
    wheels[0].setVelocity(left_speed)
    wheels[1].setVelocity(right_speed)
    wheels[2].setVelocity(left_speed)
    wheels[3].setVelocity(right_speed)

    # --- Konsolė ---
    if step_count % 50 == 0:
        print(f"\n--- Žingsnis {step_count} | Būsena: {state} ---")
        print(f"  Atstumo sensoriai: L={lv:.0f}  R={rv:.0f}")
        print(f"  Šviesos sensorius: {light:.1f}")
        print(f"  GPS: X={cx:.3f}  Y={cy:.3f}")
        print(f"  Atstumas: {total_distance:.3f} m")
        print(f"  Greitis: L={left_speed:.2f}  R={right_speed:.2f}")
