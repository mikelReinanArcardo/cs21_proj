class Program:
    def __init__(self, instr_mem):
        # Memory with up to 256 addresses and 8 bits each
        self.mem = [0b00000000 for _ in range(256)]
        self.instr_mem = instr_mem

        self.pc = 0b0000000000000000

        self.acc = 0b0000
        self.cf = 0b0

        # 0 - ra, 1 - rb, ... 4 - re
        self.reg = [0b0000, 0b0000, 0b0000, 0b0000, 0b0000]

        self.temp = 0b0000000000000000
        self.ioa = 0b0000

        # checks if its the first machine code of the shutdown instruction
        self.is_shutdown = False
        # if is_shutdown and you found the next machine code of shutdown instruction simultaneously, then completely shut the program down
        self.shutdown = False

        # for handling extra inputs
        self.is_imm = False
        self.is_branch = False

        self.last_instr = ""

        self.next_pc = 1

        self.labels = dict()
        self.is_label = False

        self.jump = False

    def run(self):
        while self.pc < len(self.instr_mem):
            self.run_instr()
            self.iterate_pc()

            # for debugging
            # print("pc:", self.pc)
            # print("acc:", self.acc)

            if self.shutdown:
                break

    def iterate_pc(self):
        if self.jump:
            self.pc = self.next_pc
            self.jump = False
        else:
            self.pc += 1

    def run_instr(self):
        if self.pc >= len(self.instr_mem):
            # do nothing if no more valid instructions
            return
        self.decode(self.instr_mem[self.pc])

    def decode(self, instr: str):
        # for debugging
        # print("pc:", self.pc)
        # print("acc:", self.acc)
        # print()

        if self.is_branch:
            # b-bit
            if self.last_instr[:3] == "100":
                k = int(self.last_instr[3:5], 2)
                b = self.last_instr[5:]
                imm = int(b+instr, 2)
                # if k-th bit is 1 from right
                if (self.acc >> k) & 0b1 == 0b1:
                    # keep first five bits
                    tmp = self.pc & 0b1111100000000000
                    self.next_pc = tmp | imm
                    self.jump = True

            # bnz-a
            elif self.last_instr[:5] == "10100":
                b = self.last_instr[5:]
                imm = int(b+instr, 2)
                if self.reg[0] != 0:
                    tmp = self.pc & 0b1111100000000000
                    self.next_pc = tmp | imm
                    self.jump = True

            # bnz-b
            elif self.last_instr[:5] == "10101":
                b = self.last_instr[5:]
                imm = int(b+instr, 2)
                if self.reg[1] != 0:
                    tmp = self.pc & 0b1111100000000000
                    self.next_pc = tmp | imm
                    self.jump = True

            # beqz
            elif self.last_instr[:5] == "10110":
                b = self.last_instr[5:]
                imm = int(b+instr, 2)
                if self.acc == 0:
                    tmp = self.pc & 0b1111100000000000
                    self.next_pc = tmp | imm
                    self.jump = True

            # bnez
            elif self.last_instr[:5] == "10111":
                b = self.last_instr[5:]
                imm = int(b+instr, 2)
                if self.acc != 0:
                    tmp = self.pc & 0b1111100000000000
                    self.next_pc = tmp | imm
                    self.jump = True

            # beqz-cf
            elif self.last_instr[:5] == "11000":
                b = self.last_instr[5:]
                imm = int(b+instr, 2)
                if self.cf == 0:
                    tmp = self.pc & 0b1111100000000000
                    self.next_pc = tmp | imm
                    self.jump = True

            # bnez-cf
            elif self.last_instr[:5] == "11001":
                b = self.last_instr[5:]
                imm = int(b+instr, 2)
                if self.cf != 0:
                    tmp = self.pc & 0b1111100000000000
                    self.next_pc = tmp | imm
                    self.jump = True

            # bnz-d
            elif self.last_instr[:5] == "11011":
                b = self.last_instr[5:]
                imm = int(b+instr, 2)
                if self.reg[3] != 0:
                    tmp = self.pc & 0b1111100000000000
                    self.next_pc = tmp | imm
                    self.jump = True

            # b
            elif self.last_instr[:4] == "1110":
                b = self.last_instr[4:]
                imm = int(b+instr, 2)
                tmp = self.pc & 0b1111000000000000
                self.next_pc = tmp | imm
                self.jump = True

            # call
            elif self.last_instr[:4] == "1111":
                # although this should be +2, nabawasan di kasi accounted for
                # yung unang part ng machine code nito kaya +1 lang
                self.temp = (self.pc + 1) & 0b1111111111111111
                b = self.last_instr[4:]
                imm = int(b+instr, 2) & 0b0000111111111111
                tmp = self.pc & 0b1111000000000000
                self.next_pc = tmp | imm
                self.jump = True

            self.is_branch = False
            return

        elif self.is_imm:
            # check if first 4 bits is 0000
            if instr[:4] != "0000":
                self.is_imm = False
                return

            if self.last_instr == "01000000":
                self.acc = (self.acc + int(instr, 2)) & 0b1111
            elif self.last_instr == "01000001":
                self.acc = (self.acc - int(instr, 2)) & 0b1111
            elif self.last_instr == "01000010":
                self.acc = (self.acc & int(instr, 2)) & 0b1111
            elif self.last_instr == "01000011":
                self.acc = (self.acc ^ int(instr, 2)) & 0b1111
            elif self.last_instr == "01000100":
                self.acc = (self.acc | int(instr, 2)) & 0b1111
            elif self.last_instr == "01000110":
                self.reg[4] = int(instr, 2) & 0b1111

            # rarb or rcrd
            elif self.last_instr[:4] == "0101":
                self.reg[0] = int(self.last_instr[4:], 2) & 0b1111
                self.reg[1] = int(instr[4:], 2) & 0b1111
            elif self.last_instr[:4] == "0110":
                self.reg[2] = int(self.last_instr[4:], 2) & 0b1111
                self.reg[3] = int(instr[4:], 2) & 0b1111

        elif self.is_shutdown:
            if instr == "00111110":
                self.shutdown = True
                return

        elif self.is_label:
            # do nothing
            self.is_label = False

        else:
            # rot-r
            if instr == "00000000":
                self.acc = (self.acc >> 1) & 0b1111
            # rot-l
            elif instr == "00000001":
                self.acc = (self.acc << 1) & 0b1111
            # rot-rc
            elif instr == "00000010":
                concat = (self.cf << 4) | self.acc
                res = concat >> 1
                self.acc = res & 0b1111
                self.cf = (res & 0b10000) >> 4
            # rot-lc
            elif instr == "00000011":
                concat = (self.cf << 4) | self.acc
                res = concat << 1
                self.acc = res & 0b1111
                self.cf = (res & 0b10000) >> 4
            # from-mba
            elif instr == "00000100":
                concat = (self.reg[1] << 4) | self.reg[0]
                self.acc = self.mem[concat] & 0b1111
            # to-mba
            elif instr == "00000101":
                concat = (self.reg[1] << 4) | self.reg[0]
                self.mem[concat] = self.acc & 0b11111111
            # from-mdc
            elif instr == "00000110":
                concat = (self.reg[3] << 4) | self.reg[2]
                self.acc = self.mem[concat] & 0b1111
            # to-mdc
            elif instr == "00000111":
                concat = (self.reg[3] << 4) | self.reg[2]
                self.mem[concat] = self.acc & 0b11111111
            # addc-mba
            elif instr == "00001000":
                concat = (self.reg[1] << 4) | self.reg[0]
                res = self.acc + self.mem[concat] + self.cf
                self.acc = res & 0b1111
                self.cf = 0b1 if res >= 16 else 0b0
            # add-mba
            elif instr == "00001001":
                concat = (self.reg[1] << 4) | self.reg[0]
                res = self.acc + self.mem[concat]
                self.acc = res & 0b1111
                self.cf = 0b1 if res >= 16 or res < 0 else 0b0
            # subc-mba
            elif instr == "00001010":
                concat = (self.reg[1] << 4) | self.reg[0]
                res = self.acc - self.mem[concat] + self.cf
                self.acc = res & 0b1111
                self.cf = 0b1 if res < 0 or res > 15 else 0b0
            # sub-mba
            elif instr == "00001011":
                concat = (self.reg[1] << 4) | self.reg[0]
                res = self.acc - self.mem[concat]
                self.acc = res & 0b1111
                self.cf = 0b1 if res < 0 or res > 15 else 0b0

            # inc*-mba
            elif instr == "00001100":
                concat = (self.reg[1] << 4) | self.reg[0]
                self.mem[concat] = (self.mem[concat] + 1) & 0b11111111

            # dec*-mba
            elif instr == "00001101":
                concat = (self.reg[1] << 4) | self.reg[0]
                self.mem[concat] = (self.mem[concat] - 1) & 0b11111111

            # inc*-mdc
            elif instr == "00001110":
                concat = (self.reg[3] << 4) | self.reg[2]
                self.mem[concat] = (self.mem[concat] + 1) & 0b11111111

            # dec*-mdc
            elif instr == "00001111":
                concat = (self.reg[3] << 4) | self.reg[2]
                self.mem[concat] = (self.mem[concat] - 1) & 0b11111111

            # inc*-reg <reg>
            elif instr[:4] == "0001" and instr[-1] == "0" and int(instr[-4:-1], 2) <= 4:
                r = int(instr[-4:-1], 2)
                self.reg[r] = (self.reg[r] + 1) & 0b1111

            # dec*-reg <reg>
            elif instr[:4] == "0001" and instr[-1] == "1" and int(instr[-4:-1], 2) <= 4:
                r = int(instr[-4:-1], 2)
                self.reg[r] = (self.reg[r] - 1) & 0b1111

            # and-ba
            elif instr == "00011010":
                concat = (self.reg[1] << 4) | self.reg[0]
                self.acc = (self.acc & self.mem[concat]) & 0b1111

            # xor-ba
            elif instr == "00011011":
                concat = (self.reg[1] << 4) | self.reg[0]
                self.acc = (self.acc ^ self.mem[concat]) & 0b1111

            # or-ba
            elif instr == "00011100":
                concat = (self.reg[1] << 4) | self.reg[0]
                self.acc = (self.acc | self.mem[concat]) & 0b1111

            # and*-ba
            elif instr == "00011101":
                concat = (self.reg[1] << 4) | self.reg[0]
                self.mem[concat] = (self.acc & self.mem[concat]) & 0b11111111

            # xor*-ba
            elif instr == "00011110":
                concat = (self.reg[1] << 4) | self.reg[0]
                self.mem[concat] = (self.acc ^ self.mem[concat]) & 0b11111111

            # or*-ba
            elif instr == "00011111":
                concat = (self.reg[1] << 4) | self.reg[0]
                self.mem[concat] = (self.acc | self.mem[concat]) & 0b11111111

            # to-reg <reg>
            elif instr[:4] == "0010" and instr[-1] == "0" and int(instr[-4:-1], 2) <= 4:
                r = int(instr[-4:-1], 2)
                self.reg[r] = self.acc

            # from-reg <reg>
            elif instr[:4] == "0010" and instr[-1] == "1" and int(instr[-4:-1], 2) <= 4:
                r = int(instr[-4:-1], 2)
                self.acc = self.reg[r]

            # clr-cf
            elif instr == "00101010":
                self.cf = 0

            # set-cf
            elif instr == "00101011":
                self.cf = 1

            # ret
            elif instr == "00101110":
                # get first 4 bits
                four_bits = self.pc & 0b1111000000000000
                twelve_bits = self.temp & 0b0000111111111111
                # Since may pc + 1 pa after neto, may offset na -1
                self.pc = ((four_bits | twelve_bits) - 1) & 0b1111111111111111
                self.temp = 0b0000000000000000

            # from-ioa
            elif instr == "00110010":
                self.acc = self.ioa & 0b1111

            # inc
            elif instr == "00110001":
                self.acc = (self.acc + 1) & 0b1111

            # bcd
            elif instr == "00110110":
                if self.acc >= 10 or self.cf == 1:
                    self.acc = (self.acc + 6) & 0b1111
                    self.cf = 0b1

            # shutdown
            elif instr == "00110111":
                self.is_shutdown = True
                return

            # nop
            elif instr == "00111110":
                ...

            # dec
            elif instr == "00111111":
                self.acc = (self.acc - 1) & 0b1111

            # Immediate instructions
            # See each opeartion at the top
            elif instr in ["01000000", "01000001", "01000010", "01000011", "01000100", "01000110"] or instr[:4] in ["0101", "0110"]:
                self.last_instr = instr
                self.is_imm = True
                return

            # acc
            elif instr[:4] == "0111":
                self.acc = int(instr[4:], 2) & 0b1111

            # bit instructions
            elif instr[:3] in ["100", "101", "110", "111"]:
                self.last_instr = instr
                self.is_branch = True
                return

            # label
            elif instr == "01001000":
                self.is_label = True
                return

        # don't forget to revert this
        self.is_shutdown = False
        self.shutdown = False
        self.is_imm = False
        self.last_instr = ""
        self.is_branch = False
        self.is_label = False


# test = Program([])
# print(test.acc)
# test.decode("00000101")
# print(test.acc)
# test.decode("00000001")
# print(test.acc)
# test.decode("00000000")
# print(test.acc)
# test.decode("00000010")
# print(test.acc)
# print(test.cf)
# test.decode("00000011")
# print(test.acc)
# print(test.cf)
# test.decode("00000100")
# print(test.acc)

# -- Sub Test --
# test.decode("00000101")  # MEM[rb:ra] = acc
# print(test.acc)
# test.acc = 4  # 0b0100
# acc = acc - mem[rb:ra] + cf = 0b0100 - 0b1111 + 0b0 = 0b10101 -> 0b0101 = 5
# cf = 1
# test.decode("00001010")
# print(test.acc)
# print(test.cf)

# -- Test 3--
# (test.decode("00011100"))
# (test.decode("00010000"))
# (test.decode("00010010"))
# (test.decode("00010100"))
# (test.decode("00010110"))
# (test.decode("00011000"))
# (test.decode("00011010"))

# -- Test 4 --
# test.decode("01000000")
# test.decode("01000011")
# print(test.acc)
# test.decode("01000000")
# test.decode("00000011")
# print(test.acc)
# test.decode("01000001")
# test.decode("00000011")
# print(test.acc)
