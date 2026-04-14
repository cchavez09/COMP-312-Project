import pygame

from platformer_project.button import Button

class Title:
    def __init__(self, screen_width: int, screen_height: int) -> None:
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.title_font = pygame.font.SysFont("Times New Roman", 100, True, True)
        self.background_color = "#D3E4DF"
        self.play_button = Button("Play", (screen_width // 2, 350), 300, 100, self.background_color)

    # event in relation to button click
    def handle_event(self, event: pygame.event.Event) -> None:
        self.play_button.handle_event(event)

    # draw background 
    def draw(self, screen: pygame.Surface) -> None:
        # Draw Title with play button
        screen.fill(pygame.Color(self.background_color))
        game_name = self.title_font.render("Comp 312 Project", True, pygame.Color("#000000"))
        screen.blit(game_name, (game_name.get_rect(center=(self.screen_width // 2, 125))))
        self.play_button.draw(screen)