#Version 5.1.5
#Escape by TyReesh Boedhram
#NOTE: This game must be run in Command Prompt on Windows or Terminal in Linux to work properly.
#This game will not work properly on Sololearn or in IDLE.
#Not tested on Mac OSX yet.
#Please report any bugs.

import os
import pickle
import random
import platform
import resources.tools.config as config
import resources.tools.highscore as highscore 

os.system('title Escape')
op_sys = platform.system()

class GameObject:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        #color uses the GameObject class
        #background color = x and forground color = y

def clear():
    if op_sys == 'Windows':
        os.system('cls')
    else:
        os.system('clear')
    return

def grid():
    global matrix, li
    clear()
    matrix = [[ ' ' for x in range(grid_size.x)] for y in range(grid_size.y)]
    for sublist in matrix:
        #--top and bottdom border--
        g = 0
        while g < grid_size.x:
            matrix[0][g] = '-'
            matrix[grid_size.y-1][g] = '-'
            g += 1
        #--game objects--
        matrix[door][grid_size.x-1] = '}'
        matrix[player.y][player.x] = 'i'
        matrix[guard1.y][guard1.x] = '#'
        matrix[guard2.y][guard2.x] = '#'
        matrix[guard3.y][guard3.x] = '#'
        matrix[guard4.y][guard4.x] = '#'
        if li == True:
            matrix[life_orb.y][life_orb.x] = '*'
        else:
            matrix[life_orb.y][life_orb.x] = '-'
        #--removes extra characters--
        s = str(sublist)
        s = s.replace('[', '|').replace(']', '|').replace(',','').replace('\'','')
        print (s)
    print ('Score:',score,'Lives:',life_count)
    return

#--Player Commands--
def player_input():
    global player
    Y = input()
    if Y == 'w' and player.y > 1:
        player.y -= 1
    if Y == 'a' and player.x > 0:
        player.x -= 1
    if Y == 's' and player.y < grid_size.y-2:
        player.y += 1
    if Y == 'd' and player.x < grid_size.x-1:
        player.x += 1
        if player.y != door and player.x == grid_size.x-1:
            player.x -= 1
    if Y == 'e':
        pause()
    return

#--Guard Movement AI--
def ai():
    global guards, guard1, guard2, guard3, guard4
    for guard in guards:
        direction = random.randint(1,4)
        if direction == 1 and guard.y > 1:
            guard.y -= 1
        if direction == 2 and guard.x < grid_size.x-2:
            guard.x += 1
        if direction == 3 and guard.y < grid_size.y-2:
            guard.y += 1
        if direction == 4 and guard.x > 0:
            guard.x -= 1

def new_round():
    global door, player, guards, guard1, guard2, guard3, guard4, life_orb, li
    door = random.randint(1,grid_size.y-2)
    player = GameObject(0,random.randint(1,grid_size.y-2))
    guard1 = GameObject(random.randint(2,grid_size.x-2),random.randint(1,grid_size.y-2))
    guard2 = GameObject(random.randint(2,grid_size.x-2),random.randint(1,grid_size.y-2))
    guard3 = GameObject(random.randint(2,grid_size.x-2),random.randint(1,grid_size.y-2))
    guard4 = GameObject(random.randint(2,grid_size.x-2),random.randint(1,grid_size.y-2))
    guards = [guard1, guard2, guard3, guard4]
    if random.randint(1,5) == 3:
        li = True
        life_orb = GameObject(random.randint(grid_size.x/2,grid_size.x-2),random.randint(1,grid_size.y-2))
        for guard in guards:
            if life_orb.y == guard.y and life_orb.x == guard.x:
                life_orb = GameObject(random.randint(grid_size.x/2,grid_size.x-2),random.randint(1,grid_size.y-2))
    else:
        li = False
        life_orb = GameObject(grid_size.x-1,grid_size.y-1)
    grid()
    return

def life():
    global life_count
    life_count += 1
    if life_count > 10:
        life_count = 10
    return

def life_2():
    global life_orb, li
    life_orb.y = grid_size.y-1
    life_orb.x = grid_size.x-1
    li = False
    grid()
    return

def end_round():
    global life_count
    life_count -= 1
    if life_count == 0:
        end_game()
    else:
        new_round()
    return

def end_game():
    global game, menu, sv, save_location
    if sv == True:
        os.remove(save_location)
    clear()
    highscore.update(score)
    print('Game Over\nScore =',score,'\nPress "H" to view highscores')
    a = input()
    clear()
    if a == 'H' or a == 'h':
        highscore.display()
    game = False
    menu = True
    return

def save():
    global save_location, sv
    try:
        with open(save_location, 'wb') as f:
            pickle.dump([grid_size, score, life_count, life_orb, li, player, guards, guard1, guard2, guard3, guard4, door], f)                
        clear()
        print('Save Complete')
        input()
        sv = True
    except OSError:
        print('Error: Save Failed\nInvalid file name entered')
        input()
       
def pause():
    global game, menu, save_location
    pause = True
    while pause == True:
        clear()
        print('Type the number of an option.\n\n1: Return to Game\n2: Save\n3: Main Menu')
        n = input()
        if n == '1':
            pause = False
        if n == '2':
            clear()
            print('Name this save file\nPress ENTER to use defualt name')
            save_location = 'resources/save_data/' + input() + '.pickle'
            if save_location == 'resources/save_data/.pickle':
                save_location = 'resources/save_data/svdta.pickle'
            clear()
            if os.path.isfile(save_location):
                print('WARNING: A save file with that name already exists\nSaving will overwrite the last save game\nWould you still like to save the game?\n1: Yes\n2: No')
                s = input()
                if s == '1':
                    save()
                if s == '2':
                    pass
            else:
                save()   
        if n == '3':
            pause = False
            menu = True
            game = False
    clear()
    n = False
    grid()
    return

def settings():
    global grid_size
    settings = True
    while settings == True:
        clear()
        print('Settings\n\nType the number of an option.\n\n1: Change grid length\n2: Change grid height')
        if op_sys == 'Windows':
            print('3: Change Color\n4: Back')
        if op_sys != 'Windows':
            print('3: Back')
        o = input()
        clear()
        if o == '1':
            print('Enter a new length\nCurrent length', grid_size.x)
            try:
                xnew = int(input())
            except ValueError:
                xnew = grid_size.x
            if xnew < 10:
                if xnew > 4:
                    print('WARNING: This grid size might not be playable')
                    input()
                if xnew < 5:
                    print('Entered value is to small. Length set to 10')
                    xnew = 10
                    input()
            grid_size.x = xnew
        if o == '2':
            grid_size.y -= 2
            print('Enter a new height\nCurrent height', grid_size.y)
            try:
                ynew = int(input())
            except ValueError:
                ynew = grid_size.y
            if ynew < 8:
                if ynew > 4:
                    print('WARNING: This grid size might not be playable')
                    input()
                if ynew < 5:
                    print('Entered value is to small. Height set to 8')
                    ynew = 8
                    input()
            grid_size.y = ynew + 2
        if o == '3' and op_sys == 'Windows':
            print('Pick a new color\nColors\n0 = Black       8 = Gray\n1 = Blue        9 = Light Blue\n2 = Green       A = Light Green\n3 = Aqua        B = Light Aqua\n4 = Red         C = Light Red\n5 = Purple      D = Light Purple\n6 = Yellow      E = Light Yellow\n7 = White       F = Bright White\nEntering anything other than one of the colors listed will set colors to default')
            color_list = ['1','2','3','4','5','6','7','8','9','0','a','b','c','d','e','f','A','B','C','D','E','F']
            print('Background Color')
            background = input()
            if background not in color_list:
                background = color.x
            print('Text Color')
            foreground = input()
            if foreground not in color_list:
                foreground = color.y
            if background == foreground:
                print('ERROR: Background and text color cannot be the same.\nRestoring from config file.\nPress ENTER to continue.')
                input()
                background = color.x
                foreground = color.y
            color.x = background
            color.y = foreground
            os.system('color ' + color.x + color.y)
        if o == '3' and op_sys != 'Windows':
            settings = False
        if o == '4' and op_sys == 'Windows':
            settings = False
    with open('resources/data/config.pickle', 'wb') as config_file:
                    pickle.dump([grid_size, color], config_file)
    return

#--master loop--
try:
    with open('resources/data/config.pickle', 'rb') as config_file:
        grid_size, color = pickle.load(config_file)
except FileNotFoundError:
    config.setup('resources/data/config.pickle', 'continue')
    with open('resources/data/config.pickle', 'rb') as config_file:
        grid_size, color = pickle.load(config_file)
os.system('color ' + color.x + color.y)
master = True
menu = True
game = False
while master == True:
    #--menu loop--
    while menu == True:
        clear()
        print('Type the number of an option.\n\n1: New Game\n2: Load Game\n3: Highscore\n4: Instructions\n5: Settings\n6: Quit')
        m = input()
        clear()
        if m == '1':
            menu = False
            game = True
            sv = False
            life_count = 1
            score = 0
            new_round()
        if m == '2':
            print('Type in the name of the save file.\nPress ENTER to use the defualt save file')
            save_location = 'resources/save_data/' + input() + '.pickle'
            if save_location == 'resources/save_data/.pickle':
                save_location = 'resources/save_data/svdta.pickle'
            try:
                with open(save_location, 'rb') as svdta:
                    grid_size, score, life_count, life_orb, li, player, guards, guard1, guard2, guard3, guard4, door = pickle.load(svdta)
                menu = False
                game = True
                sv = True
                grid()
            except FileNotFoundError:
                print('No save data found')
                input()
            except OSError:
                print('Error: Load Failed\nInvalid file name entered')
                input()
                
        if m == '3':
            highscore.display()
        if m == '4':
            print('Instructions\n\nGet your person (i) to the exit (})\nwithout getting caught by the guards (#).\n(*) will give you +1 life.\nUse the \'w\',\'a\',\'s\',\'d\' keys to move your character.\nUse the \'e\' key to open the pause menu.')
            input()
        if m == '5':
            settings()
        if m == '6':
            master = False
            menu = False
            game = False

    #--game loop--
    while game == True:
        n = True
        player_input()
        if n == True:
            ai()
            grid()
        if player.y == door and player.x == grid_size.x-1:
            score += 1
            new_round()
        if player.y == life_orb.y and player.x == life_orb.x:
            life()
            life_2()
        for guard in guards:
            if life_orb.y == guard.y and life_orb.x == guard.x:
                life_2()
            if player.y == guard.y and player.x == guard.x:
                end_round()
            if player.y == guard.y and player.x == guard.x-1:
                end_round()
            if player.y == guard.y and player.x == guard.x+1:
                end_round()
            if player.y == guard.y-1 and player.x == guard.x:
                end_round()
            if player.y == guard.y+1 and player.x == guard.x:
                end_round()
