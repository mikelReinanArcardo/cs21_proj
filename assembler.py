import sys
from convert import convert_inst

if __name__ == "__main__":
    # takes in two arguments as specified in the specs
    input_filename = sys.argv[1]
    format = sys.argv[2]
    output = []

    # read instructions
    with open(input_filename, "r") as f:
        for line in f:
            instr = line.strip().split(" ")

            # if whiteline or comment
            if not instr[0] or instr[0][0] == "#":
                continue

            # .byte directive
            if instr[0] == ".byte":
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
