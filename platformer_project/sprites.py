import pygame



class Player(pygame.sprite.Sprite):
    SIZE = 15
    ACCEL = 3000.0
    MAX_SPEED = 500
    FRICTION = 15
    GRAVITY = 3000.0
    JUMP_SPEED = 1000.0

    def __init__(self, x: int, y: int):
        # Set initial values to player attributes
        super().__init__()
        self.image = pygame.Surface((self.SIZE, self.SIZE))
        self.image.fill(pygame.Color("#001068"))
        self.rect = pygame.Rect(0, 0, self.SIZE, self.SIZE)
        self.pos = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0,0)
        self.jump_requested = False
        self.on_ground = True

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
        self.rect.center = (int(self.pos.x), int(self.pos.y))

class Platform(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, width: int, height: int):
        # Create platform class to make boundaries
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(pygame.Color("#000000"))
        self.rect = self.image.get_rect(topleft=(x, y))


# Hazards like spikes or fire (As we buld we can change this class name to "Spike" or "Fire"
# to distinguish which type of hazard
class Hazard:
    def __init__(self):
        super().__


# Collectible Sprites like coins or powerups
# 
class Collectible:
    def __init__(self):
        pass
