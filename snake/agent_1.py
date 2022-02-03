from snake_env import Snake

import random
import numpy as np
from keras import Sequential
from collections import deque
from keras.layers import Dense
import matplotlib.pyplot as plt
from keras.optimizers import Adam
from plot_script import plot_result
import time
from ra_agent import RA_agent

class DQN:
    """ Deep Q Network """
    def __init__(self, env, params):

        self.action_space = env.action_space
        self.state_space = env.state_space
        self.epsilon = params['epsilon']
        self.gamma = params['gamma']
        self.batch_size = params['batch_size']
        self.epsilon_min = params['epsilon_min']
        self.epsilon_decay = params['epsilon_decay']
        self.learning_rate = params['learning_rate']
        self.layer_sizes = params['layer_sizes']
        self.memory = deque(maxlen=2500)
        self.model = self.build_model()

    def build_model(self):
        model = Sequential()
        for i in range(len(self.layer_sizes)):
            if i == 0:
                model.add(Dense(self.layer_sizes[i], input_shape=(
                    self.state_space,), activation='relu'))
            else:
                model.add(Dense(self.layer_sizes[i], activation='relu'))
        model.add(Dense(self.action_space, activation='softmax'))
        model.compile(loss='mse', optimizer=Adam(lr=self.learning_rate))
        return model

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):

        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_space)
        act_values = self.model.predict(state)
        return np.argmax(act_values[0])

    def replay(self):

        if len(self.memory) < self.batch_size:
            return

        minibatch = random.sample(self.memory, self.batch_size)
        states = np.array([i[0] for i in minibatch])
        actions = np.array([i[1] for i in minibatch])
        rewards = np.array([i[2] for i in minibatch])
        next_states = np.array([i[3] for i in minibatch])
        dones = np.array([i[4] for i in minibatch])

        states = np.squeeze(states)
        next_states = np.squeeze(next_states)

        targets = rewards + self.gamma * \
            (np.amax(self.model.predict_on_batch(next_states), axis=1))*(1-dones)
        targets_full = self.model.predict_on_batch(states)

        ind = np.array([i for i in range(self.batch_size)])
        targets_full[[ind], [actions]] = targets

        self.model.fit(states, targets_full, epochs=1, verbose=0)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def save(self, name):
        self.model.save_weights(name)

    def load(self, name):
        self.model.load_weights(name)



def train_dqn(episode, env):
    
    sum_of_rewards = []
    agent = DQN(env, params)

    e=66
    env.seed(e)

    for e in range(episode):
        # set seed for the model
        RA= RA_agent ()
        state = env.reset()
        state = np.reshape(state, (1, env.state_space))
        score = 0
        max_steps = 10000
        #print("######################################")
        for i in range(max_steps):
            action = agent.act(state)
            # print(action)
            prev_state = state
            food_check=env.eaten_food
            ra_reward_step =RA.trace(food_check, env)
            #env.update_score()
            next_state, reward, done,_ = env.step(action)
            
            #print(env.pair)
            #env.pair=1
            #print(food_check) # fine
            
            #t_reward_ra+=t_reward_ra
            
            t_reward=reward+ra_reward_step
            #print("reward=",reward)
            #print("ra_reward_step=",ra_reward_step)
            #score = score + reward
            
            score = score + reward + ra_reward_step
            #print("score",score)
            next_state = np.reshape(next_state, (1, env.state_space))
            agent.remember(state, action, t_reward, next_state, done)
            state = next_state
            if params['batch_size'] > 1:
                agent.replay()
            if done:
                #print(f'final state before dying: {str(prev_state)}')
                print(f'episode: {e+1}/{episode}, score: {score}')
                
                
                break
        sum_of_rewards.append(score)
        # save the trained DQN model and weights to restore it later
        agent.save('final_weights.h5')
        #plot_result(sum_of_rewards)
                 
    return sum_of_rewards

# load the model and model weights from saved model to predict the next action then run the game for 10 episodes
def test_dqn(episode, env):
    score=0
    agent = DQN(env, params)
    agent.load('final_weights.h5')
    env.seed(66)
    sum_of_rewards=[]
    for e in range(episode):
        state = env.reset()
        state = np.reshape(state, (1, env.state_space))
        score = 0
        max_steps = 10000
        for i in range(max_steps):
            action = agent.act(state)
            prev_state = state
            next_state, reward, done,_ = env.step(action)
            next_state = np.reshape(next_state, (1, env.state_space))
            state = next_state
            score = score + reward
            if done:
                print(f'episode: {e+1}/{episode}, score: {score}')
                break
        sum_of_rewards.append(score)

    return sum_of_rewards



    
if __name__ == '__main__':

    params = dict()
    params['name'] = None
    params['epsilon'] = 1
    params['gamma'] = .95
    params['batch_size'] = 500
    params['epsilon_min'] = .01
    params['epsilon_decay'] = .995
    params['learning_rate'] = 0.00025
    params['layer_sizes'] = [128, 128, 128]
    train = True #change it to false to test the trained model

    results = dict()
    ep = 60
    ep_test=15

    # for batchsz in [1, 10, 100, 1000]:
    #     print(batchsz)
    #     params['batch_size'] = batchsz
    #     nm = ''
    #     params['name'] = f'Batchsize {batchsz}'
    env_infos = {'States: only walls': {'state_space': 'no body knowledge'}, 'States: direction 0 or 1': {
        'state_space': ''}, 'States: coordinates': {'state_space': 'coordinates'}, 'States: no direction': {'state_space': 'no direction'}}

    # for key in env_infos.keys():
    #     params['name'] = key
    #     env_info = env_infos[key]
    #     print(env_info)
    #     env = Snake(env_info=env_info)
    env = Snake()
    if train:
        sum_of_rewards = train_dqn(ep, env)
    else:
        # run test dqn
        sum_of_rewards = test_dqn(ep_test, env)
    print(sum_of_rewards)
        
    results[params['name']] = sum_of_rewards


    plot_result(results, direct=True, k=20)
