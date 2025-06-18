import os
import json

from gpt_env import OnePieceTCGEnv
from gym.envs.registration import register
import gym
def read_log_files(directory_path):
    data_list = []
    for filename in os.listdir(directory_path):
        if filename.endswith('.json'):
            file_path = os.path.join(directory_path, filename)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    data_list.append(data)
            except json.JSONDecodeError as e:
                print(f"Error leyendo {file_path}: {e}")
    return data_list
def read_card_files(directory_path):
    card_list = []
    if not os.path.exists(directory_path):
        print(f"Ruta no encontrada: {directory_path}")
        return card_list
    for filename in os.listdir(directory_path):
        if filename.endswith('.json'):
            file_path = os.path.join(directory_path, filename)
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                card_list.append(data)
    return card_list
# Este wrapper asegura que se pase correctamente a gym.make
def make_onepiece_env():
    catalogo = read_card_files("assets/JSON/Cards")
    logs = read_log_files("assets/JSON/Battle_log")
    return OnePieceTCGEnv(logs, catalogo)

register(
    id="OnePieceTCG-v0",
    entry_point="env_registry:make_onepiece_env",
)
