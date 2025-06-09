import os
import pyxel  # type: ignore
from decoder import Program


class Emulator:
    def __init__(self, instructions):
        self.blocksize = 16
        self.offset_y = 1  # shift game down by 1 block (16px)
        self.instructions = instructions
        # Arch-242 program
        self.program = Program(instructions)
        # TEMPORARY: assign snake head
        # self.program.mem[218] = 0b00001110

        pyxel.init(22*self.blocksize, (16 + self.offset_y)
                   * self.blocksize, fps=80000)

        pyxel.cls(0)
        # self.program.run()

        # this is for input reset delays
        self.ticks = 0

        pyxel.run(self.update, self.draw)

    def update_grid(self):
        for y in range(3, 13):
            for x in range(1, 21):
                offset = (y-3) * 20 + (x-1)
                addr = 192 + offset // 4
                k = offset % 4
                color = 9 if self.program.mem[addr] >> k & 0b1 == 1 else 7
                pyxel.rect(x*self.blocksize, (y+self.offset_y)*self.blocksize,
                           self.blocksize, self.blocksize, color)

    def get_input(self):
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.program.ioa |= 0b1000
        if pyxel.btn(pyxel.KEY_LEFT):
            self.program.ioa |= 0b0100
        if pyxel.btn(pyxel.KEY_DOWN):
            self.program.ioa |= 0b0010
        if pyxel.btn(pyxel.KEY_UP):
            self.program.ioa |= 0b0001

    def snake_orientation(self):
        d = self.program.mem[48]
        if d & 0b1:
            return f"up, {d}"
        if d & 0b10:
            return f"down, {d}"
        if d & 0b100:
            return f"left, {d}"
        if d & 0b1000:
            return f"right, {d}"

    def next_snake_orientation(self):
        d = self.program.mem[60]
        if d & 0b1:
            return f"up, {d}"
        if d & 0b10:
            return f"down, {d}"
        if d & 0b100:
            return f"left, {d}"
        if d & 0b1000:
            return f"right, {d}"

    def print_mem(self):
        print(f"at pc {self.program.pc}:")
        for i, row in enumerate(self.program.mem):
            print(f"row {i}:", bin(row))
        print()

    def game_over(self):
        pyxel.cls(1)
        pyxel.text(9*self.blocksize + 3, (6 + self.offset_y)
                   * self.blocksize + 5, "GAME OVER!", 7)
        pyxel.text(8*self.blocksize, (8 + self.offset_y) *
                   self.blocksize + 5, "Press 'R' to Restart", 7)
        state = "You Win" if self.program.mem[90] else "You Lose"
        pyxel.text(9*self.blocksize + 6, (5 + self.offset_y)
                   * self.blocksize + 5, state, 7)

    def update(self):
        if not self.program.shutdown and self.program.pc < 2*len(self.program.instr_mem):
            self.ticks += 1
            self.program.run_instr()
            self.program.iterate_pc()

            if self.ticks % 20:
                self.program.ioa = 0
                self.get_input()
        else:
            if pyxel.btn(pyxel.KEY_R):
                self.program = Program(self.instructions)

    def draw(self):
        if self.program.shutdown:
            self.game_over()
        else:
            pyxel.cls(0)
            mem = self.program.mem

            # Draw grid lines
            grid_color = 13  # Light gray
            for x in range(21):
                pyxel.line((x+1)*self.blocksize, (3+self.offset_y)*self.blocksize,
                           (x+1)*self.blocksize, (10+3+self.offset_y)*self.blocksize, grid_color)
            for y in range(11):
                pyxel.line(1*self.blocksize, (y+3+self.offset_y)*self.blocksize,
                           (20+1)*self.blocksize, (y+3+self.offset_y)*self.blocksize, grid_color)

            # Draw coordinate labels
            label_color = 7  # White
            for x in range(20):
                pyxel.text((x+1)*self.blocksize + 2, (3+self.offset_y)*self.blocksize - 10,
                           str(x), label_color)
            for y in range(10):
                pyxel.text(1*self.blocksize - 15, (y+3+self.offset_y)*self.blocksize + 5,
                           str(y), label_color)

            for y in range(3, 13):
                for x in range(1, 21):
                    offset = (y-3) * 20 + (x-1)
                    addr = 192 + offset // 4
                    k = offset % 4

                    def concat(lower, upper):
                        return int(bin(upper)[2:].zfill(
                            4)[-4:] + bin(lower)[2:].zfill(4)[-4:], 2)

                    if mem[addr] >> k & 0b1 == 1:
                        is_head = True if addr == concat(
                            mem[1], mem[2]) and mem[97] == pow(2, k) else False
                        is_fruit = True if addr == concat(
                            mem[50], mem[51]) and mem[52] == pow(2, k) else False
                        color = 8 if is_head else 9 if is_fruit else 11

                        pyxel.rect(
                            x*self.blocksize,
                            (y + self.offset_y)*self.blocksize,
                            self.blocksize-2,
                            self.blocksize-2,
                            color
                        )

            # Debug info overlay
            direction_names = {8: "RIGHT", 4: "LEFT", 2: "DOWN", 1: "UP"}
            head_x, head_y = mem_to_xy(mem[1], mem[2], mem[33])
            food_x, food_y = mem_to_xy(mem[50], mem[51], mem[52])
            pyxel.text(5, 5, f"Head: ({head_x},{head_y})", 7)
            pyxel.text(5, 15, f"Food: ({food_x},{food_y})", 7)
            dir = f"Facing: {direction_names.get(mem[48], 'UNKNOWN')}"
            pyxel.text(5, 25, dir, 7)

            score = self.program.mem[40] - 3
            pyxel.text(5, 35, f"Score: {score}", 7)


def mem_to_xy(low, high, bit_val):
    addr = (high << 4) | low
    offset = addr - 192
    x_base = offset % 5
    bit_index = {1: 0, 2: 1, 4: 2, 8: 3}.get(bit_val, 0)
    x = x_base * 4 + bit_index
    y = offset // 5
    return x, y


if __name__ == "__main__":
    # set .asm file here
    program_file = "input.asm"

    # compile the instruction code
    os.system(f'python3 assembler.py {program_file} bin')

    # set output file of assembler here / usually same name just different file format
    input_filename = "input.txt"

    machine_code_instructions = []

    # compiled instruction code is stored in input.txt
    with open(input_filename, "r") as f:
        for line in f:
            instr = line.strip()
            machine_code_instructions.append(instr)

    Emulator(machine_code_instructions)  # import os
