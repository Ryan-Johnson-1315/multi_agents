# To give credit where credit is do, this code is based off of the works found at the following sites:
#   https://keon.io/deep-q-learning/
#   https://github.com/keon/deep-q-learning/blob/master/ddqn.py
#   https://sergioskar.github.io/Deep_Q_Learning/
# I have taken the information from both the sites and combined it into my representation below.

import numpy as np
import keras
from keras.models import Sequential, load_model
from keras.layers import Dense, Conv2D, LSTM, Dropout, AlphaDropout, PReLU
from keras.optimizers import Adam, RMSprop, Nadam
from keras import backend as Kpredict
import tensorflow as tf

from collections import deque
import random
from tqdm import tqdm

"""
    Notes:
        state_size, is the input to the model
        
"""

class DQNAgent:
    def __init__(self, state_size, num_agenst):
        self._state_size = state_size
        self._num_agents = num_agenst
        self._memory = deque(maxlen=2000)
        self._gamma = 0.95    # discount rate
        self._epsilon = 1.0  # exploration rate
        self._epsilon_min = 0.1
        self._epsilon_decay = 0.995
        self._learning_rate = 0.001
        self._batch_size = 32
        self._model = self._build_model()
        self._target_model = self._build_model()
        self._update_target_model()
        self._count = 0
        self._is_finished = False
        self._loss = None


    def _build_model(self):
        model = Sequential()
        model.add(Dense(40, input_dim=self._state_size, activation='selu'))
        model.add(Dense(40, activation='selu'))
        model.add(Dense(40, activation='selu'))
        model.add(Dense(self._num_agents, activation='linear'))
        model.compile(optimizer=Adam(lr=self._learning_rate), loss='mse')

        """
            TODO: Ask Zach about different modes of compiling the model
        """

        # model.compile(optimizer=Nadam(lr=self._learning_rate), loss='mse')

        # # model.add(Dense(self._num_agents, activation='softmax'))
        # # model.compile(loss='mse', optimizer=Adam(lr=self._learning_rate))
        # model.compile(loss='binary_crossentropy', optimizer=Nadam(lr=self._learning_rate))
        return model

    def _update_target_model(self):
        # copy weights from model to target_model
        self._target_model.set_weights(self._model.get_weights())

    def remember(self, state, action, reward, next_state, done):
        self._memory.append((state, action, reward, next_state, done))

    def predict(self, state): # used to be act
        action = None
        if np.random.rand() <= self._epsilon:
            action = random.randrange(self._num_agents)

        else:
            act_values = self._model.predict(state)
            action = np.argmax(act_values[0])

        return action

    def fit(self, batch_size):  # used to be replay
        # DQN
        minibatch = random.sample(self._memory, batch_size)
        for state, action, reward, next_state, done in minibatch:
            target = reward
            if not done:
                Q_next = self._model.predict(next_state)[0]
                target = (reward + self._gamma *np.amax(Q_next))
        
            target_f = self._model.predict(state)
            target_f[0][action] = target
            #train network
            self._model.fit(state, target_f, epochs=1, verbose=0)

        self._decay_epsilon()

    def _decay_epsilon(self):
        self._count += 1
        # if self._count % 20 == 0 and self._epsilon > self._epsilon_min:
        if self._epsilon > self._epsilon_min:
            self._epsilon *= self._epsilon_decay

    def load(self, name, use_weights=True):
        if use_weights:
            self._model.load_weights(name)
        else:
            self._model = load_model(name)

    def save(self, name):
        self._model.save_weights(name.replace('.h5', '-weights.h5'))
        self._model.save(name)
