SCALL 0
ADD R0,R1,R2
SCALL 0
ADD R0,R1,R3

Loop_in:
BRAZ R3,Loop_out

DIV R2,2,R4
MULT R4,2,R4
SEQ R2,R4,R4

BRANZ R4,Even_op
MULT R2,3,R2
ADD R2,1,R2
SUB R3,1,R3
JMP Loop_in,R31

Even_op:
DIV R2,2,R2
SUB R3,1,R3
JMP Loop_in,R31

Loop_out:
ADD R0,R2,R1
SCALL 1
STOP