import gym
from gym import spaces
import numpy as np
import random

class OnePieceTCGEnv(gym.Env):
    def __init__(self, logs, catalogo_cartas):
        super(OnePieceTCGEnv, self).__init__()

        self.logs = logs
        self.catalogo = catalogo_cartas
        self.max_mano = 15
        self.max_board = 5

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

        self.action_space = spaces.Discrete(self.max_mano + 1 + self.max_board)  # 15 + 1 + 5 = 21

        self.pointer = 0
        self.log_actual = None
        self.log_keys = []
        self.done = False
        self.current_obs = None
        self.state = {}
    def generar_acciones_validas(self, obs):
        """
        Retorna una lista de índices de acciones válidas basado en la observación actual:
        - Acción 0: pasar turno (siempre válida)
        - Acciones 1 a max_mano: invocar cartas que tengan coste > 0
        - Acciones max_mano+1 a max_mano+max_board: atacar con personajes activos en el board
        """
        acciones = [0]  # pasar turno siempre permitida

        # Invocar desde mano (acciones 1 a 15)
        for i, coste in enumerate(obs["mano_coste"]):
            if coste > 0:
                acciones.append(i + 1)  # acción 1 es la primera carta, etc.

        # Atacar con personajes activos del board (acciones 16 a 20)
        for j, estado in enumerate(obs["board_estado"]):
            if estado == 1:  # solo si está activo
                acciones.append(self.max_mano + 1 + j)

        return acciones

    def reset(self):
        self.log_actual = random.choice(self.logs)
        self.log_keys = sorted(self.log_actual.keys())
        self.pointer = 0
        self.done = False
        self.state = {}

        estados_encontrados = {"mano": False, "board": False, "trash": False, "vida": False}

        while self.pointer < len(self.log_keys):
            paso = self.log_actual[self.log_keys[self.pointer]]
            self.pointer += 1
            accion = paso.get("action", "")

            if accion == "Hand state" and "cards" in paso:
                self.state["mano"] = paso["cards"]
                estados_encontrados["mano"] = True
            elif accion == "Board state" and "cards" in paso:
                self.state["board"] = paso["cards"]
                estados_encontrados["board"] = True
            elif accion == "Trash state" and "cards" in paso:
                self.state["trash"] = paso["cards"]
                estados_encontrados["trash"] = True
            elif accion == "Life state" and "life" in paso:
                self.state["vida"] = paso["life"]
                estados_encontrados["vida"] = True

            if all(estados_encontrados.values()):
                self.current_obs = self._extraer_observacion()
                return self.current_obs

        # 🚨 Si no se encontró todo, inicializa lo faltante para evitar crash
        self.state.setdefault("mano", [])
        self.state.setdefault("board", [])
        self.state.setdefault("trash", [])
        self.state.setdefault("vida", 5)

        print("⚠️ Estado incompleto, se usarán valores por defecto donde falte.")
        self.current_obs = self._extraer_observacion()
        return self.current_obs

    def step(self, action):
        reward = 0.0
        done = False
        info = {}
        next_obs = self.current_obs
        prev_obs = self.current_obs

        # 🚫 Validación inmediata de acción inválida
        if action >= self.max_mano + 1 + self.max_board:
            reward = -2.0  # penaliza dummy
            done = False
            info["reason"] = "accion_invalida_dummy"
            return self.current_obs, reward, done, info

        max_pasos = 1000
        pasos_recorridos = 0

        while self.pointer < len(self.log_keys) and pasos_recorridos < max_pasos:
            paso = self.log_actual[self.log_keys[self.pointer]]
            self.pointer += 1
            pasos_recorridos += 1

            accion_log = paso.get("action", "")
            vida_actual = paso.get("life", prev_obs["vida"])

            # Recompensas por acción detectada
            if accion_log == "Played card":
                if 1 <= action <= self.max_mano:
                    reward += 2
                else:
                    reward -= 2
            elif accion_log.lower() == "attacking":
                if action >= self.max_mano + 1:
                    reward += 3
                else:
                    reward -= 3
            elif accion_log == "End turn":
                if action == 0:
                    reward += 0.5
                else:
                    reward -= 0.5

            # Castigo por daño recibido
            if vida_actual < prev_obs["vida"]:
                reward -= 4

            # Fin de partida
            if accion_log in ["Wins!", "Loses"]:
                done = True
                if accion_log == "Wins!":
                    reward += 5
                    info["reason"] = "win"
                else:
                    reward = 0
                    info["reason"] = "lost"
                break

            # Castigo por atacar con carta descansada
            if action >= self.max_mano + 1:
                idx = action - (self.max_mano + 1)
                if idx < len(prev_obs["board_estado"]) and prev_obs["board_estado"][idx] == 0:
                    reward -= 1

            self._actualizar_estado(paso)

            if self._es_estado_completo():
                next_obs = self._extraer_observacion()
                break

        if pasos_recorridos >= max_pasos or self.pointer >= len(self.log_keys):
            done = True
            info["reason"] = "log_exhausted"
            reward -= 2

        if reward == 0:
            reward -= 0.1

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

    def _actualizar_estado(self, paso):
        accion = paso.get("action", "")
        if accion in ["Hand", "Current Hand", "Hand state"]:
            self.state["mano"] = paso.get("cards", [])
        elif accion in ["Board", "Current Board", "Board state"]:
            self.state["board"] = paso.get("board", [])
        elif accion in ["Trash", "Current Trash", "Trash state"]:
            self.state["trash"] = paso.get("trash", [])
        elif accion in ["Life", "Current Life", "Life state"]:
            self.state["vida"] = paso.get("life", 5)

    def _es_estado_completo(self):
        return all(k in self.state for k in ["mano", "vida", "board", "trash"])

    def _extraer_observacion(self):
        mano_ids = self.state.get("mano", [])
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

        board_cards = self.state.get("board", [])
        board_poder = np.zeros(self.max_board, dtype=np.int32)
        board_estado = np.ones(self.max_board, dtype=np.int32)
        board_tipo_blocker = np.zeros(self.max_board, dtype=np.int32)
        board_tipo_rush = np.zeros(self.max_board, dtype=np.int32)

        for i in range(min(len(board_cards), self.max_board)):
            if isinstance(board_cards[i], dict):
                card_id = board_cards[i].get("card_id")
                rested = board_cards[i].get("rested", False)
            else:
                card_id = board_cards[i]
                rested = False

            carta = self.catalogo.get(card_id, {})
            board_poder[i] = carta.get("power", 0)
            board_estado[i] = int(not rested)
            efecto = (carta.get("effect", "") or "") + (carta.get("type", "") or "")
            board_tipo_blocker[i] = int("Blocker" in efecto)
            board_tipo_rush[i] = int("Rush" in efecto)

        trash = self.state.get("trash", [])
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
            "vida": self.state.get("vida", 0)
        }
