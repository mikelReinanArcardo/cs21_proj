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
acc 1
rarb 54
to-mba
# self.orientation = right  # [0b0 - up, 0b10 - down, 0b100 - left, 0b1000 - right]
acc 8
rarb 48
to-mba
# self.points = 0
rarb 49
acc 0
to-mba

# set MEM[53] to 5 which indicates number of addresses per row
acc 5
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
# row 8
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
rcrd 218
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
rcrd 218
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
rarb 54
from-mba
bnez tick 
shutdown

tick:
# TODO: if need to add other stuff before moving put it here
b move

move:
# get next orientation
from-ioa
# temporarily set MEM[60] to ioa
rarb 60
to-mba
# get current orientation
rarb 48
# is moving vertically if acc becomes 0
from-mba
rot-r
rot-r
beqz is_vertical
b is_horizontal

# NOTE: b-bit should've worked but I think my implementation is buggy
is_vertical:
# we know that it can only move left or right from here
# prio right
rarb 60
; b-bit 3 right
from-mba
and 8
bnez right

; b-bit 2 left
from-mba
and 4
bnez left
# if no keys were pressed retain orientation
b new_head

is_horizontal:
# we know that it can only move up or down from here
# prio down
rarb 60
; b-bit 1 down
from-mba
and 2
bnez down

; b-bit 0 up
from-mba
and 1
bnez up
# if no keys were pressed retain orientation
b new_head

# set next orientation
up:
rarb 48
acc 1 
to-mba
b new_head

down:
rarb 48
acc 2 
to-mba
b new_head

left:
rarb 48
acc 4 
to-mba
b new_head

right:
rarb 48
acc 8 
to-mba
b new_head


new_head:
# Temporarily store new head
# get curr head address
# store curr head address in MEM[61] and MEM[62]
rcrd 1
from-mdc
rcrd 61
to-mdc

rcrd 2
from-mdc
rcrd 62
to-mdc

# get curr head LED then store in MEM[63]
rarb 33
from-mba
rarb 63
to-mba

# move according to orientation
rarb 48
from-mba
sub 1
beqz go_up
; b-bit 0 go_up
from-mba
sub 2
beqz go_down
from-mba
sub 4
beqz go_left
from-mba
sub 8
beqz go_right
; b-bit 1 go_down
; b-bit 2 go_left
; b-bit 3 go_right

go_up:
rarb 61
# suppose head is at addr x, to go up we subtract x by 5
# use sub-mba where acc is MEM[ra:rb] and MEM[ra:rb] is 5
from-mba
rarb 53
sub-mba
rarb 61
to-mba
# if cf is 1 this means we have to subtract one to the upper nibble
beqz-cf check_collision  
rarb 62
dec*-mba
b check_collision

go_down:
rarb 61
# suppose head is at addr x, to go down we add x by 5
from-mba
rarb 53
add-mba
rarb 61
to-mba
# if cf is 1 this means we have to add one to the upper nibble
beqz-cf check_collision  
rarb 62
inc*-mba
acc 0
beqz check_collision

go_left:
rarb 63
from-mba
rot-r
to-mba
# if nagzero ibig sabihin overflow
bnez check_collision
# pag nagzero set it to 0b1000 then move yung address - 1
acc 8
to-mba
# TODO: BOUNDARY CHECKS
rarb 61
from-mba
rarb 54
sub-mba
rarb 61
to-mba

beqz-cf check_collision  
rarb 62
dec*-mba
b check_collision

go_right:
rarb 63
from-mba
rot-l
to-mba
# if nagzero ibig sabihin overflow
bnez check_collision

acc 1
to-mba
# TODO: BOUNDARY CHECKS
rarb 61
from-mba
rarb 54
add-mba
rarb 61
to-mba

beqz-cf check_collision  
rarb 62
inc*-mba
b check_collision

check_collision:
# TODO
# MEM[61]-MEM[62] and MEM[63] currently contains the information of the next head

# BORDER COLLISION
	# vertical - just check if addr is < 192 or > 241
vertical_check:
	rcrd 61
	from-mdc
	to-reg ra
	rcrd 62
	from-mdc
	to-reg rb
	# if upper bits < 1100, it's mem addr is less than 192
	from-reg rb
	rot-r
	rot-r
	sub 3
	bnez did_collide
	# if upper bits is < 1111 then fs within range 
	from-reg rb
	sub 15
	bnez horizontal_check
	# otherwise check if yung lower nibble > 1
	from-reg ra
	rot-r
	bnez did_collide

	# horizontal - since we listed the rows of every address, just check if 
	# the orientation is horizontal, and new head has different row index
	# than curr head. There is a horizontal collision
horizontal_check:
	# get orientation
	rarb 48
	from-mba
	rot-r
	rot-r
	beqz self_check
	# get new head
	rarb 61
	from-mba
	to-reg rc
	rarb 62
	from-mba
	sub 4
	to-reg rd
	# MEM[rdrc] or from-mdc contains row index of next head
	# store it to MEM[67]
	rarb 67
	from-mdc
	to-mba
	# get curr head
	rarb 1
	from-mba
	to-reg rc
	rarb 2
	from-mba
	sub 4
	to-reg rd
	# compare acc (curr head index) - MEM[67] (next) head
	from-mdc
	rarb 67
	sub-mba
	# if acc is zero then we good, if not nag overflow siya
	bnez did_collide

self_check:
# SELF COLLISION
	# calls a function that goes through each snake segment and checks if its the same

# FOOD COLLISION

b move_snake

did_collide:
# Set is_alive to 0
rarb 54
acc 0
to-mba
b loop


# FUNCTIONS
# Now the new head should be at MEM[MEM[62]:MEM[61]] and its LED mapping is at MEM[63]
# We then start from the tail then copy its next
# NOTE: call and ret functions are buggy
move_snake:
# head
	# store information to MEM[64]-MEM[65] and MEM[66]
	rarb 1
	from-mba
	rarb 64
	to-mba

	rarb 2
	from-mba
	rarb 65
	to-mba

	rarb 33
	from-mba
	rarb 66
	to-mba

	# copy from MEM[61]-MEM[62] and MEM[63]
	rarb 61
	from-mba
	rarb 1
	to-mba

	rarb 62
	from-mba
	rarb 2
	to-mba

	rarb 63
	from-mba
	rarb 33
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

	call move_tmp

# component 1
	# store information to MEM[64]-MEM[65] and MEM[66]
	rarb 3
	from-mba
	rarb 64
	to-mba

	rarb 4
	from-mba
	rarb 65
	to-mba

	rarb 34
	from-mba
	rarb 66
	to-mba

	# copy from MEM[61]-MEM[62] and MEM[63]
	rarb 61
	from-mba
	rarb 3
	to-mba

	rarb 62
	from-mba
	rarb 4
	to-mba

	rarb 63
	from-mba
	rarb 34
	to-mba

	# Draw Snake
	rcrd 3
	from-mdc
	to-reg ra
	rcrd 4
	from-mdc
	to-reg rb
	rcrd 34
	from-mdc
	or*-mba

	call move_tmp

# component 2
	# store old information to MEM[64]-MEM[65] and MEM[66]
	rarb 5
	from-mba
	rarb 64
	to-mba

	rarb 6
	from-mba
	rarb 65
	to-mba

	rarb 35
	from-mba
	rarb 66
	to-mba

	# copy from MEM[61]-MEM[62] and MEM[63]
	rarb 61
	from-mba
	rarb 5
	to-mba

	rarb 62
	from-mba
	rarb 6
	to-mba

	rarb 63
	from-mba
	rarb 35
	to-mba

	# Draw Snake
	rcrd 5
	from-mdc
	to-reg ra
	rcrd 6
	from-mdc
	to-reg rb
	rcrd 35
	from-mdc
	or*-mba

	call move_tmp

done_move:
	# Remove snake tail 
	rcrd 61
	from-mdc
	to-reg ra
	rcrd 62
	from-mdc
	to-reg rb
	rcrd 63
	from-mdc
	xor*-mba
	b loop

# TODO: do the same for components 3-14

# TODO: may mali sa either call or ret function implementation
# when moving snake it moves MEM[64]-MEM[66] to MEM[61]-MEM[63]
move_tmp:
	rarb 64
	from-mba
	rarb 61
	to-mba

	rarb 65
	from-mba
	rarb 62
	to-mba

	rarb 66
	from-mba
	rarb 63
	to-mba
	ret
