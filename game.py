#This game is written by Xi Zhang on May 8, 2017

import pygame, os, random, time
from pygame.locals import *

# set up the window
WINDOWWIDTH = 550
WINDOWHEIGHT = 750
HALF_WINWIDTH = int(WINDOWWIDTH / 2)
HALF_WINHEIGHT = int(WINDOWHEIGHT / 2)

# set up the colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
LIGHTBLUE = (198,228,244)
PINK = (255,221,232)

# set up the frame rate
FRAMERATE = 40

#set up the statistics and put them into a list
movespeed = 15 #moving speed of the player
initialbones = 15 #the initial amount of bones
addeachround = 2 #the amount of bones added each round
livesnum = 5 #the number of the player's lives
catelives = 5 #the number of the enemy's lives
cateaddeachround = 2 #the amount of lives added to the enemy each round
roundnum = 0 #the round number
game_start_time = 0 #the game starting time
stats = [movespeed, initialbones, addeachround, livesnum, catelives, cateaddeachround, roundnum, game_start_time]

#create a backup version of the stats
back_up_stats = [movespeed, initialbones, addeachround, livesnum, catelives, cateaddeachround, roundnum, game_start_time]


def terminate():
    """ This function is called when the user closes the window or presses ESC """
    pygame.quit()
    os._exit(1)


def drawText(text, font, surface, x, y, textcolour):
    """ Draws the text on the surface at the location specified """
    textobj = font.render(text, 1, textcolour)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)


def load_image(filename):
    """ Load an image from a file.  Return the image and corresponding rectangle """
    image = pygame.image.load(filename)
    image = image.convert_alpha()
    return image, image.get_rect()


def display_menu(windowSurface):
    """ Displays the menu """
    windowSurface.fill(LIGHTBLUE)

    #put the title
    title, title_rect = load_image("gametitle.png")
    windowSurface.blit(title,(80,230))
    
    #set up the font and height of the options
    optionFont = pygame.font.SysFont("Comic Sans MS", 32)
    optionheight = 430

    #draw the options onto the screen
    options = ['1. New Game', '2. Instruction']
    for i in range(len(options)):
        drawText(options[i], optionFont, windowSurface, 170, optionheight, BLACK)
        optionheight += 100

    #draw Doge and Cate onto the screen
    dogeimg, doge_rect = load_image('doge.png')
    cateimg, cate_rect = load_image('cate.png')
    windowSurface.blit(dogeimg,(175,100))
    windowSurface.blit(cateimg,(275,102))
    
    pygame.display.update()


def display_instruction(windowSurface):
    """Displays the instruction"""
    windowSurface.fill(PINK)

    #set to True if the user presses the back button
    backtomenu = False

    #set up the font and height of the title
    font = pygame.font.SysFont("Comic Sans MS", 28)
    height = 18

    #draw the title onto the screen
    title = "Instruction"
    drawText(title, font, windowSurface, 200, height, BLACK)

    #draw the word instructions
    smallFont = pygame.font.SysFont("Comic Sans MS", 20)
    drawText("Press 'P' to pause during the game.", smallFont, windowSurface, 100, 645, BLACK)
    drawText("Click on the back button to return to the menu.", smallFont, windowSurface, 50, 680, BLACK)
    
    #draw the instruction image 
    instruction, instruction_rect = load_image("instruction.png")
    windowSurface.blit(instruction,(65,72))
    
    #draw the back button onto the screen
    back, back_rect = load_image("backbutton.png")
    backbutton = windowSurface.blit(back,(25,15))

    pygame.display.update()

    #go back to the menu if the user clicks the back button
    while not backtomenu:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                if backbutton.collidepoint(pos):
                    backtomenu == True
                    display_menu(windowSurface)
                    return
                
                
def choose_menu(windowSurface):
    """Reacts when the user chooses different options"""
    #set to true after the user chooses the menu 
    menuchosen = False
    
    while not menuchosen:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                #if the user presses 1, start the game
                if event.key == ord('1'):
                    menuchosen = True
                #if the user presses 2, display the instruction
                elif event.key == ord('2'):
                    display_instruction(windowSurface)
            elif event.type == KEYUP:
                if event.key == K_ESCAPE:
                    terminate()


def enter_next_round(windowSurface):
    """congratulate the user when the level is completed, and enter the next round"""
    windowSurface.fill(PINK)
    font = pygame.font.SysFont("Comic Sans MS", 30)
    drawText("Congratulations!", font, windowSurface, 150, 270, BLACK)
    drawText("You will be entering the next round.", font, windowSurface, 25, 370, BLACK)
    pygame.display.update()
    pygame.time.delay(2100)

    
class Player(pygame.sprite.Sprite):
    """The player controlled by the user"""
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        #set up the image facing right
        self.image_right, self.rect = load_image("smalldoge.png")

        #set up the image facing left
        self.image_left = pygame.transform.flip(self.image_right, True, False)
        
        #By default, Doge points right
        self.image = self.image_right
 
        #set the position of Doge to the centre of the screen
        self.rect.centerx = HALF_WINWIDTH
        self.rect.centery = HALF_WINHEIGHT
       
        #set up movement variables
        self.moveLeft = False
        self.moveRight = False
        self.moveUp = False
        self.moveDown = False


    def update(self, movespeed):
        """Change the position of the player's rectangle"""
        if self.moveDown and self.rect.bottom < WINDOWHEIGHT:
            self.rect.top += movespeed
        elif self.moveUp and self.rect.top > 0:
            self.rect.top -= movespeed
        elif self.moveLeft and self.rect.left > 0:
            self.rect.left -= movespeed
            self.image = self.image_left
        elif self.moveRight and self.rect.right < WINDOWWIDTH:
            self.rect.right += movespeed
            self.image = self.image_right

          
class Cate(pygame.sprite.Sprite):
    """The enemy controlled by the computer"""
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image("smallcate.png")

        #set up the position of Cate
        self.rect.x = random.randint(150, 300)
        self.rect.y = random.randint(200, 450)

        #set up movement variables
        self.moveLeft = False
        self.moveRight = False
        self.moveUp = False
        self.moveDown = False

        #set up the options of her speed
        self.xspeed = [-2,-3,2,3]
        self.yspeed = [-2,-3,2,3]

        #pick a speed
        self.xrand = random.randint(0,3)
        self.yrand = random.randint(0,3)
    

    def update(self):
        """Change the position of the cate's rectangle"""
        #if cate goes beyond the left edge, move her right
        if self.rect.left <= 0:
            self.xrand = random.randint(2,3)
            self.yrand = random.randint(0,3)

        #if cate goes beyond the right edge, move her left
        elif self.rect.right >= 550:
            self.xrand = random.randint(0,1)
            self.yrand = random.randint(0,3)

        #if cate goes beyond the top edge, move her down
        elif self.rect.top <= 0:
            self.xrand = random.randint(0,3)
            self.yrand = random.randint(2,3)

        #if cate goes beyond the bottom edge, move her up
        elif self.rect.bottom >= 750:
            self.xrand = random.randint(0,3)
            self.yrand = random.randint(0,1)

        #set up the new speed
        self.changex = self.xspeed[self.xrand]
        self.changey = self.yspeed[self.yrand]

        #update cate's position
        self.rect.top += self.changey
        self.rect.right += self.changex

 
class Bones(pygame.sprite.Sprite):
    """Objects that attack the player"""
    def __init__(self, cateleft, catetop, cateright, catebot):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image("bone.png")

        #set up the moving speed of the bone
        self.changex = random.randint(-3,3)
        self.changey = random.randint(-3,3)
        
        #if the bone is stationary, reset the moving speed
        while self.changex == 0 and self.changey == 0:
            self.changex = random.randint(-3,3)
            self.changey = random.randint(-3,3)

        #place the bone to a random location around cate
        self.rect.x = random.randint(cateleft-60, cateright)
        self.rect.y = random.randint(catetop-60, catebot)
       

    def update(self):
        """ Change the position of the bones' rectangle """
        self.rect.top += self.changex
        self.rect.right += self.changey


class Bombs(pygame.sprite.Sprite):
    """Objects thaat attack the player"""
    def __init__(self, cateleft, catetop, cateright, catebot):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image("bomb.png")
    
        #set up the moving speed of the bomb
        self.changex = random.randint(-1,1)
        self.changey = random.randint(-1,1)
        
        #if the bomb is stationary, reset the moving speed
        while self.changex == 0 and self.changey == 0:
            self.changex = random.randint(-1,1)
            self.changey = random.randint(-1,1)

        #place the bomb to a random location around cate
        self.rect.x = random.randint(cateleft-60, cateright)
        self.rect.y = random.randint(catetop-60, catebot)

       
    def update(self):
        """ Change the position of the bomb's rectangle """
        self.rect.top += self.changex
        self.rect.right += self.changey


class Lives(pygame.sprite.Sprite):
    """The player's lives"""
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image("life.png")

        #place the lives to the upper left corner of the screen
        self.rect.x = 30
        self.rect.y = 20
        

class Fishes(pygame.sprite.Sprite):
    """The player's weapon"""
    def __init__(self, dogeleft, dogeright, dogebot, dogetop, direction):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image("fish.png")

        #if the fish is going left
        if direction == "left":
            self.rect.x = dogeleft-70
            self.rect.y = dogetop-12
            self.changex = -7
            self.changey = 0
        #if the fish is going right
        elif direction == "right":
            self.rect.x = dogeright-30
            self.rect.y = dogetop-12
            self.changex = 7
            self.changey = 0
        #if the fish is going up
        elif direction == "up":
            self.rect.x = dogeright-80
            self.rect.y = dogetop-60
            self.changex = 0
            self.changey = -7
        #if the fish is going down
        elif direction == "down":
            self.rect.x = dogeright-80
            self.rect.y = dogebot-18
            self.changex = 0
            self.changey = 7
        elif direction == " ":
            self.changex = 0
            self.changey = 0

        
    def update(self):
        """update the fishes' positions"""
        self.rect.y += self.changey
        self.rect.x += self.changex
        

class Game():
    """The main game loop"""
    def __init__(self, stats, back_up_stats):
        #initialize the stats
        self.movespeed = stats[0]
        self.initialbones = stats[1]
        self.addeachround = stats[2]
        self.livesnum = stats[3]
        self.catelives = stats[4]
        self.cateaddeachround = stats[5]
        self.roundnum = stats[6]
        self.game_start_time = stats[7]

        #set to true when the level is completed
        self.level_completed = False

        #the round number
        self.roundnum = 0

        #set to true when the user pauses the game
        self.pause = False

        #set to true when the player runs out out lives
        self.gameover = False

        #set up music
        self.play = False
        self.doge_gets_hit_sound = pygame.mixer.Sound('doge_gets_hit.wav')
        self.game_over_sound = pygame.mixer.Sound('gameover.wav')
        self.cate_gets_hit_sound = pygame.mixer.Sound('cate_gets_hit.wav')
        self.level_completed_sound = pygame.mixer.Sound('levelcomplete.wav')
        self.bomb_explosion_sound = pygame.mixer.Sound('bombexplosion.wav')
        self.bomb_explosion_sound.set_volume(0.25)
 
        #set up the invulnerable settings for doge
        self.doge_invulnerableMode = True
        self.doge_invulnerableStartTime = time.time()
        self.doge_invulntime = 2

        #initialize a player sprite group and add doge to the group
        self.doge_sprite = pygame.sprite.Group()
        self.player = Player()
        self.doge_sprite.add(self.player)
        
        #get the positions of doge
        self.dogeleft = self.player.rect.left
        self.dogetop = self.player.rect.top
        self.dogeright = self.player.rect.right
        self.dogebot = self.player.rect.bottom 

        #set up the invulnerable settings for cate
        self.cate_invulnerableMode = False
        self.cate_invulnerableStartTime = 0
        self.cate_invulntime = 2

        #initialize a cate sprite group and add cate to the group
        self.cate_sprite = pygame.sprite.Group()
        self.cate = Cate()
        self.cate_sprite.add(self.cate)

        #get the positions of cate
        cateleft = self.cate.rect.left
        catetop = self.cate.rect.top
        cateright = self.cate.rect.right
        catebot = self.cate.rect.bottom

        #initialize the fish group and add fishes
        self.fish_sprites = pygame.sprite.Group()
        direction = " "
        self.afish = Fishes(self.dogeleft, self.dogeright, self.dogebot, self.dogetop, direction)

        #initialize another sprite group and add everything else to it
        self.all_sprites = pygame.sprite.Group()

        #add bombs to the screen
        self.bomb = Bombs(cateleft, catetop, cateright, catebot)
        self.all_sprites.add(self.bomb)
   
        #add bones to the screen
        self.bones = pygame.sprite.Group()
        for i in range(self.initialbones):
            abone = Bones(cateleft, catetop, cateright, catebot)
            self.bones.add(abone)
            self.all_sprites.add(abone)
        
        #adds lives to the screen
        self.lives = []
        for x in range(self.livesnum):
            alife = Lives()
            alife.rect.x += 30*x
            self.lives.append(alife)
            self.all_sprites.add(alife)
        
            
    def process_events(self, windowSurface):
        """ Process all of the keyboard and mouse events."""
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
                
            elif event.type == KEYDOWN:
                #press left arrow key to go left
                if event.key == K_LEFT:
                    self.player.moveRight = False
                    self.player.moveLeft = True
                #press right arrow key to go right
                elif event.key == K_RIGHT:
                    self.player.moveLeft = False
                    self.player.moveRight = True
                #press up arrow key to go up
                elif event.key == K_UP:
                    self.player.moveDown = False
                    self.player.moveUp = True
                #press down arrow key to go down
                elif event.key == K_DOWN:
                    self.player.moveUp = False
                    self.player.moveDown = True
                #press 'a' key to go throw a fish leftward
                elif event.key == ord('a'):
                    direction = "left"
                    afish = Fishes(self.dogeleft, self.dogeright, self.dogebot, self.dogetop, direction)
                    self.fish_sprites.add(afish)
                    self.all_sprites.add(afish)
                #press 'd' key to go throw a fish rightward
                elif event.key == ord('d'):
                    direction = "right"
                    afish = Fishes(self.dogeleft, self.dogeright, self.dogebot, self.dogetop, direction)
                    self.fish_sprites.add(afish)
                    self.all_sprites.add(afish)
                #press 'w' key to go throw a fish upward
                elif event.key == ord('w'):
                    direction = "up"
                    afish = Fishes(self.dogeleft, self.dogeright, self.dogebot, self.dogetop, direction)
                    self.fish_sprites.add(afish)
                    self.all_sprites.add(afish)
                #press 's' key to go throw a fish downward
                elif event.key == ord('s'):
                    direction = "down"
                    afish = Fishes(self.dogeleft, self.dogeright, self.dogebot, self.dogetop, direction)
                    self.fish_sprites.add(afish)
                    self.all_sprites.add(afish)
                    
            elif event.type == KEYUP:
                if event.key == K_ESCAPE:
                    terminate()
                elif event.key == K_LEFT:
                    self.player.moveLeft = False
                elif event.key == K_RIGHT:
                    self.player.moveRight = False
                elif event.key == K_UP:
                    self.player.moveUp = False
                elif event.key == K_DOWN:
                    self.player.moveDown = False
                elif event.key == K_p:
                    #pause if the user presses "P"
                    if self.pause == False:
                        self.pause = True
                        font = pygame.font.SysFont("Comic Sans MS", 30)
                        drawText("Press 'P' again to continue", font, windowSurface, 85, 200, BLACK)
                    #continue if the user presses "P" again
                    elif self.pause == True:
                        self.pause = False
               
            elif event.type == pygame.MOUSEBUTTONDOWN:
                #click to restart the game when it is over
                if self.gameover:
                    #restore the stats
                    for x in range(len(stats)):
                        stats[x] = back_up_stats[x]
                    #record the game starting time for invulnerability
                    game_start_time = time.time()
                    stats[7] = game_start_time
                    self.__init__(stats, back_up_stats)

    
    def run_logic(self, windowSurface):
        """ This method is run each time through the frame. It updates positions and checks for collisions. """
        #turn off doge's invulnerable mode after 2 seconds
        if self.doge_invulnerableMode and time.time() - self.doge_invulnerableStartTime > self.doge_invulntime:
            self.doge_invulnerableMode = False

        #turn off cate's invulnerable mode after 2 seconds
        if self.cate_invulnerableMode and time.time() - self.cate_invulnerableStartTime > self.cate_invulntime:
            self.cate_invulnerableMode = False

        #if the player has lives
        if len(self.lives) > 0:
            #if a bone moves out of the scree, remove that bone
            for abone in self.bones:
                if abone.rect.x < 0 or abone.rect.y < 0 or abone.rect.x > 550 or abone.rect.y > 750:
                    abone.kill()
                    
                #if doge touches a bone
                if self.player.rect.colliderect(abone) or self.player.rect.colliderect(self.cate):
                    if not self.doge_invulnerableMode:
                        self.doge_gets_hit_sound.play()
                        #turn on invulnerable mode for 2 seconds
                        self.doge_invulnerableMode = True
                        self.doge_invulnerableStartTime = time.time()
                        removed = False
                        #remove a life
                        for alife in self.lives:
                            if not removed:
                                abone.kill()
                                self.lives.pop(0)
                                alife.kill()
                                removed = True
                                
            #get the positions of cate
            cateleft = self.cate.rect.left
            catetop = self.cate.rect.top
            cateright = self.cate.rect.right
            catebot = self.cate.rect.bottom

            #add new bones around cate
            if len(self.bones) <= self.initialbones:
                abone = Bones(cateleft, catetop, cateright, catebot)
                self.bones.add(abone)
                self.all_sprites.add(abone)
        
            #check for collision between cate and fish
            for afish in self.fish_sprites:
                if self.cate.rect.colliderect(afish):
                    if not self.cate_invulnerableMode:
                        self.cate_gets_hit_sound.play()
                        self.catelives-=1

                        if self.catelives > 0:
                            self.level_completed = False
                        #enter the next round when cate runs out of lives
                        else:
                            self.level_completed = True

                        #make cate invulnerable for 2 seconds   
                        self.cate_invulnerableMode = True
                        self.cate_invulnerableStartTime = time.time()

            #if a bomb moves out of the screen
            if self.bomb.rect.x < 0 or self.bomb.rect.y < 0 or self.bomb.rect.x > 550 or self.bomb.rect.y > 750:
                #remove that bomb
                self.bomb.kill()
                #then add a new bomb
                self.bomb = Bombs(cateleft, catetop, cateright, catebot) 
                self.all_sprites.add(self.bomb)
    
            #check for collision between the player and the bomb
            if self.player.rect.colliderect(self.bomb):
                if not self.doge_invulnerableMode:
                    self.bomb_explosion_sound.play()
                    self.bomb.kill()
                    for alife in self.lives:
                        alife.kill() #remove all lives from the screen
                    self.lives[:] = [] #clear the life list and game over
                    
        #if the player has no lives             
        else:
            self.gameover = True

                    
    def display_frame(self, windowSurface):
        """ Display everything to the screen for the game. """
        #when the game is not over
        if not self.gameover:
            if not self.level_completed:
                if not self.pause:
                    #draw the black background onto the screen
                    windowSurface.fill(LIGHTBLUE)
                          
                    #draw all the objects except doge onto the screen
                    self.all_sprites.draw(windowSurface)
              
                    #draw cate's lives onto the screen
                    cate_lives_display = str(self.catelives)
                    font = pygame.font.SysFont("Comic Sans MS", 26)
                    drawText(cate_lives_display, font, windowSurface, 480, 12, BLACK)

                    #make doge flash when invulnerable and draw him onto the screen
                    self.doge_flashIsOn = round(time.time(), 1) * 10 % 2 == 1
                    if not (self.doge_invulnerableMode and self.doge_flashIsOn):
                        self.doge_sprite.draw(windowSurface)

                    #make cate flash when invulnerable and draw her onto the screen
                    self.cate_flashIsOn = round(time.time(), 1) * 10 % 2 == 1
                    if not (self.cate_invulnerableMode and self.cate_flashIsOn):
                        self.cate_sprite.draw(windowSurface)

                    #get the new positions of doge
                    self.dogeleft = self.player.rect.left
                    self.dogetop = self.player.rect.top
                    self.dogeright = self.player.rect.right
                    self.dogebot = self.player.rect.bottom
                    
                    #draw the round number
                    drawText("Round "+str(stats[6]+1), font, windowSurface,250,12, BLACK)
                             
                    #update the positions of the bomb, bones and fishes
                    self.all_sprites.update()

                    #update cate's position
                    self.cate_sprite.update()

                    #update the player's position
                    self.player.update(self.movespeed)

            else:
                #change the stats, display a message, and enter the next round
                self.level_completed_sound.play()
                enter_next_round(windowSurface)

                stats[1] += stats[2]
                stats[3] = len(self.lives)
                stats[4] += stats[5]
                stats[6] += 1

                #record the game starting time for invulnerability
                game_start_time = time.time()
                stats[7] = game_start_time
                
                self.__init__(stats, back_up_stats)
                        
        #when the game is over
        else:
            #display game over screen
            if not self.play:
                self.game_over_sound.play()
                self.play = True
            windowSurface.fill(PINK)
            font = pygame.font.SysFont("Comic Sans MS", 26)
            drawText("Game over. You survived", font, windowSurface, 50, 300, BLACK)
            drawText(str(stats[6])+" round.", font, windowSurface, 365, 300, BLACK) 
            drawText("Click to to restart the game.", font, windowSurface, 50, 400, BLACK)

                 
        # draw the window onto the screen
        pygame.display.update()


def main():
    """ Mainline for the program """
    
    pygame.init()
    mainClock = pygame.time.Clock()

    windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)
    pygame.display.set_caption("Doge's Revenge")

    #initialize and play the background music
    pygame.mixer.music.load('backgroundmusic.wav')
    pygame.mixer.music.play(-1, 0.0)

    #display the menu and let the user choose
    display_menu(windowSurface)
    choose_menu(windowSurface)

    #stop the background music when the game statrs
    pygame.mixer.music.stop()

    #record the game starting time for invulnerability
    game_start_time = time.time()
    stats[7] = game_start_time

    #start the game
    game = Game(stats, back_up_stats)
    
    # run the game loop until the user quits
    while True:

        # Process events (keystrokes, mouse clicks, etc)
        game.process_events(windowSurface)

        # Update object positions
        game.run_logic(windowSurface)
        
        # Draw the current frame
        game.display_frame(windowSurface)        
        
        mainClock.tick(FRAMERATE)
        
main()
