"""import ast

with open("bigram_matice.txt", "r", encoding="utf-8") as file:
    bigrMatice = ast.literal_eval(file.read())

liga = 0

for i in bigrMatice:
    liga+= bigrMatice[i]

print(liga)"""

abc = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]

new_dict = {}

for i in abc:
    for j in abc:
        new_dict[f"{i}{j}"] = []

with open("krakatit.txt", "r", encoding="utf-8") as file:
    smallControl = file.read().split("_")

for i in smallControl:
    if len(i) > 2:
        prefix = i[0:2]
        if prefix in new_dict and i not in new_dict[prefix]:
            new_dict[prefix].append(i)

with open(f"krakaWORDS.txt", "w", encoding="utf-8") as file:
    file.write(str(new_dict))


import os

print(os.listdir("Testovaci_soubory"))