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

        pyxel.cls(0)

        pyxel.run(self.update, self.draw)

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
        if pyxel.btnp(pyxel.KEY_RIGHT):
            self.program.ioa |= 0b1000
        if pyxel.btnp(pyxel.KEY_LEFT):
            self.program.ioa |= 0b0100
        if pyxel.btnp(pyxel.KEY_DOWN):
            self.program.ioa |= 0b0010
        if pyxel.btnp(pyxel.KEY_UP):
            self.program.ioa |= 0b0001

    def update(self):
        self.get_input()

        if not self.program.shutdown:
            self.program.step()

        else:
            print("Program shut down")            
            pyxel.quit()

    def draw(self):
        try:
            pyxel.cls(0)
            
            # Draw game grid
            for y in range(20):
                for x in range(10):
                    # Calculate memory address for this position
                    addr = 192 + (y * 10 + x) // 4
                    bit_pos = (y * 10 + x) % 4
                    led_on = (self.program.mem[addr] >> bit_pos) & 1
                    
                    if led_on:
                        color = 11  # Snake color
                        # Check if it's the head (MEM[33] has the head LED bit)
                        if addr == (192 + (self.program.mem[1] * 10 + self.program.mem[2]) // 4):
                            if bit_pos == (self.program.mem[1] * 10 + self.program.mem[2]) % 4:
                                color = 8  # Head color
                        
                        pyxel.rect(x * self.blocksize + 6 * self.blocksize, 
                                (y + 3) * self.blocksize,
                                self.blocksize - 1, self.blocksize - 1, color)
            
            # Draw score
            score = self.program.mem[49] & 0xF
            pyxel.text(2 * self.blocksize, 2 * self.blocksize, 
                    f"Score: {score}", 7)
            
            # Draw tick count
            ticks = self.program.mem[0] & 0xFF
            pyxel.text(2 * self.blocksize, 4 * self.blocksize, 
                    f"Tick: {ticks}", 7)
            
        except Exception as e:
            print("Drawing error:", e)


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
