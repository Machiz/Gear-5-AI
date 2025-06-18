from Training_model import Agent
import numpy as np
import env_registry
from gym.spaces.utils import flatten
from gym.spaces.utils import flatten_space
import gym
import tensorflow as tf
import matplotlib.pyplot as plt
import gpt_env

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
    iteracion =[]
    tf.compat.v1.disable_eager_execution()
    env = gym.make("OnePieceTCG-v0")
    lr = 0.00005
    n_games = 5000
    agent = Agent(gamma = 0.99, epsilon = 1.0, lr = lr, input_dims = flatten_space(env.observation_space).shape, n_actions = env.action_space.n, mem_size = 10000, batch_size = 64)
    scores = []
    eps_history = []
    for i in range(n_games):
        done = False
        score = 0
        observation = env.reset()
        while not done:
            action = agent.choose_action(observation)
            obs_, reward, done, info =  env.step(action)
            obs = flatten(env.observation_space, observation)
            obs_ = flatten(env.observation_space, obs_)
            score += reward
            agent.store_transition(obs, action, reward, obs_, done)
            obs = obs_
            agent.learn()
        eps_history.append(agent.epsilon)
        scores.append(score)

        avg_score = np.mean(scores[-100:])
        print('episode: ', i, 'score %.2f' % score, 'average_score %.2f' %avg_score, 'epsilon %.2f' % agent.epsilon)

    filename = 'tcg_test.png'
    x = [i+1 for i in range(n_games)]
    plot_learning_curve(x, scores, eps_history, filename)