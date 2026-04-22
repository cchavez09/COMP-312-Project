import pygame

from platformer_project.sprites import Player
from platformer_project.level import Level
from platformer_project.title import Title

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
WORLD_WIDTH = 2500

class Game:
   def __init__(self) -> None:
        self.fps = 60
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

        self.state = "title"
        self.camera_x = 0

        self.menu = Title(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.level = Level(LEVEL_1, LEVEL_1_HAZARDS, WORLD_WIDTH)
        self.player = Player(LEVEL_1_SPAWN[0], LEVEL_1_SPAWN[1])

        # --- NEW: Load the background image ---
        try:
            # Load image and scale it to match the screen height
            loaded_bg = pygame.image.load("platformer_project/Assets/bg.png").convert()
            # Calculate the new width to keep the image's aspect ratio correct
            aspect_ratio = loaded_bg.get_width() / loaded_bg.get_height()
            new_width = int(SCREEN_HEIGHT * aspect_ratio)
            self.bg_image = pygame.transform.scale(loaded_bg, (new_width, SCREEN_HEIGHT))
        except FileNotFoundError:
            # Fallback just in case you forget to add the image
            self.bg_image = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            self.bg_image.fill(pygame.Color("#333333"))

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.event.post(pygame.event.Event(pygame.QUIT))

        # Handle events based on the game state
        if self.state == "title":
            self.menu.handle_event(event)
        elif self.state == "play":
            self.player.handle_event(event)
        elif self.state == "dead":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                self.restart()
        elif self.state == "win":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                self._next_level()

    def _handle_collisions(self) -> None:
        # Handle for collisions with platforms, walls, hazards, collectibles and goals
        hits = [platform for platform in self.level.platforms if self.player.hitbox.colliderect(platform.rect)]
        for platform in hits:
            if self.player.velocity.y >= 0 and self.player.prev_bottom <= platform.rect.top:
                self.player.hitbox.bottom = platform.rect.top
                self.player.pos.y = self.player.hitbox.centery
                self.player.rect.center = (int(self.player.pos.x), int(self.player.pos.y))
                self.player.velocity.y = 0
                self.player.on_ground = True

        # Handle for wall collisions, not allowing player to move through them while
        # being able to jump on top of the walls
        wall_hits = [wall for wall in self.level.walls if self.player.hitbox.colliderect(wall.rect)]
        for wall in wall_hits:
            if self.player.prev_right <= wall.rect.left:
                self.player.hitbox.right = wall.rect.left
                self.player.pos.x = self.player.hitbox.centerx
                self.player.rect.center = (int(self.player.pos.x), int(self.player.pos.y))
                self.player.velocity.x = 0
            elif self.player.prev_left >= wall.rect.right:
                self.player.hitbox.left = wall.rect.right
                self.player.pos.x = self.player.hitbox.centerx
                self.player.rect.center = (int(self.player.pos.x), int(self.player.pos.y))
                self.player.velocity.x = 0
            elif self.player.prev_bottom <= wall.rect.top:
                self.player.hitbox.bottom = wall.rect.top
                self.player.pos.y = self.player.hitbox.centery
                self.player.rect.center = (int(self.player.pos.x), int(self.player.pos.y))
                self.player.velocity.y = 0
                self.player.on_ground = True

        # Handle for player faling off the world and resulting in death
        if self.player.pos.y > 800:
            self.state = "dead"

        hazard_hits = [hazard for hazard in self.level.hazards if self.player.hitbox.colliderect(hazard.rect)]
        if hazard_hits:
            self.state = "dead"

        collectible_hit = [col for col in self.level.collectibles if self.player.hitbox.colliderect(col.rect)]
        for collectible in collectible_hit:
            collectible.kill()

        goal_hit = [g for g in self.level.goals if self.player.hitbox.colliderect(g.rect)]
        if goal_hit:
            self.state = "win"

    def _update_camera(self) -> None:
        screen_width = self.screen.get_width()
        self.camera_x = int(self.player.pos.x) - screen_width // 2
        self.camera_x = max(0, min(self.camera_x, self.level.world_width - screen_width))

    def update(self, dt: float) -> None:
        if self.state == "title":
            if self.menu.play_button.clicked:
                self.state = "play"

        elif self.state == "play":
            self.player.update(dt)
            self.level.update(dt)
            self._handle_collisions()
            self._update_camera()

    # Added restart method and build level method to reset the level
    # when player dies
    def restart(self) -> None:
        self.level._build_level(self.current_level)
        self.player.reset(*self.level.spawn)
        self.camera_x = 0
        self.state = "play"

    # When player wins, move to the next level and reset player and camera
    # and return to menu when all levels done
    def _next_level(self) -> None:
        self.current_level += 1
        if self.current_level > 2:
            self.current_level = 1
            self.menu.play_button.clicked = False
            self.state = "title"
            return
        self.level._build_level(self.current_level)
        self.player.reset(*self.level.spawn)
        self.camera_x = 0
        self.state = "play"

  def draw(self) -> None:
        if self.state == "title":
            self.menu.draw(self.screen)

        elif self.state == "play":
            # --- NEW: Parallax Scrolling Background ---
            # 0.5 makes the background move at half the speed of the camera
            parallax_speed = 0.5 
            bg_width = self.bg_image.get_width()
            
            # Use modulo (%) to loop the x position infinitely
            bg_x = -(self.camera_x * parallax_speed) % bg_width
            
            # Draw two copies of the background side-by-side so it never runs out
            self.screen.blit(self.bg_image, (int(bg_x), 0))
            self.screen.blit(self.bg_image, (int(bg_x) - bg_width, 0))

            # Draw the level and player on top of the background
            self.level.draw(self.screen, self.camera_x)
            offset_rect = self.player.rect.move(-self.camera_x, 0)
            self.screen.blit(self.player.image, offset_rect)

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

        elif self.state == "win":
            font = pygame.font.SysFont(None, 100)
            message = font.render("LEVEL COMPLETE!", True, pygame.Color("#00CC44"))
            direction = font.render("Press ENTER for next level", True, pygame.Color("#00CC44"))
            self.screen.blit(message, message.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40)))
            self.screen.blit(direction, direction.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40)))
            
