# === CONVENTIONS ===
# use ra and rb for memory addresses
# MEM[0] = ticks
# cf = is_alive = 1
# snake length = RE
# snake coordinates address (lower-upper) = MEM[1]-[2] to MEM[31]-[32]
# LED per segment = MEM[33]-[47]
# orientation = MEM[48], next = ioa
# points = MEM[49]
# food = MEM[50] + [51], LED = MEM[52]

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

# === SNAKE COORDINATES ===
# Head: (6,3), segment 1: (5,3), segment 2: (4,3)

# Head
rcrd 200
from-reg rc
rarb 1
to-mba
rarb 2
from-reg rd
to-mba
acc 8
rarb 33
to-mba

# Segment 1
rcrd 200
from-reg rc
rarb 3
to-mba
rarb 4
from-reg rd
to-mba
acc 4
rarb 34
to-mba

# Segment 2
rcrd 200
from-reg rc
rarb 5
to-mba
rarb 6
from-reg rd
to-mba
acc 2
rarb 35
to-mba

# === DRAW INITIAL SNAKE ===
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

# === FOOD ===
rcrd 230
from-reg rc
rarb 50
to-mba
rarb 51
from-reg rd
to-mba
acc 4
rarb 52
to-mba

rcrd 50
from-mdc
to-reg ra
rcrd 51
from-mdc
to-reg rb
rcrd 52
from-mdc
or*-mba

# === MAIN LOOP ===
loop:
bnez-cf tick
shutdown

# === TICK ===
tick:
rarb 0
inc*-mba
from-mba
and 0          
beqz move
bnez loop

# === MOVE ===
move:
	# clear old segments
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

	# shift coords
	rarb 3
	from-mba
	rarb 5
	to-mba
	rarb 4
	from-mba
	rarb 6
	to-mba

	rarb 1
	from-mba
	rarb 3
	to-mba
	rarb 2
	from-mba
	rarb 4
	to-mba

	# get orientation
	rarb 48
	from-mba
	to-reg re

	# current head pos to ra/rb
	rarb 1
	from-mba
	to-reg ra
	rarb 2
	from-mba
	to-reg rb

	# get input
	from-pa
	beqz no_input
	to-reg re
	rarb 48
	to-mba

no_input:
	from-reg re
	xor 8
	beqz move_right
	from-reg re
	xor 4
	beqz move_left
	from-reg re
	xor 2
	beqz move_down
	b move_up

move_right:
	from-reg ra
	inc
	rarb 1
	to-mba
	b move_done

move_left:
	from-reg ra
	dec
	rarb 1
	to-mba
	b move_done

move_down:
	from-reg rb
	inc
	rarb 2
	to-mba
	b move_done

move_up:
	from-reg rb
	dec
	rarb 2
	to-mba

move_done:
	# redraw segments
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