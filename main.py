import torch as T
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from inference_sdk import InferenceHTTPClient, InferenceConfiguration
import pprint
from dqnv2 import Agent
from accion_executor import ejecutar_accion
import tkinter as tk
from tkinter import ttk

# NUEVO: encodeador básico
from typing import Dict

def encode_state(player: Dict, enemy: Dict):
    state = []

    # Player info
    state.append(len(player["hand"]))  # número de cartas en mano
    state.append(player["don"])
    state.append(player["rested_don"])
    state.append(player["life"])

    # Enemy info
    state.append(len(enemy["hand"]))
    state.append(enemy["don"])
    state.append(enemy["rested_don"])
    state.append(enemy["life"])

    # Player characters
    for i in range(5):
        if i < len(player["characters"]):
            c = player["characters"][i]
            state.extend([
                hash(c["class"]) % 1000 / 1000.0,
                float(c["isRested"]),
                c["attached_don"]
            ])
        else:
            state.extend([0.0, 0.0, 0.0])

    # Enemy characters
    for i in range(5):
        if i < len(enemy["characters"]):
            c = enemy["characters"][i]
            state.extend([
                hash(c["class"]) % 1000 / 1000.0,
                float(c["isRested"]),
                c["attached_don"]
            ])
        else:
            state.extend([0.0, 0.0, 0.0])

    # Padding para llegar a 97 dimensiones si hace falta
    while len(state) < 97:
        state.append(0.0)

    return T.tensor([state], dtype=T.float)

# Configuración de Roboflow
MY_KEY = "tx7I4BVTJr13AyXuOGfU"
img_path = "./Roboflow/img_1753.jpg"

# Inicialización del agente
estratega = Agent(
    gamma=0.99,
    epsilon=0.0,
    lr=0.0005,
    input_dims=[97],
    batch_size=64,
    n_actions=4,
    fname="final_model.pth"
)

# Funciones de formato de cartas y estado
CARD_WIDTH = 95  # aprox
RESTED_cARD_WIDTH = 125  # aprox

def add_card(prd, agent, type):
    isRested = prd["height"] < 120
    agent[type].append({
        "class": prd["class"],
        "position": pos_in_table(prd),
        "x": prd["x"],
        "y": prd["y"],
        "confidence": prd["confidence"],
        "isRested": isRested,
        "attached_don": 0
    })

def pos_in_table(prd):
    pos = 0
    if prd["y"] > 800 or prd["y"] < 430:
        return -1
    startX = 780
    return round((prd["x"] - startX) / CARD_WIDTH) + 1

def format_main_cards_player(prd, agent):
    if 740 < prd["y"] < 780 and 960 < prd["x"] < 1040:
        add_card(prd, agent, "leader")
    elif prd["x"] < 600 and prd["y"] < 950:
        add_card(prd, agent, "hand")
    elif 600 < prd["y"] < 640 and 760 < prd["x"] < 1400:
        add_card(prd, agent, "characters")
    elif prd["x"] > 1200 and prd["y"] > 900:
        agent["trash"].append(prd)

def format_main_cards_enemy(prd, agent):
    if 290 < prd["y"] < 360 and 900 < prd["x"] < 940:
        add_card(prd, agent, "leader")
    elif prd["x"] < 300 and prd["y"] < 170:
        agent["trash"].append(prd)
    elif 430 < prd["y"] < 470 and 680 < prd["x"] < 1200:
        add_card(prd, agent, "characters")

# Estado inicial del jugador y enemigo
player = {"leader": [], "hand": [], "characters":[], "don" : 0, "rested_don": 0, "attached_don": [], "trash" : [], "life": 0 }
enemy = {"leader": [], "hand": [], "characters":[], "don" : 0, "rested_don": 0, "attached_don": [], "trash" : [], "life": 0 }

# Aquí se insertaría la inferencia de Roboflow
result = {"predictions": []}  # <- reemplazar por resultado real

# Procesamiento de predicciones
for prd in result["predictions"]:
    if prd["y"] > 600:
        format_main_cards_player(prd, player)
        if prd["class"] == "don":
            if prd["height"] > 110:
                player["don"] = round(((prd["width"] - 95.7) / 28) + 1)
            else:
                player["rested_don"] = round(((prd["width"] - 50) / 28) + 1)
        elif prd["class"] == "attached_don":
            player["attached_don"].append({"x": prd["x"], "y": prd["y"], "position": pos_in_table(prd), "count": round(((prd["height"] - 44) / 11) + 1)})
        elif prd["class"] == "life":
            player["life"] = round(((prd["height"] - 131) / 26) + 1)
    else:
        format_main_cards_enemy(prd, enemy)
        if prd["class"] == "don":
            if prd["height"] > 110:
                enemy["don"] = round(((prd["width"] - 95.7) / 28) + 1)
            else:
                enemy["rested_don"] = round(((prd["width"] - 50) / 28) + 1)
        elif prd["class"] == "attached_don":
            enemy["attached_don"].append({"x": prd["x"], "y": prd["y"], "position": pos_in_table(prd), "count": round(((prd["height"] - 44) / 11) + 1)})
        elif prd["class"] == "life":
            enemy["life"] = round(((prd["height"] - 131) / 26) + 1)

# Asignar attached_don
for dones in enemy["attached_don"]:
    if dones["position"] == -1:
        enemy["leader"][0]["attached_don"] = dones["count"]
    else:
        for character in enemy["characters"]:
            if character["position"] == dones["position"]:
                character["attached_don"] = dones["count"]

for dones in player["attached_don"]:
    if dones["position"] == -1:
        player["leader"][0]["attached_don"] = dones["count"]
    else:
        for character in player["characters"]:
            if character["position"] == dones["position"]:
                character["attached_don"] = dones["count"]

# Codificación del estado
action_tensor = encode_state(player, enemy)
accion_index = estratega.choose_action(action_tensor)

# Interfaz gráfica para mostrar la acción sugerida
window = tk.Tk()
window.title("Recomendación del Estratega IA")
window.geometry("600x300")

label = ttk.Label(window, text="Recomendación del turno:", font=("Arial", 14))
label.pack(pady=10)

output = tk.Text(window, wrap="word", width=60, height=10, font=("Courier", 10))
output.pack(padx=20, pady=10)

# Simulación de posibles acciones (esto deberías obtenerlo de tus logs o sistema de acciones reales)
acciones_disponibles = [
    {"tipo": "atacar", "atacante": "Luffy", "objetivo": "Robin", "coords_atacante": (200, 500), "coords_objetivo": (900, 500)},
    {"tipo": "atacar", "atacante": "Zoro", "objetivo": "Usopp", "coords_atacante": (250, 500), "coords_objetivo": (950, 500)},
    {"tipo": "invocar", "carta": "Sanji", "coords": (180, 650)},
    {"tipo": "pasar_turno"},
]

accion_elegida = acciones_disponibles[accion_index] if accion_index < len(acciones_disponibles) else {"tipo": "pasar_turno"}

output.insert("1.0", pprint.pformat(accion_elegida))

window.mainloop()
