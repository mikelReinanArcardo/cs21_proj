# test b-bit
# Test program for b-bit instruction
acc 5        
b-bit 0 42   
nop          

no_branch1:
acc 2        
b-bit 1 84   
             
shutdown     

branch2:
acc 4        
b-bit 2 126  
nop          

no_branch2:
acc 1        
b-bit 3 168  
             
shutdown     