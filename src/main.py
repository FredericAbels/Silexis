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
        json.dump(sildict, f, indent=4, ensure_ascii=False, sort_keys=True)


def main():
    sildict = load_dict(path_sildict)
    phondict = load_dict(path_phonemes)

    print("\nOptions:")
    print("0 [eng] [F]")
    print("1 [eng] [F] [tier]")
    print("2 [F] [P] [eng]")
    print("3 [NP] [F] [P] [eng]")
    print("4 refresh dictionary")
    print()

    one_loop_completed = False
    while True:

        scmd = None

        if len(sys.argv) == 1 or one_loop_completed:
            cmd = input()
            scmd = cmd.split()
        else:
            scmd = sys.argv[1:]

        if scmd == []:
            break

        elif scmd[0] in ["0", "1"]:

            if scmd[0] == "0":
                _, eng, F = scmd
                T = str(len(F))
            elif scmd[0] == "1":
                _, eng, F, T = scmd

            add_rand_term_to_dict(eng, F, T, sildict, phondict)
            one_loop_completed = True

        elif scmd[0] in ["2", "3"]:

            if scmd[0] == "2":
                _, F, P, eng = scmd
                NP = "1"*len(F)

            elif scmd[0] == "3":
                _, NP, F, P, eng = scmd

            T = None
            if len(F) == 2:
                T = str(int(NP[0]) + int(NP[1]))
            elif len(F) == 4:
                T = str(int(NP[0]) + int(NP[1]) + int(NP[2]) + int(NP[3]))
            else:
                raise ValueError("F must be an even number of digits")

            node = get_node(sildict, F, T, NP, P)

            sil = P_to_sil_XX(F, NP, P, phondict)

            if node == None:
                print("taken")
            else:
                add_to_node(node, eng, sil, P)
            
            save_dict(sildict)

            one_loop_completed = True

        elif scmd[0] in ["4"]:

            refresh_dict_XX(sildict, phondict)
            save_dict(sildict)

            one_loop_completed = True


def add_rand_term_to_dict(eng, F, T, sildict, phondict):

    if len(F) == 2:
        sildict = rand_XX_sil_and_add(sildict, phondict, eng, F, T)
            
    elif len(F) == 4:
        sildict = rand_XXXX_sil_and_add(sildict, phondict, eng, F, T)

    save_dict(sildict)



def rand_XX_sil_and_add(sildict, phondict, eng, F, T, NP=None, P=None):
    
    while True:

        np1 = random.randint(1, int(T) - 1)
        np2 = int(T) - np1
        NP = f"{np1}{np2}"

        P = to_rand_sil_code([np1, np2])
        sil = P_to_sil_XX(F, [np1, np2], P, phondict)

        node = get_node(sildict, F, T, NP, P)

        if node != None:
            # ans = input(f"How about {sil} for {eng}? yes, continue or quit? ")
            ans = "y"
            if ans in ("y", "yes"):
                add_to_node(node, eng, sil, P)
                print(f"P{P} {sil} was added for {eng}\n")
                break
            elif ans in ("quit", "q"):
                break

    return sildict

def rand_XXXX_sil_and_add(sildict, phondict, eng, F, T, NP=None, P=None):

    while True:

        np1 = random.randint(1, int(T) - 3)
        np2 = random.randint(1, int(T) - np1 - 2)
        np3 = random.randint(1, int(T) - (np1 + np2) - 1)
        np4 = int(T) - (np1 + np2 + np3)
        NP = f"{np1}{np2}{np3}{np4}"

        P = to_rand_sil_code([np1, np2, np3, np4])
        sil = p_code_to_sil_XXXX(F, [np1, np2, np3, np4], P, phondict)

        node = get_node(sildict, F, T, NP, P)

        if "P"+P not in node:
            # ans = input(f"How about {sil} for {eng}? yes, continue or quit? ")
            ans = "y"
            if ans in ("y", "yes"):
                node["P"+P] = {"sil": sil, "eng": [eng.replace("_", " ")]}
                print(f"P{P} {sil} was added for {eng}\n")
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


def get_node(sildict, F, T, NP, P):

    node = None
    if len(F) == 2:
        if T == "1": # This does not work yet
            node = ensure_path(sildict["1F"], F[0]+"X", F, "T"+T, "NP" + NP)
        if T == "2":
            node = ensure_path(sildict["1F"], F[0]+"X", F, "T"+T, "NP" + NP, f"P{P[0]}X")
        elif T == "3":
            node = ensure_path(sildict["1F"], F[0]+"X", F, "T"+T, "NP" + NP, f"P{P[0]}XX", f"P{P[0]}{P[1]}X")
    elif len(F) == 4:
        if T == "4":
            node = ensure_path(sildict["2F"], F[0]+"XXX", f"{F[0]}{F[1]}XX", f"{F[0]}{F[1]}{F[2]}X", F, "T"+T, "NP" + NP, f"P{P[0]}XXX", f"P{P[0]}{P[1]}XX", f"P{P[0]}{P[1]}{P[2]}X")

    if "P"+P not in node:
        return node

    return None

def add_to_node(node, eng, sil, P):
    node["P"+P] = {"sil": sil, "eng": eng.replace("_", " ").split(",")}

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

    for XX_key, XX in sildict["1F"].items():
        for F_key, F in XX.items():
            for T_key, T in F.items():
                if T_key == "T2":
                    for NP_key, NP in T.items():
                        for PX_key, PX in NP.items():
                            for P_key in PX:
                                sil = P_to_sil_XX(F_key, NP_key[2:], P_key[1:], phondict)
                                sildict["1F"][XX_key][F_key][T_key][NP_key][PX_key][P_key]["sil"] = sil







if __name__ == "__main__":
    main()
