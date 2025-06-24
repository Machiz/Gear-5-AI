import numpy as np
import tensorflow as tf
from tensorflow import keras
from keras.optimizers import Adam
from keras.models import load_model



#shape memory
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
    
#create dqn model
def build_dqn(lr, n_actions, input_dims, fc1_dims, fc2_dims):
    #layers from the model
    model = keras.Sequential([
        keras.Input(shape= input_dims),
        #keras.Input(shape = 141),
        keras.layers.Dense(fc1_dims, activation = 'relu'),
        keras.layers.Dense(fc2_dims, activation = 'relu'),
        keras.layers.Dense(n_actions, activation = None)])
    model.compile(optimizer = Adam(learning_rate = lr), loss = 'mean_squared_error')
    model.summary()
    return model

class Agent():
    
    def __init__(self, lr, gamma, n_actions, epsilon, batch_size, input_dims, 
                 epsilon_dec = 1e-3, epsion_end = 0.01, mem_size = 2000, 
                 fname = 'dqn_model.h5'):
        self.action_space =[i for i in range(n_actions)]
        self.gamma = gamma
        self.epsilon = epsilon
        self.eps_dec = epsilon_dec
        self.eps_min = epsion_end
        self.batch_size = batch_size
        self.model_file = fname
        self.memory = ReplayBuffer(mem_size, input_dims)
        self.q_eval = build_dqn(lr, n_actions, input_dims, 256, 256)
        self.q_next = build_dqn(lr, n_actions, input_dims, 256, 256)
        #print("acciones: ", n_actions)
    def store_transition(self, state, action, reward, new_state, done):
        self.memory.store_transition(state, action, reward, new_state, done)
    
    def choose_action(self, observation):
        if np.random.rand()< self.epsilon:
            action = np.random.choice(self.action_space)
        else:
            state = np.array([observation])
            states = np.array(list(states))
            action = self.q_eval.predict(state)
        return action
    #@tf.function
    def learn(self):
        
        #tf.config.run_functions_eagerly(True)
        if self.memory.mem_cntr< self.batch_size:
            return
        states, actions, rewards, states_, dones = \
            self.memory.sample_buffer(self.batch_size)
        states= np.array(list(states))
        states_ = np.array(list(states))
        print("🧪 Tipo de states:", type(states))
        print("🧪 Shape de states:", np.shape(states))
        print("🧪 Ejemplo de estado:", states[0])
        q_eval = self.q_eval.predict(states)
        q_next = self.q_eval.predict(states_)
        print(q_eval, q_next)
        q_target = np.copy(q_eval)
        batch_index = np.arrange(self.batch_size, dtype = np.int32)

        q_target[batch_index, actions] = rewards +  \
            self.gamma * np.max(q_next, axis = 1)*dones
        
        self.q_eval.train_on_batch(states, q_target)

        self.epsilon = self.epsilon - self.eps_dec if self.epsilon > \
            self.eps_min else self.eps_min

    def save_model(self):
        self.q_eval.save(self.model_file)
    
    def load_model(self):
        self.q_eval = load_model(self.model_file)