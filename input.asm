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
rarb 1
to-mba

acc 5
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