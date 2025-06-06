            # Draw score
            score = self.program.mem[49] & 0xF
            pyxel.text(2 * self.blocksize, 2 * self.blocksize, 
                    f"Score: {score}", 7)
            
            # Draw tick count
            ticks = self.program.mem[0] & 0xFF
            pyxel.text(2 * self.blocksize, 4 * self.blocksize, 
                    f"Tick: {ticks}", 7)