a_type = ["add", "and", "divide", "greaterthan", "lessthan", "or", "multiply", "subtract", "brancheq", "jump",
          "jumpandlink", "load", "store"]
v_type = ["set"]

pseudo = ["addval", "andval", "branchnoteq", "copy", "divideval", "equalto", "equaltoval", "greaterthanval",
          "lessthanval", "loadatval", "orval", "multiplyval", "storeatval", "subtractval"]
a_type_dict = {
    "add": "0",
    "and": "1",
    "divide": "2",
    "greaterthan": "3",
    "lessthan": "4",
    "or": "5",
    "multiply": "6",
    "subtract": "8",
    "brancheq": "9",
    "jump": "A",
    "jumpandlink": "B",
    "load": "C",
    "store": "D",
    "zero": "0",
    "ra": "1",
    "stack": "2",
    "global": "3",
    "frame": "4",
    "k0": "5",
    "a0": "6",
    "fa0": "7",
    "fa1": "8",
    "fr0": "9",
    "fr1": "A",
    "v0": "B",
    "v1": "C",
    "sv0": "D",
    "sv1": "E",
    "sv2": "F"
}

v_type_dict = {
    "set": "7",
    "zero": "0",
    "ra": "1",
    "stack": "2",
    "global": "3",
    "frame": "4",
    "k0": "5",
    "a0": "6",
    "fa0": "7",
    "fa1": "8",
    "fr0": "9",
    "fr1": "A",
    "v0": "B",
    "v1": "C",
    "sv0": "D",
    "sv1": "E",
    "sv2": "F"
}


def convert_a_type(instr):
    converted = [x if x not in a_type and x not in a_type_dict.keys() else a_type_dict[x] for x in instr]
    if instr[0] == "store":
        converted.append(converted[2])
        converted[2] = "0"
        return '0x' + ''.join(converted)
    # figure out jump, jumpandlink
    elif instr[0] == "jump":
        print(f"{instr=}")
        converted.extend(["0", converted[1]])
        converted[1] = "0"
        return '0x' + ''.join(converted)
    elif instr[0] == "jumpandlink":
    # converted.extend(["0", converted[1]])
    # converted[1] = "0"
    # return '0x' + ''.join(converted)
    # What are we doing here
        ...
    return '0x' + ''.join(converted)


def convert_v_type(instr):
    hex_string = str(hex(int(instr[2]))).replace("x", "").replace("0", "")
    if len(hex_string) == 2:
        pass
    elif len(hex_string) == 1:
        hex_string = "0" + hex_string
    else:
        print(f"ERROR: This is not length 1 or 2 in hex... :{hex_string}")
    return f"0x7{a_type_dict[instr[1]]}{hex_string.upper()}"


def convert_pseudo():
    ...


def main(filename):
    file = open(filename, "r")
    text = file.read()
    instructions = text.split("\n")
    a_type_inst = []
    v_type_inst = []
    all_translated = []

    for inst in instructions:
        inst = inst.replace(" ", "")
        if inst.split("$")[0] in a_type:
            inst = inst.replace(",", "")
            a_type_inst.append(inst.split("$"))
            all_translated.append(convert_a_type(inst.split("$")))
        elif inst.split("$")[0] in v_type:
            inst = inst.replace(",", "$")
            v_type_inst.append(inst.split("$"))
            all_translated.append(convert_v_type(inst.split("$")))
        elif inst.split("$")[0] in pseudo:
            pass
        else:
            print(f"ERROR: Type cannot be identified for instruction: {inst.replace('$', ' $')}")
    print(f'A-Types: {a_type_inst}')
    print(f'V-Types: {v_type_inst}')
    # a_type_translated = []
    #
    # for i, instr in enumerate(a_type_inst):
    #     converted = [x if x not in a_type and x not in a_type_dict.keys() else a_type_dict[x] for x in instr]
    #     a_type_translated.append(converted)
    #     if instr[0] == "store":
    #         converted.append(converted[2])
    #         converted[2] = "0"
    # a_type_translated = ['0x' + ''.join(x) for x in a_type_translated]
    # print(f"Machine A-Types: {a_type_translated}")

    # v_type_translated = []
    # for instr in v_type_inst:
    #     hex_string = str(hex(int(instr[2]))).replace("x", "").replace("0", "")
    #     if len(hex_string) == 2:
    #         pass
    #     elif len(hex_string) == 1:
    #         hex_string = "0" + hex_string
    #     else:
    #         print(f"ERROR: This is not length 1 or 2 in hex... :{hex_string}")
    #     v_type_translated.append(f"0x7{a_type_dict[instr[1]]}{hex_string.upper()}")
    # v_types_translated = [''.join(x) for x in v_type_translated]
    # print(f"Machine V-Types: {v_types_translated}")

    print(f"Machine ALL: {all_translated}")

    file.close()


if __name__ == '__main__':
    main("lilak.txt")
