import pygame
from platformer_project.sprites import Platform, Wall, Hazard, Collectible, Goal

class Level:
    def __init__(self) -> None:
        self.platforms    = pygame.sprite.Group()
        self.walls        = pygame.sprite.Group()
        self.hazards      = pygame.sprite.Group()
        self.collectibles = pygame.sprite.Group()
        self.goals        = pygame.sprite.Group()
        self.spawn       = (0, 0)
        self.world_width = 0

    def all_sprites(self) -> list:
        return list(self.platforms) + list(self.walls) + list(self.hazards) + list(self.collectibles) + list(self.goals)

    def _build_level(self, level: int) -> None:
        self.platforms.empty()
        self.walls.empty()
        self.hazards.empty()
        self.collectibles.empty()
        self.goals.empty()
        if level == 1:
            self.world_width = 2500
            self.spawn = (40, 650)
            platforms = [
                # Continuous floor 
                (0, 680, 2500, 40),

                # Platforms — alternating heights, encouraging jumping
                (200,  560, 150, 20),
                (420,  440, 150, 20),
                (650,  560, 150, 20),
                (900,  440, 150, 20),
                (1150, 320, 150, 20),
                (1400, 440, 150, 20),
                (1650, 320, 150, 20),
                (1900, 440, 150, 20),
                (2150, 560, 150, 20),
            ]

            coins = [
                (275,  530), (495,  410),
                (725,  530), (975,  410),
                (1225, 290), (1475, 410),
                (1725, 290), (1975, 410),
                (2225, 530),
            ]

            hazards = [
                (350,  660, 80, 20, "spikes"),
                (750,  660, 80, 20, "lava"),
                (1050, 660, 80, 20, "spikes"),
                (1300, 660, 80, 20, "lava"),
                (1550, 660, 80, 20, "spikes"),
                (1800, 660, 80, 20, "lava"),
                (2050, 660, 80, 20, "spikes"),
            ]

            for (x, y, w, h) in platforms:
                self.platforms.add(Platform(x, y, w, h))
            for (x, y) in coins:
                self.collectibles.add(Collectible(x, y))
            for (x, y, w, h, t) in hazards:
                self.hazards.add(Hazard(x, y, w, h, t))
            self.goals.add(Goal(2460, 680))

        elif level == 2:
            self.world_width = 2500
            self.spawn = (40, 650)
            platforms = [
                # Ground floor
                (0, 680, 470, 40),
                
                # First platform jump
                (150, 560, 100,  15),

                # Ladder climbing section
                
                (480, 610, 100,  15),   
                (650, 490, 100,  15),   
                (480, 370, 100,  15),   
                (650, 250, 100,  15),
                (480, 150, 270,  15),

                # Floating platforms with no ground underneath
                (850, 350, 100, 15),
                (1050, 220, 150, 15),
                (1050, 500, 100, 15),
                (1270, 130, 150, 15),
                (1490, 220, 150, 15),
                (1700, 150, 200, 15),

                # Section 4 — descent
                (1950, 280, 120, 15),
                (2100, 420, 120, 15),
                (2230, 560, 100, 15),

                # Goal Floor
                (2400, 680, 100, 40),
            ]

            walls = [
                (750, 150, 30, 570),   # chimney right wall
            ]

            coins = [
                # First jump
                (200, 530),
                # Ladder
                (700, 460), (530, 340), (700, 220),
                # Floating Platforms
                (1100, 470), (1125, 190), (1345, 100), (1600, 190), (1800, 120),
                # Descent
                (1975, 250), (2120, 390),
            ]

            hazards = [
                # First jump
                (250, 660, 70,  20, "spikes"),
                # Floating platforms — on top of platforms
                (1490, 200, 80, 20, "spikes"),
                # Descent — on top of descent platforms
                (2000, 260, 70, 20, "lava"),
                (2160, 400, 60, 20, "spikes"),
                (2230, 545, 100, 20, "spikes"),
            ]

            for (x, y, w, h) in platforms:
                self.platforms.add(Platform(x, y, w, h))
            for (x, y, w, h) in walls:
                self.walls.add(Wall(x, y, w, h))
            for (x, y) in coins:
                self.collectibles.add(Collectible(x, y))
            for (x, y, w, h, t) in hazards:
                self.hazards.add(Hazard(x, y, w, h, t))
            self.goals.add(Goal(2460, 680))


    def update(self, dt: float) -> None:
        self.hazards.update(dt)
        self.collectibles.update(dt)

    def draw(self, screen: pygame.Surface, camera_x: int) -> None:
        for sprite in self.all_sprites():
            offset_rect = sprite.rect.move(-camera_x, 0)
            screen.blit(sprite.image, offset_rect)
