import pygame

class PlayerBlock:
    def __init__(self, posX, posY, cellSize) -> None:
        self.posX = posX
        self.posY = posY
        self.cellSize = cellSize
        self.sprite = pygame.image.load("Data\Tiles\player-block.png").convert_alpha()
        self.hitBox = pygame.Rect(self.posX, self.posY, cellSize, cellSize)

    def draw(self, surface):
        surface.blit(pygame.transform.scale(self.sprite, (self.cellSize, self.cellSize)), (self.posX, self.posY)) 
