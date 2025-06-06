import gym
from gym import Env
from gym.spaces import Discrete, Box, Dict, MultiDiscrete
import numpy as np
import json
import os
import random
from typing import Dict, List, Optional, Tuple
from collections import defaultdict

def read_multiple_json_files(directory_path):
    data_list = []
    for filename in os.listdir(directory_path):
        if filename.endswith('.json'):
            file_path = os.path.join(directory_path, filename)
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                data_list.append(data)
    return data_list

class OnePieceTCGEnv(gym.Env):
    def __init__(self):
        