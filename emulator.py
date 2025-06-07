import os
import pyxel
from decoder import Program


class Emulator:
    def __init__(self, instructions):
        self.blocksize = 16

        # Arch-242 program
        self.program = Program(instructions)
        # TEMPORARY: assign snake head
        # self.program.mem[218] = 0b00001110

        pyxel.init(26*self.blocksize, 16*self.blocksize, fps=1500)

        pyxel.cls(0)
        # self.program.run()

        pyxel.run(self.update, self.draw)

    def update_grid(self):
        for y in range(3, 13):
            for x in range(3, 23):
                # get address line
                offset = (y-3) * 20 + (x-3)
                addr = 192 + offset // 4

                # get shift
                k = offset % 4

                color = 9 if self.program.mem[addr] >> k & 0b1 == 1 else 7
                pyxel.rect(x*self.blocksize, y*self.blocksize,
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

    def update(self):
        # for debugging: slower ticks
        if self.program.pc < 2*len(self.program.instr_mem):
            self.program.run_instr()
            self.program.iterate_pc()
            # self.print_mem()
            # print(self.program.ioa)
            print("curr snake orientation", self.snake_orientation())
            print("next snake orientation", self.next_snake_orientation())

            # pc of game tick
            if self.program.pc == 126:
                # reset ioa
                self.program.ioa = 0
                self.get_input()

            if self.program.shutdown:
                pyxel.cls(1)

        # temp
        if self.program.shutdown:
            print("SHUTDOWN")

    def draw(self):
        self.update_grid()


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

    Emulator(machine_code_instructions)
