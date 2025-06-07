import os
import pyxel
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
        pyxel.run(self.update, self.draw)

    def get_input(self):
        """Optimized input handling with direct key checks"""
        self.program.ioa = (
            0b1000 * pyxel.btn(pyxel.KEY_RIGHT) |  # Changed from btnp to btn
            0b0100 * pyxel.btn(pyxel.KEY_LEFT) |
            0b0010 * pyxel.btn(pyxel.KEY_DOWN) |
            0b0001 * pyxel.btn(pyxel.KEY_UP)
        )
        
            

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

if __name__ == "__main__":
    program_file = "input.asm"
    os.system(f'python3 assembler.py {program_file} bin')
    
    with open("input.txt", "r") as f:
        Emulator([line.strip() for line in f])