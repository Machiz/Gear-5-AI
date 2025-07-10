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

ROBOFLOW_MODEL_ID = "one-piece-card-game-l" # Replace with your project ID
ROBOFLOW_MODEL_VERSION = 2 # Replace with your model version number (e.g., 2)

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

def format_main_cards_player(prd: Dict, player_data: Dict):
    if 740 < prd["y"] < 780 and 960 < prd["x"] < 1040:
        add_card(prd, player_data, "leader")
    elif prd["x"] < 600 and prd["y"] < 950:
        add_card(prd, player_data, "hand")
    elif 600 < prd["y"] < 640 and 760 < prd["x"] < 1400:
        add_card(prd, player_data, "characters")
    elif prd["x"] > 1200 and prd["y"] > 900:
        player_data["trash"].append(prd)

def format_main_cards_enemy(prd: Dict, enemy_data: Dict):
    if 290 < prd["y"] < 360 and 900 < prd["x"] < 940:
        add_card(prd, enemy_data, "leader")
    elif prd["x"] < 300 and prd["y"] < 170:
        enemy_data["trash"].append(prd)
    elif 430 < prd["y"] < 470 and 680 < prd["x"] < 1200:
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
            version=ROBOFLOW_MODEL_VERSION
        )
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
            enemy["leader"][0]["attached_don"] = dones["count"]
        else:
            for character in enemy.get("characters", []):
                if character.get("position") == dones["position"]:
                    character["attached_don"] = dones["count"]

    for dones in player.get("attached_don", []):
        if dones["position"] == -1 and player.get("leader"):
            player["leader"][0]["attached_don"] = dones["count"]
        else:
            for character in player.get("characters", []):
                if character.get("position") == dones["position"]:
                    character["attached_don"] = dones["count"]

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

    acciones_disponibles = [
        {"tipo": "atacar", "descripcion": "Atacar al líder enemigo"},
        {"tipo": "atacar", "descripcion": "Atacar a un personaje (primero disponible)"},
        {"tipo": "invocar", "descripcion": "Invocar una carta de tu mano (primera disponible)"},
        {"tipo": "pasar_turno", "descripcion": "Pasar el turno"}
    ]

    accion_elegida = acciones_disponibles[accion_index] if accion_index < len(acciones_disponibles) else {"tipo": "ERROR: Acción desconocida", "descripcion": "El índice de acción está fuera de los límites de las acciones disponibles."}

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