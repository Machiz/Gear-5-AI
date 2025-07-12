import torch as T
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from inference_sdk import InferenceHTTPClient
import pprint
from dqnv2 import Agent # Assuming dqnv2.py is in the same directory
from accion_executor import ejecutar_accion
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import mss
import time
import os
import json

# NUEVO: encodeador básico
from typing import Dict, List

def encode_state(player: Dict, enemy: Dict):
    """
    Encodes the game state into a numerical tensor for the DQN agent.
    This function assumes a fixed maximum number of characters (5) for both
    player and enemy.
    """
    state = []

    # Player info
    state.append(len(player.get("hand", [])))
    state.append(player.get("don", 0))
    state.append(player.get("rested_don", 0))
    state.append(player.get("life", 0))

    # Enemy info
    state.append(len(enemy.get("hand", [])))
    state.append(enemy.get("don", 0))
    state.append(enemy.get("rested_don", 0))
    state.append(enemy.get("life", 0))

    # Player characters
    player_characters = player.get("characters", [])
    for i in range(5):
        if i < len(player_characters):
            c = player_characters[i]
            state.extend([
                hash(c.get("class", "unknown")) % 1000 / 1000.0,
                float(c.get("isRested", False)),
                c.get("attached_don", 0)
            ])
        else:
            state.extend([0.0, 0.0, 0.0])

    # Enemy characters
    enemy_characters = enemy.get("characters", [])
    for i in range(5):
        if i < len(enemy_characters):
            c = enemy_characters[i]
            state.extend([
                hash(c.get("class", "unknown")) % 1000 / 1000.0,
                float(c.get("isRested", False)),
                c.get("attached_don", 0)
            ])
        else:
            state.extend([0.0, 0.0, 0.0])

    # Padding to reach 97 dimensions
    while len(state) < 97:
        state.append(0.0)

    return T.tensor([state[:97]], dtype=T.float)

# --- Roboflow Configuration ---
MY_KEY = "qRLJutrdvLsdTJbXhPZy" # Your API key
ROBOFLOW_API_URL = "https://detect.roboflow.com/" # Standard Roboflow Inference API URL

try:
    client = InferenceHTTPClient(
        api_key=MY_KEY,
        api_url=ROBOFLOW_API_URL
    )
    print("Roboflow client initialized successfully.")
except Exception as e:
    print(f"Error initializing Roboflow client: {e}")
    print("Please ensure your API Key and API URL are correct.")
    exit()

ROBOFLOW_MODEL_ID = "card-detection-hbgys/4" # Replace with your project ID

# --- Agent Initialization ---
# CORRECTED: Removed 'fname' from Agent constructor, as confirmed by your screenshot
estratega = Agent(
    gamma=0.99,
    epsilon=1,
    lr=0.0005,
    input_dims=[97],
    batch_size=64,
    n_actions=21,
    max_mem_size=100000, # Added as seen in your Agent.__init__ screenshot
    eps_end=0.01,       # Added as seen in your Agent.__init__ screenshot
    eps_dec=0.0005      # Added as seen in your Agent.__init__ screenshot
)

# Define filename for loading the model
MODEL_FILENAME = "final_dqn_model.pth"

try:
    # Explicitly pass the filename to load_models()
    # Assuming load_models in dqnv2.py accepts a filename and uses self.Q_eval internally
    estratega.load_models(MODEL_FILENAME)
    print(f"DQN model loaded successfully from {MODEL_FILENAME}.")
except Exception as e:
    print(f"Error loading DQN model from {MODEL_FILENAME}: {e}")
    print(f"Please ensure '{MODEL_FILENAME}' exists and is a valid model file and that Agent.load_models uses self.Q_eval.")
    exit()

# --- Card and State Formatting Functions (unchanged) ---
CARD_WIDTH = 95
RESTED_CARD_WIDTH = 125

def add_card(prd: Dict, agent_data: Dict, card_type: str):
    isRested = prd["height"] < 120
    agent_data[card_type].append({
        "class": prd["class"],
        "position": pos_in_table(prd),
        "x": prd["x"],
        "y": prd["y"],
        "confidence": prd["confidence"],
        "isRested": isRested,
        "attached_don": 0
    })

def pos_in_table(prd: Dict) -> int:
    if prd["y"] > 800 or prd["y"] < 430:
        return -1
    startX = 780
    return round((prd["x"] - startX) / CARD_WIDTH) + 1

def pos_in_table_hand(card, min_x, player):
    CARD_WIDTH = 95 #aprox
    dif = 1 if (len(player["hand"])) < 4 else (len(player["hand"]) - 3)
    CARD_WIDTH -= 10 * dif
    # RESTED_cARD_WIDTH = 125 #aprox
    startX = min_x - 10
    pos = round((card["x"] - startX)/CARD_WIDTH) + 1
    print(startX, (card["x"] - startX)/CARD_WIDTH + 1)
    return pos

def format_main_cards_player(prd: Dict, player_data: Dict):
    if(prd["y"] > 790 and prd["y"] < 935): # LEADER
        if(prd["x"] > 950 and prd["x"] < 1058):
            add_card(prd, player_data, "leader")

    elif(prd["x"] < 600): # HAND
        add_card(prd, player_data, "hand")

    elif(prd["y"] > 630 and prd["y"] < 780): # CHARACTER
        if(prd["x"] > 700 and prd["x"] < 1300):
            add_card(prd, player_data, "characters")
            
    elif(prd["x"] > 1190 and prd["y"] > 1100): # TRASH
        player_data["trash"].append(prd)

def format_main_cards_enemy(prd: Dict, enemy_data: Dict):
    if(prd["y"] > 275 and prd["y"] < 435): # LEADER
        if(prd["x"] > 855 and prd["x"] < 959):
            add_card(prd, enemy_data, "leader")

    elif(prd["x"] < 730 and prd["y"] < 200): # TRASH
        enemy_data["trash"].append(prd)

    elif(prd["y"] > 430 and prd["y"] < 600): # CHARACTER
        if(prd["x"] > 610 and prd["x"] < 1220):
            add_card(prd, enemy_data, "characters")

# --- Screen Capture Function ---
SCREENSHOT_DIR = "screenshots"
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

def take_screenshot():
    with mss.mss() as sct:
        monitor = sct.monitors[1] # Assumes your game is on your primary monitor.
        sct_img = sct.grab(monitor)

        img = Image.frombytes("RGB", sct_img.size, sct_img.rgb)

        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(SCREENSHOT_DIR, f"screenshot_{timestamp}.png")

        img.save(filename)
        print(f"Screenshot saved to: {filename}")
        return filename
#catalogo = read_card_files("assets/JSON/Cards")
def interpretar_accion(action_index, player, catalogo_cartas):
    if 0 <= action_index <= 14:
        if action_index < len(player["hand"]):
            carta = player["hand"][action_index]
            class_name = carta.get("class", "").strip()

            if not class_name:
                return {"tipo": "invalida", "descripcion": f"Carta sin nombre en slot {action_index}"}

            carta_info = catalogo_cartas.get(class_name, {})
            coste = carta_info.get("cost", None)

            dons_disponibles = player.get("don", 0)
            if coste > dons_disponibles:
                return {
                    "tipo": "invalida",
                    "descripcion": f"No hay suficientes dons: coste {coste}, dons disponibles {dons_disponibles}"
                }

            return {
                "tipo": "invocar",
                "mano_slot": action_index,
                "descripcion": f"✅ Invocar carta: {class_name} (coste {coste})"
            }
        else:
            return {"tipo": "invalida", "descripcion": "Slot de mano inválido"}

    elif 15 <= action_index <= 19:
        board_slot = action_index - 15
        for personaje in player.get("characters", []):
            if personaje.get("position") == board_slot and not personaje.get("rested", True):
                return {
                    "tipo": "atacar",
                    "quien": f"personaje en posición {board_slot}",
                    "descripcion": f"✅ Atacar con personaje en posición {board_slot}"
                }
        return {
            "tipo": "invalida",
            "descripcion": f"No hay personaje activo en posición {board_slot} para atacar"
        }

    elif action_index == 20:
        if player.get("leader") and not player["leader"][0].get("rested", True):
            return {
                "tipo": "atacar",
                "quien": "líder",
                "descripcion": "✅ Atacar con el líder"
            }
        else:
            return {"tipo": "invalida", "descripcion": "El líder está descansado o no está detectado"}

    elif action_index == 21:
        return {"tipo": "pasar_turno", "descripcion": "⏭️ Pasar el turno"}

    else:
        return {"tipo": "ERROR", "descripcion": f"Índice fuera de rango: {action_index}"}

def read_card_files(directory_path):
    catalogo = {}
    #count = 0
    for archivo in os.listdir(directory_path):
        if archivo.endswith(".json"):
            path = os.path.join(directory_path, archivo)
            try:
                with open(path, "r", encoding="utf-8") as f:
                    contenido = json.load(f)

                    if isinstance(contenido, dict):
                        # ✅ Cada key es un ID y el value es la carta
                        for carta_id, carta in contenido.items():
                            if isinstance(carta, dict):
                                catalogo[carta_id] = carta
                            else:
                                print(f"❌ Carta inválida en {archivo}: {carta}")
                    elif isinstance(contenido, list):
                        for carta in contenido:
                            if not isinstance(carta, dict):
                                print(f"❌ Carta no válida en {archivo}: {carta}")
                                continue
                            carta_id = carta.get("card_id") or carta.get("id")
                            if carta_id:
                                catalogo[carta_id] = carta
                            else:
                                print(f"❌ Carta sin ID en {archivo}: {carta}")
                    else:
                        print(f"⚠️ {archivo} ignorado: contenido no compatible.")
                #count +=1
                #if count >= max_cards:
                  #  break

            except json.JSONDecodeError as e:
                print(f"❌ Error leyendo {archivo}: {e}")

    print(f"✅ Cartas cargadas: {len(catalogo)}")
    return catalogo
# --- Function to run AI inference and update GUI ---
def run_ai_inference(current_image_path):
    # Reset player and enemy state for each inference
    player = {"leader": [], "hand": [], "characters":[], "don" : 0, "rested_don": 0, "attached_don": [], "trash" : [], "life": 0 }
    enemy = {"leader": [], "hand": [], "characters":[], "don" : 0, "rested_don": 0, "attached_don": [], "trash" : [], "life": 0 }

    print(f"Performing Roboflow inference on: {current_image_path}")
    try:
        result = client.infer(
            current_image_path,
            model_id=ROBOFLOW_MODEL_ID,
        )
        print(result)
        print("Roboflow inference completed.")
    except Exception as e:
        print(f"Error during Roboflow inference: {e}")
        messagebox.showerror("Error de Roboflow", f"No se pudo realizar la inferencia: {e}")
        result = {"predictions": []}

    print("Processing Roboflow predictions...")
    for prd in result.get("predictions", []):
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

    for dones in enemy.get("attached_don", []):
        if dones["position"] == -1 and enemy.get("leader"):
            if(len(enemy["leader"]) == 0): continue
            enemy["leader"][0]["attached_don"] = dones["count"]
        else:
            for character in enemy.get("characters", []):
                if character.get("position") == dones["position"]:
                    character["attached_don"] = dones["count"]

    for dones in player.get("attached_don", []):
        if dones["position"] == -1 and player.get("leader"):
            if(len(player["leader"]) == 0): continue
            player["leader"][0]["attached_don"] = dones["count"]
        else:
            for character in player.get("characters", []):
                if character.get("position") == dones["position"]:
                    character["attached_don"] = dones["count"]
    min_x = 10000
    for i in range(len(player["hand"])): 
        if(player["hand"][i]["x"] < min_x):
            min_x = player["hand"][i]["x"]
    
    for card in player["hand"]:
        
        card["position"] = pos_in_table_hand(card, min_x, player)

    print("\n--- Current Player State ---")
    pprint.pprint(player)
    print("\n--- Current Enemy State ---")
    pprint.pprint(enemy)

    print("\nEncoding state and choosing action...")
    action_tensor = encode_state(player, enemy)
    with T.no_grad():
        # Ensure that estratega.choose_action uses self.Q_eval internally
        accion_index = estratega.choose_action(action_tensor)
    print(f"Chosen action index: {accion_index}")
    catalogo = read_card_files("assets/JSON/Cards")
    accion_elegida = interpretar_accion(accion_index, player, catalogo)

    output_text.delete("1.0", tk.END)
    output_text.insert("1.0", pprint.pformat(accion_elegida))

# --- GUI Setup ---
root = tk.Tk()
root.title("Recomendación del Estratega IA")

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

window_width = 400
window_height = 500

x = screen_width - window_width - 20
y = 20

root.geometry(f"{window_width}x{window_height}+{x}+{y}")
root.attributes("-topmost", True)

ai_frame = ttk.LabelFrame(root, text="Decisión del Modelo IA", padding="10")
ai_frame.pack(padx=10, pady=10, fill="both", expand=True)

label = ttk.Label(ai_frame, text="Recomendación del turno:", font=("Arial", 12, "bold"))
label.pack(pady=5)

output_text = tk.Text(ai_frame, wrap="word", width=40, height=10, font=("Courier", 10), state="normal")
output_text.pack(padx=5, pady=5, fill="both", expand=True)

screenshot_frame = ttk.LabelFrame(root, text="Control de Captura", padding="10")
screenshot_frame.pack(padx=10, pady=10, fill="x")

def on_capture_button_click():
    captured_image_path = take_screenshot()
    if captured_image_path:
        run_ai_inference(captured_image_path)
        messagebox.showinfo("Captura y Análisis", "Pantalla capturada y analizada.")
    else:
        messagebox.showerror("Error", "No se pudo tomar la captura de pantalla.")

capture_button = ttk.Button(screenshot_frame, text="Tomar Captura y Analizar", command=on_capture_button_click)
capture_button.pack(pady=5)

root.mainloop()