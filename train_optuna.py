import gym
import torch as T
from dqnv2 import Agent
import numpy as np
import optuna
import env_registry  # si tu env lo necesita

env = gym.make("OnePieceTCG-v0")

def flatten_state(state_dict):
    return np.concatenate([np.array(v, dtype=np.float32).flatten() for v in state_dict.values()])

def objective(trial):
    gamma = trial.suggest_float("gamma", 0.90, 0.999)
    lr = trial.suggest_float("lr", 1e-5, 1e-3, log=True)
    eps_dec = trial.suggest_float("eps_dec", 1e-5, 1e-3)

    agent = Agent(
        gamma=gamma, epsilon=1.0, lr=lr,
        input_dims=[97],
        n_actions=env.action_space.n,
        eps_end=0.01,
        batch_size=64,
        eps_dec=eps_dec
    )

    scores = []
    n_games = 200  # o menos para pruebas rápidas
    for i in range(n_games):
        done = False
        observation = env.reset()
        score = 0
        while not done:
            flat_obs = flatten_state(observation)
            action = agent.choose_action(flat_obs)
            observation_, reward, done, _ = env.step(action)
            flat_obs_ = flatten_state(observation_)
            score += reward
            agent.store_transition(flat_obs, action, reward, flat_obs_, done)
            agent.learn()
            observation = observation_
        scores.append(score)

    avg_score = np.mean(scores[-50:])
    return avg_score

if __name__ == "__main__":
    study = optuna.create_study(direction="maximize")
    study.optimize(objective, n_trials=20)
    print("✅ Best hyperparameters:", study.best_params)
