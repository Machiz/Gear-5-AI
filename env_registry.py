import os
import json

from gpt_env import OnePieceTCGEnv
from gym.envs.registration import register
import gym
def read_log_files(directory_path):#, max_files = 30):
    """Lee todos los logs de partidas desde una carpeta y los devuelve en una lista."""
    data_list = []
    #count =0
    for filename in os.listdir(directory_path):
        if filename.endswith('.json') :
            file_path = os.path.join(directory_path, filename)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if isinstance(data, dict):  # los logs deben ser dict
                        data_list.append(data)
                
                    else:
                        print(f"⚠️ {filename} ignorado: no es un diccionario.")
                #count +=1
                #if count >=max_files:
                   # break
            except json.JSONDecodeError as e:
                print(f"❌ Error leyendo {file_path}: {e}")
    print(f"✅ logs cargados: {len(data_list)}")
    return data_list



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

# Este wrapper asegura que se pase correctamente a gym.make
def make_onepiece_env():
    catalogo = read_card_files("assets/JSON/Cards")
    logs = read_log_files("assets/JSON/Battle_log")
    return OnePieceTCGEnv(logs, catalogo)

register(
    id="OnePieceTCG-v0",
    entry_point="env_registry:make_onepiece_env",
)