import gym
from gym import spaces
import numpy as np
import random

class OnePieceTCGEnv(gym.Env):
    """
    Entorno Gym completo para One Piece Card Game, ahora con:
    - Campo con estado active/rested
    - Clasificación por tipo (blocker, rush...)
    """

    def __init__(self, logs, catalogo_cartas):
        super(OnePieceTCGEnv, self).__init__()

        self.logs = logs
        self.catalogo = catalogo_cartas
        self.max_mano = 15
        self.max_board = 5

        # Espacio de observación extendido
        self.observation_space = spaces.Dict({
            "mano_coste": spaces.Box(0, 10, (self.max_mano,), dtype=np.int32),
            "mano_poder": spaces.Box(0, 13000, (self.max_mano,), dtype=np.int32),
            "mano_counter": spaces.Box(0, 2000, (self.max_mano,), dtype=np.int32),
            "mano_tipo_blocker": spaces.MultiBinary(self.max_mano),
            "mano_tipo_rush": spaces.MultiBinary(self.max_mano),

            "board_poder": spaces.Box(0, 13000, (self.max_board,), dtype=np.int32),
            "board_estado": spaces.MultiBinary(self.max_board),
            "board_tipo_blocker": spaces.MultiBinary(self.max_board),
            "board_tipo_rush": spaces.MultiBinary(self.max_board),

            "trash_count": spaces.Discrete(40),
            "vida": spaces.Discrete(6),
        })

        self.action_space = spaces.Discrete(self.max_mano + 1 + self.max_board)

        self.pointer = 0
        self.log_actual = None
        self.log_keys = []
        self.done = False
        self.current_obs = None
    def _extraer_observacion_combinada(self, paso_cards, paso_life):
        """
        Une dos pasos consecutivos: uno con 'cards' y otro con 'life',
        útil cuando están separados en el log.
        """
        combinado = dict(paso_cards)
        combinado["life"] = paso_life.get("life", 0)
        return self._extraer_observacion(combinado)

    def reset(self):
        self.log_actual = random.choice(self.logs)
        self.log_keys = sorted(self.log_actual.keys())
        self.pointer = 0
        self.done = False

        # Últimos valores conocidos
        mano = []
        board = []
        trash = []
        vida = 5  # valor por defecto

        for key in self.log_keys:
            paso = self.log_actual[key]

            if "cards" in paso and paso.get("action") == "Hand state":
                mano = paso["cards"]

            if "board" in paso and paso.get("action") == "Board state":
                board = paso["board"]

            if "trash" in paso and paso.get("action") == "Trash state":
                trash = paso["trash"]

            if "life" in paso and paso.get("action") == "Life state":
                vida = paso["life"]

    # Construimos el estado manualmente
        paso_completo = {
            "cards": mano,
            "board": board,
            "trash": trash,
            "life": vida
        }

        self.current_obs = self._extraer_observacion(paso_completo)
        return self.current_obs
    def step(self, action):
        reward = 0.0
        done = False
        info = {}
        next_obs = self.current_obs
        prev_obs = self.current_obs  # snapshot para comparar

        while self.pointer < len(self.log_keys) - 1:
            self.pointer += 1
            step = self.log_actual[self.log_keys[self.pointer]]
            accion_log = step.get("action", "")

            vida_actual = step.get("life", prev_obs["vida"])

            # 🎯 Recompensas y castigos intermedios
            if accion_log == "Played card":
                if 1 <= action <= self.max_mano:
                    reward += 1
                else:
                    reward -= 1

            elif accion_log == "Attacking":
                if action >= self.max_mano + 1:
                    reward += 2
                else:
                    reward -= 2

            elif accion_log == "End turn":
                if action == 0:
                    reward += 1
                else:
                    reward -= 1
            if accion_log == "Life state" and step.get("life", 1) <= 0:
                done = True
                reward = 5.0  
            # 🔻 Castigo por recibir daño
            if vida_actual < prev_obs["vida"]:
                reward -= 3

            # 🔻 Castigo por jugar en slot vacío
            #if 1 <= action <= self.max_mano:
            #    idx = action - 1
            #    if prev_obs["mano_coste"][idx] == 0:
            #       reward -= 1.0

        # 🔻 Castigo por atacar con carta descansada
            if action >= self.max_mano + 1:
                idx = action - (self.max_mano + 1)
                if prev_obs["board_estado"][idx] == 0:
                    reward -= 1.0

        # 🔻 Castigo por no actuar cuando debía
            #if accion_log == "Played card" and action == 0:
            #    reward -= 0.5

        # ✅ ÚLTIMO: castigo por perder la partida
            if vida_actual <= 0:
                reward = 0
                done = True
                info["reason"] = "lost"
                break

        # 🧠 Si encontramos estado jugable, salimos del bucle
            if self._es_estado_completo(step):
                next_obs = self._extraer_observacion(step)
                break

        self.current_obs = next_obs
        self.done = done
        return next_obs, reward, done, info

    def render(self, mode="human"):
        print(" VIDA:", self.current_obs["vida"])
        print(" MANO (coste):", self.current_obs["mano_coste"])
        print(" BOARD (poder):", self.current_obs["board_poder"])
        print(" BOARD (activo):", self.current_obs["board_estado"])
        print(" BLOCKER:", self.current_obs["board_tipo_blocker"])
        print(" RUSH:", self.current_obs["board_tipo_rush"])

    def _es_estado_completo(self, paso):
        return (
            paso.get("action") in ["Hand state", "Board state", "Life state", "Trash state"]
            and "cards" in paso and "life" in paso
        )

    def _extraer_observacion(self, paso):
        mano_ids = paso.get("cards", [])
        mano_coste = np.zeros(self.max_mano, dtype=np.int32)
        mano_poder = np.zeros(self.max_mano, dtype=np.int32)
        mano_counter = np.zeros(self.max_mano, dtype=np.int32)
        mano_tipo_blocker = np.zeros(self.max_mano, dtype=np.int32)
        mano_tipo_rush = np.zeros(self.max_mano, dtype=np.int32)

        for i in range(min(len(mano_ids), self.max_mano)):
            carta = self.catalogo.get(mano_ids[i], {})
            mano_coste[i] = carta.get("cost", 0)
            mano_poder[i] = carta.get("power", 0)
            mano_counter[i] = carta.get("counter", 0)

            efecto = (carta.get("effect", "") or "") + (carta.get("type", "") or "")
            mano_tipo_blocker[i] = int("Blocker" in efecto)
            mano_tipo_rush[i] = int("Rush" in efecto)

        board_cards = paso.get("board", [])
        board_poder = np.zeros(self.max_board, dtype=np.int32)
        board_estado = np.ones(self.max_board, dtype=np.int32)  # Default: active
        board_tipo_blocker = np.zeros(self.max_board, dtype=np.int32)
        board_tipo_rush = np.zeros(self.max_board, dtype=np.int32)

        for i in range(min(len(board_cards), self.max_board)):
            if isinstance(board_cards[i], dict):
                card_id = board_cards[i].get("card_id")
                rested = board_cards[i].get("rested", False)
            else:
                card_id = board_cards[i]
                rested = False  # si no hay estado, asumimos activo

            carta = self.catalogo.get(card_id, {})
            board_poder[i] = carta.get("power", 0)
            board_estado[i] = int(not rested)

            efecto = (carta.get("effect", "") or "") + (carta.get("type", "") or "")
            board_tipo_blocker[i] = int("Blocker" in efecto)
            board_tipo_rush[i] = int("Rush" in efecto)

        trash = paso.get("trash", [])
        trash_count = len(trash)

        return {
            "mano_coste": mano_coste,
            "mano_poder": mano_poder,
            "mano_counter": mano_counter,
            "mano_tipo_blocker": mano_tipo_blocker,
            "mano_tipo_rush": mano_tipo_rush,
            "board_poder": board_poder,
            "board_estado": board_estado,
            "board_tipo_blocker": board_tipo_blocker,
            "board_tipo_rush": board_tipo_rush,
            "trash_count": trash_count,
            "vida": paso.get("life", 0)
        }
