import gym
from gym import spaces
import numpy as np
import json
import os

class OnePieceReplayEnv(gym.Env):
    """
    Entorno Gym personalizado para el juego One Piece Card Game,
    basado en un archivo de logs JSON con datos reales de partida.
    Este entorno reproduce las jugadas secuenciales del log y permite
    al agente aprender de ambas perspectivas (ambos jugadores).
    """

    def __init__(self, log_path):
        """
        Inicializa el entorno leyendo el archivo de log JSON.
        - log_path: ruta al archivo de log con la partida.
        """
        super(OnePieceReplayEnv, self).__init__()

        # Carga el log (diccionario de eventos secuenciales)
        with open(log_path, "r", encoding="utf-8") as f:
            self.log_data = json.load(f)

        # Ordenamos las claves del log (ej: log-001, log-002...)
        self.sorted_keys = sorted(self.log_data.keys())
        self.pointer = 0  # Apunta al paso actual del replay

        # Definimos un máximo de 10 cartas en mano, -1 representa un slot vacío
        self.max_mano = 10
        self.num_cartas_posibles = 200  # Asumimos 200 cartas distintas (ajustable)

        # Observación: dict con la mano, vida y dones del jugador actual
        self.observation_space = spaces.Dict({
            "mano": spaces.Box(low=-1, high=self.num_cartas_posibles - 1,
                               shape=(self.max_mano,), dtype=np.int32),
            "vida": spaces.Discrete(6),
            "don": spaces.Discrete(11)
        })

        # Acción: pasar (0), jugar cartas 1-10 (slot de la mano)
        self.action_space = spaces.Discrete(self.max_mano + 1)

        # Estado interno (se inicializa al hacer reset)
        self.current_obs = None
        self.done = False

    def reset(self):
        """
        Reinicia el entorno al primer paso del log.
        Devuelve la primera observación.
        """
        self.pointer = 0
        self.done = False

        # Avanza hasta el primer estado válido
        while self.pointer < len(self.sorted_keys):
            step_data = self.log_data[self.sorted_keys[self.pointer]]
            if self._es_paso_de_jugador(step_data):
                self.current_obs = self._extraer_observacion(step_data)
                return self.current_obs
            self.pointer += 1

        raise Exception("No se encontró un paso de jugador válido en el log.")

    def step(self, action):
        """
        Recibe una acción del agente, y devuelve la tupla:
        (obs_siguiente, recompensa, done, info)
        """
        if self.pointer >= len(self.sorted_keys):
            self.done = True
            return self.current_obs, 0.0, self.done, {}

        paso_actual = self.log_data[self.sorted_keys[self.pointer]]

        # Asignamos una recompensa según si la acción coincide con la del jugador humano
        accion_real = self._extraer_accion(paso_actual)
        reward = 1.0 if action == accion_real else -0.1

        # ¿Terminó la partida? Asumimos que el campo `game_result` marca eso
        self.done = paso_actual.get("game_result", "") in ["win", "lose"]

        # Avanzamos al siguiente paso que sea de un jugador (ignoramos cosas como draws)
        self.pointer += 1
        while self.pointer < len(self.sorted_keys):
            siguiente = self.log_data[self.sorted_keys[self.pointer]]
            if self._es_paso_de_jugador(siguiente):
                self.current_obs = self._extraer_observacion(siguiente)
                break
            self.pointer += 1

        return self.current_obs, reward, self.done, {}

    def render(self, mode="human"):
        """
        Representación simple por consola del estado actual.
        """
        print("Vida:", self.current_obs["vida"])
        print("Don:", self.current_obs["don"])
        print("Mano:", self.current_obs["mano"])

    ### Métodos auxiliares

    def _es_paso_de_jugador(self, paso):
        """
        Determina si este paso corresponde a una acción jugable (no shuffle, draw, etc.)
        """
        return "mano" in paso and "vida" in paso and "don" in paso

    def _extraer_observacion(self, paso):
        """
        Extrae la observación desde un paso del log.
        Retorna un diccionario compatible con `observation_space`.
        """
        mano = paso.get("mano", [])
        # Convertimos a array de longitud fija
        mano_array = np.full((self.max_mano,), -1, dtype=np.int32)
        for i, carta in enumerate(mano[:self.max_mano]):
            mano_array[i] = carta

        return {
            "mano": mano_array,
            "vida": paso.get("vida", 0),
            "don": paso.get("don", 0)
        }

    def _extraer_accion(self, paso):
        """
        Extrae la acción jugada en este paso. 
        Por ahora asumimos que viene como índice (0 = pasar, 1-10 jugar carta i-1).
        Este método se puede adaptar si tus logs usan nombres o descripciones.
        """
        return paso.get("action_id", 0)  # default: pasar
