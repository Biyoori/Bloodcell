import pygame


class Enemy:
    def __init__(self, posX, posY, cellSize) -> None:
        self.posX = posX
        self.posY = posY
        self.cellSize = cellSize
        
        self.idleSprite = pygame.image.load("Data/Sprites/Enemy/EnemyIdle.png").convert_alpha()
        self.idleFrames = self.loadFrames(self.idleSprite, 0, 4)
        self.prevAnim = self.idleFrames
        self.activeAnim = self.animChange(self.idleFrames)
        self.currentFrame = 0
        self.animationSpeed = 0.06

        self.hitBox = pygame.Rect(self.posX + self.cellSize/4, self.posY + self.cellSize/2, *pygame.Surface.get_size(self.activeAnim[0]))
    def loadFrames(self, spritesheet, startIndex, endIndex):
        frameWidth = 32
        frameHeight = 14
        frames = []
        for i in range(startIndex * frameWidth, endIndex * frameWidth, frameWidth):
            frame = spritesheet.subsurface((i, 0, frameWidth, frameHeight))
            frames.append(frame)
        return frames
    
    def draw(self, surface):
        frames = self.animChange(self.idleFrames)
        if self.isAnimChanged(frames):
            self.currentFrame = 0
        currentFrame = frames[int(self.currentFrame)]
        surface.blit(pygame.transform.scale(currentFrame, (80, 64), ), (self.posX, self.posY))

    def update(self):
        frames = self.animChange(self.idleFrames)
        if self.isAnimChanged(frames):
            self.currentFrame = 0
        self.currentFrame += self.animationSpeed
        if self.currentFrame >= len(frames):
            self.currentFrame = 0

    def animChange(self, idleAnim):
        frames = idleAnim
        self.animationSpeed = 0.06
        return frames
    
    def isAnimChanged(self, anim):
        if anim != self.prevAnim:
            self.prevAnim = anim
            return True
        else:
            return False
