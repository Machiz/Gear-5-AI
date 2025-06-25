import gym
from dqnv2 import Agent
import matplotlib.pyplot as plt
import env_registry
from gym.spaces.utils import flatten
from gym.spaces.utils import flatten_space
import numpy as np


def flatten_state(state_dict):
    return np.concatenate([np.array(v, dtype=np.float32).flatten() for v in state_dict.values()])

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

env = gym.make("OnePieceTCG-v0")
lr = 0.0005
agent = Agent(gamma = 0.99, epsilon = 1.0, lr = lr, input_dims = [97], n_actions = env.action_space.n, eps_end=0.01, batch_size = 64)
scores, eps_history = [], []
n_games = 2000
env.reset()
for i in range(n_games):
    score = 0
    done = False
    observation = env.reset()
    
    while not done:
        flat_obs = flatten_state(observation)
        
        action = agent.choose_action(flat_obs)
        observation_, reward, done, info = env.step(action)
        flat_obs_ = flatten_state(observation_)
        score += reward
        agent.store_transition(flat_obs, action, reward, flat_obs_, done)
        agent.learn()
        observation = observation_
    scores.append(score)
    eps_history.append(agent.epsilon)

    avg_score = np.mean(scores[-100:])
    print('episode', i ,'score %.2f' %score, 'average score%.2f'%avg_score, 'epsilon %.2f' % agent.epsilon )
x = [i+1 for i in range(n_games)]
filename = 'tcg_Test.png'
filename1= 'tcg_test1.png'
plot_learning_curve(x, scores, eps_history, filename)   
