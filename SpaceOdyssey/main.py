import pygame
import os
import random


class Background():
    def __init__(self, PATH):
        self.bg = pygame.image.load(PATH).convert_alpha()
        self.scroll = 1

    def transform(self, WIDTH, HEIGHT):
        self.bg = pygame.transform.scale(self.bg, (WIDTH, HEIGHT))
    
    def reset_scroll(self):
        self.scroll = 0


class Player():
    def __init__(self, PATH, start_x, start_y):
        self.icon = pygame.image.load(PATH)
        self.x = start_x
        self.y = start_y
        self.rect = self.icon.get_rect()
        self.collide = False
    
    def transform(self, WIDTH, HEIGHT):
        self.icon = pygame.transform.scale(self.icon, (WIDTH, HEIGHT))
        self.rect = self.icon.get_rect()

    def set_location(self, x, y):
        self.x = x
        self.y = y

        if self.y <= 0:
            self.y = 0
        elif self.y >= 540:
            self.y = 540

    def draw(self, screen):
        # Update coordinates of rectangle, so that in the event of collision, we can just draw it out 
        self.rect.x = self.x
        self.rect.y = self.y
        screen.blit(self.icon, (self.x, self.y))


class Sprite():
    def __init__(self, spriteList, x, y):
        self.spriteList = spriteList
        self.frame = 0
        self.x = x
        self.y = y
        self.icon = self.spriteList[self.frame]
        self.last_update = pygame.time.get_ticks()

    def animate(self, screen):
        current_time = pygame.time.get_ticks()
        
        if current_time - self.last_update >= 250:
            self.frame += 1
            if self.frame > len(self.spriteList) - 1:
                self.frame = 0
        
        self.icon = self.spriteList[self.frame]
        screen.blit(self.icon, (self.x + 20, self.y + 60))


class Obstacle():
    def __init__(self, PATH, scroll):
        self.icon = pygame.image.load(PATH)
        self.scroll = scroll

    def transform(self, WIDTH, HEIGHT):
        self.icon = pygame.transform.scale(self.icon, (WIDTH, HEIGHT))
        self.radius = WIDTH/2

    def set_location(self, x, y):
        self.x = x
        self.y = y
        self.center = (x + self.radius, y + self.radius)

    def draw(self, screen):
        self.circle = pygame.draw.circle(screen, (0,0,0), self.center, self.radius, 1)
        screen.blit(self.icon, (self.x, self.y))


def main():
    pygame.init()
    clock = pygame.time.Clock()

    HEIGHT = 600
    WIDTH = 1000

    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    background = Background('images/background.jpg')
    background.transform(WIDTH, HEIGHT)
    background.reset_scroll()

    pygame.display.set_caption("Space Odyssey")
    game_icon = pygame.image.load('images/controller.png')
    pygame.display.set_icon(game_icon)
    
    # Create ufo player
    player = Player('images/ufo.png', 0.1*WIDTH, 0.45*HEIGHT)
    player.transform(70, 60) 
    # Initial change in height == 7. Meaning 'Gravity' applied the moment game is started
    playerY_change = 7
    
    # Create sprite for ufo jetpack
    animation_list = []
    for image in os.listdir('images/flame'):
        animation_list.append(pygame.transform.rotate(pygame.image.load('images/flame/' + image), 270))
    
    flame = Sprite(animation_list, player.x, player.y)
    
    # Create obstacle
    obstacles_list = []
    obs_SIZE = 175

    for obs in os.listdir('images/obstacles'):
        obstacle = Obstacle('images/obstacles/' + obs, -8)
        obstacle.transform(obs_SIZE, obs_SIZE)
        obstacles_list.append(obstacle)
   
    running = True
    up = False

    font = pygame.font.SysFont(None, 50)
    score = 0
    GAME_START = False

    while running:
        clock.tick(60)

        for i in range(2):
            screen.blit(background.bg, (i * WIDTH + background.scroll, 0))
        
       # Distance score based on travel
        score += 0.02
        # Display score remove decimals using int casting, then cast to string for display
        img = font.render(str(int(score)), True, (255,255,255))
        screen.blit(img, (0,0))

        player.draw(screen)
        
        # Check if game has started
        while not GAME_START:
            # Display 'press any key to start'
            start_font = pygame.font.SysFont(None, 35)
            start = start_font.render('PRESS ANY KEY TO START', True, (255,255,255))
            screen.blit(start, (WIDTH/2 - 300, HEIGHT/2))
            # Display rest of contents including this start message
            pygame.display.update()

            for event in pygame.event.get():
                # A key is pressed, exit the loop
                if event.type == pygame.KEYDOWN:
                    GAME_START = True

                if event.type == pygame.QUIT:
                    # User quits the game
                    running = False
                    GAME_START = True
        
        timePoint = pygame.time.get_ticks()

        # To be worked on: how obstacles are positioned and how they move
        while timePoint % 10 == 0:
            obstacle = obstacles_list[random.randrange(0, len(obstacles_list))]
        obstacle.set_location(WIDTH + obstacle.scroll + 10, HEIGHT/2)
        obstacle.draw(screen)
        obstacle.scroll -= 8
 
        # Set obstacle and background scroll to be the same so that they move together
        background.scroll -= 8

        if abs(background.scroll) > WIDTH:
            background.reset_scroll()
        
        # Change when to load a new obstacle, with random height between a range
        #for obstacle in obstacles_list:
        #    if obstacle.x < -obs_SIZE:
        #        obstacle.y = random.randrange(0+10, (HEIGHT-obs_SIZE)-10)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                up = True
                playerY_change = -7

            if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                up = False
                playerY_change = 7
        
        player.y += playerY_change
        player.set_location(player.x, player.y)
        
        # If player collided into obstacle or player collided with the top or bottom of screen
        # Draw red rectangle around it and set collide to True
        # Collision is not perfect now because using colliderect
        #for obstacle in obstacles_list:
        #    if player.rect.colliderect(obstacle.circle) or player.y == 0 or player.y == 540:
        #        pygame.draw.rect(screen, (255,0,0), player.rect, 4)
        #        player.collide = True
        #        break
        
        # If moving up, activate jetpack sprite
        if up:
            flame.x = player.x
            flame.y = player.y
            flame.animate(screen)

        pygame.display.update() 
        
        # If collided, freeze for 1 sec then end the program
        if player.collide:
            pygame.time.wait(1000)
            running = False


if __name__ == '__main__':
    main()
