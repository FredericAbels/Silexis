import json
import random
import sys

path_sildict = "../silexicon/dictionary.json"
path_phonemes = "../silexicon/phonemes.json"

def ensure_path(d, *keys):
    for key in keys:
        d = d.setdefault(key, {})
    return d        

def load_dict(file_path):
    with open(file_path, "r") as file:
        return json.load(file)   

def save_dict(sildict):
    with open(path_sildict, "w") as f:
        json.dump(sildict, f, indent=4, ensure_ascii=False)


def main():
    sildict = load_dict(path_sildict)
    phondict = load_dict(path_phonemes)

    example1 = "example 60 4"
    example2 = "example 8245 6"

    print("Options:")
    print("convert0 (from add_to_dict.json)")
    print("0 [eng] [F] [tier]")
    print("1 " + example1)
    print("2 " + example2)
    print("3 [F] [NP] [P] [eng]")
    print("4 (refresh dictionary)")
    
    if sys.argv[0] == None:
        cmd = input()
        if cmd == "1":
            cmd = "1 " + example1
        if cmd == "2":
            cmd = "2 " + example2

        scmd = cmd.split()
    else:
        scmd = sys.argv[1:]

    if scmd[0] in ["0", "1", "2"]:
        add_rand_term_to_dict(scmd, sildict, phondict)

    if scmd[0] in ["3"]:
        _, F, NP, P, eng = scmd

        np1 = int(NP[0])
        np2 = int(NP[1])
        T = str(np1 + np2)

        node = get_node(sildict, F, T, NP, P)

        sil = P_to_sil_XX(F, NP, P, phondict)

        if node == None:
            print("taken")
        else:
            add_to_node(node, eng, sil, P)
        
        save_dict(sildict)

    if scmd[0] in ["4"]:
        refresh_dict_XX(sildict, phondict)

def add_rand_term_to_dict(scmd, sildict, phondict):

    _, eng, F, T = scmd

    if len(F) == 2:
        sildict = rand_XX_sil_and_add(sildict, phondict, eng, F, T)
            
    elif len(F) == 4:
        sildict = rand_XXXX_sil_and_add(sildict, phondict, eng, F, T)

    save_dict(sildict)


def rand_XX_sil_and_add(sildict, phondict, eng, F, tier, NP=None, P=None):
    
    while True:

        np1 = random.randint(1, int(tier) - 1)
        np2 = int(tier) - np1
        NP = f"{np1}{np2}"
        P = to_rand_sil_code([np1, np2])
        sil = P_to_sil_XX(F, [np1, np2], P, phondict)

        node = get_node(sildict, F, tier, NP, P)

        if node != None:
            ans = input(f"How about {sil} for {eng}? yes, continue or quit? ")
            if ans in ("y", "yes"):
                add_to_node(node, eng, sil, P)
                break
            elif ans in ("quit", "q"):
                break

    return sildict

def get_node(sildict, F, T, NP, P):
    
    node = ensure_path(sildict["XX"], F[0]+"X", F, "T"+T, "NP" + NP, f"P{P[0]}X")
    if "P"+P not in node:
        return node

    return None

def add_to_node(node, eng, sil, P):
    node["P"+P] = {"sil": sil, "eng": [eng.replace("_", " ")]}

def to_rand_sil_code(np_list):
    silcode = ""
    for i in np_list:
        j = i
        rand = -1
        while j >= 1:
            rand = random.randint(rand + 1, 5 - j + 1)
            silcode = silcode + str(rand)
            j = j - 1
    return silcode

def P_to_sil_XX(F, NP, P, phondict):
    np1 = int(NP[0])
    np2 = int(NP[1])
    sil = ""
    for i in range(0, np1 + np2):

        phon = phondict["V1"][F[0 if i < np1 else 1]][int(P[i])]

        is_cons = int(P[i]) in [0, 2, 3, 5]
        is_vow = int(P[i]) in [1, 4]
        there_is_next = len(P) > i + 1

        if is_cons and there_is_next and int(P[i + 1]) in [1, 4]:
            phon = phon[:-1]
        if is_vow and there_is_next and int(P[i + 1]) in [1, 4]:
            phon = phon + "k"

        sil = sil + phon

    return sil

def refresh_dict_XX(sildict, phondict):
    for XX in sildict["XX"]:
        for F in XX:
            for T in F:
                if T == "2":
                    for NP in T:
                        for PX in NP:
                            for P in PX:
                                sil = P_to_sil_XX(F, NP[:2], P[:1], phondict)
                                sildict["XX"][XX][F][T][NP][PX][P]["sil"] = sil


def rand_XXXX_sil_and_add(eng, F, tier, sildict, phondict):

    while True:
        np1 = random.randint(1, int(tier) - 3)
        np2 = random.randint(1, int(tier) - np1 - 2)
        np3 = random.randint(1, int(tier) - (np1 + np2) - 1)
        np4 = int(tier) - (np1 + np2 + np3)
        div = f"{np1}{np2}{np3}{np4}"
        code = to_rand_sil_code([np1, np2, np3, np4])
        sil = p_code_to_sil_XXXX(F, [np1, np2, np3, np4], code, phondict)

        node = ensure_path(sildict["XXXX"], F[0]+"XXX", F[:2]+"XX", F[:3]+"X", F, "T"+tier, "NP"+tier)
        if "P"+code not in node:
            print(f"f: {F}, div: {div}, code: {code}")
            ans = input(f"How about {sil} for {eng}? yes, continue or quit? ")
            if ans in ("y", "yes"):
                node["P"+code] = {"sil": sil, "eng": [eng.replace("_", " ")]}
                break
            elif ans in ("quit", "q"):
                break

    return sildict

def p_code_to_sil_XXXX(f, np_list, code, phondict):
    sil = ""
    for i in range(0, sum(np_list)):

        ds_index = None
        if i < np_list[0]:
            ds_index = 0
        elif i < sum(np_list[:2]):    
            ds_index = 1
        elif i < sum(np_list[:3]):
            ds_index = 2
        else:
            ds_index = 3

        phon = phondict["V1"][f[ds_index]][int(code[i])]

        is_cons = int(code[i]) in [0, 2, 3, 5]
        is_vow = int(code[i]) in [1, 4]
        there_is_next = len(code) > i + 1

        if is_cons and there_is_next and int(code[i + 1]) in [1, 4]:
            phon = phon[:-1]
        if is_vow and there_is_next and int(code[i + 1]) in [1, 4]:
            phon = phon + "k"

        sil = sil + phon

    return sil






if __name__ == "__main__":
    main()
