import pygame
import sys
from helpers.keyboard_handler import KeyboardHandler
from maze import Maze
from search import Search


class Game:
    def __init__(self):
        pygame.init()
        self.WINDOW_HEIGHT = 600
        self.WINDOW_WIDTH = 800
        self.CELL_SIZE = 20
        self.GRID_COLS = int(self.WINDOW_WIDTH / self.CELL_SIZE)
        self.GRID_ROWS = int(self.WINDOW_HEIGHT / self.CELL_SIZE)
        self.size = (self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
        self.screen = pygame.display.set_mode(self.size)
        self.keyboard_handler = KeyboardHandler()
        self.font = pygame.font.SysFont(pygame.font.get_fonts()[0], 64)
        self.time = pygame.time.get_ticks()
        self.maze = Maze(self.GRID_COLS, self.GRID_ROWS, self.size)
        self.maze.generate_open_maze()
        self.maze.colorExit()
        self.search = Search(self.maze)

    def game_loop(self):
        current_time = pygame.time.get_ticks()
        self.time = current_time
        self.handle_events()
        self.draw_components()

    def draw_components(self):
        self.screen.fill([255, 255, 255])
        self.maze.draw_maze(self.screen)
        pygame.display.flip()

    def draw_score(self):
        text = self.font.render(str(self.maze.target.distance), True, (0,0,0))
        self.screen.blit(text, (self.size[0]/2-64, 20))


    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                self.handle_key_down(event)
            if event.type == pygame.KEYUP:
                self.handle_key_up(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_mouse_pressed(event)

    def handle_key_down(self, event):
        self.keyboard_handler.key_pressed(event.key)
        if event.key == pygame.K_g:
            print("Greedy")
            self.search.dijkstra()

    def handle_key_up(self, event):
        self.keyboard_handler.key_released(event.key)

    def handle_mouse_pressed(self, event):
        x = int(event.pos[0] / self.maze.cell_width)
        y = int(event.pos[1] / self.maze.cell_height)
        if event.button == 1:
            self.maze.set_target(self.maze.grid[x][y])


if __name__ == "__main__":
    game = Game()
    while True:
        game.game_loop()
