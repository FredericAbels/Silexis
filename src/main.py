import json

def main():
    sildict = load_dict()

    entry = input("Enter [digits] [tier] [permutation] [eng]")
    digits, tier, perm, eng = entry.split()

    if len(digits) is 2:
        sildict["X" * 2][digits[0] + "X"][tier][perm] = "":
        

def load_dict():
    with open("../Silexian\ Dictionary.json", "r") as file:
        return json.load(file)        

if __name__ == "__main__":
    main()