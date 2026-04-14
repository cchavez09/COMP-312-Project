import pygame
from platformer_project.sprites import Platform, Hazard, Collectible

# Level data: each entry is (x, y, width, height)
LEVEL_1_SPAWN = (40, 675)

LEVEL_1 = [
    (0,   680, 5000, 40),  # floor
    (300, 550,  200, 20),           # platform
    (600, 420,  150, 20),           # platform
    (850, 300,  200, 20),           # platform
]

class Level:

    def __init__(self, platform_data: list, world_width: int) -> None:
        self.world_width = world_width
        self.platforms   = pygame.sprite.Group()
        self.hazards     = pygame.sprite.Group()
        self.collectibles = pygame.sprite.Group()

        for (x, y, w, h) in platform_data:
            p = Platform(x, y, w, h)
            self.platforms.add(p)

    def all_sprites(self) -> list:
        # Returns every sprite in this level so Game can render them
        return list(self.platforms) + list(self.hazards) + list(self.collectibles)

    def update(self, dt: float) -> None:
        self.hazards.update(dt)
        self.collectibles.update(dt)

    def draw(self, screen: pygame.Surface, camera_x: int) -> None:
        for sprite in self.all_sprites():
            offset_rect = sprite.rect.move(-camera_x, 0)
            screen.blit(sprite.image, offset_rect)
