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
    "store": "D"
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
        a_type_translated.append([x if x not in a_type or x not in a_type_dict.keys() else a_type_dict[x] for x in instr])
    print(a_type_translated)





    file.close()


if __name__ == '__main__':
    main("lilak.txt")
