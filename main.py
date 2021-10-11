a_type = ["add", "and", "divide", "greaterthan", "lessthan", "or", "multiply", "subtract", "brancheq", "jump",
          "jumpandlink", "load", "store", "equalto"]
v_type = ["set"]

pseudo = ["addval", "andval", "branchnoteq", "copy", "divideval", "equaltoval", "greaterthanval",
          "lessthanval", "loadatval", "loadaddr", "orval", "multiplyval", "storeatval", "subtractval", "jumpval"]
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
    "equalto": "E",
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
    elif instr[0] == "jump":
        converted.extend(["0", converted[1]])
        converted[1] = "0"
        return '0x' + ''.join(converted)
    elif instr[0] == "jumpandlink":
        converted.extend(["0", converted[1]])
        converted[1] = "0"
        return '0x' + ''.join(converted)
    elif instr[0] == "load":
        return '0x' + ''.join(converted) + "0"
    return '0x' + ''.join(converted)


def convert_v_type(instr):
    instr = [inst.replace(",", "") for inst in instr]
    hex_string = str(hex(int(instr[1]))).replace("x", "")
    hex_string = hex_string[1::]
    if len(hex_string) == 2:
        pass
    elif len(hex_string) == 1:
        hex_string = "0" + hex_string
    else:
        print(f"ERROR: This is not length 1 or 2 in hex... :{hex_string}")
    hex_string = hex_string.upper()
    return f"0x7{hex_string}{a_type_dict[instr[2].replace('$', '')]}"


def convert_pseudo(instr):
    set = []
    if len(instr) > 2:
        temp = instr[1].split(",")[0]
        instr.append(instr[2])
        instr[2] = instr[1].split(",")[1]
        instr[1] = temp
        set = ["set", "a0", instr[2]]

    if instr[0] == "addval":
        add = ["add", instr[1], "a0", instr[3]]
        return [convert_v_type(set), convert_a_type(add)]
    elif instr[0] == "subtractval":
        sub = ["subtract", instr[1], "a0", instr[3]]
        return [convert_v_type(set), convert_a_type(sub)]
    elif instr[0] == "multiplyval":
        mult = ["multiply", instr[1], "a0", instr[3]]
        return [convert_v_type(set), convert_a_type(mult)]
    elif instr[0] == "divideval":
        div = ["divide", instr[1], "a0", instr[3]]
        return [convert_v_type(set), convert_a_type(div)]
    elif instr[0] == "orval":
        or_ = ["or", instr[1], "a0", instr[3]]
        return [convert_v_type(set), convert_a_type(or_)]
    elif instr[0] == "andval":
        and_ = ["and", instr[1], "a0", instr[3]]
        return [convert_v_type(set), convert_a_type(and_)]
    elif instr[0] == "lessthanval":
        lessthan = ["lessthan", instr[1], "a0", instr[3]]
        return [convert_v_type(set), convert_a_type(lessthan)]
    elif instr[0] == "greaterthanval":
        greaterthan = ["greaterthan", instr[1], "a0", instr[3]]
        return [convert_v_type(set), convert_a_type(greaterthan)]
    elif instr[0] == "equaltoval":
        equalto = ["equalto", instr[1], "a0", instr[3]]
        return [convert_v_type(set), convert_a_type(equalto)]
    elif instr[0] == "storeatval":
        instr.append(instr[1].split(",")[1])
        instr[1] = instr[1].split(",")[0]
        set = ["set", "a0", instr[2]]
        store = ["store", instr[1], "a0"]
        return [convert_v_type(set), convert_a_type(store)]
    elif instr[0] == "loadatval":
        instr.append(instr[1].split(",")[1])
        instr[1] = instr[1].split(",")[0]
        set = ["set", "a0", instr[2]]
        load = ["load", instr[1], "a0"]
        return [convert_v_type(set), convert_a_type(load)]
    elif instr[0] == "copy":
        add = ["add", instr[1], "zero", instr[3]]
        return [convert_a_type(add)]
    elif instr[0] == "branchnoteq":
        instr[2] = instr[3].split(",")[0]
        instr[3] = instr[3].split(",")[1]
        set[2] = instr[3]
        eqto = ["equalto", instr[1], instr[2], instr[1]]
        brancheq = ["brancheq", instr[1], "zero", "a0"]
        return [convert_v_type(set), convert_a_type(eqto), convert_a_type(brancheq)]
    elif instr[0] == "loadaddr":
        immediate_length = 16
        temp = instr[1].split(",")
        instr = [instr[0], temp[0], temp[1]]
        num = instr[2]
        binnum = bin(int(num)).replace("0b", "")
        if len(binnum) < immediate_length:
            binnum = "0" * (immediate_length - len(binnum)) + binnum
        set1_num = binnum[0:int(immediate_length / 2)]
        set2_num = binnum[int(immediate_length / 2):immediate_length]
        set1 = ["set", instr[1], int(set1_num, 2)]
        set2 = ["set", "a0", int(set2_num, 2)]
        and_ = ["and", instr[1], "a0", instr[1]]
        return [convert_v_type(set1), convert_v_type(set2), convert_a_type(and_)]
    elif instr[0] == "jumpval":
        set = ["set", "a0", instr[1]]
        jumpandlink = ["jump", "a0"]
        return [convert_v_type(set), convert_a_type(jumpandlink)]
    elif instr[0] == "jumpandlinkval":
        set = ["set", "a0", instr[1]]
        jumpandlink = ["jump", "a0"]
        return [convert_v_type(set), convert_a_type(jumpandlink)]
    print(f"Did not match any known pseudo instructions: {instr}")
    return ["something went wrong", "something went wrong"]


def main(filename_read, filename_write):
    file = open(filename_read, "r")
    text = file.read()
    instructions = [inst for inst in text.split("\n") if inst != ""]
    a_type_inst = []
    v_type_inst = []
    all_translated = []
    file.close()

    for inst in instructions:
        if "jumpandlinkval" not in inst and "jumpval" not in inst:
            if "set" not in inst:
                inst = inst.replace(" ", "")
        else:
            all_translated.extend(convert_pseudo(inst.split(" ")))
        if inst.split("$")[0] in a_type:
            inst = inst.replace(",", "")
            a_type_inst.append(inst.split("$"))
            all_translated.append(convert_a_type(inst.split("$")))
        elif inst.split(" ")[0] in v_type:
            v_type_inst.append(inst.split(" "))
            all_translated.append(convert_v_type(inst.split(" ")))
        elif inst.split("$")[0] in pseudo:
            all_translated.extend(convert_pseudo(inst.split("$")))
        elif "jumpandlinkval" not in inst and "jumpval" not in inst:
            print(f"ERROR: Type cannot be identified for instruction: {inst.replace('$', ' $')}")

    print(f"Machine ALL: {all_translated}")
    print(f"Number of instructions: {len(all_translated)}")
    for inst in all_translated:
        print(inst)

    file = open(filename_write, "w")
    for instr in all_translated[0:len(all_translated) - 1]:
        file.write(instr)
        file.write("\n")
    file.write(all_translated[-1])


if __name__ == '__main__':
    main("lilak.txt", "translated.txt")
