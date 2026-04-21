import pygame

from platformer_project.sprites import Player
from platformer_project.level import Level
from platformer_project.title import Title

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
WORLD_WIDTH = 5000

class Game:
    def __init__(self) -> None:
        self.fps = 60
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

        self.state = "title"
        self.camera_x = 0

        self.menu = Title(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.world_width = WORLD_WIDTH

        self.current_level = 1
        self.level = Level()
        self.level._build_level(self.current_level)
        self.player = Player(*self.level.spawn)

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.event.post(pygame.event.Event(pygame.QUIT))

        if self.state == "title":
            self.menu.handle_event(event)
        elif self.state == "play":
            self.player.handle_event(event)
        elif self.state == "dead":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                self.restart()

    def _handle_collisions(self) -> None:
        hits = [platform for platform in self.level.platforms if self.player.hitbox.colliderect(platform.rect)]
        for platform in hits:
            if self.player.velocity.y >= 0:
                self.player.hitbox.bottom = platform.rect.top
                self.player.pos.y = self.player.hitbox.centery
                self.player.rect.center = (int(self.player.pos.x), int(self.player.pos.y))
                self.player.velocity.y = 0
                self.player.on_ground = True

        hazard_hits = [hazard for hazard in self.level.hazards if self.player.hitbox.colliderect(hazard.rect)]
        if hazard_hits:
            self.state = "dead"

        collectible_hit = [col for col in self.level.collectibles if self.player.hitbox.colliderect(col.rect)]
        for collectible in collectible_hit:
            collectible.kill()

    def _update_camera(self) -> None:
        screen_width = self.screen.get_width()
        self.camera_x = int(self.player.pos.x) - screen_width // 2
        self.camera_x = max(0, min(self.camera_x, self.world_width - screen_width))

    def update(self, dt: float) -> None:
        if self.state == "title":
            if self.menu.play_button.clicked:
                self.state = "play"

        elif self.state == "play":
            self.player.update(dt)
            self.level.update(dt)
            self._handle_collisions()
            self._update_camera()

    def restart(self) -> None:
        self.level._build_level(self.current_level)
        self.player.pos = pygame.Vector2(self.level.spawn)
        self.player.velocity.x = 0
        self.player.velocity.y = 0
        self.state = "play"

    def draw(self) -> None:
        if self.state == "title":
            self.menu.draw(self.screen)

        elif self.state == "play":
            self.screen.fill(pygame.Color("#ACA9A9"))
            self.level.draw(self.screen, self.camera_x)
            offset_rect = self.player.rect.move(-self.camera_x, 0)
            self.screen.blit(self.player.image, offset_rect)

        elif self.state == "dead":
            font = pygame.font.SysFont(None, 100)
            message = font.render("YOU DIED", True, pygame.Color("#FF0000"))
            direction = font.render("Press ENTER to restart", True, pygame.Color("#FF0000"))
            self.screen.blit(message, message.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40)))
            self.screen.blit(direction, direction.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40)))
            
