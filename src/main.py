import json
import random

def main():
    path_sildict = "../silexicon/dictionary.json"
    sildict = load_dict(path_sildict)
    path_phonemes = "../silexicon/phonemes.json"
    phondict = load_dict(path_phonemes)

    prompt = input("Enter command")
    split_prompt = prompt.split()

    if split_prompt[0] == "engtorandsil" or split_prompt[0] == "etrs":

        comnd, eng, ds, div = split_prompt
        tier, n, m = extract_from_div(div)

        code = torandsil(ds, tier, n, m)
        sildict["XX"][ds[0] + "X"]["T" + tier][div] = 

    # check if word already exists
        

def load_dict(file_path):
    with open(file_path, "r") as file:
        return json.load(file)        

def extract_from_div(s):
    n, m = s.split("-")
    return string(int(n) + int(m)), int(n), int(m)

def torandsil(ds, tier, n, m):
    silcode = ""
    for i in [n, m]:
        j = i
        rand = 0
        while j >= 1:
            rand = random.randint(rand, 5 - j + 1)
            silcode = silcode + string(rand)
            j = j - 1
    


if __name__ == "__main__":
    main()