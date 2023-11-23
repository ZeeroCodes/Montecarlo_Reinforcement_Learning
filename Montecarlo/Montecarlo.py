import numpy as np
import time
from datetime import datetime
from Mapa.Map import Map
import matplotlib.pyplot as plt

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

class Montecarlo:

    def __init__(self, env = None, episode_log = 20, show_graphs = True):
        self.set_episode_log(episode_log)
        self.env = env
        self.reset()
        self.total_episodes_steps = list()
        self.total_episodes_time = list()
        self.total_movements = list()


    def set_episode_log(self, episode_log):
        self.episode_log = episode_log

    def set_action_values(self, action_values):
        self.action_values = action_values

    def set_environment(self, env):
        self.env = env

    def get_episode_log(self):
        return self.episode_log

    def get_action_values(self):
        return self.action_values
    
    def get_environment(self):
        return self.env

    def reset(self):
        self.action_values = np.zeros(shape=(20, 20, 4))

    def is_inside(self,state):
        if(state[0] < 0 or state[1] < 0 or state[0] >= 20 or state[1] >= 20):
            return False
        return True
    
    def is_barrier(self, state):
        return self.env.is_barrier(state)

    def get_feasible_actions(self, state):
        state_t = np.copy(state)
        feasible_actions = []


        if(self.is_inside(state_t + np.array([0, -1])) and not self.is_barrier(state_t + np.array([0, -1]))):
            feasible_actions.append(UP)
        if(self.is_inside(state_t + np.array([1, 0])) and not self.is_barrier(state_t + np.array([1, 0]))):
            feasible_actions.append(RIGHT)
        if(self.is_inside(state_t + np.array([0, 1])) and not self.is_barrier(state_t + np.array([0, 1]))):
            feasible_actions.append(DOWN)
        if(self.is_inside(state_t + np.array([-1, 0])) and not self.is_barrier(state_t + np.array([-1, 0]))):
            feasible_actions.append(LEFT)

        if(feasible_actions == []):
            return [0]
        
        return feasible_actions

    def policyMCoP(self, state, epsilon = 0.2):

        if np.random.random() < epsilon:
            return np.random.choice(4)
        else:
            av = self.action_values[state[0]][state[1]]
            return np.random.choice(np.flatnonzero(av == av.max()))
        
    

    def save_training_data(self, number):

        file_name = "total_training_steps_" + number + ".npy"

        with(open(file_name, 'wb') as f):
            np.save(f, self.total_episodes_steps)

        file_name = "total_training_time_" + number + ".npy"

        with(open(file_name, 'wb') as f):
            np.save(f, self.total_episodes_time)

        file_name = "total_movements_" + number + ".npy"

        with(open(file_name, 'wb') as f):
            np.save(f, self.total_episodes_time)


        
    def MCoP(self, episodes, gamma=0.99, e=0.2):
        epsilon = e
        sa_returns = {}
        
        cont_episodes = 0

        best_mov = 10000000
        worst_mov = 0

        start = time.time()
        end = time.time()

        self.env.reset()
        self.env.set_caption(f"Initial Policy")
        self.env.plot_policy(self.action_values)
    
        for episode in range(1, episodes + 1):

            state = self.env.reset()
            done = False
            transitions = []
            steps = 0
            movements = []

            while not done:                
             
                action = self.policyMCoP(state, epsilon)
                movements.append(action)
                next_state, reward, done, _ = self.env.step(action)
  
                steps += 1

                transitions.append([state, action, reward])
                state = np.copy(next_state)

            return_G = 0

            for state_t, action_t, reward_t in reversed(transitions):

                return_G = reward_t + gamma * return_G
                state_t = tuple(state_t)

                if not (state_t, action_t) in sa_returns:
                    sa_returns[(state_t, action_t)] = [0, 0]

                sa_returns[(state_t, action_t)][0] += return_G
                sa_returns[(state_t, action_t)][1] += 1

            for key in sa_returns.keys():
                state_t = key[0]
                action_t = key[1]
                self.action_values[state_t[0]][state_t[1]][action_t] = sa_returns[(state_t, action_t)][0]/sa_returns[(state_t, action_t)][1]
            
            len_transitions = len(transitions)

            cont_episodes += len_transitions
            best_mov = min(len_transitions, best_mov)
            worst_mov = max(len_transitions, worst_mov)

            if(episode % self.episode_log == 0):

                end = time.time()

                print(f"EPISODE {episode}")
                print(f"EPSILON {epsilon}")
                print(f"{time.asctime(time.localtime())}")
                print(f"MEDIUM AVERAGE OF LAST {self.episode_log} EPISODES: {round(cont_episodes/self.episode_log)}")
                print(f"BEST TRAJECTORY OF LAST {self.episode_log} EPISODES: {best_mov}")
                print(f"WORST TRAJECTORY OF LAST {self.episode_log} EPISODES: {worst_mov}")
                print(f"DURATION OF LAST {self.episode_log} EPISODES: {round(end - start, 1)} SECONDS")
                print(f"AVERAGE DURATION OF LAST {self.episode_log} EPISODES: {round((end - start)/self.episode_log, 5)} SECONDS")
                print()

                self.total_episodes_time.append(round((end - start), 1))
                self.total_episodes_steps.append((best_mov, round(cont_episodes/self.episode_log), worst_mov))

                start = time.time()

                epsilon = round(epsilon - 0.005, 3)
                best_mov = 10000000
                worst_mov = 0
                cont_episodes = 0
            
            self.env.set_caption(f"Episode {episode}")
            self.env.plot_policy2(self.action_values)
            #time.sleep(0.5)

        return True



    def train(self, episodes, gamma = 0.99, epsilon = 0.):
        self.MCoP(episodes, gamma, epsilon)



    def plot_policy(self):
        self.env.plot_policy(self.action_values)



    def save_data(self, file_name = None):

        if file_name == None:
            now = datetime.now()
            file_name = now.strftime("%d%m%Y_%H:%M:%s" + ".npy")

        with(open(file_name, 'wb') as f):
            np.save(f, self.action_values)



    def load_data(self, file_name):
        
        with(open(file_name, 'rb') as f):
            self.action_values = np.load(f)



    def test_agent(self, real_path = False):
        
        done = False
        position = (0,0)
        self.env.reset()
        movs = 0

        self.env.plot_policy(self.action_values)
        time.sleep(5)

        while(not done):
            action = 0
            if(real_path):
                action = np.argmax(self.action_values[position[0]][position[1]]) 
            else:
                action = self.policyMCoP(position, 0.5)
            
            position, _, done, _ = self.env.step(action)
            movs += 1
            self.env.plot_map()

            time.sleep(0.5)

        print(f"Total movements: {movs}")       