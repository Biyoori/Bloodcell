import pygame
from pygame.locals import *
from player import Player
from enemy import Enemy

winWidth, winHeight = 740, 740
fps = 60

cellSize = 64

colors = {"black": (0, 0, 0),
          "white": (255, 255, 255),
          "gray": (50, 50, 50),
          "red": (200, 30, 30),
          "darkblue": (24, 20, 37)}

grid = [[1,1,1,1,1,1,1,1,1,1],
        [1,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,2,0,0,0,1],
        [1,0,1,1,1,1,1,1,1,1],
        [1,0,0,0,0,0,1,1,1,1],
        [1,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,3,3,0,0,1],
        [1,1,1,1,1,1,2,0,0,1],
        [1,1,1,1,1,1,1,1,1,1]]

def main():
    pygame.init()

    screen = pygame.display.set_mode((winWidth, winHeight))
    clock = pygame.time.Clock()
    pygame.display.set_caption("2D Puzzle")

    tile = pygame.image.load("Data\Tiles\\tile2.png").convert_alpha()
    playerBlock = pygame.image.load("Data\Tiles\player-block.png").convert_alpha()
    player = Player(8*cellSize, 2*cellSize, cellSize)

    enemyList = []

    run = True
    while run:
        clock.tick(fps)
        pygame.display.update()

        screen.fill("black")
        
        for i, row in enumerate(grid):
            for j, cell in enumerate(row):
                if cell == 1:
                    screen.blit(pygame.transform.scale(tile, (cellSize, cellSize)), (j* cellSize, i*cellSize))
                elif cell == 2:
                    screen.blit(pygame.transform.scale(playerBlock, (cellSize, cellSize)), (j* cellSize, i*cellSize)) 
                elif cell == 3:
                    pygame.draw.rect(screen, colors["darkblue"], (j * cellSize, i * cellSize, cellSize, cellSize))
                    if not any(enemy.posX == j * cellSize and enemy.posY == i * cellSize for enemy in enemyList):
                        newEnemy = Enemy(j * cellSize, i * cellSize, cellSize)
                        enemyList.append(newEnemy)
                else:
                    pygame.draw.rect(screen, colors["darkblue"], (j * cellSize, i * cellSize, cellSize, cellSize))

        for enemy in enemyList:
            enemy.draw(screen)
            enemy.update()
            player.isDeadCheck(enemy.hitBox)
            #pygame.draw.rect(screen, colors["red"], enemy.hitBox)

        player.draw(screen)
        player.update()
        player.moveUpdate(grid)
        



        for e in pygame.event.get():
            if e.type == QUIT:
                run = False
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_a:
                    player.move(-1, grid)
                elif e.key == pygame.K_d:
                    player.move(1, grid)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.move(-1, grid)
        if keys[pygame.K_RIGHT]:
            player.move(1, grid)
            

if __name__ == "__main__":
    main()