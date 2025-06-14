import gym
from gym import Env
from gym.spaces import Discrete, Box, Dict, MultiDiscrete
import numpy as np

import random
from typing import Dict, List, Optional, Tuple
from collections import defaultdict



class OnePieceTCGEnv(gym.Env):
    def __init__(self):
        self.action_space = Discrete()
        """
        consultar cual usar
        0: loss
        1: fails
        2: destroyed
        3: hit 1 life
        4: win

        ----------
        0: draw don
        1: draw card
        2: main
        3: end 
        """

