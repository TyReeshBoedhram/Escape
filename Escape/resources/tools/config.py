#This tool is used to generate the default config file
#This tool can be used to override an existing config file

import os
import pickle

class GameObject:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        #color uses the Game_Object class
        #background color = x and forground color = y
  
def setup(location):
    print('Generating config.pickle ...')
    grid_size = GameObject(16, 10)
    color = GameObject('0', '7')
    with open(location, 'wb') as file:
        pickle.dump([grid_size, color], file)
    print('Finished generating config.pickle')
    print('Press ENTER to exit')
    input()
    return

if __name__ == '__main__':
    setup('../data/config.pickle')
