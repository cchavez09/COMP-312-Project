import pygame

from platformer_project.sprites import Player, Platform

class Game:

    def __init__(self) -> None:
        
        self.fps = 60
        self.screen = pygame.display.set_mode((1280, 720))
        
        # Set game state to play to see what the game mechanics would look like
        self.state = "play"

        self.sprites = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()

        self.player = Player(40, 300)
        self.sprites.add(self.player)

        floor = Platform(0, 680, 1280, 40)
        self.sprites.add(floor)
        self.platforms.add(floor)

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.event.post(pygame.event.Event(pygame.QUIT))
        self.player.handle_event(event)

    def _handle_collisions(self) -> None:
        if self.player.velocity.y > 0:
            hits = pygame.sprite.spritecollide(self.player, self.platforms, False)
            for platform in hits:
                self.player.rect.bottom = platform.rect.top
                self.player.pos.y = self.player.rect.centery
                self.player.velocity.y = 0
                self.player.on_ground = True

    def update(self, dt: float) -> None:
        if self.state == "play":
            self.sprites.update(dt) 
            self._handle_collisions()
            
    def draw(self) -> None:
        self.screen.fill(pygame.Color("#ACA9A9"))
        self.sprites.draw(self.screen)
        