import pyxel


class Emulator:
    def __init__(self):
        self.blocksize = 16

        # Arch-242 program
        self.program = Program([])
        # TEMPORARY: assign snake head
        self.program.mem[200] = 0b00001110

        self.grid = [[0]*10 for _ in range(20)]

        pyxel.init(22*self.blocksize, 26*self.blocksize)

        self.init_game()

        pyxel.run(self.update, self.draw)

    def init_game(self):
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

    def update(self):
        ...

    def draw(self):
        self.update_grid()


Emulator()
