import os
import pyxel # type: ignore
from decoder import Program

class Emulator:
    def __init__(self, instructions):
        self.blocksize = 16
        self.program = Program(instructions)
        self.last_head_pos = (0, 0)
        self.frame_count = 0
        self.input_map = {
            0b1000: "RIGHT",
            0b0100: "LEFT", 
            0b0010: "DOWN",
            0b0001: "UP",
            0b0000: "NONE"
        }
        
        # Pre-calculate display coordinates
        self.border_rect = (
            1*self.blocksize, 3*self.blocksize,
            20*self.blocksize, 10*self.blocksize
        )
        
        pyxel.init(22*self.blocksize, 16*self.blocksize)
        pyxel.cls(0)
<<<<<<< Updated upstream
=======
        # self.program.run()

        # this is for input reset delays
        self.ticks = 0
        self.input_buffer = 0


>>>>>>> Stashed changes
        pyxel.run(self.update, self.draw)

    def get_input(self):
<<<<<<< Updated upstream
        """Optimized input handling with direct key checks"""
        self.program.ioa = (
            0b1000 * pyxel.btn(pyxel.KEY_RIGHT) |  # Changed from btnp to btn
            0b0100 * pyxel.btn(pyxel.KEY_LEFT) |
            0b0010 * pyxel.btn(pyxel.KEY_DOWN) |
            0b0001 * pyxel.btn(pyxel.KEY_UP)
        )
        
            
=======
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
        # shows a game over screen
        pyxel.cls(1)
        pyxel.text(9*self.blocksize + 5, 6 *
                   self.blocksize , "GAME OVER!", 7)
        pyxel.text(8*self.blocksize + 4, 8 *
                   self.blocksize + 8, "Press 'R' to Restart", 7)
>>>>>>> Stashed changes

    def update(self):
        self.frame_count += 1
        self.get_input()
        
        # Store previous head position
        mem = self.program.mem  # Local reference for faster access
        self.last_head_pos = (mem[1], mem[2])
        
        if not self.program.shutdown:
            # Batch execute instructions
            for _ in range(10):
                if self.program.shutdown:
                    break
                self.program.step()
                
                # Debug head movement
                new_head = (mem[1], mem[2])
                if new_head != self.last_head_pos:
                    print(f"Head moved to: {new_head}")
                    self.last_head_pos = new_head
        else:
            new_head = (mem[1], mem[2])
            print("Program shut down")

    def draw(self):
<<<<<<< Updated upstream
        pyxel.cls(0)
        mem = self.program.mem
        
        # Draw game border (20x10 grid)
        border_color = 8  # Red
        pyxel.rectb(1*self.blocksize, 3*self.blocksize, 
                20*self.blocksize, 10*self.blocksize, border_color)
        
        # Draw grid lines (visual debugging)
        grid_color = 13  # Light gray
        # Vertical lines
        for x in range(20):
            pyxel.line((x+1)*self.blocksize, 3*self.blocksize,
                    (x+1)*self.blocksize, (10+3)*self.blocksize, grid_color)
        # Horizontal lines
        for y in range(10):
            pyxel.line(1*self.blocksize, (y+3)*self.blocksize,
                    (20+1)*self.blocksize, (y+3)*self.blocksize, grid_color)
        
        # Draw coordinate labels
        label_color = 7  # White
        for x in range(20):
            pyxel.text((x+1)*self.blocksize + 2, 3*self.blocksize - 10, str(x), label_color)
        for y in range(10):
            pyxel.text(1*self.blocksize - 15, (y+3)*self.blocksize + 5, str(y), label_color)
        
        # Draw snake segments with position indicators
        for i in range(3):
            seg_x, seg_y = mem[1 + i*2], mem[2 + i*2]
            color = 8 if i == 0 else 11  # Head pink, body blue
            
            # Draw segment
            pyxel.rect(
                (seg_x + 1)*self.blocksize + 1, 
                (seg_y + 3)*self.blocksize + 1,
                self.blocksize-2, 
                self.blocksize-2, 
                color
            )
            
            # Position label (head only)
            if i == 0:
                pyxel.text(
                    (seg_x + 1)*self.blocksize + 2,
                    (seg_y + 3)*self.blocksize + 2,
                    f"{seg_x},{seg_y}", 
                    7 if color == 8 else 0  # White on pink, black on blue
                )
        
        # Draw food with position indicator
        food_x, food_y = mem[50], mem[51]
        pyxel.rect(
            (food_x + 1)*self.blocksize + 1,
            (food_y + 3)*self.blocksize + 1,
            self.blocksize-2,
            self.blocksize-2,
            9  # Peach color
        )
        pyxel.text(
            (food_x + 1)*self.blocksize + 2,
            (food_y + 3)*self.blocksize + 2,
            f"{food_x},{food_y}", 
            7  # White text
        )
        
        # Debug info overlay
        direction_names = {8: "RIGHT", 4: "LEFT", 2: "DOWN", 1: "UP"}
        pyxel.text(5, 5, f"Head: ({mem[1]},{mem[2]})", 7)
        pyxel.text(5, 15, f"Food: ({mem[50]},{mem[51]})", 7)
        pyxel.text(5, 25, f"Facing: {direction_names.get(mem[48], 'UNKNOWN')}", 7)
=======
        if self.program.shutdown:
            None
            # self.game_over()
        else:
            pyxel.cls(0)
            mem = self.program.mem

            # Draw grid lines 
            grid_color = 13  # Light gray
            # Vertical lines
            for x in range(21):
                pyxel.line((x+1)*self.blocksize, 3*self.blocksize,
                           (x+1)*self.blocksize, (10+3)*self.blocksize, grid_color)
            # Horizontal lines
            for y in range(11):
                pyxel.line(1*self.blocksize, (y+3)*self.blocksize,
                           (20+1)*self.blocksize, (y+3)*self.blocksize, grid_color)

            # Draw coordinate labels
            label_color = 7  # White
            for x in range(20):
                pyxel.text((x+1)*self.blocksize + 2, 3 *
                           self.blocksize - 10, str(x), label_color)
            for y in range(10):
                pyxel.text(1*self.blocksize - 15, (y+3) *
                           self.blocksize + 5, str(y), label_color)

            for y in range(3, 13):
                for x in range(1, 21):
                    # get address line
                    offset = (y-3) * 20 + (x-1)
                    addr = 192 + offset // 4

                    # get shift
                    k = offset % 4

                    def concat(lower, upper):
                        return int(bin(upper)[2:].zfill(
                            4)[-4:]+bin(lower)[2:].zfill(4)[-4:], 2)

                    # if has data (snake or fruit)
                    if mem[addr] >> k & 0b1 == 1:
                        is_head = True if addr == concat(
                            mem[1], mem[2]) and mem[33] == pow(2, k) else False
                        is_fruit = True if addr == concat(
                            mem[50], mem[51]) and mem[52] == pow(2, k) else False

                        color = 8 if is_head else 9 if is_fruit else 11
                    # else:
                    #     color = 0

                        # Draw segment
                        pyxel.rect(
                            x*self.blocksize,
                            y*self.blocksize,
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
            
def mem_to_xy(low, high, bit_val):
    addr = (high << 4) | low
    offset = addr - 192
    x_base = offset % 5
    bit_index = {1: 0, 2: 1, 4: 2, 8: 3}.get(bit_val, 0)
    x = x_base * 4 + bit_index
    y = offset // 5
    return x, y


>>>>>>> Stashed changes

if __name__ == "__main__":
    program_file = "input.asm"
    os.system(f'python3 assembler.py {program_file} bin')
    
    with open("input.txt", "r") as f:
        Emulator([line.strip() for line in f])