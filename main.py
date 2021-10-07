a_type = ["add", "and", "divide", "greaterthan", "lessthan", "or", "multiply", "subtract", "brancheq", "jump",
          "jumpandlink", "load", "store"]
v_type = ["set"]

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
    "set": "7"
}


def main(filename):
    file = open(filename, "r")
    text = file.read()
    instructions = text.split("\n")
    a_type_inst = []
    v_type_inst = []
    for inst in instructions:
        inst = inst.replace(" ", "")
        if inst.split("$")[0] in a_type:
            inst = inst.replace(",", "")
            a_type_inst.append(inst.split("$"))
        elif inst.split("$")[0] in v_type:
            inst = inst.replace(",", "$")
            v_type_inst.append(inst.split("$"))
        else:
            print(f"ERROR: Type cannot be identified for instruction: {inst}")
    print(f'A-Types: {a_type_inst}')
    print(f'V-Types: {v_type_inst}')
    a_type_translated = []
    for instr in a_type_inst:
        a_type_translated.append([x if x not in a_type and x not in a_type_dict.keys() else a_type_dict[x] for x in instr])
    print(a_type_translated)





    file.close()


if __name__ == '__main__':
    main("lilak.txt")
