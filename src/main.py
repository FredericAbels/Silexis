import json
import random

def main():
    path_sildict = "../silexicon/dictionary.json"
    sildict = load_dict(path_sildict)
    path_phonemes = "../silexicon/phonemes.json"
    phondict = load_dict(path_phonemes)

    example1 = "example 60 4"
    example2 = "example 8245 6"

    print("Options:")
    print("0 convert from add_to_dict.json")
    print("1 [eng] [ds] [tier]")
    print("2 " + example1)
    print("3 " + example2)

    cmd = input()
    if cmd == "2":
        cmd = "2 " + example1
    if cmd == "3":
        cmd = "3 " + example2

    split_cmd = cmd.split()

    if split_cmd[0] in ["1", "2", "3"]:
        # fist check if it is in already ??
        cmd, eng, ds, tier = split_cmd

        if len(ds) == 2:

            while True:
                np1 = random.randint(1, int(tier) - 1)
                np2 = int(tier) - np1
                div = str(np1) + str(np2)

                code = to_rand_sil_code(ds, tier, [np1, np2])
                sil = code_to_sil_XX(ds, [np1, np2], code, phondict)
                
                if ds[0] + "X" not in sildict["XX"]:
                    sildict["XX"][ds[0] + "X"] = {}

                if ds not in sildict["XX"][ds[0] + "X"]:
                    sildict["XX"][ds[0] + "X"][ds] = {}

                if "T" + tier not in sildict["XX"][ds[0] + "X"][ds]:
                    sildict["XX"][ds[0] + "X"][ds]["T" + tier] = {}

                if "NP" + div not in sildict["XX"][ds[0] + "X"][ds]["T" + tier]:
                    sildict["XX"][ds[0] + "X"][ds]["T" + tier]["NP" + div] = {}

                if "P" + code not in sildict["XX"][ds[0] + "X"][ds]["T" + tier]["NP" + div]:
                    ans = input("How about " + sil + " for " + eng + "? yes, continue or quit? ")
                    if ans == "y" or ans == "yes":
                        sildict["XX"][ds[0] + "X"][ds]["T" + tier]["NP" + div]["P" + code] = {"sil": sil, "eng": eng.replace("_", " ")}
                        break
                    elif ans == "quit" or ans == "q":
                        break

        elif len(ds) == 4:

            while True:
                np1 = random.randint(1, int(tier) - 3)
                np2 = random.randint(1, int(tier) - np1 - 2)
                np3 = random.randint(1, int(tier) - np2 - 1)
                np4 = int(tier) - (np1 + np2 + np3)
                np_list = [np1, np2, np3, np4]
                div = str(np1) + str(np2) + str(np3) + str(np4)

                print("THINK ABOUT ADDING [DS]")

                code = to_rand_sil_code(ds, tier, np_list)
                sil = code_to_sil_XXXX(ds, np_list, code, phondict)

                if ds[0] + "XXX" not in sildict["XXXX"]:
                    sildict["XXXX"][ds[0] + "XXX"] = {}

                if ds[:2] + "XX" not in sildict["XXXX"][ds[0] + "XXX"]:
                    sildict["XXXX"][ds[0] + "XXX"][ds[:2] + "XX"] = {}

                if ds[:3] + "X" not in sildict["XXXX"][ds[0] + "XXX"][ds[:2] + "XX"]:
                    sildict["XXXX"][ds[0] + "XXX"][ds[:2] + "XX"][ds[:3] + "X"] = {}

                if "T" + tier not in sildict["XXXX"][ds[0] + "XXX"][ds[:2] + "XX"][ds[:3] + "X"]:
                    sildict["XXXX"][ds[0] + "XXX"][ds[:2] + "XX"][ds[:3] + "X"]["T" + tier] = {}

                if "NP" + div not in sildict["XXXX"][ds[0] + "XXX"][ds[:2] + "XX"][ds[:3] + "X"]["T" + tier]:
                    sildict["XXXX"][ds[0] + "XXX"][ds[:2] + "XX"][ds[:3] + "X"]["T" + tier]["NP" + tier] = {}

                if "P" + code not in sildict["XXXX"][ds[0] + "XXX"][ds[:2] + "XX"][ds[:3] + "X"]["T" + tier]["NP" + tier]:
                    ans = input("How about " + sil + " for " + eng + "? yes, continue or quit? ")
                    if ans == "y" or ans == "yes":
                        sildict["XXXX"][ds[0] + "XXX"][ds[:2] + "XX"][ds[:3] + "X"]["T" + tier]["NP" + tier]["P" + code] = {"sil": sil, "eng": eng.replace("_", " ")}
                        break
                    elif ans == "quit" or ans == "q":
                        break

    with open(path_sildict, "w") as f:
        json.dump(sildict, f, indent=4)

        
def load_dict(file_path):
    with open(file_path, "r") as file:
        return json.load(file)        

def to_rand_sil_code(ds, tier, np_list):
    silcode = ""
    for i in np_list:
        j = i
        rand = -1
        while j >= 1:
            rand = random.randint(rand + 1, 5 - j + 1)
            silcode = silcode + str(rand)
            j = j - 1
    return silcode

def code_to_sil_XX(ds, np_list, code, phondict):
    sil = ""
    for i in range(0, sum(np_list)):

        phon = phondict[ds[0 if i < np_list[0] else 1]][int(code[i])]

        is_cons = int(code[i]) in [0, 2, 3, 5]
        is_vow = int(code[i]) in [1, 4]
        there_is_next = len(code) > i + 1

        if is_cons and there_is_next and int(code[i + 1]) in [1, 4]:
            phon = phon[:-1]
        if is_vow and there_is_next and int(code[i + 1]) in [1, 4]:
            phon = phon + "h"

        sil = sil + phon

    return sil

def code_to_sil_XXXX(ds, np_list, code, phondict):
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

        phon = phondict[ds[ds_index]][int(code[i])]

        is_cons = int(code[i]) in [0, 2, 3, 5]
        is_vow = int(code[i]) in [1, 4]
        there_is_next = len(code) > i + 1

        if is_cons and there_is_next and int(code[i + 1]) in [1, 4]:
            phon = phon[:-1]
        if is_vow and there_is_next and int(code[i + 1]) in [1, 4]:
            phon = phon + "h"

        sil = sil + phon

    return sil


if __name__ == "__main__":
    main()