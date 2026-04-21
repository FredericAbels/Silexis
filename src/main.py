import json
import random

def main():
    path_sildict = "../silexicon/dictionary.json"
    sildict = load_dict(path_sildict)
    path_phonemes = "../silexicon/phonemes.json"
    phondict = load_dict(path_phonemes)

    # prompt = input("Enter command ")
    cmd = "engtorandsil millenialism 49 2-1"
    split_cmd = cmd.split()

    if split_cmd[0] == "engtorandsil" or split_cmd[0] == "etrs":

        comnd, eng, ds, div = split_cmd
        tier, n, m = extract_from_div(div)

        while True:
            code = to_rand_sil_code(ds, tier, n, m)
            sil = code_to_sil(ds, n, m, code, phondict)
            
            if ds[0] + "X" not in sildict["XX"]:
                sildict["XX"][ds[0] + "X"] = {}

            if "T" + tier not in sildict["XX"][ds[0] + "X"]:
                sildict["XX"][ds[0] + "X"]["T" + tier] = {}

            if div not in sildict["XX"][ds[0] + "X"]["T" + tier]:
                sildict["XX"][ds[0] + "X"]["T" + tier][div] = {}

            if code not in sildict["XX"][ds[0] + "X"]["T" + tier][div]:
                ans = input("How about " + sil + " for " + eng + "? yes or no?")
                if ans == "y" or ans == "yes":
                    sildict["XX"][ds[0] + "X"]["T" + tier][div][code] = {"sil": sil, "eng": eng}
                    break
    
    # check if word already exists
        
def load_dict(file_path):
    with open(file_path, "r") as file:
        return json.load(file)        

def extract_from_div(s):
    n, m = s.split("-")
    return str(int(n) + int(m)), int(n), int(m)

def to_rand_sil_code(ds, tier, n, m):
    silcode = ""
    for i in [n, m]:
        j = i
        rand = -1
        while j >= 1:
            rand = random.randint(rand + 1, 5 - j + 1)
            silcode = silcode + str(rand)
            j = j - 1
    return silcode

def code_to_sil(ds, n, m, code, phondict):
    sil = ""
    for i in range(0, n + m):

        phon = phondict[ds[0 if i < n else 1]][int(code[i])]

        is_cons = int(code[i]) in [0, 2, 3, 5]
        there_is_next = len(code) > i + 1

        if is_cons and there_is_next and int(code[i + 1]) in [1, 4]:
            phon = phon[:-1]

        sil = sil + phon

    return sil


if __name__ == "__main__":
    main()