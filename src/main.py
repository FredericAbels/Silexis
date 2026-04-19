import json

def main():
    sildict = load_dict()

    entry = input("Enter [digits] [tier] [permutation] [eng]")
    digits, tier, perm, eng = entry.split()

    if len(digits) is 2:
        sildict["X" * 2][digits[0] + "X"][tier][perm] = "":


    prompt = input("Enter command")
    split_prompt = prompt.split()
    if split_prompt[0] == "engtorandsil":
        comnd, eng, ds, perm = split_prompt

    # check if word already exists
        

def load_dict():
    with open("../silexicon/silexian\ ictionary.json", "r") as file:
        return json.load(file)        

if __name__ == "__main__":
    main()