import os
import pyxel
from decoder import Program


class Emulator:
    def __init__(self, instructions):
        self.blocksize = 16

        # Arch-242 program
        self.program = Program(instructions)
        # TEMPORARY: assign snake head
        # self.program.mem[200] = 0b00001110

        self.grid = [[0]*10 for _ in range(20)]

        pyxel.init(22*self.blocksize, 26*self.blocksize)

        self.init_game()

        pyxel.run(self.update, self.draw)

    def init_game(self):
        # self.timer = 0
        #
        # self.len = 3
        # self.snake_coords = [[-1, -1] for _ in range(self.len)]
        #
        # # coordinates of the head
        # self.snake_coords[0][0] = 6
        # self.snake_coords[0][1] = 3
        #
        # self.orientation = 0  # [0 - left, 1 - up, 2 - right, 3 - down]
        # self.next_orientation = -1
        #
        # for i in range(1, self.len):
        #     self.snake_coords[i][0] = self.snake_coords[i-1][0] + 1 if self.orientation == 0 else self.snake_coords[i -
        #                                                                                                             1][0] - 1 if self.orientation == 2 else self.snake_coords[i-1][0]
        #     self.snake_coords[i][1] = self.snake_coords[i-1][1] + 1 if self.orientation == 1 else self.snake_coords[i -
        #                                                                                                             1][1] - 1 if self.orientation == 3 else self.snake_coords[i-1][1]
        #
        # for x, y in self.snake_coords:
        #     self.grid[y][x] = 1
        #
        # self.has_food = True
        # self.food_x = 4
        # self.food_y = 15
        # self.grid[self.food_y][self.food_x] = 1
        #
        # self.points = 0
        # self.dead = False
        #
        pyxel.cls(0)

    def update_grid(self):
        for y in range(3, 23):
            for x in range(6, 16):
                # get address line
                offset = (y-3) * 10 + (x-6)
                addr = 192 + offset // 4

                # get shift
                k = offset % 4

                color = 9 if self.program.mem[addr] >> k & 0b1 == 1 else 7
                pyxel.rect(x*self.blocksize, y*self.blocksize,
                           self.blocksize, self.blocksize, color)

    def get_input(self):
        if pyxel.btnp(pyxel.KEY_DOWN):
            self.program.ioa |= 0b1000
        if pyxel.btnp(pyxel.KEY_UP):
            self.program.ioa |= 0b0100
        if pyxel.btnp(pyxel.KEY_RIGHT):
            self.program.ioa |= 0b0010
        if pyxel.btnp(pyxel.KEY_LEFT):
            self.program.ioa |= 0b0001

    def update(self):
        self.get_input()
        self.program.run_instr()
        self.program.iterate_pc()

        # should reset every tick
        # print(self.program.ioa)

        # if not self.dead:
        #     self.timer += 1
        #
        #     if pyxel.btnp(pyxel.KEY_UP) and self.orientation != 3:
        #         self.next_orientation = 1
        #     if pyxel.btnp(pyxel.KEY_DOWN) and self.orientation != 1:
        #         self.next_orientation = 3
        #     if pyxel.btnp(pyxel.KEY_LEFT) and self.orientation != 2:
        #         self.next_orientation = 0
        #     if pyxel.btnp(pyxel.KEY_RIGHT) and self.orientation != 0:
        #         self.next_orientation = 2
        #
        #     if self.timer % 25 == 0 and not self.has_food:
        #         new_x = randint(0, 9)
        #         new_y = randint(0, 19)
        #         while self.grid[new_y][new_x] == 1:
        #             new_x = randint(0, 9)
        #             new_y = randint(0, 19)
        #
        #         self.has_food = True
        #         self.food_x = new_x
        #         self.food_y = new_y
        #         self.grid[self.food_y][self.food_x] = 1
        #
        #     if self.timer % 5 == 0:
        #         self.grid[self.snake_coords[-1][1]
        #                   ][self.snake_coords[-1][0]] = 0
        #
        #         self.orientation = self.next_orientation if self.next_orientation > - \
        #             1 else self.orientation
        #
        #         x, y = self.snake_coords[0][0], self.snake_coords[0][1]
        #         if self.orientation == 0:
        #             x -= 1
        #         elif self.orientation == 1:
        #             y -= 1
        #         elif self.orientation == 2:
        #             x += 1
        #         elif self.orientation == 3:
        #             y += 1
        #
        #         # out of bounds
        #         if not (0 <= x < 10) or not (0 <= y < 20):
        #             pyxel.cls(1)
        #             self.dead = True
        #             self.grid = [[0]*10 for _ in range(20)]
        #             pyxel.text(11*self.blocksize, 13 *
        #                        self.blocksize, "Game Over", 2)
        #             return
        #
        #         # if it touches itself
        #         for x2, y2 in self.snake_coords:
        #             if x == x2 and y == y2:
        #                 pyxel.cls(1)
        #                 self.dead = True
        #                 self.grid = [[0]*10 for _ in range(20)]
        #                 pyxel.text(11*self.blocksize, 13 *
        #                            self.blocksize, "Game Over", 2)
        #                 return
        #
        #         # if touches food
        #         if x == self.food_x and y == self.food_y:
        #             self.has_food = False
        #             self.grid[self.food_y][self.food_x] = 0
        #             self.snake_coords.append([-1, -1])
        #             self.len += 1
        #
        #         # change snake coords
        #         for i in range(self.len-1, 0, -1):
        #             self.snake_coords[i][0] = self.snake_coords[i-1][0]
        #             self.snake_coords[i][1] = self.snake_coords[i-1][1]
        #
        #         self.snake_coords[0][0], self.snake_coords[0][1] = x, y
        #
        #         for x, y in self.snake_coords:
        #             self.grid[y][x] = 1
        #
        #             self.next_orientation = -1
        #
        # else:
        #     if pyxel.btnp(pyxel.KEY_R):
        #         self.init_game()

    def draw(self):
        self.update_grid()


if __name__ == "__main__":
    # set .asm file here
    program_file = "input.asm"

    # set output file of assembler here / usually same name just different file format
    input_filename = "input.txt"

    # compile the instruction code
    os.system(f'python3 assembler.py {program_file} bin')

    machine_code_instructions = []

    # compiled instruction code is stored in input.txt
    with open(input_filename, "r") as f:
        for line in f:
            instr = line.strip()
            machine_code_instructions.append(instr)

    Emulator(machine_code_instructions)
