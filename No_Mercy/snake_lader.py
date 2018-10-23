import pygame, sys, time, random
import pygame.mixer as gameMusic
import os

gameMusic.pre_init(44100, 16, 2, 4096) 
pygame.init()

gameMusic.set_num_channels(5)
gameVolume = [0.3, 0.7] # 40 % for background and 70 % for sound
FPS = 60 # 60 hz game
fpsClock = pygame.time.Clock() # clock for framing rate
big = False # for show images function
startGame = 0 # For starting, pausing and ending game
# 0 for pause
# 1 for start
# 2 for end
# 3 for about game
# 4 for about developer

isSoundp = True # for sound on start screen
isSoundg = True # for sound on game screen
isDiceRolled = False # check for condition of dice roll
prevDiceNum = 0 # previous dice number
justStarted = False # game is just started
playerTurn = None # player turn
startPlayerScreenTime = time.time() # time to show player's screen
playerDirection = [1,1] # direction of both player to right

#gameDisplay = pygame.display.set_mode((900, 650), pygame.FULLSCREEN)
gameDisplay = pygame.display.set_mode((900, 650))
pygame.display.set_caption('NO MERCY!')
dice_board = pygame.image.load('dice/dice_board.png')
diceList = [ pygame.image.load('dice/dice1.png'),
             pygame.image.load('dice/dice2.png'),
             pygame.image.load('dice/dice3.png'),
             pygame.image.load('dice/dice4.png'),
             pygame.image.load('dice/dice5.png'),
             pygame.image.load('dice/dice6.png')]
             
logoList = [ pygame.image.load('logo/logo10.png'),
             pygame.image.load('logo/logo20.png'),
             pygame.image.load('logo/logo30.png'),
             pygame.image.load('logo/logo40.png'),
             pygame.image.load('logo/logo50.png'),
             pygame.image.load('logo/logo60.png'),
             pygame.image.load('logo/logo70.png'),
             pygame.image.load('logo/logo80.png'),
             pygame.image.load('logo/logo90.png'),
             pygame.image.load('logo/logo100.png'),
             pygame.image.load('logo/logo200.png')]

diceSoundList = [ 'sound/dice_sound/dice_1.wav',
                  'sound/dice_sound/dice_2.wav',
                  'sound/dice_sound/dice_3.wav',
                  'sound/dice_sound/dice_4.wav',
                  'sound/dice_sound/dice_5.wav',
                  'sound/dice_sound/dice_6.wav',]
heli_moving_image = [pygame.image.load('show_images/heli3.png'),
                     pygame.image.load('show_images/heli2.png')]
player = [
    [pygame.image.load('girl/girl1.png'),
    pygame.image.load('girl/girl2.png')],
    
    [pygame.image.load('boy/boy1.png'),
    pygame.image.load('boy/boy2.png')]]
hole_boy = [[pygame.image.load('boy/boy1.png'),
            pygame.image.load('boy/boyl25.png'),
            pygame.image.load('boy/boyl20.png'),
            pygame.image.load('boy/boyl15.png'),
            pygame.image.load('boy/boyl10.png'),
            pygame.image.load('boy/boyl5.png')],
            [pygame.image.load('boy/boy2.png'),
            pygame.image.load('boy/boyr25.png'),
            pygame.image.load('boy/boyr20.png'),
            pygame.image.load('boy/boyr15.png'),
            pygame.image.load('boy/boyr10.png'),
            pygame.image.load('boy/boyr5.png')]]

hole_girl = [[pygame.image.load('girl/girl1.png'),
            pygame.image.load('girl/girll25.png'),
            pygame.image.load('girl/girll20.png'),
            pygame.image.load('girl/girll15.png'),
            pygame.image.load('girl/girll10.png'),
            pygame.image.load('girl/girll5.png')],
            [pygame.image.load('girl/girl2.png'),
            pygame.image.load('girl/girlr25.png'),
            pygame.image.load('girl/girlr20.png'),
            pygame.image.load('girl/girlr15.png'),
            pygame.image.load('girl/girlr10.png'),
            pygame.image.load('girl/girlr5.png')]]

playerPosition = [0,0] # position of the players
playerGraphicalPosition = [[5,550],[30,550]] # actual x,y coordinate of players
playerName = ["Roman", "Shasha"]
startPosition = ((5,550),(30,550)) # for reference use of starting positions
             
# all color code for game
white = (255, 255, 255, 80)
yellow = (255, 255, 0, 80)
red = (255, 0, 0, 80)
blue = (0, 0, 255, 80)
green = (0, 255, 0, 80)
black = (0,0,0, 80)
darkgray  = ( 64,  64,  64)
gray      = (128, 128, 128)
lightgray = (212, 208, 200)
forestgreen = (34,139,34)
button = (28,28,28)
mate = (88,88,88)

paper_hole_list = [17, 54, 62, 64, 87, 93, 95, 98]
lader_hole_list = [7, 34, 19, 60, 36, 73, 75, 79]

heli_list = [2,4,9,21,28,51,72,80]
heli_pad_list = [38,14, 31, 42, 84, 67, 91, 99]

# init buttons coordinate
play_x = [350,350, 350, 350, 350]
game_x = [650, 650, 650]
play_y = [370, 420, 470, 520, 570]
game_y = [260, 310, 360]
play_name = ["Play Game", "Settings", "About Game", "Developer", "Quit"]
game_name = ["RESET", "HOME", "QUIT"]
play_hover_name = ["Play Game", "Settings", "About Game", "Developer", "Quit"]
game_hover_name = ["RESET", "HOME", "QUIT"]
randomGenerated = False # generate random number at start for player turn

# filling white color on display
gameDisplay.fill(white)

def gameName(i, j):
    # show background image
    background = pygame.image.load('background3.jpg')
    gameDisplay.blit(background, (0, 0))

    fontObj = pygame.font.Font('font/blambot_youmurderer-bb/youmurdererbb_reg.otf', 120)
    textSurface = fontObj.render("NO MERCY !!!", True, (180,0,0))
    textRect = textSurface.get_rect()
    textRect.center = (i,j)
    gameDisplay.blit(textSurface, textRect) # show game name

def fullGameName(i):
    gameName(450, 70) # showing game name

    fontObj = pygame.font.Font('font/kc-fonts_black-asylum/BlackAsylumDEMO-KCFonts.ttf', i)
    textSurface = fontObj.render("YOU ARE GOING DOWN", True, black)
    textRect = textSurface.get_rect()
    textRect.center = (450, 90+220+i)
    gameDisplay.blit(textSurface, textRect) # show full game name

def showLogo(ind, factor):
    gameDisplay.blit(logoList[ind], (325+factor, 110+factor))   
    
# START SCREEN FOR GAME
def init_game():
    gameMusic.Channel(0).play(gameMusic.Sound('sound/start_sound.wav'), loops=-1) # loading startin sound
    gameMusic.Channel(0).set_volume(gameVolume[0])
    #gameMusic1.music.play()
    for i in range(0,455, 25):
        gameName(i, 70)
        # clock & updating
        fpsClock.tick(FPS)
        pygame.display.update()
        
    for i in range(1, 35, 3):
        fullGameName(i)
        if i > 11:
            showLogo(10, 0)
        else:
            showLogo(i-1, (10-i)*5)
           
        # clock & updating
        fpsClock.tick(FPS)
        pygame.display.update()
        time.sleep(0.01)
    gameMusic.Channel(4).play(gameMusic.Sound('sound/missed.wav'))
    buttonRendering1(len(play_x))

# set all button
def buttonRendering1(i):
    gameName(450, 70) # showing game name
    fullGameName(35) # showing full game name
    showLogo(10,0) # showing game logo
    playText = pygame.font.Font('font/sansation/Sansation-BoldItalic.ttf',25)
    for ind in range(len(play_x)):
        if i != ind:
            pygame.draw.rect(gameDisplay, button , (play_x[ind], play_y[ind] , 200, 40))
            pygame.draw.rect(gameDisplay, darkgray, (play_x[ind], play_y[ind]+40, 203, 3))
            pygame.draw.rect(gameDisplay, darkgray, (play_x[ind]+200, play_y[ind], 3, 40))
            textSurf = playText.render(play_name[ind].upper(), True, white)
            textRect = textSurf.get_rect()
            textRect.center = (play_x[ind]+100, play_y[ind] + 20)
            gameDisplay.blit(textSurf, textRect)

# set all button for game screen
def buttonGameRendering1(i):
    global isSoundg
    
    isSoundg = True
    playText = pygame.font.Font('font/sansation/Sansation-BoldItalic.ttf',25)
    for ind in range(len(game_x)):
        if i != ind:
            pygame.draw.rect(gameDisplay, button , (game_x[ind], game_y[ind] , 200, 40))
            pygame.draw.rect(gameDisplay, darkgray, (game_x[ind], game_y[ind]+40, 203, 3))
            pygame.draw.rect(gameDisplay, darkgray, (game_x[ind]+200, game_y[ind], 3, 40))
            textSurf = playText.render(game_name[ind].upper(), True, white)
            textRect = textSurf.get_rect()
            textRect.center = (game_x[ind]+100, game_y[ind] + 20)
            gameDisplay.blit(textSurf, textRect)
            continue
        isSoundg = False
       
# button processing
def buttonRendering(ind, ch):
    global startGame
    global justStarted
    global startPlayerScreenTime
    global playerPosition
    global randomGenerated
    global playerGraphicalPosition
    global playerDirection
    
    playText = pygame.font.Font('font/sansation/Sansation-BoldItalic.ttf',27)
    if ch==1: # hovered buttons
        buttonRendering1(ind)
        pygame.draw.rect(gameDisplay, button , (play_x[ind], play_y[ind] , 200, 40))
        pygame.draw.rect(gameDisplay, darkgray, (play_x[ind], play_y[ind]+40, 203, 3))
        pygame.draw.rect(gameDisplay, darkgray, (play_x[ind]+200, play_y[ind], 3, 40))
        textSurf = playText.render(play_hover_name[ind].upper(), True, red)
        textRect = textSurf.get_rect()
        textRect.center = (play_x[ind]+100, play_y[ind] + 20)
        gameDisplay.blit(textSurf, textRect)
    elif ch==2: # pressed buttons
        #playing sound
        gameMusic.Channel(1).play(gameMusic.Sound('sound/button_press.wav'))
        
        buttonRendering1(ind)
        playText = pygame.font.Font('font/sansation/Sansation-BoldItalic.ttf',20)
        # play button
        pygame.draw.rect(gameDisplay, button , (play_x[ind], play_y[ind] , 200, 40))
        pygame.draw.rect(gameDisplay, gray, (play_x[ind], play_y[ind]+40, 203, 3))
        pygame.draw.rect(gameDisplay, gray, (play_x[ind]+200, play_y[ind], 3, 40))
        textSurf = playText.render(play_hover_name[ind].upper(), True, white)
        textRect = textSurf.get_rect()
        textRect.center = (play_x[ind]+100, play_y[ind] + 20)
        gameDisplay.blit(textSurf, textRect)
        if ind == 0:
            startGame = 1 # game will be started now
            justStarted = True
            playerGraphicalPosition = [[5,550],[30,550]] # actual x,y coordinate of players
            startPlayerScreenTime = time.time()
            playerPosition = [0,0] # set both player at 0
            randomGenerated = False
            playerDirection = [1,1]
            gameMusic.Channel(0).stop()
            gameMusic.Channel(1).play(gameMusic.Sound('sound/play_game.wav'))
            gameMusic.Channel(0).play(gameMusic.Sound('sound/game_sound.wav'), loops=-1)
            gameMusic.Channel(0).set_volume(gameVolume[0])
        elif ind == 2:
            startGame = 3 # show about game
        elif ind == 3:
            startGame = 4 # show about developer
        elif ind == 4:
            startGame = 2 # end the game
    #else: # all button set
        # play button

def buttonGameRendering(ind, ch):
    global startGame
    global justStarted
    global startPlayerScreenTime
    global playerPosition
    global randomGenerated
    global playerGraphicalPosition
    global playerDirection
    global isDiceRolled

    pygame.draw.rect(gameDisplay, gray,(650+180, 435, 3, 167))
    pygame.draw.rect(gameDisplay, gray, (669, 425+174, 163, 3))
    
    playText = pygame.font.Font('font/sansation/Sansation-BoldItalic.ttf',27)
    if ch==1: # hovered buttons
        buttonGameRendering1(ind)
        pygame.draw.rect(gameDisplay, button , (game_x[ind], game_y[ind] , 200, 40))
        pygame.draw.rect(gameDisplay, darkgray, (game_x[ind], game_y[ind]+40, 203, 3))
        pygame.draw.rect(gameDisplay, darkgray, (game_x[ind]+200, game_y[ind], 3, 40))
        textSurf = playText.render(game_hover_name[ind].upper(), True, red)
        textRect = textSurf.get_rect()
        textRect.center = (game_x[ind]+100, game_y[ind] + 20)
        gameDisplay.blit(textSurf, textRect)
    elif ch==2: # pressed buttons
        #playing sound
        gameMusic.Channel(1).play(gameMusic.Sound('sound/button_press.wav'))
        time.sleep(0.3)
        buttonGameRendering1(ind)
        playText = pygame.font.Font('font/sansation/Sansation-BoldItalic.ttf',20)
        # play button
        pygame.draw.rect(gameDisplay, button , (game_x[ind], game_y[ind] , 200, 40))
        pygame.draw.rect(gameDisplay, gray, (game_x[ind], game_y[ind]+40, 203, 3))
        pygame.draw.rect(gameDisplay, gray, (game_x[ind]+200, game_y[ind], 3, 40))
        textSurf = playText.render(game_hover_name[ind].upper(), True, white)
        textRect = textSurf.get_rect()
        textRect.center = (game_x[ind]+100, game_y[ind] + 20)
        gameDisplay.blit(textSurf, textRect)
        if ind == 0:
            startGame = 1 # game will be started now
            justStarted = True
            startPlayerScreenTime = time.time()
            playerPosition = [0,0] # set both player at 0
            randomGenerated = False
            playerDirection = [1,1]
            playerGraphicalPosition = [[5,550],[30,550]] # actual x,y coordinate of players
            gameMusic.Channel(0).stop()
            gameMusic.Channel(1).play(gameMusic.Sound('sound/play_game.wav'))
            gameMusic.Channel(0).play(gameMusic.Sound('sound/game_sound.wav'), loops=-1)
            gameMusic.Channel(0).set_volume(gameVolume[0])
        elif ind == 1:
            startGame = 0 # start screen
            gameMusic.Channel(0).play(gameMusic.Sound('sound/start_sound.wav'), loops=-1)
            gameMusic.Channel(0).set_volume(gameVolume[0])
        elif ind ==2:
            startGame = 2 # game end
            
          
# show images
def showImages(heliMoved):
    global big
    heli,pad = None, None
    hole, ladHole = None, None
    heli_moved = pygame.image.load('show_images/hole1.png')

    heli = pygame.image.load('show_images/heli1.png')
    pad = pygame.image.load('show_images/pad1.png')
        
    # setting hole and hole with lader
    hole = pygame.image.load('show_images/paper_hole1.png')
    ladHole =  pygame.image.load('show_images/lader_hole1.png')
    
    # at 1,4,9,28,21,51,72,80-helicopter
    i = 0
    
    tile = pygame.Surface((50, 50), pygame.SRCALPHA)
    tile.fill(red)
    gameDisplay.blit(tile, (60+5+55, 550))
    if i != heliMoved:
        gameDisplay.blit(heli, (60+5+55, 550)) # at 1
    else:
        gameDisplay.blit(heli_moved, (60+5+55, 550)) # at 1
    i += 1
    
    tile = pygame.Surface((50, 50), pygame.SRCALPHA)
    tile.fill(red)
    gameDisplay.blit(tile, (230, 550))
    if i != heliMoved:
        gameDisplay.blit(heli, (230, 550)) # at 4
    else:
        gameDisplay.blit(heli_moved, (230, 550)) # at 4

    i += 1
    tile = pygame.Surface((50, 50), pygame.SRCALPHA)
    tile.fill(red)
    gameDisplay.blit(tile, (505, 550))
    if i != heliMoved:
        gameDisplay.blit(heli, (505, 550)) # at 9
    else:
        gameDisplay.blit(heli_moved, (505, 550)) # at 9
        
    i+=1
    tile = pygame.Surface((50, 50), pygame.SRCALPHA)
    tile.fill(red)
    gameDisplay.blit(tile, (60+5, 440))
    if i != heliMoved:
        gameDisplay.blit(heli, (60+5, 440)) # at 21
    else:
        gameDisplay.blit(heli_moved, (60+5, 440)) # at 21
        
    i +=1
    tile = pygame.Surface((50, 50), pygame.SRCALPHA)
    tile.fill(red)
    gameDisplay.blit(tile, (450, 440))
    if i != heliMoved:
        gameDisplay.blit(heli, (450, 440)) # at 28
    else:
        gameDisplay.blit(heli_moved, (450, 440)) # at 28
        
    i+= 1
    tile = pygame.Surface((50, 50), pygame.SRCALPHA)
    tile.fill(red)
    gameDisplay.blit(tile, (560, 275))
    if i != heliMoved:
        gameDisplay.blit(heli, (560, 275)) # at 51
    else:
        gameDisplay.blit(heli_moved, (560, 275)) # at 51
        
    i+=1
    tile = pygame.Surface((50, 50), pygame.SRCALPHA)
    tile.fill(red)
    gameDisplay.blit(tile, (505, 165))
    if i != heliMoved:
        gameDisplay.blit(heli, (505, 165)) # at 72
    else:
        gameDisplay.blit(heli_moved, (505, 165)) # at 72
        
    i += 1
    tile = pygame.Surface((50, 50), pygame.SRCALPHA)
    tile.fill(red)
    gameDisplay.blit(tile, (60+5, 165))
    if i != heliMoved:
        gameDisplay.blit(heli, (60+5, 165)) # at 80
    else:
        gameDisplay.blit(heli_moved, (60+5, 165)) # at 80

    # at 14, 31, 38, 42, 67, 84, 91, 99- helipad
    gameDisplay.blit(pad, (345+50, 495)) # at 14
    gameDisplay.blit(pad, (560, 440-55)) # at 31
    gameDisplay.blit(pad, (230-55, 440-55)) # at 38
    gameDisplay.blit(pad, (60+60, 440-110)) # at 42
    gameDisplay.blit(pad, (345+50, 165+55)) # at 67
    gameDisplay.blit(pad, (230, 165-55)) # at 84
    gameDisplay.blit(pad, (560, 165-110)) # at 91
    gameDisplay.blit(pad, (60+60, 165-110)) # at 99

    # at 17, 54, 62, 64, 87, 93, 95, 98 - paper hole
    gameDisplay.blit(hole, (225, 550-60)) # at 17
    gameDisplay.blit(hole, (345+50-5, 275-5)) # at 54
    gameDisplay.blit(hole, (60+60-5, 165+55-5)) # at 62
    gameDisplay.blit(hole, (225, 165+55-5)) # at 64
    gameDisplay.blit(hole, (345+50-5, 165-55-5)) # at 87
    gameDisplay.blit(hole, (450-5, 165-110-5)) # at 93
    gameDisplay.blit(hole, (345-10, 165-110-5)) # at 95
    gameDisplay.blit(hole, (230-55-5, 165-110-5)) # at 98

    # at 7,19,34, 36, 60, 73, 75, 79 - lader hole
    gameDisplay.blit(ladHole, (345+50, 550)) # at 7
    gameDisplay.blit(ladHole, (60+60, 495)) # at 19
    gameDisplay.blit(ladHole, (345+50, 440-55)) # at 34
    gameDisplay.blit(ladHole, (225+55,440-55)) # at 36
    gameDisplay.blit(ladHole, (60+5, 275)) # at 60
    gameDisplay.blit(ladHole, (450, 165)) # at 73
    gameDisplay.blit(ladHole, (345-5, 165)) # at 75
    gameDisplay.blit(ladHole, (120, 165)) # at 79

    big = not big

def showLogoGame():
    # show logo image
    background = pygame.image.load('logo/logo200.png')
    gameDisplay.blit(background, (630, 70)) # change 100 with 5

    fontObj = pygame.font.Font('font/blambot_youmurderer-bb/youmurdererbb_reg.otf', 60)
    textSurface = fontObj.render("NO MERCY!", True, red)
    textRect = textSurface.get_rect()
    textRect.center = (300, 25)
    gameDisplay.blit(textSurface, textRect) # show number on board

def showDice(role):
    global prevDiceNum
    global isDiceRolled
    if role:
        gameMusic.Channel(1).play(gameMusic.Sound('sound/button_press.wav'))
        prevDiceNum = random.randint(0,5) # generate random number from 0 to 5
        rollDiceTime = time.time()
        isDiceRolled = True # dice is rolled
        i = 0 # index at 0
        gameMusic.Channel(2).play(gameMusic.Sound('sound/dice_roll.wav'), loops=-1)
        while True:
            gameDisplay.blit(dice_board, (650, 425)) # show dice board
            gameDisplay.blit(diceList[i%6], (710, 475)) # show dice in dice board
            i += 1
            # clock & updating
            
            fpsClock.tick(60)
            pygame.display.update()
            time.sleep(0.08)
            endDiceTime = time.time()
            if (endDiceTime - rollDiceTime) >= 1:
                break
        gameDisplay.blit(dice_board, (650, 425)) # show dice board
        gameDisplay.blit(diceList[prevDiceNum], (710, 475)) # show dice in dice board
        gameMusic.Channel(2).stop()
        gameMusic.Channel(2).play(gameMusic.Sound(diceSoundList[prevDiceNum]))
    else:
        gameDisplay.blit(dice_board, (650, 425)) # show dice board 350 with 450
        gameDisplay.blit(diceList[prevDiceNum], (710, 475)) # 450 with 500 show dice in dice board
        
def standingPlayer(atPlace):
    #checking for player 1 "mahi"
    if atPlace[0] == -1:
        gameDisplay.blit(player[1][playerDirection[1]], (playerGraphicalPosition[1][0], playerGraphicalPosition[1][1])) # girl at position
    elif atPlace[1] == -1:
        gameDisplay.blit(player[0][playerDirection[0]], (playerGraphicalPosition[0][0], playerGraphicalPosition[0][1])) # girl at position
    else:
        # show both player at static position
        gameDisplay.blit(player[0][playerDirection[0]], (playerGraphicalPosition[0][0], playerGraphicalPosition[0][1])) # girl at position
        gameDisplay.blit(player[1][playerDirection[1]], (playerGraphicalPosition[1][0], playerGraphicalPosition[1][1])) # boy at position

def updatePlayerScore():
    gameDisplay.blit(player[0][1], (400, 605)) # girl at position
    gameDisplay.blit(player[1][1], (200, 605)) # boy at position

    fontObj = pygame.font.Font('font/sansation/Sansation-BoldItalic.ttf', 30)
    textSurface = fontObj.render(" -> " + str(playerPosition[1]), True, white, black)
    textRect = textSurface.get_rect()
    textRect.center = (300, 625)
    gameDisplay.blit(textSurface, textRect) # show number on board

    textSurface = fontObj.render(" -> " + str(playerPosition[0]), True, white, black)
    textRect = textSurface.get_rect()
    textRect.center = (500, 625)
    gameDisplay.blit(textSurface, textRect) # show number on board

# Print snake lader board
def showBoard(atPlace, buttonInd, buttonStatus, heliPosition=len(heli_list)):
    global big

    # show background image
    background = pygame.image.load('background1.jpg')
    gameDisplay.blit(background, (0,0))
    # show home image
    home = pygame.image.load('home1.png')
    gameDisplay.blit(home, (5, 475))
    # show logo image
    showLogoGame()
    # show dice
    showDice(False)
    # updating score of player
    updatePlayerScore()

    gameDisplay.blit(pygame.image.load('mate1.jpg'), (60,50))
    #pygame.draw.rect(gameDisplay, black, (60, 50, 555, 555)) # background mate
    number = 1
    for y in range(500+50, 4+50, -55):
        for x in range(5+60, 550+60, 55):
            if number%3 == 1:
                tile = pygame.Surface((50, 50), pygame.SRCALPHA)
                tile.fill(yellow)
                gameDisplay.blit(tile, (x,y))
            elif number%3 == 2:
                tile = pygame.Surface((50, 50), pygame.SRCALPHA)
                tile.fill(green)
                gameDisplay.blit(tile, (x,y))
            else:
                tile = pygame.Surface((50, 50), pygame.SRCALPHA)
                tile.fill(red)
                gameDisplay.blit(tile, (x,y))
            number += 1
        number+= 1
    pygame.draw.rect(gameDisplay, yellow, (2+60, 500+47, 53, 53))
    pygame.draw.rect(gameDisplay, red, (3+60, 3+50 , 53, 53))
    
    showImages(heliPosition)
    # finishing image
    finish = pygame.image.load('show_images/finish1.png')
    gameDisplay.blit(finish, (60+5, 50+5))
    
    # setting number on the board
    left = False # direction of moving
    for i in range(1, 11):
        left = not left
        for j in range(1, 11):
            col = j
            if left:
                col = 11 - j
                
            add1, add2 = 60, 50
            line1, line2 = i*5, col*5
            sq1, sq2 = (i-1)*50, (col-1)*50
            
            x, y = add1+line1+sq1, add2+line2+sq2
            
            if (((10-i)*10) + j) in paper_hole_list+lader_hole_list+heli_list+heli_pad_list+[100]:
                continue
            if (((10-i)*10) + j) == 1:
                fontObj = pygame.font.Font('font/sansation/Sansation-BoldItalic.ttf', 15)
                textSurface = fontObj.render("START", True, black)
                textRect = textSurface.get_rect()
                textRect.center = (y+30, x+10)
                gameDisplay.blit(textSurface, textRect) # show number on board
            
            fontObj = pygame.font.Font('font/sansation/Sansation-BoldItalic.ttf', 20)
            textSurface = fontObj.render(str(((10-i)*10) + j), True, black)
            textRect = textSurface.get_rect()
            textRect.center = (y+25, x+25)
            gameDisplay.blit(textSurface, textRect) # show number on board

    #show player at position after generating the board on screen
    standingPlayer(atPlace)
    
    # show button
    if buttonStatus == 0:
        buttonGameRendering1(len(game_x))
    else:
        buttonGameRendering(buttonInd, buttonStatus)
        
# helicopter encountered
def helicopterMove():
    global playerPosition
    global playerGraphicalPosition
    global playerDirection

    atPlace = None
    if playerTurn == 0:
        atPlace = (-1, 1)
    else:
        atPlace = (1, -1)

    x_cor = playerGraphicalPosition[playerTurn][0] # x position of player
    y_cor = playerGraphicalPosition[playerTurn][1] # y position of player
    heli_position = heli_pad_list[heli_list.index(playerPosition[playerTurn])]
    y_mov = heli_position//10
    x_mov = heli_position- (y_mov*10)
    if (y_mov+1)%2 == 0:
        x_mov = 11 - x_mov
    final_x = startPosition[playerTurn][0] + (55 * x_mov) # final x position of helicopter
    final_y = startPosition[playerTurn][1] - (55 * y_mov) # final y position of helicopter
    playerDirection[playerTurn] = 1
    if ((heli_position//10)+1)%2 == 0:
        playerDirection[playerTurn] = 0
        
    # sound for helicopter to channel 3
    gameMusic.Channel(3).play(gameMusic.Sound('sound/heli_sound.wav'), loops=-1)
    heli = None
    if final_x < x_cor:
        for hori in range(x_cor, final_x-1, -15):
            showBoard(atPlace,len(game_x), 0, heli_list.index(playerPosition[playerTurn])) # showing board
            heli = pygame.image.load('show_images/heli3.png')
            gameDisplay.blit(heli, (hori,y_cor)) # showing player on board
            # for exit from game
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # ending game
                    pygame.quit()
                    sys.exit()
            # clock & updating
            fpsClock.tick(FPS)
            pygame.display.update()
    else:
        for hori in range(x_cor, final_x+1, 15):
            showBoard(atPlace,len(game_x), 0, heli_list.index(playerPosition[playerTurn])) # showing board
            heli = pygame.image.load('show_images/heli2.png')
            gameDisplay.blit(heli, (hori,y_cor)) # showing player on board
            # for exit from game
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # ending game
                    pygame.quit()
                    sys.exit()
            # clock & updating
            fpsClock.tick(FPS)
            pygame.display.update()
            
    for up in range(y_cor, final_y-1, -15):
        heli = heli_moving_image[playerDirection[playerTurn]]
        showBoard(atPlace,len(game_x), 0, heli_list.index(playerPosition[playerTurn])) # showing board
        gameDisplay.blit(heli, (final_x,up)) # showing player on board
        # for exit from game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # ending game
                pygame.quit()
                sys.exit()
        # clock & updating
        fpsClock.tick(FPS)
        pygame.display.update()

    # shutting down the heli sound
    gameMusic.Channel(3).stop()
    
    playerGraphicalPosition[playerTurn][0] = final_x
    playerGraphicalPosition[playerTurn][1] = final_y
    playerPosition[playerTurn] = heli_position
    
# player encounter with hole
def holeEncountered():
    global playerTurn
    global playerPosition
    global playerGraphicalPosition
    global playerDirection

    atPlace = None
    if playerTurn == 0:
        atPlace = (-1, 1)
    else:
        atPlace = (1, -1)

    x_cor = playerGraphicalPosition[playerTurn][0] # x position of player
    y_cor = playerGraphicalPosition[playerTurn][1] # y position of player
    final_position = lader_hole_list[paper_hole_list.index(playerPosition[playerTurn])]

    print(final_position) # final position for debugging
    
    y_mov = final_position//10
    x_mov = final_position - (y_mov*10)
    if (y_mov+1)%2 == 0:
        x_mov = 11 - x_mov
    if x_mov == 0:
        x_mov = 1
    final_x = startPosition[playerTurn][0] + (55 * x_mov) # final x position of helicopter
    final_y = startPosition[playerTurn][1] - (55 * y_mov) # final y position of helicopter
    # getting direction of player
    playerDirection[playerTurn] = 1
    if ((final_position//10)+1)%2 == 0:
        playerDirection[playerTurn] = 0
    sound_scream  = 'sound/boy_scream.wav'
    listImages = hole_boy[playerDirection[playerTurn]]
    if playerTurn == 0:
        listImages = hole_girl[playerDirection[playerTurn]]
        sound_scream = 'sound/girl_scream.wav'

    # sound for scream to channel 3
    gameMusic.Channel(3).play(gameMusic.Sound(sound_scream))
    gameMusic.Channel(3).set_volume(gameVolume[0])
    
    for index, image in enumerate(listImages):
        showBoard(atPlace,len(game_x), 0) # showing board
        gameDisplay.blit(image, (x_cor+25-((6-index)*5),y_cor+25-((6-index)*5))) # showing player on board
        # for exit from game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # ending game
                pygame.quit()
                sys.exit()
        # clock & updating
        time.sleep(0.1)
        fpsClock.tick(FPS)
        pygame.display.update()

    for image in listImages[::-1]:
        showBoard(atPlace,len(game_x), 0) # showing board
        gameDisplay.blit(image, (final_x+25-(index*5),final_y+25-(index*5))) # showing player on board
        # for exit from game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # ending game
                pygame.quit()
                sys.exit()
        # clock & updating
        time.sleep(0.1)
        fpsClock.tick(FPS)
        pygame.display.update()
    gameMusic.Channel(4).play(gameMusic.Sound('sound/missed.wav'))
    
    playerGraphicalPosition[playerTurn][0] = final_x
    playerGraphicalPosition[playerTurn][1] = final_y
    playerPosition[playerTurn] = final_position
    
# move player to next position
def playerMove(diceCount):
    global playerTurn
    global playerPosition
    global playerGraphicalPosition
    global playerDirection

    if (playerPosition[playerTurn] == 0) and (diceCount+1 not in [1,6]):
        # sound for laugh player to channel 4
        gameMusic.Channel(4).play(gameMusic.Sound('sound/laugh.wav'))
        if playerTurn == 0:
            playerTurn = 1
        else:
            playerTurn = 0
        return
    
    if playerPosition[playerTurn]+diceCount+1 > 100:
        # sound for laugh player to channel 4
        gameMusic.Channel(4).play(gameMusic.Sound('sound/laugh.wav'))
        if playerTurn == 0:
            playerTurn = 1
        else:
            playerTurn = 0
        return
    
    atPlace = None
    if playerTurn == 0:
        atPlace = (-1, 1)
    else:
        atPlace = (1, -1)

    # sound for walking player to channel 3
    gameMusic.Channel(3).play(gameMusic.Sound('sound/walking.wav'), loops=-1)
    
    for i in range(diceCount+1):
        x_cor = playerGraphicalPosition[playerTurn][0] # x position of player
        y_cor = playerGraphicalPosition[playerTurn][1] # y position of player
        position = playerPosition[playerTurn] # player actual position till yet
        direction = 1
        if ((position//10)+1)%2 == 0:
            direction = 0
        playerDirection[playerTurn] = direction
        x_move = True
        if ((position%10) == 0) and (position != 0):
            x_move = False
            
        if x_move:
            if direction == 1:
                for move in range(x_cor, x_cor+56, 15):
                    showBoard(atPlace,len(game_x), 0) # showing board
                    gameDisplay.blit(player[playerTurn][direction], (move,y_cor)) # showing player on board
                    # for exit from game
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            print('exit from system')
                    # clock & updating
                    fpsClock.tick(FPS)
                    pygame.display.update()
                    
                playerGraphicalPosition[playerTurn][0] += 55 # updating x position of player
            else:
                for move in range(x_cor, x_cor-56, -15):
                    showBoard(atPlace,len(game_x), 0) # showing board
                    gameDisplay.blit(player[playerTurn][direction], (move,y_cor)) # showing player on board
                    # for exit from game
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            # ending game
                            pygame.quit()
                            sys.exit()
                    # clock & updating
                    fpsClock.tick(FPS)
                    pygame.display.update()
                    
                playerGraphicalPosition[playerTurn][0] -= 55 # updating x position of player
        else:
            for move in range(y_cor, y_cor-51,-15):
                showBoard(atPlace,len(game_x), 0) # showing board
                gameDisplay.blit(player[playerTurn][direction], (x_cor,move)) # showing player on board
                # for exit from game
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        # ending game
                        pygame.quit()
                        sys.exit()
                # clock & updating
                fpsClock.tick(FPS)
                pygame.display.update()
            playerGraphicalPosition[playerTurn][1] -= 55 # updating y position of player
            
        playerPosition[playerTurn] += 1

    # switch off sound for walking
    gameMusic.Channel(3).stop()

    if playerPosition[playerTurn] == 100: # game won by current player
        gameMusic.Channel(3).play(gameMusic.Sound('sound/at100.wav'))
        gameFinished()
        
    if playerPosition[playerTurn] in heli_list:
        helicopterMove()
    if playerPosition[playerTurn] in paper_hole_list:
        holeEncountered()
    if playerTurn == 0:
        playerTurn = 1
    else:
        playerTurn = 0
                
def gameFinished():
    global playerTurn
    global randomGenerated
    
    pygame.draw.rect(gameDisplay, black, (135, 90, 425, 220))
    pygame.draw.rect(gameDisplay, forestgreen, (145, 100, 405, 200))

    # showing player's description on board
    fontObj = pygame.font.Font('font/sansation/Sansation-BoldItalic.ttf', 30)
    textSurface = fontObj.render("Game won by difference of {}".format(abs(playerPosition[0]-playerPosition[1])), True, white)
    textRect = textSurface.get_rect()
    textRect.center = (350, 120)
    gameDisplay.blit(textSurface, textRect)

    # showing player's image and player name
    gameDisplay.blit(player[playerTurn][1], (190,160))
    fontObj = pygame.font.Font('font/sansation/Sansation-BoldItalic.ttf', 20)
    textSurface = fontObj.render(" {} is the winner.".format(playerName[0]), True, white)
    textRect = textSurface.get_rect()
    textRect.center = (400, 175)
    gameDisplay.blit(textSurface, textRect)
    
    turnString = "No Mercy next time!"

    textSurface = fontObj.render(turnString, True, white)
    textRect = textSurface.get_rect()
    textRect.center = (350, 250)
    gameDisplay.blit(textSurface, textRect)
    startTime = time.time()
    while True:
        # for exit from game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # ending game
                pygame.quit()
                sys.exit()
        endTime = time.time()
        if endTime - startTime >= 4:
            break
        # clock & updating
        fpsClock.tick(FPS)
        pygame.display.update()

    buttonGameRendering(0, 2) # calling for reset

#started screen for player
def playerStartScreen():
    global playerTurn
    global randomGenerated
    
    pygame.draw.rect(gameDisplay, black, (140, 90, 420, 220))
    pygame.draw.rect(gameDisplay, mate, (150, 100, 400, 200))

    # showing player's description on board
    fontObj = pygame.font.Font('font/sansation/Sansation-BoldItalic.ttf', 30)
    textSurface = fontObj.render("Player's Description", True, white)
    textRect = textSurface.get_rect()
    textRect.center = (350, 120)
    gameDisplay.blit(textSurface, textRect)

    # showing player's image and player name
    gameDisplay.blit(player[0][1], (190,160))
    fontObj = pygame.font.Font('font/sansation/Sansation-BoldItalic.ttf', 20)
    textSurface = fontObj.render(playerName[0], True, white)
    textRect = textSurface.get_rect()
    textRect.center = (250, 175)
    gameDisplay.blit(textSurface, textRect)
    
    gameDisplay.blit(player[1][1], (360, 160))
    textSurface = fontObj.render(playerName[1], True, white)
    textRect = textSurface.get_rect()
    textRect.center = (420, 175)
    gameDisplay.blit(textSurface, textRect)

    if not randomGenerated:
        playerTurn = random.randint(0,1) # generate random number between 0 & 1
        randomGenerated = True
    turnString = "I selecting {} to roll the dice first!".format(playerName[playerTurn])

    textSurface = fontObj.render(turnString, True, white)
    textRect = textSurface.get_rect()
    textRect.center = (350, 250)
    gameDisplay.blit(textSurface, textRect)

# about developer information
def aboutDeveloper():
    about_developer = [
        'This game is developed by Rahul Dangi from JK Lakshmipat University Jaipur,',
'India. Game Theme is selected by Amit Bohra and Design idea is given by Vikas Mishra from JK',
'Lakshmipat University Jaipur, India.',
'',
'For any query, please email us on rdsquare144@gmail.com',
        '',
'or',
        '',
'for to see my other projects like Mitra (Python), TicTacToe (QT with C++), Proxy Server etc.',
'Please visit me on github using below link',
'',
'https://github.com/rdsquare',
'',
'Thanks for downloading this game.',
]
    
    # show background image
    background = pygame.image.load('background2.jpg')
    gameDisplay.blit(background, (0, 0))

    # showing game name
    fontObj = pygame.font.Font('font/FFF-Tusj/FFF_Tusj.ttf', 60)
    textSurface = fontObj.render("NO MERCY!", True, red)
    textRect = textSurface.get_rect()
    textRect.center = (455,55)
    gameDisplay.blit(textSurface, textRect) # show game name

    start_with = 300
    for index, line in enumerate(about_developer):
        fontObj = pygame.font.Font('font/sansation/Sansation-Regular.ttf',20)
        textSurface = fontObj.render(line, True, black, white)
        textRect = textSurface.get_rect()
        textRect.center = ((100+800)/2, 150+(index*25))
        gameDisplay.blit(textSurface, textRect) # show full game name
        
    playText = pygame.font.Font('font/sansation/Sansation-BoldItalic.ttf',30)
    pygame.draw.rect(gameDisplay, button , (680, 580 , 200, 40))
    pygame.draw.rect(gameDisplay, darkgray, (680, 580+40, 203, 3))
    pygame.draw.rect(gameDisplay, darkgray, (680+200, 580, 3, 40))
    textSurf = playText.render("Back", True, red)
    textRect = textSurf.get_rect()
    textRect.center = (680+100, 580 + 20)
    gameDisplay.blit(textSurf, textRect)
    
# show game information
def aboutGame():
    
    about_game = [
    'NO MERCY is a simple game which is extended and animated horror version of',
    'snake & ladder game. You can download its source code from github by visiting',
    'below link -',
    '',
    'https://github.com/rdsquare/NO-MERCY-game-in-Python',
    '',
    'This game is designed for entertainment purpose only and it used images freely',
    'available on internet (as it is not a proprietary game).',
    '',
    'Copyright (C) 2018  Rahul Dangi',
    '',
    'JK Lakshmipat University Jaipur, India',
    '',
    'for any kind of feedback or suggestion, please mail me on rdsquare144@gmail.com.',
    '',
    'This program is free software: you can redistribute it and/or modify',
    'it under the terms of the GNU General Public License as published by',
    'the Free Software Foundation, either version 3 of the License, or',
    '(at your option) any later version.',
    '',
    'This program is distributed in the hope that it will be useful,',
    'but WITHOUT ANY WARRANTY; without even the implied warranty of',
    'MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the',
    'GNU General Public License for more details.',
    ]
    
    # show background image
    background = pygame.image.load('background2.jpg')
    gameDisplay.blit(background, (0, 0))

    # showing game name
    fontObj = pygame.font.Font('font/FFF-Tusj/FFF_Tusj.ttf', 60)
    textSurface = fontObj.render("NO MERCY!", True, red)
    textRect = textSurface.get_rect()
    textRect.center = (455,55)
    gameDisplay.blit(textSurface, textRect) # show game name
    
    # making background board
    #pygame.draw.rect(gameDisplay, black, (50, 100, 770, 470))
    #pygame.draw.rect(gameDisplay, mate, (60, 110, 750, 450))
    
    start_with = 300
    for index, line in enumerate(about_game):
        fontObj = pygame.font.Font('font/sansation/Sansation-Regular.ttf',18)
        textSurface = fontObj.render(line, True, black, white)
        textRect = textSurface.get_rect()
        textRect.center = ((60+750)/2, 120+(index*20))
        gameDisplay.blit(textSurface, textRect) # show full game name
        
    playText = pygame.font.Font('font/sansation/Sansation-BoldItalic.ttf',30)
    pygame.draw.rect(gameDisplay, button , (680, 580 , 200, 40))
    pygame.draw.rect(gameDisplay, darkgray, (680, 580+40, 203, 3))
    pygame.draw.rect(gameDisplay, darkgray, (680+200, 580, 3, 40))
    textSurf = playText.render("Back", True, red)
    textRect = textSurf.get_rect()
    textRect.center = (680+100, 580 + 20)
    gameDisplay.blit(textSurf, textRect)
    
start_time = time.time() # to initialize the board

init_game() # initializing the start window of game

while startGame != 2:
    # if dice is already rolled
    if isDiceRolled:
        playerMove(prevDiceNum) # move player to rolled dice position
        isDiceRolled = False
        continue
    # drawing button for startin window
    if startGame == 0:
        isRender = True
        buttonInd = None
        mouse = pygame.mouse.get_pos() # getting mouse position
        for ind in range(len(play_x)):
            if (play_x[ind]+200 > mouse[0] > play_x[ind]) and \
               (play_y[ind]+40 > mouse[1] > play_y[ind]):
                buttonRendering(ind, 1)
                isRender = False
                if isSoundp:
                    gameMusic.Channel(1).play(gameMusic.Sound('sound/tick.wav'))
                    isSoundp = not isSoundp
                break
        if isRender:
            buttonRendering1(len(play_x))
            isSoundp = True

    gameButtonValue = 0
    gameButtonInd = -1

    if startGame == 1:
        buttonInd = None
        mouse = pygame.mouse.get_pos() # getting mouse position
        for ind in range(len(game_x)):
            if (game_x[ind]+200 > mouse[0] > game_x[ind]) and \
               (game_y[ind]+40 > mouse[1] > game_y[ind]):
                gameButtonValue = 1
                gameButtonInd = ind
                if isSoundg:
                    gameMusic.Channel(1).play(gameMusic.Sound('sound/tick.wav'))
                break
            
    if startGame == 1: # for dice board animation
        pygame.draw.rect(gameDisplay, gray,(650+180, 435, 3, 167))
        pygame.draw.rect(gameDisplay, gray, (669, 425+174, 163, 3))
    
    # for exit from game
    for event in pygame.event.get():
        mouse = pygame.mouse.get_pos() # getting mouse position
        if ((650+200 > mouse[0] > 650) and \
               (425+200 > mouse[1] > 425)) and (startGame == 1):
            playText = pygame.font.Font('font/sansation/Sansation-BoldItalic.ttf',20)
            textSurf = playText.render("Click on dice to roll!", True, red)
            textRect = textSurf.get_rect()
            textRect.center = (650+100, 420)
            gameDisplay.blit(textSurf, textRect)
        if event.type == pygame.QUIT:
            startGame = 2 # call for end the game
        elif (event.type == pygame.MOUSEBUTTONDOWN) and (startGame == 0):
            for ind in range(len(play_x)):
                if (play_x[ind]+200 > mouse[0] > play_x[ind]) and \
               (play_y[ind]+40 > mouse[1] > play_y[ind]):
                    buttonRendering(ind, 2)
        elif (event.type == pygame.MOUSEBUTTONDOWN) and (startGame == 1) and (not justStarted):
            for ind in range(len(game_x)):
                if (game_x[ind]+200 > mouse[0] > game_x[ind]) and \
               (game_y[ind]+40 > mouse[1] > game_y[ind]):
                    gameButtonValue=2
                    gameButtonInd = ind
            if (650+200 > mouse[0] > 650) and \
               (425+200 > mouse[1] > 425):
                showDice(True) # call for show dice or roll the dice
                #isDiceRolled = True
                pygame.draw.rect(gameDisplay, lightgray,(650+180, 435, 3, 167))
                pygame.draw.rect(gameDisplay, lightgray, (669, 425+174, 163, 3))
                pygame.display.update()
                time.sleep(0.05)
        elif (event.type == pygame.MOUSEBUTTONDOWN) and (startGame == 3):
            mouse = pygame.mouse.get_pos() # getting mouse position
            if (680+200 > mouse[0] > 680) and \
               (580+200 > mouse[1] > 580):

                #playing sound
                gameMusic.Channel(1).play(gameMusic.Sound('sound/button_press.wav'))
                
                startGame = 0 # game at init position
                
                playText = pygame.font.Font('font/sansation/Sansation-BoldItalic.ttf',30)
                pygame.draw.rect(gameDisplay, button , (680, 580 , 200, 40))
                pygame.draw.rect(gameDisplay, gray, (680, 580+40, 203, 3))
                pygame.draw.rect(gameDisplay, gray, (680+200, 580, 3, 40))
                textSurf = playText.render("Back", True, red)
                textRect = textSurf.get_rect()
                textRect.center = (680+100, 580 + 20)
                gameDisplay.blit(textSurf, textRect)

                # clock & updating
                fpsClock.tick(FPS)
                pygame.display.update()
                
        elif (event.type == pygame.MOUSEBUTTONDOWN) and (startGame == 4):
            mouse = pygame.mouse.get_pos() # getting mouse position
            if (680+200 > mouse[0] > 680) and \
               (580+200 > mouse[1] > 580):

                #playing sound
                gameMusic.Channel(1).play(gameMusic.Sound('sound/button_press.wav'))
                
                startGame = 0 # game at init position
                
                playText = pygame.font.Font('font/sansation/Sansation-BoldItalic.ttf',30)
                pygame.draw.rect(gameDisplay, button , (680, 580 , 200, 40))
                pygame.draw.rect(gameDisplay, gray, (680, 580+40, 203, 3))
                pygame.draw.rect(gameDisplay, gray, (680+200, 580, 3, 40))
                textSurf = playText.render("Back", True, red)
                textRect = textSurf.get_rect()
                textRect.center = (680+100, 580 + 20)
                gameDisplay.blit(textSurf, textRect)

                # clock & updating
                fpsClock.tick(FPS)
                pygame.display.update()
                
    if startGame == 3:
        aboutGame() # show about game
        # clock & updating
        fpsClock.tick(FPS)
        pygame.display.update()
        continue
    if startGame == 4:
        aboutDeveloper() # show about game
        # clock & updating
        fpsClock.tick(FPS)
        pygame.display.update()
        continue
    
    if startGame != 1:
        # clock & updating
        fpsClock.tick(FPS)
        pygame.display.update()
        continue
    
    end_time = time.time()
    if gameButtonInd == -1:
        if end_time - start_time >= 0.5:
            start_time = end_time
            showBoard((1,1),len(game_x), 0) # showing board
    else:
        showBoard((1,1),gameButtonInd, gameButtonValue)
        
    if justStarted:
        playerStartScreen() # started the player start screen
    if (end_time - startPlayerScreenTime) >= 3:
        justStarted = False
        
    # clock & updating
    fpsClock.tick(FPS)
    pygame.display.update()

# ending game
pygame.quit()
sys.exit()
