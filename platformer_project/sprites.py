import pygame

WORLD_WIDTH = 5000

class Player(pygame.sprite.Sprite):
    SIZE = 60
    ACCEL = 3000.0
    MAX_SPEED = 500
    FRICTION = 15
    GRAVITY = 3000.0
    JUMP_SPEED = 1000.0

    def __init__(self, x: int, y: int):
        # Set initial values to player attributes
        super().__init__()
        image = pygame.image.load("platformer_project/Assets/test.png").convert_alpha()
        self.image = pygame.transform.scale(image, (self.SIZE, self.SIZE))
        self.rect = self.image.get_rect()
        self.pos = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0,0)
        self.jump_requested = False
        self.on_ground = True
        self.hitbox = pygame.Rect(0, 0, self.SIZE - 30, self.SIZE)

    def _read_horizontal(self) -> float:
        # see if player is moving left or right using arrow keys or WASD
        keys = pygame.key.get_pressed()
        x = 0

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            x -= 1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            x += 1

        return float(x)
    
    def handle_event(self, event: pygame.event.Event) -> None:
        # Handle jump requests
        if event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_w) or (event.key == pygame.K_UP):
                self.jump_requested = True

    def update(self, dt: float) -> None:
        if self.on_ground:
            self.velocity.y = self.GRAVITY * dt

        x = self._read_horizontal()

        # Read horizontal movement and apply acceleration & max speed to player
        # as well as Friction when player is not inputting movement button
        self.velocity.x += x * self.ACCEL * dt
        if x == 0:
            self.velocity.x -= self.velocity.x * min (1.0, self.FRICTION * dt)
        self.velocity.x  = max(-self.MAX_SPEED, min(self.MAX_SPEED, self.velocity.x))

        if self.jump_requested == True and self.on_ground == True:
            self.on_ground = False
            self.velocity.y = -self.JUMP_SPEED
        self.jump_requested = False

        # Gravity implementation
        self.velocity.y += self.GRAVITY * dt
        
        self.pos += self.velocity * dt

        # Prevent leaving the left world boundary
        if self.pos.x < self.SIZE / 2:
            self.pos.x = self.SIZE / 2
            self.velocity.x = 0
        
        if self.pos.x > WORLD_WIDTH - self.SIZE / 2:
            self.pos.x = WORLD_WIDTH - self.SIZE / 2
            self.velocity.x = 0

        self.rect.center = (int(self.pos.x), int(self.pos.y))
        self.hitbox.center = self.rect.center
        self.on_ground = False

class Platform(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, width: int, height: int):
        # Create platform class to make boundaries
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(pygame.Color("#000000"))
        self.rect = self.image.get_rect(topleft=(x, y))


# Hazards like spikes or fire (As we buld we can change this class name to "Spike" or "Fire"
# to distinguish which type of hazard
class Hazard(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, width: int, height: int, hazard_type: str = "spikes"):
        super().__init__()
        self.hazard_type = hazard_type
        
        self.image = pygame.Surface((width, height))
        
        if self.hazard_type == "lava":
            self.image.fill(pygame.Color("#FF6400"))
        else:
            self.image.fill(pygame.Color("#FF0000"))
            
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self, dt: float) -> None:
        pass


# Collectible Sprites like coins or powerups
# 
class Collectible:
    def __init__(self):
        pass
