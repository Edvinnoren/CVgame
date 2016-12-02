import pygame
import time
import random


pygame.init()

green = (0, 255, 0)
black = (0,0,0)
red = (255, 0, 0)
cyan = (0, 255, 255)
white = (255, 255, 255)

display_width = 800
display_height = 600

Fg = 9.82*3
FPS = 30
T = 1/FPS
laserSpeed = 50

imgHero = pygame.image.load('Hero.png')


gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('CV')

clock =  pygame.time.Clock()
font = pygame.font.SysFont(None, 25)


def text_objects(text, color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()
        
def message_to_screen(msg, color):
    textSurf, textRect = text_objects(msg,color)
    textRect.center = (display_width/2), (display_height/2)
    gameDisplay.blit(textSurf, textRect)

class creature:
    def __init__(self, ID, pos, HP, xSpeed, ySpeed):
        self.ID = ID
        self.pos = pos
        self.HP = HP
        self.xSpeed = xSpeed
        self.ySpeed = ySpeed

    def move(self, dx, dy):
        self.pos[0] = dx*xSpeed
        self.pos[1] = dy*ySpeed



class creatureFactory:
    creatureArray = []
    defPos = (100, 100)
    defHP = 100
    defxSpeed = 0
    defySpeed = 0
    defExists = True
    
    def __init__(self):
        pass
    def newCreature():
        tmp = creature(len(creatureArray), defPos, defHP, defxSpeed, defySpeed)
        creatureArray.append(tmp)
        return tmp.ID

    def creatureFromID(ID):
        if ID < 0 or ID >= len(creatureArray):
            return null
        return creatureArray(ID)    

    def creaturesInRectangle(TLC, LRC):
        ret = []
        for c in creatureArray: 
            if c.pos[0] > TLC[0] and c.pos[1] > TLC[1] and c.pos[0] < LRC[0] and c.pos[1] < LRC[1]:
                ret.append(c)
        return ret

class monster(creature):
    def __init__(self, ID, pos, noArms):
        self.ID = ID
        self.pos = pos
        self.HP = 100
        self.xSpeed = 20
        self.ySpeed = 10
        self.noArms = noArms

    def jump(self):
        self.move(0, 1)


def gameLoop():
    laserShot = False
    laser = []
    laserRight = False
    gameExit = False
    gameOver = False
    lead_y = 300
    lead_x = 300
    lead_x_change = 0
    lead_y_change = 0
    step_size = 10
    ground_level = display_height-step_size
    
    randObjectX = round(random.randrange(0, display_width-step_size)/step_size)*step_size
    randObjectY = round(random.randrange(0, display_height-step_size)/step_size)*step_size

    cf = creatureFactory()
    cf.defPos = (200, 200)
    
    
    while not gameExit:

        while gameOver == True:
            gameDisplay.fill(black)
            message_to_screen("Game over, press C to play again or Q to quit", red)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameExit = True
                    gameOver = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        gameExit = True
                        gameOver = False
                    if event.key == pygame.K_c:
                        gameLoop()

                        
## Movements on ground level
        if lead_y >= ground_level:              
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameOver = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        lead_x_change = -step_size
                        laserRight = False
                    if event.key == pygame.K_RIGHT:
                        lead_x_change = step_size
                        laserRight = True
                    if event.key == pygame.K_UP:
                        lead_y_change = -step_size        
                    if event.key == pygame.K_s:
                        laserShot = True
                        
            lead_x_change = lead_x_change*0.9
            if abs(lead_x_change) < 1:
                lead_x_change = 0  

## Movements in the air
        if lead_y < ground_level:              
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameOver = True            
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        lead_x_change = -abs(lead_x_change)
                        laserRight = False
                    if event.key == pygame.K_RIGHT:               
                        lead_x_change = abs(lead_x_change)
                        laserRight = True
                    if event.key == pygame.K_s:
                        laserShot = True 
## Laser
        
                  
## Updating position
        lead_x += lead_x_change
        lead_y += lead_y_change       
## Defining ground level
        if lead_y >= ground_level:
            lead_y = ground_level
## Gravity
        elif lead_y < ground_level:
            lead_y_change += Fg/FPS

        
        if lead_x < 0 or lead_x >= display_width or lead_y < 0:
            gameOver = True

        if lead_x == randObjectX and lead_y == randObjectY:
            randObjectX = round(random.randrange(0, display_width-step_size)/step_size)*step_size
            randObjectY = round(random.randrange(0, display_height-step_size)/step_size)*step_size 
            snakeLength += 1

        
        gameDisplay.fill(white)
        pygame.draw.rect(gameDisplay, red, [randObjectX, randObjectY, step_size, step_size])
        Hero = pygame.transform.scale2x(imgHero)

        
        gameDisplay.blit(Hero, [lead_x-20, lead_y-20])
        ##pygame.draw.rect(gameDisplay, green, [lead_x, lead_y, step_size, step_size])
        ##pygame.draw.rect(gameDisplay, cyan, [laser_x, laser_y, step_size/2, step_size/2])


##
        
        if laserShot == True:
            laser.append(lead_x)
            laser.append(lead_y)
            laserShot = False

        if len(laser) > 0:
            if laser[0] > 0 or laser[0] < display_width:
                if laserRight == True:
                    laser[0] = laser[0] + laserSpeed
                    pygame.draw.rect(gameDisplay, cyan, [laser[0], laser[1], step_size*10, step_size/3])
                if laserRight == False:
                    laser[0] = laser[0] - laserSpeed
                    pygame.draw.rect(gameDisplay, cyan, [laser[0]-step_size*30, laser[1], step_size*30, step_size/3])
            if laser[0] < 0 or laser[0] > display_width:
                del laser[0]
                del laser[0]
        

##

        pygame.display.update()

        
        clock.tick(FPS)
                         
    pygame.quit()
    quit()


gameLoop()
