import gym
import torch
import torch.nn as nn
import torch.optim as optim
import random
from gym.spaces.utils import flatten
from gym.spaces.utils import flatten_space
import numpy as np
from collections import deque
import gpt_env
import env_registry
from env_registry import OnePieceTCGEnv
import matplotlib.pyplot as plt

import numpy as np
import tensorflow as tf
import keras as keras
from keras.optimizers import Adam
#from network import DeepQNetwork
#from replay_memory import ReplayBuffer
class ReplayBuffer():
    def __init__(self, max_size, input_dims):
        self.mem_size = max_size
        self.mem_cntr = 0
        self.state_memory = np.zeros((self.mem_size, *input_dims), dtype = np.float32)
        self.new_state_memory = np.zeros((self.mem_size, *input_dims), dtype=np.float32)
        self.action_memory = np.zeros(self.mem_size, dtype=np.int32)
        self.reward_memory = np.zeros(self.mem_size, dtype=np.int32)
        self.terminal_memory = np.zeros(self.mem_size, dtype=np.int32)
    def store_transition(self, state, action, reward, state_, done):
        index = self.mem_cntr % self.mem_size
        self.state_memory[index]= state
        self.new_state_memory[index] = state_
        self.reward_memory[index] = reward
        self.action_memory[index] = action
        self.terminal_memory[index] = 1-int(done)
        self.mem_cntr +=1
    
    def sample_buffer(self, batch_size):
        max_mem = min(self.mem_cntr, self.mem_size)
        batch  = np.random.choice(max_mem, batch_size, replace = False)

        states = self.state_memory[batch]
        states_ = self.new_state_memory[batch]
        rewards = self.reward_memory[batch]
        actions = self.action_memory[batch]
        terminal = self.terminal_memory[batch]

        return states, actions, rewards, states_, terminal
def build_dqn(lr, n_actions, input_dims, fc1_dims, fc2_dims):
    #layers from the model
        model = keras.Sequential()
        #keras.Input(shape= input_dims),
        #keras.Input(shape = 141),
        keras.layers.Dense(fc1_dims, activation = 'relu'),
        keras.layers.Dense(fc2_dims, activation = 'relu'),
        keras.layers.Dense(n_actions, activation = None)
        model.compile(optimizer = Adam(learning_rate = lr), loss = 'mean_squared_error')

        return model

class Agent:
    def __init__(self, gamma, epsilon, lr, n_actions, input_dims, batch_size,
                 mem_size=2000,  eps_min=0.01, eps_dec=1e-3,
                 replace=1000, fname = 'dqn_model.h5'):
        self.gamma = gamma
        self.epsilon = epsilon
        self.lr = lr
        self.n_actions = n_actions
        self.input_dims = input_dims
        self.batch_size = batch_size
        self.eps_min = eps_min
        self.eps_dec = eps_dec
        self.replace_target_cnt = replace
        self.action_space = [i for i in range(n_actions)]
        self.learn_step_counter = 0
        self.fname = fname
        self.memory = ReplayBuffer(mem_size, input_dims)
        self.q_eval = build_dqn(lr, n_actions, input_dims, 256, 256)
        self.q_next = build_dqn(lr, n_actions, input_dims, 256, 256)
    
    def save_models(self):
        self.q_eval.save(self.fname+'q_eval')
        self.q_next.save(self.fname+'q_next')
        print('... models saved successfully ...')

    def load_models(self):
        self.q_eval = keras.models.load_model(self.fname+'q_eval')
        self.q_next = keras.models.load_model(self.fname+'q_next')
        print('... models loaded successfully ...')

    def store_transition(self, state, action, reward, state_, done):
        self.memory.store_transition(state, action, reward, state_, done)

    def sample_memory(self):
        state, action, reward, new_state, done = \
                                  self.memory.sample_buffer(self.batch_size)
        states = tf.convert_to_tensor(state)
        rewards = tf.convert_to_tensor(reward)
        dones = tf.convert_to_tensor(done)
        actions = tf.convert_to_tensor(action, dtype=tf.int32)
        states_ = tf.convert_to_tensor(new_state)
        return states, actions, rewards, states_, dones

    def choose_action(self, observation):
        if np.random.random() > self.epsilon:
            state = tf.convert_to_tensor([observation])
            actions = self.q_eval(state)
            action = tf.math.argmax(actions, axis=1).numpy()[0]
        else:
            action = np.random.choice(self.action_space)
        return action

    def replace_target_network(self):
        if self.learn_step_counter % self.replace_target_cnt == 0:
            self.q_next.set_weights(self.q_eval.get_weights())

    def decrement_epsilon(self):
        self.epsilon = self.epsilon - self.eps_dec \
                           if self.epsilon > self.eps_min else self.eps_min

    def learn(self):
        if self.memory.mem_cntr < self.batch_size:
            return

        self.replace_target_network()

        states, actions, rewards, states_, dones = self.sample_memory()

        indices = tf.range(self.batch_size, dtype=tf.int32)
        print(actions.shape)
        exit()
        action_indices = tf.stack([indices, actions], axis=1)

        with tf.GradientTape() as tape:
            q_pred = tf.gather_nd(self.q_eval(states), indices=action_indices)
            q_next = self.q_next(states_)

            max_actions = tf.math.argmax(q_next, axis=1, output_type=tf.int32)
            max_action_idx = tf.stack([indices, max_actions], axis=1)

            q_target = rewards + \
                self.gamma*tf.gather_nd(q_next, indices=max_action_idx) *\
                (1 - dones.numpy())

            loss = keras.losses.MSE(q_pred, q_target)

        params = self.q_eval.trainable_variables
        grads = tape.gradient(loss, params)

        self.q_eval.optimizer.apply_gradients(zip(grads, params))

        self.learn_step_counter += 1

        self.decrement_epsilon()