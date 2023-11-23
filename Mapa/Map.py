import pygame
import numpy as np
import os

MAP_WIDTH = 20
MAP_HEIGHT = 20

PAWN = 'O'
START_TILE = 'S'
FINISH_TILE = 'F'
EMPTY_TILE = '·'
OBSTACLE = 'X'
BARRIER = 'B'

PAWN_PATH = 'pawn.png'
START_TILE_PATH = 'start_tile.png'
FINISH_TILE_PATH = 'finish_tile.png'
EMPTY_TILE_PATH = 'empty_tile.png'
OBSTACLE_PATH = 'obstacle.png'
BARRIER_PATH = 'barrier.png'

UP_SIGN_PATH = 'up_sign.png'
RIGHT_SIGN_PATH = 'right_sign.png'
DOWN_SIGN_PATH = 'down_sign.png'
LEFT_SIGN_PATH = 'left_sign.png'

IMAGES_PATH = "Mapa"

PAWN_RADIUS = 11
TILE_SIZE = 30
TILE_WIDTH = 30
TILE_HEIGHT = 30

PAWN_DIFFERENCE = TILE_SIZE/2 - PAWN_RADIUS

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

FINISH_POSITION = (MAP_WIDTH -1, MAP_HEIGHT-1)

FONT_SIZE = 16
FONT_DIFFERENCE = 8

# --> j
# |
# V i

BASE_MAP = np.array([   ['S', '·', '·', '·', '·', '·', '·', 'X', '·', 'X', '·', '·', '·', 'X', '·', '·', '·', '·', '·', '·'],
                        ['·', '·', '·', '·', 'B', '·', '·', 'X', '·', 'X', '·', 'X', '·', 'X', 'X', 'X', '·', 'X', '·', 'X'],
                        ['·', '·', 'X', 'X', 'X', '·', '·', 'X', '·', '·', '·', 'X', 'X', 'X', '·', 'X', '·', 'X', '·', '·'],
                        ['·', '·', 'B', '·', '·', '·', '·', 'X', '·', '·', 'X', '·', '·', 'X', '·', 'B', 'B', 'X', 'X', '·'],
                        ['·', '·', '·', '·', '·', '·', '·', 'X', '·', 'X', '·', '·', '·', '·', 'X', '·', '·', 'X', '·', '·'],
                        ['·', 'X', 'X', 'X', '·', 'X', '·', 'X', '·', '·', '·', 'X', 'X', '·', 'X', '·', 'X', 'X', '·', 'X'],
                        ['·', 'X', '·', '·', '·', 'X', '·', 'X', '·', '·', 'X', 'B', 'X', '·', 'X', '·', 'X', 'X', '·', '·'],
                        ['·', 'X', 'B', '·', '·', 'X', 'X', 'X', '·', '·', 'X', '·', '·', '·', 'X', '·', 'X', 'X', 'X', '·'],
                        ['·', 'X', '·', '·', '·', '·', 'B', 'B', '·', '·', 'X', '·', '·', 'X', '·', '·', 'X', 'X', '·', '·'],
                        ['·', 'X', '·', '·', '·', '·', '·', 'B', 'X', '·', '·', 'X', 'X', '·', '·', '·', '·', 'X', '·', 'X'],
                        ['·', 'X', '·', 'X', 'X', 'X', '·', '·', '·', 'X', '·', '·', '·', '·', '·', '·', 'B', 'X', '·', '·'],
                        ['B', 'X', '·', 'X', '·', 'X', '·', 'X', '·', '·', '·', '·', '·', '·', 'B', '·', '·', 'X', 'X', '·'],
                        ['·', 'X', '·', 'X', '·', 'X', '·', 'X', '·', 'X', 'X', 'X', '·', 'X', 'X', 'X', '·', '·', 'X', '·'],
                        ['X', 'X', '·', 'X', '·', 'X', '·', 'X', '·', 'X', '·', '·', '·', '·', '·', 'X', '·', '·', '·', '·'],
                        ['·', '·', '·', 'X', '·', 'X', '·', 'X', '·', 'X', '·', 'X', 'X', 'X', '·', 'X', '·', 'X', 'B', 'X'],
                        ['X', 'X', '·', 'X', '·', 'X', '·', 'X', '·', 'X', '·', 'X', 'X', 'X', '·', 'X', '·', 'X', '·', 'X'],
                        ['·', 'X', '·', 'X', '·', 'X', '·', 'X', '·', 'X', '·', 'X', 'X', 'X', '·', 'B', '·', 'X', '·', '·'],
                        ['·', 'X', '·', 'X', '·', 'X', '·', 'X', '·', 'X', '·', 'X', 'X', 'X', '·', 'X', '·', 'X', 'X', '·'],
                        ['·', 'X', '·', 'X', '·', 'X', '·', 'X', '·', 'X', '·', 'X', 'X', 'X', '·', 'X', '·', 'X', '·', '·'],
                        ['·', '·', '·', 'X', '·', '·', '·', 'X', '·', 'X', '·', '·', 'B', '·', '·', 'X', '·', 'X', '·', 'F']    ])



class Map:



    def __init__(self):
        pygame.init()
        self.base_path = os.path.abspath(os.getcwd())
        self.screen = pygame.display.set_mode(((MAP_WIDTH+2)*TILE_WIDTH, (MAP_HEIGHT+2)*TILE_HEIGHT), display = 0)
        self.pawn_position = np.array([0,0])
        self.on_barrier = False
        self.load_images()
        self.font = pygame.font.SysFont(None, FONT_SIZE)
        self.directions = np.zeros((MAP_WIDTH, MAP_HEIGHT))
        self.plot_map()



    def set_caption(self, text):
         pygame.display.set_caption(text)



    def create_map(self):
        for i in range(MAP_WIDTH+2):
            for j in range(MAP_HEIGHT+2):
                if(i == 0 or i == MAP_WIDTH+1 or j== 0 or j == MAP_HEIGHT+1):
                    self.screen.blit(self.obstacle,(TILE_SIZE*j,TILE_SIZE*i))
                else:
                    if(BASE_MAP[i-1][j-1] == EMPTY_TILE):
                        self.screen.blit(self.empty_tile,(TILE_SIZE*j,TILE_SIZE*i))
                    elif(BASE_MAP[i-1][j-1] == OBSTACLE):
                        self.screen.blit(self.obstacle,(TILE_SIZE*j,TILE_SIZE*i))
                    elif(BASE_MAP[i-1][j-1] == BARRIER):
                        self.screen.blit(self.barrier,(TILE_SIZE*j,TILE_SIZE*i))
                    elif(BASE_MAP[i-1][j-1] == START_TILE):
                        self.screen.blit(self.start_tile,(TILE_SIZE*j,TILE_SIZE*i))
                    elif(BASE_MAP[i-1][j-1] == FINISH_TILE):
                        self.screen.blit(self.finish_tile,(TILE_SIZE*j,TILE_SIZE*i))
        
        self.screen.blit(self.pawn,(TILE_SIZE + (TILE_SIZE)*self.pawn_position[1] + PAWN_DIFFERENCE,TILE_SIZE + (TILE_SIZE)*self.pawn_position[0] + PAWN_DIFFERENCE))
        #print(f"{self.pawn_position} : {BASE_MAP[self.pawn_position[0]][self.pawn_position[1]]}")
    
    
    
    def load_images(self):
        self.pawn = pygame.image.load(os.path.join(self.base_path, IMAGES_PATH, PAWN_PATH)).convert_alpha()
        self.empty_tile = pygame.image.load(os.path.join(self.base_path, IMAGES_PATH, EMPTY_TILE_PATH)).convert_alpha()
        self.start_tile = pygame.image.load(os.path.join(self.base_path, IMAGES_PATH, START_TILE_PATH)).convert_alpha()
        self.finish_tile = pygame.image.load(os.path.join(self.base_path, IMAGES_PATH, FINISH_TILE_PATH)).convert_alpha()
        self.barrier = pygame.image.load(os.path.join(self.base_path, IMAGES_PATH, BARRIER_PATH)).convert_alpha()
        self.obstacle = pygame.image.load(os.path.join(self.base_path, IMAGES_PATH, OBSTACLE_PATH)).convert_alpha()
        self.up_sign = pygame.image.load(os.path.join(self.base_path, IMAGES_PATH, UP_SIGN_PATH)).convert_alpha()
        self.right_sign = pygame.image.load(os.path.join(self.base_path, IMAGES_PATH, RIGHT_SIGN_PATH)).convert_alpha()
        self.down_sign = pygame.image.load(os.path.join(self.base_path, IMAGES_PATH, DOWN_SIGN_PATH)).convert_alpha()
        self.left_sign = pygame.image.load(os.path.join(self.base_path, IMAGES_PATH, LEFT_SIGN_PATH)).convert_alpha()



    def plot_map(self):
        self.create_map()
        pygame.display.flip()



    def reset(self):
        self.pawn_position = (0,0)
        return self.pawn_position



    def feasible(self, state, action):
        last_position = np.copy(state)

        if action == UP:
            last_position += np.array([0, -1])
        elif action == RIGHT:
            last_position += np.array([+1, 0])
        elif action == DOWN:
            last_position += np.array([0, 1])
        elif action == LEFT:
            last_position += np.array([-1, 0])

        if(last_position[0] < 0 or last_position[0] >= MAP_WIDTH or 
           last_position[1] < 0 or last_position[1] >= MAP_HEIGHT or 
           BASE_MAP[last_position[1]][last_position[0]] == OBSTACLE):
            return False

        return True



    def is_barrier(self, state):
        if(BASE_MAP[state[0]][state[1]] == BARRIER):
            return True
        
        return False



    def step(self, action):
        last_position = np.copy(self.pawn_position)
        finished = False
        moved = True
        reward = -1

        if action == UP:
            #self.pawn_position += np.array([0, -1])
            self.pawn_position += np.array([-1, 0])
        elif action == RIGHT:
            #self.pawn_position += np.array([+1, 0])
            self.pawn_position += np.array([0, +1])
        elif action == DOWN:
            #self.pawn_position += np.array([0, 1])
            self.pawn_position += np.array([1, 0])
        elif action == LEFT:
            #self.pawn_position += np.array([-1, 0])
            self.pawn_position += np.array([0, -1])
            
        if(self.pawn_position[0] < 0 or self.pawn_position[0] >= MAP_WIDTH or 
           self.pawn_position[1] < 0 or self.pawn_position[1] >= MAP_HEIGHT or 
           BASE_MAP[self.pawn_position[0]][self.pawn_position[1]] == OBSTACLE or
           self.on_barrier):
            moved = False
            self.pawn_position = np.copy(last_position)

        if(BASE_MAP[self.pawn_position[0]][self.pawn_position[1]] == BARRIER):
            
            if(self.on_barrier):
                self.on_barrier = False
            else:
                self.on_barrier = True
                #reward = -10
        

        if((self.pawn_position == np.array([FINISH_POSITION])).all()):
            finished = True

        return self.pawn_position, reward, finished, moved
        


    def plot_action_values(self, action_values):
        for i in range(MAP_WIDTH+2):
            for j in range(MAP_HEIGHT+2):
                if(i == 0 or i == MAP_WIDTH+1 or j== 0 or j == MAP_HEIGHT+1):
                    self.screen.blit(self.obstacle,(TILE_SIZE*i,TILE_SIZE*j))
                else:
                    weight = round(max(action_values[i-1][j-1]), 1)
                    if(BASE_MAP[j-1][i-1] == EMPTY_TILE):
                        self.screen.blit(self.empty_tile,(TILE_SIZE*i,TILE_SIZE*j))
                        text = self.font.render(str(weight), True, pygame.Color(0, 0, 0))
                        self.screen.blit(text,(TILE_SIZE*i + FONT_DIFFERENCE,TILE_SIZE*j + FONT_DIFFERENCE))
                    elif(BASE_MAP[j-1][i-1] == OBSTACLE):
                        self.screen.blit(self.obstacle,(TILE_SIZE*i,TILE_SIZE*j))
                    elif(BASE_MAP[j-1][i-1] == BARRIER):
                        self.screen.blit(self.barrier,(TILE_SIZE*i,TILE_SIZE*j))
                        text = self.font.render(str(weight), True, pygame.Color(0, 0, 0))
                        self.screen.blit(text,(TILE_SIZE*i + FONT_DIFFERENCE,TILE_SIZE*j + FONT_DIFFERENCE))
                    elif(BASE_MAP[j-1][i-1] == START_TILE):
                        self.screen.blit(self.start_tile,(TILE_SIZE*i,TILE_SIZE*j))
                    elif(BASE_MAP[j-1][i-1] == FINISH_TILE):
                        self.screen.blit(self.finish_tile,(TILE_SIZE*i,TILE_SIZE*j))
        
        pygame.display.flip()



    def update_map(self,action_values):
        for i in range(MAP_WIDTH):

            for j in range(MAP_HEIGHT):
                
                if((BASE_MAP[j][i] == EMPTY_TILE) and (np.argmax(action_values[i][j]) != self.directions[i][j])):
                    self.directions[i][j] = np.argmax(action_values[i][j])



    def plot_policy2(self, action_values):

        for i in range(MAP_WIDTH+2):

            for j in range(MAP_HEIGHT+2):

                if(i == 0 or i == MAP_WIDTH+1 or j== 0 or j == MAP_HEIGHT+1):

                    pass

                else:

                    if(BASE_MAP[i-1][j-1] != OBSTACLE or BASE_MAP[i-1][j-1] != FINISH_TILE):

                        direction = np.argmax(action_values[i-1][j-1])

                        if(self.directions[i-1][j-1] != direction):

                            rect = pygame.Rect(TILE_SIZE*j,TILE_SIZE*i,TILE_SIZE, TILE_SIZE)

                            if(BASE_MAP[i-1][j-1] == EMPTY_TILE):
                                
                                self.screen.blit(self.empty_tile,(TILE_SIZE*j,TILE_SIZE*i))

                            elif(BASE_MAP[i-1][j-1] == BARRIER):

                                self.screen.blit(self.barrier,(TILE_SIZE*j,TILE_SIZE*i))

                            elif(BASE_MAP[i-1][j-1] == START_TILE):

                                self.screen.blit(self.start_tile,(TILE_SIZE*j,TILE_SIZE*i))

                            if(direction == UP):
                                self.screen.blit(self.up_sign,(TILE_SIZE*j,TILE_SIZE*i))
                            elif(direction == RIGHT):
                                self.screen.blit(self.right_sign,(TILE_SIZE*j,TILE_SIZE*i))
                            elif(direction == DOWN):
                                self.screen.blit(self.down_sign,(TILE_SIZE*j,TILE_SIZE*i))
                            elif(direction == LEFT):
                                self.screen.blit(self.left_sign,(TILE_SIZE*j,TILE_SIZE*i))

                            pygame.display.update(rect)



    def plot_policy(self, action_values):

        for i in range(MAP_WIDTH+2):

            for j in range(MAP_HEIGHT+2):

                if(i == 0 or i == MAP_WIDTH+1 or j== 0 or j == MAP_HEIGHT+1):

                    self.screen.blit(self.obstacle,(TILE_SIZE*j,TILE_SIZE*i))

                else:

                    direction = np.argmax(action_values[i-1][j-1])

                    if(BASE_MAP[i-1][j-1] == EMPTY_TILE):

                        self.screen.blit(self.empty_tile,(TILE_SIZE*j,TILE_SIZE*i))
                        if(direction == UP):
                            self.screen.blit(self.up_sign,(TILE_SIZE*j,TILE_SIZE*i))
                        elif(direction == RIGHT):
                            self.screen.blit(self.right_sign,(TILE_SIZE*j,TILE_SIZE*i))
                        elif(direction == DOWN):
                            self.screen.blit(self.down_sign,(TILE_SIZE*j,TILE_SIZE*i))
                        elif(direction == LEFT):
                            self.screen.blit(self.left_sign,(TILE_SIZE*j,TILE_SIZE*i))

                    elif(BASE_MAP[i-1][j-1] == OBSTACLE):

                        self.screen.blit(self.obstacle,(TILE_SIZE*j,TILE_SIZE*i))

                    elif(BASE_MAP[i-1][j-1] == BARRIER):

                        self.screen.blit(self.barrier,(TILE_SIZE*j,TILE_SIZE*i))
                        if(direction == UP):
                            self.screen.blit(self.up_sign,(TILE_SIZE*j,TILE_SIZE*i))
                        elif(direction == RIGHT):
                            self.screen.blit(self.right_sign,(TILE_SIZE*j,TILE_SIZE*i))
                        elif(direction == DOWN):
                            self.screen.blit(self.down_sign,(TILE_SIZE*j,TILE_SIZE*i))
                        elif(direction == LEFT):
                            self.screen.blit(self.left_sign,(TILE_SIZE*j,TILE_SIZE*i))

                    elif(BASE_MAP[i-1][j-1] == START_TILE):

                        self.screen.blit(self.start_tile,(TILE_SIZE*j,TILE_SIZE*i))
                        if(direction == UP):
                            self.screen.blit(self.up_sign,(TILE_SIZE*j,TILE_SIZE*i))
                        elif(direction == RIGHT):
                            self.screen.blit(self.right_sign,(TILE_SIZE*j,TILE_SIZE*i))
                        elif(direction == DOWN):
                            self.screen.blit(self.down_sign,(TILE_SIZE*j,TILE_SIZE*i))
                        elif(direction == LEFT):
                            self.screen.blit(self.left_sign,(TILE_SIZE*j,TILE_SIZE*i))

                    elif(BASE_MAP[i-1][j-1] == FINISH_TILE):

                        self.screen.blit(self.finish_tile,(TILE_SIZE*j,TILE_SIZE*i))

        pygame.display.flip()

    






