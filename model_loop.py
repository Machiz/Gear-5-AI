from Training_model import Agent
import json
import os
import numpy as np
import gym
import tensorflow as tf
import matplotlib.pyplot as plt
import optcg_env
from optcg_env import OnePieceTCGEnv
def read_log_files(directory_path):
    data_list = []
    for filename in os.listdir(directory_path):
        if filename.endswith('.json'):
            file_path = os.path.join(directory_path, filename)
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                data_list.append(data)
    return data_list
def read_card_files(directory_path):
    card_list = []
    for filename in os.listdir(directory_path):
        if filename.endswith('.json'):
            file_path = os.path.join(directory_path, filename)
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                card_list.append(data)
    return card_list

catalogo = read_card_files("assets/JSON/Cards")
logs = read_log_files("assets/JSON/Battle_log")

def plot_learning_curve(x, scores, eps_history, filename):
    fig, ax1 = plt.subplots()

    color = 'tab:blue'
    ax1.set_xlabel('Episode')
    ax1.set_ylabel('Score', color=color)
    ax1.plot(x, scores, color=color, label='Score')
    ax1.tick_params(axis='y', labelcolor=color)

    # Segunda escala en el mismo gráfico para epsilon
    ax2 = ax1.twinx()
    color = 'tab:red'
    ax2.set_ylabel('Epsilon', color=color)
    ax2.plot(x, eps_history, color=color, linestyle='--', label='Epsilon')
    ax2.tick_params(axis='y', labelcolor=color)

    plt.title('Learning Curve')
    fig.tight_layout()
    plt.grid(True)

    # Guardar o mostrar la gráfica
    if filename:
        plt.savefig(filename)
    else:
        plt.show()

if __name__ == '__main__':
    tf.compat.v1.disable_eager_execution()
    env = OnePieceTCGEnv(game_logs_path='assets/JSON/Battle_log', cards_path='assets/JSON/Cards')#need explanation and correction
    lr = 0.001
    n_games = 2000
    agent = Agent(gamma = 0.99, epsilon = 1.0, lr = lr, input_dims = env.observation_space.shape, n_actions = env.action_space.n, mem_size = 1000000, batch_size = 64, epsilon_end = 0.01)
    scores = []
    eps_history = []
    for i in range(n_games):
        done = False
        score = 0
        observation = env.reset()
        while not done:
            action = agent.choose_action(observation)
            observation_, reward, done, info =  env.step(action)
            score += reward
            agent.store_transition(observation, action, reward, observation_, done)
            observation = observation_
            agent.learn()
        eps_history.append(agent.epsilon)
        scores.append(score)

        avg_score = np.mean(scores[-100:])
        print('episode: ', i, 'score %.2f' % score, 'average_score %.2f' %avg_score, 'epsilon %.2f' % agent.epsilon)

    filename = 'tcg_test.png'
    x = [i+1 for i in range(n_games)]
    plot_learning_curve(x, scores, eps_history, filename)