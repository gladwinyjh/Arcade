import pygame
import os


class Background():
    def __init__(self, PATH):
        self.PATH = PATH
        self.bg = pygame.image.load(self.PATH).convert_alpha()
        self.scroll = 1

    def transform(self, WIDTH, HEIGHT):
        self.bg = pygame.transform.scale(self.bg, (WIDTH, HEIGHT))
    
    def reset_scroll(self):
        self.scroll = 0


class Player():
    def __init__(self, PATH, start_x, start_y):
        self.PATH = PATH
        self.icon = pygame.image.load(PATH)
        self.x = start_x
        self.y = start_y
        self.rect = self.icon.get_rect()
    
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
        if self.y == 0 or self.y == 540:
            self.rect.x = self.x
            self.rect.y = self.y
            pygame.draw.rect(screen, (255,0,0), self.rect, 4)
        
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
        screen.blit(self.icon, (self.x + 15, self.y + 55))


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

    player = Player('images/ufo.png', 0.1*WIDTH, 0.45*HEIGHT)
    player.transform(60, 60) 
    playerY_change = 0
    
    animation_list = []
    for image in os.listdir('images/flame'):
        animation_list.append(pygame.transform.rotate(pygame.image.load('images/flame/' + image), 270))
    
    flame = Sprite(animation_list, player.x, player.y)

    running = True
    up = False
    while running:
        clock.tick(60)
        
        for i in range(2):
            screen.blit(background.bg, (i * WIDTH + background.scroll, 0))

        background.scroll -= 10

        if abs(background.scroll) > WIDTH:
            background.reset_scroll()
        
        player.draw(screen)

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
        
        if up:
            flame.x = player.x
            flame.y = player.y
            flame.animate(screen)

        pygame.display.update() 



if __name__ == '__main__':
    main()
