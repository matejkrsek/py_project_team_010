import random
import math
import ast
import os
from collections import defaultdict

from string import ascii_uppercase

with open("bigram_matice.txt", "r", encoding="utf-8") as file:
    bigrMatice = ast.literal_eval(file.read())

with open("trigram_matice.txt", "r", encoding="utf-8") as file:
    trigrMatice = ast.literal_eval(file.read())

with open("krakaWORDS.txt", "r", encoding="utf-8") as file:
    smallControl = ast.literal_eval(file.read())

abc = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "_"]


# Перемешать 2 символа
def shuffle(code_list):
    num1 = random.randint(0, 26)
    num2 = random.randint(0, 26)
    while num2 == num1:
        num2 = random.randint(0, 26)
    char1 = code_list[num1]
    char2 = code_list[num2]
    code_list[num2] = char1
    code_list[num1] = char2
    return code_list


# Заменник нового ключа
def key_update(key):
    key_decoder = {}
    cnt = 0
    while cnt < len(key):
        key_decoder[key[cnt]] = abc[cnt]
        cnt += 1
    return key_decoder


# Создание текста по новому ключу
def text_update(key_decoder, cpText):
    new_text = ""
    for i in cpText:
        if i in key_decoder:
            new_text += key_decoder[i]
    return new_text

"""
# Создание биграмки нового текста
def bigram_build(rel_text):
    shifr_dict = {}
    for i in abc:
        for j in abc:
            shifr_dict[f"{i}{j}"] = 0
    char = 1
    while char < len(rel_text):
        if rel_text[char-1]+rel_text[char] in shifr_dict:
            shifr_dict[rel_text[char-1]+rel_text[char]] = shifr_dict[rel_text[char-1]+rel_text[char]] + 1
        char += 1
    return shifr_dict
"""


def bigram_build(rel_text):
    shifr_dict = defaultdict(int)
    for i in range(len(rel_text) -1):
        shifr_dict[rel_text[i] + rel_text[i+1]] += 1
    return shifr_dict


"""
# Создание триграмки нового текста
def trigram_build(rel_text):
    shifr_dict = {}
    shifr_trigram_base = {}
    for i in abc:
        for j in abc:
            for k in abc:
                shifr_trigram_base[f"{i}{j}{k}"] = 0
    triple_char = 0
    while triple_char < len(rel_text)-2:
        if f"{rel_text[triple_char]}{rel_text[triple_char+1]}{rel_text[triple_char+2]}" in shifr_dict:
            shifr_dict[f"{rel_text[triple_char]}{rel_text[triple_char+1]}{rel_text[triple_char+2]}"] = shifr_dict[f"{rel_text[triple_char]}{rel_text[triple_char+1]}{rel_text[triple_char+2]}"] + 1
        triple_char += 1
    return shifr_dict
"""
def trigram_build(rel_text):
    shifr_dict = defaultdict(int)
    for i in range(len(rel_text) -2):
        shifr_dict[rel_text[i] + rel_text[i+1] + rel_text[i+2]] += 1
    return shifr_dict

# Замена нулей
def null_defender(dct):
    for i in dct:
        if dct[i] == 0:
            dct[i] = 1
    return dct

"""
# Проверка сходства
def prob_update(bigram_rel, trigram_rel):
    prob_bi = 0
    for i in bigrMatice:
        prob_bi += math.log(bigrMatice[i]) * bigram_rel[i]
    prob_tri = 0
    for i in trigrMatice:
        prob_tri += math.log(trigrMatice[i]) * trigram_rel[i]
    return (prob_bi * prob_tri)
"""

def prob_update(bigram_rel, trigram_rel):
    prob_bi = 0
    for i in bigram_rel:
        prob_bi += math.log(bigrMatice[i]) * bigram_rel[i]
    prob_tri = 0
    for i in trigram_rel:
        prob_tri += math.log(trigrMatice[i]) * trigram_rel[i]
    return (prob_bi + prob_tri)
"""
def prob_update(bi_rel, tri_rel):
    return sum(math.log(bigrMatice[i]) * bi_rel[i] for i in bi_rel) + \
           sum(math.log(trigrMatice[i]) * tri_rel[i] for i in tri_rel)
"""
# Доп. контроль малого текста
def smallCpr(prob, n_text):
    text_look = n_text.split("_")
    prob_upgrade = 1
    for i in text_look:
        if len(i) > 2 and i in smallControl[i[0:2]]:
            prob_upgrade += 0.2
    return (prob * prob_upgrade)


# Расшифровка
def decrypt(ciprText, multipl, sml):
    current_key = abc.copy()
    random.shuffle(current_key)

    first_text = text_update(key_update(current_key), ciprText)
    first_bigram = bigram_build(first_text)
    first_trigram = trigram_build(first_text)

    best_probability = prob_update(first_bigram, first_trigram)

    highest_prob = best_probability
    highest_text = first_text
    highest_key = current_key.copy()
    print(best_probability)
    for i in range(1, 10000*multipl+1):
        new_key = shuffle(current_key.copy())
        new_decoder = key_update(new_key)
        new_text = text_update(new_decoder, ciprText)
        rel_bigram = bigram_build(new_text)
        rel_trigram = trigram_build(new_text)
        prob = prob_update(rel_bigram, rel_trigram)
        if sml == "on":
            prob = smallCpr(prob, new_text)

        prob_rel = prob / best_probability

        if prob > highest_prob:
            highest_prob = prob
            highest_key = new_key.copy()
            highest_text = new_text

        if prob_rel > 1:
            current_key = new_key.copy()
            best_probability = prob
        elif random.randint(1, 1000) < 5:
            current_key = new_key.copy()
            best_probability = prob
            

        if i % 1000 == 0:
            print(f"Iter {i} | Plausibility: {best_probability:.2f}")
            

        if i == 10000*multipl:
            print(f"Best prob: {best_probability:.3f}  |  Highest prob: {highest_prob:.3f}")
            break
    return [highest_text, highest_key]

"""
with open(f"Testovaci_soubory/text_250_sample_3_ciphertext.txt", "r", encoding="utf-8") as file:
    cipher = file.read()
decrypted = decrypt(cipher, 3, "on")
with open(f"text_250_sample_3_plaintext.txt", "w", encoding="utf-8") as file:
        file.write(decrypted[0])
with open(f"text_250_sample_3_key.txt", "w", encoding="utf-8") as file:
    file.write("".join(decrypted[1]))
"""


for i in os.listdir("Testovaci_soubory"):
    with open(f"Testovaci_soubory/{i}", "r", encoding="utf-8") as file:
        cipher = file.read()
    parts = i.split("_")
    mult = 2
    smallCypr = "off"
    if int(parts[1]) < 1000:
        mult += 1
        smallCypr = "on"
    decrypted = decrypt(cipher, mult, smallCypr)

    filepart = "_".join(parts[0:-1])

    with open(f"Decrypted_text/{filepart}_plaintext.txt", "w", encoding="utf-8") as file:
        file.write(decrypted[0])
    with open(f"Decrypted_keys/{filepart}_key.txt", "w", encoding="utf-8") as file:
        file.write("".join(decrypted[1]))
