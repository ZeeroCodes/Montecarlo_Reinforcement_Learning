from Mapa.Map import Map
from Montecarlo.Montecarlo import Montecarlo
import time
import numpy as np

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

def prueba(env):
    env.reset()
    env.plot_map()
    time.sleep(1)

    env.step(RIGHT)
    env.plot_map()
    time.sleep(1)

    env.step(RIGHT)
    env.plot_map()
    time.sleep(1)

    env.step(DOWN)
    env.plot_map()
    time.sleep(1)

    env.step(DOWN)
    env.plot_map()
    time.sleep(1)

    env.step(DOWN)
    env.plot_map()
    time.sleep(1)


def print_movements():
    time_values = list()
    with(open('total_movements_1000000.npy', 'rb') as f):
        time_values = np.load(f)

    env = Map()

    ep_count = 0

    for episode in time_values:

        mov_cont = 0
        env.reset()
        done = False

        while(not done):

            action = episode[mov_cont]
            
            position, _, done, _ = env.step(action)

            env.plot_map()

            mov_cont +=1

            if(ep_count%10000 == 0):
                time.sleep(0.5)
            else:
                time.sleep(0.01)
        
        ep_count += 1

def test_data():

    time_values = list()
    with(open('total_movements_1000000.npy', 'rb') as f):
        time_values = np.load(f)

    print(time_values[1])


# Defining main function
def main():

    episodes = 1000000
    gamma = 0.99
    epsilon = 1.0

    env = Map() 
    MCoP = Montecarlo(env, episodes/100)

    MCoP.train(episodes, gamma, epsilon)

    MCoP.save_data('YTdata.npy')

    #MCoP.load_data('YTdata.npy')

    MCoP.test_agent(True)

if __name__=="__main__":
    main()