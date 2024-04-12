import pygame
from enemy import Enemy

class Player:
    def __init__(self, posX, posY, cellSize) -> None:
        self.posX = posX
        self.posY = posY
        self.idleSprite = pygame.image.load("Data\Sprites\Player\player-idle.png").convert_alpha()
        self.moveSprite = pygame.image.load("Data\Sprites\Player\player-move.png").convert_alpha()
        self.fallSprite = pygame.image.load("Data\Sprites\Player\player-fall.png").convert_alpha()
        self.deathSprite = pygame.image.load("Data\Sprites\Player\player-death.png").convert_alpha()
        self.currentFrame = 0
        self.idleFrames = self.loadFrames(self.idleSprite, 0, 6)
        self.moveFrames = self.loadFrames(self.moveSprite, 0, 8)
        self.fallFrames = self.loadFrames(self.fallSprite, 0, 3)
        self.deathFrames = self.loadFrames(self.deathSprite, 0, 9)
        self.animationSpeed = 0.1
        self.cellSize = cellSize
        self.speed = 3
        self.targetX = self.posX
        self.targetY = self.posY
        self.isMoving = False
        self.isFalling = False
        self.isDead = False
        self.prevAnim = self.idleFrames
        self.activeDirection = 1
        self.activeAnim = self.animChange(self.idleFrames, self.moveFrames, self.fallFrames, self.deathFrames)
        self.hitBox = pygame.Rect(self.posX + self.cellSize/4, self.posY + self.cellSize/4, *pygame.Surface.get_size(self.activeAnim[0]))

    def loadFrames(self, spritesheet, startIndex, endIndex):
        frameWidth = 32
        frameHeight = 32
        frames = []
        for i in range(startIndex * frameWidth, endIndex * frameWidth, frameWidth):
            frame = spritesheet.subsurface((i, 0, frameWidth, frameHeight))
            frames.append(frame)
        return frames
    
    def draw(self, surface):
        frames = self.animChange(self.idleFrames, self.moveFrames, self.fallFrames, self.deathFrames)
        if self.isAnimChanged(frames):
            self.currentFrame = 0
        currentFrame = frames[int(self.currentFrame)]
        if self.activeDirection == -1:
            currentFrame = pygame.transform.flip(currentFrame, True, False)
        surface.blit(pygame.transform.scale(currentFrame, (74, 74), ), (self.posX, self.posY))

    def update(self):
        frames = self.animChange(self.idleFrames, self.moveFrames, self.fallFrames, self.deathFrames)
        if self.isAnimChanged(frames):
            self.currentFrame = 0
        self.currentFrame += self.animationSpeed
        if self.currentFrame >= len(frames):
            if not self.isDead:
                self.currentFrame = 0
            else: 
                self.currentFrame = len(frames)-1

    def animChange(self, idleAnim, moveAnim, fallAnim, deathAnim):
        if self.isMoving:
            frames = moveAnim
            self.animationSpeed = 0.2
        elif self.isFalling:
            frames = fallAnim
            self.animationSpeed = 0.1
        elif self.isDead:
            frames = deathAnim
            self.animationSpeed = 0.1
        else:
            frames = idleAnim
            self.animationSpeed = 0.1
        return frames

    def isAnimChanged(self, anim):
        if anim != self.prevAnim:
            self.prevAnim = anim
            return True
        else:
            return False

    def move(self, direction, grid):
            if self.posX == self.targetX and not self.isFalling and not self.isDead:
                newTargetX = self.posX + direction * self.cellSize
                if grid[self.posY//self.cellSize][newTargetX//self.cellSize] != 1:
                    self.targetX = newTargetX
                    self.activeDirection = direction

    def moveUpdate(self, grid):
        if self.posX == self.targetX:
            self.isMoving = False
            
        else:
            self.isMoving = True
            dx = self.targetX - self.posX
            direction = 1 if dx > 0 else -1
            step = min(abs(dx), self.speed)
            self.posX += direction * step

        self.hitBox = pygame.Rect(self.posX + self.cellSize/4, self.posY + self.cellSize/4, *pygame.Surface.get_size(self.activeAnim[0]))
        newTargetY = self.posY + self.cellSize
        targetGridX = int(self.posX//self.cellSize)
               
        if self.posY < (len(grid)-1)*self.cellSize and grid[newTargetY//self.cellSize][targetGridX] != 1:
            self.isFalling = True
            self.targetY = newTargetY
            if not self.isMoving:
                self.posY += self.speed
        else:
            self.isFalling = False

    def isColliding(self, collisionArea):
        if self.hitBox.colliderect(collisionArea):
            return True
        else:
            return False
        
    def isDeadCheck(self, enemy):
        if self.isColliding(enemy):
            self.isDead = True