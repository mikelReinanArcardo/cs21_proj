<<<<<<< Updated upstream
# === CONVENTIONS ===
# ra/rb = memory addresses
# MEM[0] = ticks
# cf = is_alive = 1
# RE = snake length
# MEM[1]-[32] = snake coordinates
# MEM[33]-[47] = LED per segment
# MEM[48] = orientation
# MEM[49] = points
# MEM[50]-[51] = food coords
# MEM[52] = food LED
=======
# Conventions
	# use ra and rb for memory addresses
	# MEM[0] = ticks
	# snake length = RE
	# snake coordinates address (Lower_Nibble-Upper_Nibble) = MEM[1]-MEM[2] to MEM[31]-MEM[32]
	# specific snake coordinate LED = MEM[33] to MEM[47]
	# orientation = MEM[48]
	# next_orientation = ioa
	# points = MEM[49]
	# food coordinate = MEM[50] + MEM[51] 
	# specific food LED = MEM[52]
	# MEM[53] - # of addresses per grid row
	# MEM[54] = is_alive
	# MEM[60] - temp storage of ioa
	# MEM[61] and MEM[62] - temp storage of new head
	# MEM[63]- temp storage of new head specific LED
	# MEM[64] - MEM[65] - temp storage when moving snake component
	# MEM[66]- temp storage of moving snake component specific LED
	# MEM[67]- temp storage of address grid row
	# MEM[192-196] row 0 cols 0-19
	# MEM[197-201] row 1 cols 0-19
	# MEM[202-206] row 2 cols 0-19
	# MEM[207-211] row 3 cols 0-19
	# MEM[212-216] row 4 cols 0-19
	# MEM[217-221] row 5 cols 0-19
	# MEM[222-226] row 6 cols 0-19
	# MEM[227-231] row 7 cols 0-19
	# MEM[232-236] row 8 cols 0-19
	# MEM[237-241] row 9 cols 0-19
>>>>>>> Stashed changes

# === INIT ===
acc 0
rarb 0
to-mba

r4 3
set-cf

acc 8
rarb 48
to-mba

rarb 49
acc 0
to-mba

# === INITIAL SNAKE ===
acc 5
<<<<<<< Updated upstream
rarb 1
to-mba

acc 5
=======
rarb 53
to-mba

# Set ROW indices of addresses, and store them in addr - 64.
# e.g. 192: 128, 193: 129, ...
# row 0
	acc 0
	rarb 128
	to-mba
	rarb 129
	to-mba
	rarb 130
	to-mba
	rarb 131
	to-mba
	rarb 132
	to-mba
# row 1
	acc 1
	rarb 133
	to-mba
	rarb 134
	to-mba
	rarb 135
	to-mba
	rarb 136
	to-mba
	rarb 137
	to-mba
# row 2
	acc 2
	rarb 138
	to-mba
	rarb 139
	to-mba
	rarb 140
	to-mba
	rarb 141
	to-mba
	rarb 142
	to-mba
# row 3
	acc 3
	rarb 143
	to-mba
	rarb 144
	to-mba
	rarb 145
	to-mba
	rarb 146
	to-mba
	rarb 147
	to-mba
# row 4
	acc 4
	rarb 148
	to-mba
	rarb 149
	to-mba
	rarb 150
	to-mba
	rarb 151
	to-mba
	rarb 152
	to-mba
# row 5
	acc 5
	rarb 153
	to-mba
	rarb 154
	to-mba
	rarb 155
	to-mba
	rarb 156
	to-mba
	rarb 157
	to-mba
# row 6
	acc 6
	rarb 158
	to-mba
	rarb 159
	to-mba
	rarb 160
	to-mba
	rarb 161
	to-mba
	rarb 162
	to-mba
# row 7
	acc 7
	rarb 163
	to-mba
	rarb 164
	to-mba
	rarb 165
	to-mba
	rarb 166
	to-mba
	rarb 167
	to-mba
# row 8
	acc 8
	rarb 168
	to-mba
	rarb 169
	to-mba
	rarb 170
	to-mba
	rarb 171
	to-mba
	rarb 172
	to-mba
# row 9
	acc 9
	rarb 173
	to-mba
	rarb 174
	to-mba
	rarb 175
	to-mba
	rarb 176
	to-mba
	rarb 177
	to-mba


# coordinates of the head
# self.snake_coords[0][0] = 6
# self.snake_coords[0][1] = 3

# <Instructions for setting snake part coordinates>
# set addr
rcrd 218
# store lower bits of addr 218
from-reg rc
rarb 1
to-mba
# store upper bits of addr 218
>>>>>>> Stashed changes
rarb 2
to-mba

acc 192
rarb 33
to-mba

acc 4
rarb 3
to-mba
acc 5
rarb 4
to-mba
acc 193
rarb 34
to-mba

acc 3
rarb 5
to-mba
acc 5
rarb 6
to-mba
acc 193
rarb 35
to-mba

# === INIT FOOD ===
acc 11
rarb 50
to-mba
acc 5
rarb 51
to-mba
acc 195
rarb 52
to-mba

# === MAIN LOOP ===
loop:
bnez-cf tick
shutdown

tick:
rarb 0
inc*-mba
from-mba
and 3
beqz move
b loop

# === MOVE HANDLING ===
move:
rarb 60
from-mba
beqz no_input
rarb 61
from-mba
beqz no_input

# problematic no input check

rcrd 1
from-mdc
rarb 60
to-mba
rcrd 2
from-mdc
rarb 61
to-mba

rcrd 1
from-mdc
to-reg ra
rcrd 2
from-mdc
to-reg rb
rcrd 33
from-mdc
xor*-mba

rcrd 3
from-mdc
to-reg ra
rcrd 4
from-mdc
to-reg rb
rcrd 34
from-mdc
xor*-mba

rcrd 5
from-mdc
to-reg ra
rcrd 6
from-mdc
to-reg rb
rcrd 35
from-mdc
xor*-mba

rarb 60
from-mba
beqz no_input
rarb 61
from-mba
beqz no_input

no_input:
b move_head

move_head:
rarb 48
from-mba
to-reg re

from-reg re
xor 8
beqz move_right
xor 4
beqz move_left
xor 2
beqz move_down
xor 1
beqz move_up

move_right:
rarb 1        
from-mba      
inc           
to-mba       
b update_segments

move_left:
rarb 1
from-mba      
dec          
to-mba        
b update_segments

move_down:
rarb 2        
from-mba      
inc           
to-mba        
b update_segments

move_up:
rarb 2
from-mba      
dec           
to-mba        
b update_segments


update_segments:
rarb 60
from-mba
rarb 3
to-mba
rarb 61
from-mba
rarb 4
to-mba

rarb 3
from-mba
rarb 5
to-mba
rarb 4
from-mba
rarb 6
to-mba

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

b loop

wall_collision:
clr-cf
shutdown