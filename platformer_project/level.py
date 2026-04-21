import pygame
from platformer_project.sprites import Platform, Hazard, Collectible

LEVEL_1_COINS = [(350, 500)]

LEVEL_1_HAZARDS = [
    (400, 660, 100, 20, "spikes"),
    (750, 400, 100, 20, "lava"),
]

class Level:
    def __init__(self) -> None:
        self.platforms   = pygame.sprite.Group()
        self.hazards     = pygame.sprite.Group()
        self.collectibles = pygame.sprite.Group()
        self.spawn = (0, 0)

    def all_sprites(self) -> list:
        return list(self.platforms) + list(self.hazards) + list(self.collectibles)
    
    def _build_level(self, level: int) -> None:
        self.platforms.empty()
        self.hazards.empty()
        self.collectibles.empty()
        if level == 1:
            self.spawn = (40, 675)
            platforms = [
                (0,   680, 5000, 40),
                (300, 550,  200, 20),
                (600, 420,  150, 20),
                (850, 300,  200, 20),
            ]

            coins = [(350, 500)]

            hazards = [
                (400, 660, 100, 20, "spikes"),
                (750, 400, 100, 20, "lava"),
            ]

            for (x, y, w, h) in platforms:
                self.platforms.add(Platform(x, y, w, h))
            for (x, y) in coins:
                self.collectibles.add(Collectible(x, y))
            for (x, y, w, h, type) in hazards:
                self.hazards.add(Hazard(x, y, w, h, type))


    def update(self, dt: float) -> None:
        self.hazards.update(dt)
        self.collectibles.update(dt)

    def draw(self, screen: pygame.Surface, camera_x: int) -> None:
        for sprite in self.all_sprites():
            offset_rect = sprite.rect.move(-camera_x, 0)
            screen.blit(sprite.image, offset_rect)
