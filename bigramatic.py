with open("krakatit.txt", "r", encoding="utf-8") as file:
    text = file.read()

abc = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "_"]

new_dict = {}

for i in abc:
    for j in abc:
        new_dict[f"{i}{j}"] = 0

all_bigram = 0

char = 1
while char < len(text):
    if text[char-1]+text[char] in new_dict:
        new_dict[text[char-1]+text[char]] = new_dict[text[char-1]+text[char]] + 1
        all_bigram += 1
    char += 1

for i in new_dict:
    new_dict[i] = (new_dict[i] / all_bigram) + 1

triple_dict = {}

for i in abc:
    for j in abc:
        for k in abc:
            triple_dict[f"{i}{j}{k}"] = 0

triple_char = 0
while triple_char < len(text)-2:
    if f"{text[triple_char]}{text[triple_char+1]}{text[triple_char+2]}" in triple_dict:
        triple_dict[f"{text[triple_char]}{text[triple_char+1]}{text[triple_char+2]}"] = triple_dict[f"{text[triple_char]}{text[triple_char+1]}{text[triple_char+2]}"] + 1
    triple_char += 1

for i in triple_dict:
    triple_dict[i] = (triple_dict[i] / triple_char) + 1


with open("bigram_matice.txt", "w", encoding="utf-8") as file:
    file.write(str(new_dict))

with open("trigram_matice.txt", "w", encoding="utf-8") as file:
    file.write(str(triple_dict))

#print(new_dict)