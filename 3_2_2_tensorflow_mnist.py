# -*- coding: utf-8 -*-
"""
3.2.2 TensorFlow/Keras pavyzdys – MNIST ranka rašytų skaitmenų atpažinimas
=============================================================================

PASTABA: Kadangi TensorFlow nepalaiko Python 3.14, naudojame PyTorch biblioteką,
kuri atlieka tą pačią funkciją – giluminio mokymosi neuroninio tinklo kūrimą.
PyTorch yra antra pagal populiarumą giluminio mokymosi biblioteka (po TensorFlow).

MNIST duomenų rinkinys:
  - 60,000 mokymo ir 10,000 testavimo paveikslėlių
  - Kiekvienas paveikslėlis yra 28×28 pikselių pilkos spalvos
  - 10 klasių (skaitmenys 0-9)

Neuroninio tinklo architektūra (analogiška TensorFlow pavyzdžiui):
  - Flatten: 28×28 → 784
  - Dense (128 neuronų, ReLU aktyvacija)
  - Dropout (20%)
  - Dense (10 neuronų, Softmax išėjimas)
"""

# ============================================================
# 1 ŽINGSNIS: Importuojame bibliotekas
# ============================================================

# torch – pagrindinė PyTorch biblioteka (analogas TensorFlow)
import torch

# torch.nn – neuroninio tinklo moduliai (sluoksniai, aktyvacijos)
import torch.nn as nn

# torch.optim – optimizavimo algoritmai (Adam, SGD ir kt.)
import torch.optim as optim

# torchvision – kompiuterinės regos duomenų rinkiniai ir transformacijos
from torchvision import datasets, transforms

# torch.utils.data – duomenų užkrovimo įrankiai (DataLoader)
from torch.utils.data import DataLoader

# numpy – skaitinių skaičiavimų biblioteka
import numpy as np

print("=" * 70)
print("MNIST SKAITMENŲ ATPAŽINIMAS SU PYTORCH")
print("=" * 70)
print(f"PyTorch versija: {torch.__version__}")

# Nustatome įrenginį – CPU arba GPU (jei yra CUDA palaikanti vaizdo plokštė)
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f"Naudojamas įrenginys: {device}")

# ============================================================
# 2 ŽINGSNIS: Paruošiame duomenų transformacijas
# ============================================================

# transforms.Compose – sujungia kelias transformacijas į vieną seką
transform = transforms.Compose([
    # ToTensor() – konvertuoja PIL paveikslėlį į PyTorch tensorių
    # ir normalizuoja pikselių reikšmes iš [0, 255] į [0.0, 1.0]
    transforms.ToTensor(),
    
    # Normalize – standartizuoja reikšmes: (x - 0.1307) / 0.3081
    # 0.1307 ir 0.3081 yra MNIST duomenų vidurkis ir standartinis nuokrypis
    transforms.Normalize((0.1307,), (0.3081,))
])

# ============================================================
# 3 ŽINGSNIS: Užkrauname MNIST duomenis
# ============================================================

# datasets.MNIST – automatiškai atsisiunčia ir užkrauna MNIST duomenų rinkinį
# train=True – mokymo rinkinys (60,000 paveikslėlių)
train_dataset = datasets.MNIST(
    root='./data',          # kur saugoti atsisiųstus duomenis
    train=True,             # mokymo rinkinys
    download=True,          # atsisiųsti, jei dar nėra
    transform=transform     # pritaikyti transformacijas
)

# train=False – testavimo rinkinys (10,000 paveikslėlių)
test_dataset = datasets.MNIST(
    root='./data',
    train=False,
    download=True,
    transform=transform
)

# DataLoader – efektyviai užkrauna duomenis partijomis (batch)
# batch_size=64 – kiek paveikslėlių apdorojama vienu metu
# shuffle=True – sumaišo duomenis kiekvieną epochą (geresniam mokymui)
train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=1000, shuffle=False)

print(f"\n1. Duomenų rinkinys: MNIST")
print(f"   Mokymo paveikslėlių: {len(train_dataset)}")
print(f"   Testavimo paveikslėlių: {len(test_dataset)}")
print(f"   Paveikslėlio dydis: 28×28 pikseliai")
print(f"   Klasių skaičius: 10 (skaitmenys 0-9)")

# ============================================================
# 4 ŽINGSNIS: Apibrėžiame neuroninio tinklo architektūrą
# ============================================================

# Kuriame klasę, kuri paveldi iš nn.Module (bazinė PyTorch tinklo klasė)
class MNISTNet(nn.Module):
    def __init__(self):
        # Iškviečiame tėvinės klasės konstruktorių
        super(MNISTNet, self).__init__()
        
        # nn.Flatten() – "ištiesina" 28×28 matricą į 784 elementų vektorių
        # Analogas TensorFlow: tf.keras.layers.Flatten()
        self.flatten = nn.Flatten()
        
        # nn.Linear(784, 128) – pilnai sujungtas sluoksnis
        # 784 įėjimai (28×28 pikseliai) → 128 neuronai
        # Analogas TensorFlow: tf.keras.layers.Dense(128)
        self.fc1 = nn.Linear(784, 128)
        
        # nn.ReLU() – ReLU aktyvacijos funkcija: f(x) = max(0, x)
        # Analogas TensorFlow: activation='relu'
        self.relu = nn.ReLU()
        
        # nn.Dropout(0.2) – atsitiktinai "išjungia" 20% neuronų mokymosi metu
        # Neleidžia modeliui "persimokinti" (overfitting prevencija)
        # Analogas TensorFlow: tf.keras.layers.Dropout(0.2)
        self.dropout = nn.Dropout(0.2)
        
        # nn.Linear(128, 10) – išėjimo sluoksnis
        # 128 įėjimų → 10 neuronų (po vieną kiekvienam skaitmenui 0-9)
        # Analogas TensorFlow: tf.keras.layers.Dense(10)
        self.fc2 = nn.Linear(128, 10)
    
    def forward(self, x):
        """Apibrėžia, kaip duomenys keliauja per tinklą (pirmyn)"""
        x = self.flatten(x)     # 28×28 → 784
        x = self.fc1(x)         # 784 → 128
        x = self.relu(x)        # ReLU aktyvacija
        x = self.dropout(x)     # Dropout regularizacija
        x = self.fc2(x)         # 128 → 10
        return x                # Grąžina logitus (neapdorotas reikšmes)

# Sukuriame modelio objektą ir perkeliame į įrenginį (CPU/GPU)
model = MNISTNet().to(device)

print(f"\n2. Modelio architektūra:")
print(model)

# Suskaičiuojame parametrų skaičių
total_params = sum(p.numel() for p in model.parameters())
print(f"   Bendras parametrų skaičius: {total_params:,}")

# ============================================================
# 5 ŽINGSNIS: Apibrėžiame nuostolių funkciją ir optimizatorių
# ============================================================

# CrossEntropyLoss – nuostolių funkcija daugiaklasei klasifikacijai
# Ji sujungia LogSoftmax + NLLLoss (neigiamų log tikimybių nuostolis)
# Analogas TensorFlow: loss='sparse_categorical_crossentropy'
criterion = nn.CrossEntropyLoss()

# Adam optimizatorius – adaptyvinė mokymosi greičio strategija
# lr=0.001 – mokymosi greitis (learning rate)
# Analogas TensorFlow: optimizer='adam'
optimizer = optim.Adam(model.parameters(), lr=0.001)

print(f"\n3. Mokymosi konfigūracija:")
print(f"   Nuostolių funkcija: CrossEntropyLoss")
print(f"   Optimizatorius: Adam (lr=0.001)")

# ============================================================
# 6 ŽINGSNIS: Treniruojame modelį
# ============================================================

print(f"\n4. Pradedame mokymą (5 epochos)...")

epochs = 5  # Kiek kartų modelis peržiūri visus duomenis

for epoch in range(epochs):
    # Perjungiame modelį į mokymo režimą (Dropout aktyvus)
    model.train()
    
    running_loss = 0.0       # Sukauptas nuostolis per epochą
    correct = 0              # Teisingos prognozės
    total = 0                # Bendras imčių skaičius
    
    for batch_idx, (data, target) in enumerate(train_loader):
        # Perkeliame duomenis į įrenginį (CPU/GPU)
        data, target = data.to(device), target.to(device)
        
        # Išvalome ankstesnius gradientus
        optimizer.zero_grad()
        
        # Pirmyn – praleidžiame duomenis per tinklą
        output = model(data)
        
        # Apskaičiuojame nuostolį
        loss = criterion(output, target)
        
        # Atgal – apskaičiuojame gradientus (backpropagation)
        loss.backward()
        
        # Atnaujiname modelio svorius
        optimizer.step()
        
        # Statistika
        running_loss += loss.item()
        _, predicted = torch.max(output, 1)   # Randa klasę su didžiausia tikimybe
        total += target.size(0)
        correct += (predicted == target).sum().item()
    
    # Epochos statistika
    avg_loss = running_loss / len(train_loader)
    accuracy = correct / total
    print(f"   Epocha {epoch+1}/{epochs}: "
          f"Nuostolis={avg_loss:.4f}, Tikslumas={accuracy:.4f} ({accuracy*100:.1f}%)")

# ============================================================
# 7 ŽINGSNIS: Įvertiname modelį testavimo duomenimis
# ============================================================

# Perjungiame modelį į vertinimo režimą (Dropout neaktyvus)
model.eval()

test_loss = 0.0
correct = 0
total = 0

# torch.no_grad() – išjungia gradientų skaičiavimą (taupome atmintį)
with torch.no_grad():
    for data, target in test_loader:
        data, target = data.to(device), target.to(device)
        output = model(data)
        test_loss += criterion(output, target).item()
        _, predicted = torch.max(output, 1)
        total += target.size(0)
        correct += (predicted == target).sum().item()

test_loss /= len(test_loader)
test_accuracy = correct / total

print(f"\n5. Testavimo rezultatai:")
print(f"   Nuostolis (loss): {test_loss:.4f}")
print(f"   Tikslumas (accuracy): {test_accuracy:.4f} ({test_accuracy*100:.1f}%)")

# ============================================================
# 8 ŽINGSNIS: Prognozuojame kelis pavyzdžius
# ============================================================

print(f"\n6. Pirmųjų 5 testavimo paveikslėlių prognozės:")

# Paimame pirmą testavimo partiją
test_data, test_targets = next(iter(test_loader))
test_data, test_targets = test_data.to(device), test_targets.to(device)

with torch.no_grad():
    outputs = model(test_data[:5])
    # Softmax paverčia logitus į tikimybes
    probabilities = torch.softmax(outputs, dim=1)
    _, predictions = torch.max(outputs, 1)

for i in range(5):
    pred = predictions[i].item()
    true = test_targets[i].item()
    prob = probabilities[i][pred].item()
    status = "✓" if pred == true else "✗"
    print(f"   #{i+1}: Prognozė={pred}, Tikrasis={true}, "
          f"Tikimybė={prob:.4f} {status}")

print("\n✓ PyTorch MNIST analizė baigta!")
