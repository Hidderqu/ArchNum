Start:
ADD R0,3,R2
ADD R0,3,R3
ADD R0,3,R4
ADD R0,1,R5
ADD R0,10,R6
ADD R0,19,R7

ADD R0,0,R8
ADD R0,0,R9
ADD R0,0,R10

End_Test:
BRAZ R4,Display_1

Line_Test:
BRAZ R3,New_Line

Col_Test:
BRAZ R2,New_Col
LOAD R0,R5,R8
LOAD R0,R6,R9
MULT R8,R9,R9
ADD R9,R10,R10
ADD R5,1,R5
ADD R6,1,R6
SUB R2,1,R2
JMP Col_Test,R31

New_Col:
STORE R0,R7,R10
ADD R7,1,R7
ADD R0,0,R10
SUB R5,3,R5
ADD R0,3,R2
SUB R3,1,R3
JMP Line_Test,R31

New_Line:
ADD R0,10,R6
ADD R0,3,R3
ADD R5,3,R5
SUB R4,1,R4
JMP End_Test,R31

Display_1:
ADD R0,19,R7
Display_2:
SLE R7,27,R8
BRAZ R8,End
LOAD R0,R7,R1
SCALL 1
ADD R7,1,R7
JMP Display_2,R31

End:
STOP