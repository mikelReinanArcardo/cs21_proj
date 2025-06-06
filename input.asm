# Conventions
	# use ra and rb for memory addresses
	# MEM[0] = ticks
	# cf = is_alive = 1
	# snake length = RE
	# snake coordinates address (Lower_Nibble-Upper_Nibble) = MEM[1]-MEM[2] to MEM[31]-MEM[32]
	# specific snake coordinate LED = MEM[33] to MEM[47]
	# orientation = MEM[48]
	# next_orientation = ioa
	# points = MEM[49]
	# food coordinate = MEM[50] + MEM[51] 
	# specific food LED = MEM[52]

# Initialize Stuff
	# Snake Length
	# Snake Coordinates
	# Orientation
	# Game Tick / Timer
	# Points
	# is_dead variable
	# Food Coordinates - memory address of food coordinate

# Game Loop
# if not is_dead:
	# tick + 1

	# <movement>
	# SUBJECT TO CHANGE: every 25 ticks check if no food yet then spawn 1



# --- ACTUAL CODE ---
acc 0
rarb 0
# self.timer = 0
to-mba
# self.len = 3
r4 3
# self.is_alive = True
set-cf
# self.orientation = right  # [0b0 - up, 0b10 - down, 0b100 - left, 0b1000 - right]
acc 8
rarb 48
to-mba
# self.points = 0
rarb 49
acc 0
to-mba

# coordinates of the head
# self.snake_coords[0][0] = 6
# self.snake_coords[0][1] = 3

# <Instructions for setting snake part coordinates>
# set addr
rcrd 200
# store lower bits of addr 200
from-reg rc
rarb 1
to-mba
# store upper bits of addr 200
rarb 2
from-reg rd
to-mba
# store specific head LED (1, 2, 4, or 8)
acc 8
rarb 33
to-mba

# set body segment 1
rcrd 200
# store lower bits of addr
rarb 3
from-reg rc
to-mba
# store upper bits of addr 
rarb 4
from-reg rd
to-mba
# store specific LED (1, 2, 4, or 8)
acc 4
rarb 34
to-mba


# set body segment 2
rcrd 200
# store lower bits of addr
rarb 5
from-reg rc
to-mba
# store upper bits of addr 
rarb 6
from-reg rd
to-mba
# store specific LED (1, 2, 4, or 8)
acc 2
rarb 35
to-mba

# Draw Snake
rcrd 1
from-mdc
to-reg ra
rcrd 2
from-mdc
to-reg rb
rcrd 33
from-mdc
or*-mba

rcrd 3
from-mdc
to-reg ra
rcrd 4
from-mdc
to-reg rb
rcrd 34
from-mdc
or*-mba

rcrd 5
from-mdc
to-reg ra
rcrd 6
from-mdc
to-reg rb
rcrd 35
from-mdc
or*-mba

# set food coords
rcrd 230
# store lower bits of addr
rarb 50
from-reg rc
to-mba
# store upper bits of addr 
rarb 51
from-reg rd
to-mba
# store specific LED (1, 2, 4, or 8)
acc 4
rarb 52
to-mba

# show food in grid
rcrd 50
from-mdc
to-reg ra
rcrd 51
from-mdc
to-reg rb
rcrd 52
from-mdc
or*-mba

# Game Loop
# Stop if dead
loop:
bnez-cf tick 
shutdown

# add 1 to game tick
tick:
rarb 0
inc*-mba

from-mba
# TODO ADJUST TICK SPEED: might be too slow (every time acc overflows = 1 tick so every 16 ticks it moves)
beqz move
bnez loop

move:



