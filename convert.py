# TODO:: RAISE ERRORS WHEN INSTRUCTION IS INVALID (e.g. instruction is longer than it should be, etc.)

# NOTE: we denote the term "special" for instructions that need other values to create their machine code / except for I-types since the instruction themselves are separate from the immediate value machine code conversion
# NOTE: -reg instructions are unclear sa specs, kindly check implementation below

# conversion table
instruction_encodings = {
    "rot-r": [0b00000000],
    "rot-l": [0b00000001],
    "rot-rc": [0b00000010],
    "rot-lc": [0b00000011],
    "from-mba": [0b00000100],
    "to-mba": [0b00000101],
    "from-mdc": [0b00000110],
    "to-mdc": [0b00000111],
    "addc-mba": [0b00001000],
    "add-mba": [0b00001001],
    "subc-mba": [0b00001010],
    "sub-mba": [0b00001011],
    "inc*-mba": [0b00001100],
    "dec*-mba": [0b00001101],
    "inc*-mdc": [0b00001110],
    "dec*-mdc": [0b00001111],
    # "inc*-reg": [0b0001RRR0]
    # "dec*-reg": [0b0001RRR1]
    "and-ba": [0b00011010],
    "xor-ba": [0b00011011],
    "or-ba": [0b00011100],
    "and*-mba": [0b00011101],
    "xor*-mba": [0b00011110],
    "or*-mba": [0b00011111],
    # "to-reg": [0b0010RRR0]
    # "from-reg": [0b0010RRR1]
    "clr-cf": [0b00101010],
    "set-cf": [0b00101011],
    "ret": [0b00101110],
    "from-ioa": [0b00110010],
    "inc": [0b00110001],
    "bcd": [0b00110110],
    "shutdown": [0b00110111, 0b00111110],
    "nop": [0b00111110],
    "dec": [0b00111111],

    # I-types
    "add": [0b01000000],
    "sub": [0b01000001],
    "and": [0b01000010],
    "xor": [0b01000011],
    "or": [0b01000100],
    "r4": [0b01000110],

    # "rarb <imm>2x": [0b0101XXXX, '0000YYYY'],

    # NOTE: sa specs it might be a typo na 0b0101... ksi if same sha sa rarb magiging conflicting

    # "rcrd <imm>2x": [0b0110XXXX, '0000YYYY'],
    # "acc <imm>x": [0b0111iiii],

    # B-types
    # "b-bit <k> <imm>2x": [0b100KKBBB, '0bAAAAAAAA'],
    # "bnz-a <imm>2x": [0b10100BBB, '0bAAAAAAAA'],
    # "bnz-b <imm>2x": [0b10101BBB, '0bAAAAAAAA'],
    # "beqz <imm>2x": [0b10110BBB, '0bAAAAAAAA'],
    # "bnez <imm>2x": [0b10111BBB, '0bAAAAAAAA'],
    # "beqz-cf <imm>2x": [0b11000BBB, '0bAAAAAAAA'],
    # "bnez-cf <imm>2x": [0b11001BBB, '0bAAAAAAAA'],
    # "b-timer <imm>2x": [0b11010BBB, '0bAAAAAAAA'],
    # "bnz-d <imm>2x": [0b11011BBB, '0bAAAAAAAA'],
    # "b <imm>2x": [0b1110BBBB, '0bAAAAAAAA'],
    # "call <imm>2x": [0b1111BBBB, '0bAAAAAAAA'],
}

special_patterns = ["rarb", "rcrd", "acc", "b-bit",
                    "bnz-a", "bnz-b", "beqz", "bnez", "beqz-cf", "bnez-cf", "b-timer", "bnz-d", "b", "call"]

reg_patterns = ["inc*-reg", "dec*-reg", "to-reg", "from-reg"]

register_names = ["RA", "RB", "RC", "RD", "RE"]


# assumes s is in binary format and converts it to clean machine code
def string_to_binary(s: str):
    return bin(int(s, 2))[2:].zfill(8)


def convert_special_inst(word, instr):
    i = special_patterns.index(word)

    # rarb/rcrd
    if 0 <= i <= 1:
        imm = bin(int(instr[-1]))[2:].zfill(8)
        x = imm[4:]
        y = imm[:4]
        pat1 = "0101" if i == 0 else "0110"
        pat2 = "0000"
        return [string_to_binary(pat1+x), string_to_binary(pat2+y)]

    # acc
    elif i == 2:
        pat1 = "0111"
        imm = bin(int(instr[-1]))[2:].zfill(8)
        # truncate last 4 LSB?
        pat2 = imm[-4:]
        return [string_to_binary(pat1+pat2)]

    # b-bit
    elif i == 3:
        k = bin(int(instr[1]))[2:].zfill(2)
        imm = bin(int(instr[-1]))[2:].zfill(11)
        return [string_to_binary("100"+k[-2:]+imm[-11:-8]), string_to_binary(imm[-8:])]

    # bnz-a
    elif i == 4:
        imm = bin(int(instr[-1]))[2:].zfill(11)
        return [string_to_binary("10100"+imm[-11:-8]), string_to_binary(imm[-8:])]

    # bnz-b
    elif i == 5:
        imm = bin(int(instr[-1]))[2:].zfill(11)
        return [string_to_binary("10101"+imm[-11:-8]), string_to_binary(imm[-8:])]

    # beqz
    elif i == 6:
        imm = bin(int(instr[-1]))[2:].zfill(11)
        return [string_to_binary("10110"+imm[-11:-8]), string_to_binary(imm[-8:])]

    # bnez
    elif i == 7:
        imm = bin(int(instr[-1]))[2:].zfill(11)
        return [string_to_binary("10111"+imm[-11:-8]), string_to_binary(imm[-8:])]

    # beqz-cf
    elif i == 8:
        imm = bin(int(instr[-1]))[2:].zfill(11)
        return [string_to_binary("11000"+imm[-11:-8]), string_to_binary(imm[-8:])]

    # bnez-cf
    elif i == 9:
        imm = bin(int(instr[-1]))[2:].zfill(11)
        return [string_to_binary("11001"+imm[-11:-8]), string_to_binary(imm[-8:])]

    # b-timer
    elif i == 10:
        imm = bin(int(instr[-1]))[2:].zfill(11)
        return [string_to_binary("11010"+imm[-11:-8]), string_to_binary(imm[-8:])]

    # bnz-d
    elif i == 11:
        imm = bin(int(instr[-1]))[2:].zfill(11)
        return [string_to_binary("11011"+imm[-11:-8]), string_to_binary(imm[-8:])]

    # b
    elif i == 12:
        imm = bin(int(instr[-1]))[2:].zfill(12)
        return [string_to_binary("1110"+imm[-12:-8]), string_to_binary(imm[-8:])]

    # call
    elif i == 13:
        imm = bin(int(instr[-1]))[2:].zfill(12)
        return [string_to_binary("1111"+imm[-12:-8]), string_to_binary(imm[-8:])]


# slicing of space separted instructions should be done in assembler.py
def convert_inst(instr: list[str]):
    output = []
    for word in instr:

        # check if word is in instruction_encodings
        if word.lower() in instruction_encodings:
            encoding = instruction_encodings[word.lower()]
            for machine_code in encoding:
                # 5 -> binary -> binary of width 8
                output.append(string_to_binary(bin(machine_code)))

        # instructions that require immediate or reg values
        elif word in special_patterns:
            return convert_special_inst(word, instr)

        # instructions that need register_names
        elif word in reg_patterns:
            if instr[-1].upper() not in register_names:
                raise TypeError(f"Invalid Register: {instr[-1]}")

            reg_index = register_names.index(instr[-1].upper())
            if reg_index > 4:
                raise TypeError(f"Can't Use Register: {instr[-1]}")

            inst_i = reg_patterns.index(word)
            pat1 = "0001" if inst_i < 2 else "0010"
            pat2 = "0" if inst_i % 2 == 0 else "1"
            return [string_to_binary(pat1+bin(reg_index)[2:].zfill(3)[-3:]+pat2)]

        # integers
        elif word.isdigit():
            output.append(string_to_binary(
                "0000"+bin(int(word))[2:].zfill(4)[-4:]))

        # invalid instructions
        else:
            raise TypeError(f"Invalid Instruction: {' '.join(instr)}")

    return output


# -- TESTING --
# print(convert_inst(["rot-r"]))
# print(convert_inst(["rot-l"]))
# print(convert_inst(["rot-rc"]))
# print(convert_inst(["rot-lc"]))
# print(convert_inst(["from-mba"]))
# print(convert_inst(["to-mba"]))
# print(convert_inst(["from-mdc"]))
# print(convert_inst(["to-mdc"]))
# print(convert_inst(["addc-mba"]))
# print(convert_inst(["add-mba"]))
# print(convert_inst(["subc-mba"]))
# print(convert_inst(["sub-mba"]))
# print(convert_inst(["inc*-mba"]))
# print(convert_inst(["dec*-mba"]))
# print(convert_inst(["inc*-mdc"]))
# print(convert_inst(["dec*-mdc"]))
# print(convert_inst(["and-ba"]))
# print(convert_inst(["xor-ba"]))
# print(convert_inst(["or-ba"]))
# print(convert_inst(["and*-mba"]))
# print(convert_inst(["xor*-mba"]))
# print(convert_inst(["or*-mba"]))
# print(convert_inst(["clr-cf"]))
# print(convert_inst(["set-cf"]))
# print(convert_inst(["set-ei"]))
# print(convert_inst(["clr-ei"]))
# print(convert_inst(["ret"]))
# print(convert_inst(["retc"]))
# print(convert_inst(["from-pa"]))
# print(convert_inst(["inc"]))
# print(convert_inst(["to-ioa"]))
# print(convert_inst(["to-iob"]))
# print(convert_inst(["to-ioc"]))
# print(convert_inst(["bcd"]))
# print(convert_inst(["shutdown"]))
# print(convert_inst(["timer-start"]))
# print(convert_inst(["timer-end"]))
# print(convert_inst(["from-timerl"]))
# print(convert_inst(["from-timerh"]))
# print(convert_inst(["to-timerl"]))
# print(convert_inst(["to-timerh"]))
# print(convert_inst(["nop"]))
# print(convert_inst(["dec"]))

# print("Special R-types")
# reg = "ra"
# print(convert_inst(["inc*-reg", reg]))
# print(convert_inst(["dec*-reg", reg]))
# print(convert_inst(["to-reg", reg]))
# print(convert_inst(["from-reg", reg]))
# reg = "rB"
# print(convert_inst(["inc*-reg", reg]))
# print(convert_inst(["dec*-reg", reg]))
# print(convert_inst(["to-reg", reg]))
# print(convert_inst(["from-reg", reg]))
# reg = "Rc"
# print(convert_inst(["inc*-reg", reg]))
# print(convert_inst(["dec*-reg", reg]))
# print(convert_inst(["to-reg", reg]))
# print(convert_inst(["from-reg", reg]))
# reg = "RD"
# print(convert_inst(["inc*-reg", reg]))
# print(convert_inst(["dec*-reg", reg]))
# print(convert_inst(["to-reg", reg]))
# print(convert_inst(["from-reg", reg]))
# reg = "rE"
# print(convert_inst(["inc*-reg", reg]))
# print(convert_inst(["dec*-reg", reg]))
# print(convert_inst(["to-reg", reg]))
# print(convert_inst(["from-reg", reg]))
#
# imm = "2047"
# print("I-types")
# print(convert_inst(["add", imm]))
# print(convert_inst(["sub", imm]))
# print(convert_inst(["and", imm]))
# print(convert_inst(["xor", imm]))
# print(convert_inst(["or", imm]))
# print(convert_inst(["r4", imm]))
# print(convert_inst(["timer", imm]))
# print(convert_inst(["rarb", imm]))
# print(convert_inst(["rcrd", imm]))
# print(convert_inst(["acc", imm]))
#
# print("B-types")
# print(convert_inst(["b-bit", "111111", imm]))
# print(convert_inst(["bnz-a", imm]))
# print(convert_inst(["bnz-b", imm]))
# print(convert_inst(["beqz", imm]))
# print(convert_inst(["bnez", imm]))
# print(convert_inst(["beqz-cf", imm]))
# print(convert_inst(["bnez-cf", imm]))
# print(convert_inst(["b-timer", imm]))
# print(convert_inst(["bnz-d", imm]))
# print(convert_inst(["b", imm]))
# print(convert_inst(["call", imm]))

# -- Error Testing --
# reg = "rf"
# print(convert_inst(["inc*-reg", reg]))
# print(convert_inst(["dec*-reg", reg]))
# print(convert_inst(["to-reg", reg]))
# print(convert_inst(["from-reg", reg]))
# reg = "abcdafdfa"
# print(convert_inst(["inc*-reg", reg]))
# print(convert_inst(["dec*-reg", reg]))
# print(convert_inst(["to-reg", reg]))
# print(convert_inst(["from-reg", reg]))

# print(convert_inst(["This is an invalid instruction"]))
# print(convert_inst(["from-reg", "ra", "ra", "some random stuff"]))
# print(convert_inst(["call", imm]))
