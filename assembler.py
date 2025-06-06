import sys
from convert import convert_inst

if __name__ == "__main__":
    # takes in two arguments as specified in the specs
    input_filename = sys.argv[1]
    format = sys.argv[2]
    output = []

    # keep track of label names:
    labels = dict()

    branch_instr = ["b-bit", "bnz-a", "bnz-b", "beqz", "bnez",
                    "beqz-cf", "bnez-cf", "b-timer", "bnz-d", "b", "call"]

    pc = 0

    # find all labels first in the instruction file and track valid instructions
    with open(input_filename, "r", encoding="utf-8") as f:
        for i, line in enumerate(f):
            instr = line.strip().split(" ")

            # if whiteline or comment
            if not instr[0] or instr[0][0] in ["#", ";"]:
                continue

            # set label PC
            elif instr[0][-1] == ':':
                label = instr[0][:-1].lower()
                if label not in labels:
                    # NOTE: if +2 it's possible na last line is a label so it might overflow
                    labels[label] = bin(pc)[2:].zfill(8)
                pc += 2

            elif instr[0] in branch_instr and not instr[1].isdigit():
                pc += 2

            elif instr[0] == ".byte":
                pc += 1
            else:
                # convert to machine code
                machine_code = convert_inst(instr)
                if not machine_code:
                    raise SyntaxError(f"Invalid Instruction: {line}")
                pc += len(machine_code)

    # read instructions
    with open(input_filename, "r", encoding="utf-8") as f:
        for line in f:
            instr = line.strip().split(" ")

            machine_code = []

            # if whiteline or comment
            if not instr[0] or instr[0][0] in ["#", ";"]:
                continue

            # ADDITIONAL LABEL INSTRUCTION
            # USE CASE: Similar to comments, this should NOT be in-line with another instruction
            elif instr[0][-1] == ':':
                # set to unused machine code
                machine_code = ["01001000"]
                label = instr[0][:-1].lower()
                machine_code.append(labels[label])

            # convert labels to immediate for branch instructions
            elif instr[0] in branch_instr and not instr[1].isdigit():
                print(instr)
                label = instr[1].lower()
                if label not in labels:
                    raise SyntaxError(f"{label} is an unknown label")
                instr[1] = str(int(labels[label], 2))
                print(instr)
                machine_code = convert_inst(instr)

            # .byte directive
            elif instr[0] == ".byte":
                machine_code = [bin(int(instr[1], 16))[2:].zfill(8)]
            else:
                # convert to machine code
                machine_code = convert_inst(instr)

            if not machine_code:
                raise SyntaxError(f"Invalid Instruction: {line}")

            # machine code line
            for mcl in machine_code:
                if format == "hex":
                    output.append(hex(int(mcl, 2))[2:].zfill(2).upper())
                else:
                    output.append(mcl)

    output_filename = input_filename[:input_filename.index(".")] + ".txt"
    with open(output_filename, "w") as f:
        for line in output:
            f.write(line)
            f.write("\n")
