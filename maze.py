import random
from datetime import datetime
from grid_element import GridElement

class Maze:

    def __init__(self, grid_size_x, grid_size_y, screen_size):
        self.targets= []
        self.grid_size = (grid_size_x, grid_size_y)
        self.cell_width = screen_size[0] / grid_size_x
        self.cell_height = screen_size[1] / grid_size_y
        self.grid = []
        #fill grid with grid_elements
        for x in range(grid_size_x):
            self.grid.append([])
            for y in range(grid_size_y):
                self.grid[x].append(GridElement(x, y, (self.cell_width, self.cell_height)))

        self.start = self.grid[0][0]
        self.target = self.grid[-1][-1]

        #set the exit node
        self.exit = self.grid[39][0]
        self.reset_all()
        random.seed(datetime.now())

    def colorExit(self):
        self.exit.set_color((255,0,0))

    def reset_all(self):
        for row in self.grid:
            for cell in row:
                cell.reset_neighbours()
        self.reset_state()
        return None

    def reset_state(self):
        for row in self.grid:
            for cell in row:
                cell.reset_state()
        self.start.set_distance(0)
        self.start.set_score(0)
        self.start.color = (0, 255, 0)
        self.target.color = (240, 60, 20)
        for target in self.targets:
            target.color = (240, 60, 20)
        return None

    def set_source(self, cell):
        if cell != self.target:
            self.start = cell
            self.reset_state()

    def set_target(self, cell):
        if cell != self.start:
            self.target = cell
            self.targets.append(cell)
            print(self.targets)
            self.reset_state()
            self.colorExit()

    def print_maze(self):
        transposed = list(zip(*self.grid))
        for row in transposed:
            print(row)
        return None

    def draw_maze(self, surface):
        for row in self.grid:
            for element in row:
                element.draw_grid_element(surface)
        return None

    def possible_neighbours(self, cell):
        neighbours = []
        if cell.position[0] > 0:  # North
            neighbours.append(self.grid[cell.position[0] - 1][cell.position[1]])
        if cell.position[0] < self.grid_size[0] - 1:  # East
            neighbours.append(self.grid[cell.position[0] + 1][cell.position[1]])
        if cell.position[1] < self.grid_size[1] - 1:  # South
            neighbours.append(self.grid[cell.position[0]][cell.position[1] + 1])
        if cell.position[1] > 0:  # West
            neighbours.append(self.grid[cell.position[0]][cell.position[1] - 1])
        return neighbours

    def del_link(self, cell1, cell2):
        if cell2 in cell1.neighbours:
            cell1.neighbours.remove(cell2)
        if cell1 in cell2.neighbours:
            cell2.neighbours.remove(cell1)
        return None

    def add_link(self, cell1, cell2):
        if cell1.manhattan_distance(cell2) == 1:
            cell1.neighbours.append(cell2)
            cell2.neighbours.append(cell1)
        return None

    def generate_open_maze(self):
        self.reset_all()
        for col in self.grid:
            for cell in col:
                cell.neighbours = self.possible_neighbours(cell)
                # first two rectangles
                for x in range(self.grid_size[0] // 4 - 5, self.grid_size[0] // 4 + 1):
                    self.del_link(self.grid[x][self.grid_size[1] // 7], self.grid[x][(self.grid_size[1] // 7) - 1])
                for y in range(self.grid_size[1] // 6 - 1, self.grid_size[1] // 6 + 2):
                    self.del_link(self.grid[self.grid_size[0] // 7][y], self.grid[(self.grid_size[0] // 7) - 1][y])
                for x in range(self.grid_size[0] // 4 - 5, self.grid_size[0] // 4 + 1):
                    self.del_link(self.grid[x][self.grid_size[1] // 4], self.grid[x][(self.grid_size[1] // 4) - 1])
                for y in range(self.grid_size[1] // 6 - 1, self.grid_size[1] // 6 + 2):
                    self.del_link(self.grid[self.grid_size[0] // 4][y], self.grid[(self.grid_size[0] // 4) + 1][y])

                for x in range(self.grid_size[0] // 4 - 5, self.grid_size[0] // 4 + 1):
                    self.del_link(self.grid[x][self.grid_size[1] // 3], self.grid[x][(self.grid_size[1] // 3) - 1])
                for x in range(self.grid_size[0] // 4 - 5, self.grid_size[0] // 4 + 1):
                    self.del_link(self.grid[x][3 * self.grid_size[1] // 4],
                                  self.grid[x][(3 * self.grid_size[1] // 4) - 1])
                for y in range(self.grid_size[1] // 6 + 5, self.grid_size[1] // 6 + 17):
                    self.del_link(self.grid[self.grid_size[0] // 4][y], self.grid[(self.grid_size[0] // 4) + 1][y])
                for y in range(self.grid_size[1] // 6 + 5, self.grid_size[1] // 6 + 17):
                    self.del_link(self.grid[self.grid_size[0] // 7][y], self.grid[(self.grid_size[0] // 7) - 1][y])

                # left bottom corner double rectangle
                for x in range(self.grid_size[0] // 4 - 10, self.grid_size[0] // 4 - 7):  # top part
                    self.del_link(self.grid[x][3 * self.grid_size[1] // 4],
                                  self.grid[x][(3 * self.grid_size[1] // 4) - 1])
                for x in range(self.grid_size[0] // 4 - 7, self.grid_size[0] // 4 + 0):
                    self.del_link(self.grid[x][7 * self.grid_size[1] // 8],
                                  self.grid[x][(7 * self.grid_size[1] // 8) + 1])
                for y in range(self.grid_size[1] // 6 + 17, self.grid_size[1] // 6 + 22):
                    self.del_link(self.grid[self.grid_size[0] // 15][y], self.grid[(self.grid_size[0] // 15) + 1][y])
                for y in range(self.grid_size[1] // 6 + 22, self.grid_size[1] // 6 + 25):
                    self.del_link(self.grid[self.grid_size[0] // 4][y], self.grid[(self.grid_size[0] // 4) - 1][y])

                # middle back wall
                for x in range(self.grid_size[0] // 4 + 3, self.grid_size[0] // 4 + 17):
                    self.del_link(self.grid[x][7 * self.grid_size[1] // 8],
                                  self.grid[x][(7 * self.grid_size[1] // 8) + 1])
                for y in range(self.grid_size[1] // 6 + 22, self.grid_size[1] // 6 + 25):
                    self.del_link(self.grid[self.grid_size[0] // 3][y], self.grid[(self.grid_size[0] // 3) - 1][y])
                for y in range(self.grid_size[1] // 6 + 22, self.grid_size[1] // 6 + 25):
                    self.del_link(self.grid[self.grid_size[0] // -3][y], self.grid[(self.grid_size[0] // -3) + 1][y])

                # right bottom corner double rectangle
                for x in range(self.grid_size[0] // 4 + 27, self.grid_size[0] // 4 + 30):  # top part
                    self.del_link(self.grid[x][3 * self.grid_size[1] // 4],
                                  self.grid[x][(3 * self.grid_size[1] // 4) - 1])
                for x in range(self.grid_size[0] // 4 + 20, self.grid_size[0] // 4 + 27):
                    self.del_link(self.grid[x][7 * self.grid_size[1] // 8],
                                  self.grid[x][(7 * self.grid_size[1] // 8) + 1])
                for y in range(self.grid_size[1] // 6 + 17, self.grid_size[1] // 6 + 22):
                    self.del_link(self.grid[self.grid_size[0] // -12][y], self.grid[(self.grid_size[0] // -12) + 1][y])
                for y in range(self.grid_size[1] // 6 + 22, self.grid_size[1] // 6 + 25):
                    self.del_link(self.grid[self.grid_size[0] // -4][y], self.grid[(self.grid_size[0] // -4) - 1][y])

                # left wall
                for y in range(self.grid_size[1] // 6 + 2, self.grid_size[1] // 2 + 4):
                    self.del_link(self.grid[self.grid_size[0] // 15][y], self.grid[(self.grid_size[0] // 15) + 1][y])
                for x in range(self.grid_size[0] // 4 - 10, self.grid_size[0] // 4 - 7):  # first
                    self.del_link(self.grid[x][self.grid_size[1] // 4], self.grid[x][(self.grid_size[1] // 4) - 1])
                for x in range(self.grid_size[0] // 4 - 10, self.grid_size[0] // 4 - 7):  # second
                    self.del_link(self.grid[x][self.grid_size[1] // 3], self.grid[x][(self.grid_size[1] // 3) - 1])
                for x in range(self.grid_size[0] // 4 - 10, self.grid_size[0] // 4 - 7):  # third
                    self.del_link(self.grid[x][3 * self.grid_size[1] // 5],
                                  self.grid[x][(3 * self.grid_size[1] // 5) + 1])

                # middle rows
                for y in range(self.grid_size[1] // 6 + 2, self.grid_size[1] // 2 + 8):
                    self.del_link(self.grid[self.grid_size[0] // 3][y], self.grid[(self.grid_size[0] // 3) - 1][y])
                for y in range(self.grid_size[1] // 6 + 2, self.grid_size[1] // 2 + 8):
                    self.del_link(self.grid[self.grid_size[0] // 3][y], self.grid[(self.grid_size[0] // 3) + 1][y])
                for x in range(self.grid_size[0] // 4 + 3, self.grid_size[0] // 4 + 4):
                    self.del_link(self.grid[x][3 * self.grid_size[1] // 15],
                                  self.grid[x][(3 * self.grid_size[1] // 15) + 1])
                for x in range(self.grid_size[0] // 4 + 3, self.grid_size[0] // 4 + 4):
                    self.del_link(self.grid[x][3 * self.grid_size[1] // 4],
                                  self.grid[x][(3 * self.grid_size[1] // 4) + 1])

                for y in range(self.grid_size[1] // 6 + 2, self.grid_size[1] // 2 + 8):
                    self.del_link(self.grid[self.grid_size[0] // -2][y], self.grid[(self.grid_size[0] // -2) - 1][y])
                for y in range(self.grid_size[1] // 6 + 2, self.grid_size[1] // 2 + 8):
                    self.del_link(self.grid[self.grid_size[0] // -2][y], self.grid[(self.grid_size[0] // -2) + 1][y])
                for x in range(self.grid_size[0] // 4 + 10, self.grid_size[0] // 4 + 11):
                    self.del_link(self.grid[x][3 * self.grid_size[1] // 15],
                                  self.grid[x][(3 * self.grid_size[1] // 15) + 1])
                for x in range(self.grid_size[0] // 4 + 10, self.grid_size[0] // 4 + 11):
                    self.del_link(self.grid[x][3 * self.grid_size[1] // 4],
                                  self.grid[x][(3 * self.grid_size[1] // 4) + 1])

                for y in range(self.grid_size[1] // 6 + 2, self.grid_size[1] // 2 + 8):
                    self.del_link(self.grid[self.grid_size[0] // -3][y], self.grid[(self.grid_size[0] // -3) - 1][y])
                for y in range(self.grid_size[1] // 6 + 2, self.grid_size[1] // 2 + 8):
                    self.del_link(self.grid[self.grid_size[0] // -3][y], self.grid[(self.grid_size[0] // -3) + 1][y])
                for x in range(self.grid_size[0] // 4 + 16, self.grid_size[0] // 4 + 17):
                    self.del_link(self.grid[x][3 * self.grid_size[1] // 15],
                                  self.grid[x][(3 * self.grid_size[1] // 15) + 1])
                for x in range(self.grid_size[0] // 4 + 16, self.grid_size[0] // 4 + 17):
                    self.del_link(self.grid[x][3 * self.grid_size[1] // 4],
                                  self.grid[x][(3 * self.grid_size[1] // 4) + 1])

                # right block
                for y in range(self.grid_size[1] // 4 + 1, self.grid_size[1] // 4 + 6):
                    self.del_link(self.grid[self.grid_size[0] // -4][y], self.grid[(self.grid_size[0] // -4) - 1][y])
                for y in range(self.grid_size[1] // 4 + 1, self.grid_size[1] // 4 + 6):
                    self.del_link(self.grid[self.grid_size[0] // -7][y], self.grid[(self.grid_size[0] // -7) - 1][y])
                for y in range(self.grid_size[1] // 4 + 9, self.grid_size[1] // 2 + 7):
                    self.del_link(self.grid[self.grid_size[0] // -4][y], self.grid[(self.grid_size[0] // -4) - 1][y])
                for y in range(self.grid_size[1] // 4 + 9, self.grid_size[1] // 2 + 7):
                    self.del_link(self.grid[self.grid_size[0] // -7][y], self.grid[(self.grid_size[0] // -7) - 1][y])
                for x in range(self.grid_size[0] // 4 + 20, self.grid_size[0] // 4 + 24):
                    self.del_link(self.grid[x][3 * self.grid_size[1] // 12],
                                  self.grid[x][(3 * self.grid_size[1] // 12) + 1])
                for x in range(self.grid_size[0] // 4 + 20, self.grid_size[0] // 4 + 24):
                    self.del_link(self.grid[x][3 * self.grid_size[1] // 6],
                                  self.grid[x][(3 * self.grid_size[1] // 6) + 1])
                for x in range(self.grid_size[0] // 4 + 20, self.grid_size[0] // 4 + 24):
                    self.del_link(self.grid[x][3 * self.grid_size[1] // 7],
                                  self.grid[x][(3 * self.grid_size[1] // 7) + 1])
                for x in range(self.grid_size[0] // 4 + 20, self.grid_size[0] // 4 + 24):
                    self.del_link(self.grid[x][3 * self.grid_size[1] // 4],
                                  self.grid[x][(3 * self.grid_size[1] // 4) - 1])

                # right wall
                for x in range(self.grid_size[0] // 4 + 27, self.grid_size[0] // 4 + 30):  # first
                    self.del_link(self.grid[x][self.grid_size[1] // 4], self.grid[x][(self.grid_size[1] // 4) - 1])
                for x in range(self.grid_size[0] // 4 + 27, self.grid_size[0] // 4 + 30):  # third
                    self.del_link(self.grid[x][3 * self.grid_size[1] // 5],
                                  self.grid[x][(3 * self.grid_size[1] // 5) + 1])
                for y in range(self.grid_size[1] // 6 + 2, self.grid_size[1] // 2 + 4):
                    self.del_link(self.grid[self.grid_size[0] // -12][y], self.grid[(self.grid_size[0] // -12) + 1][y])