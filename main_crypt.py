import random  # A library for randomizing numbers and elements.
import math    # A library for more complex mathematical calculations.
import ast     # A library used to safely convert a string from a file into a Python data structure.
import os      # A library for working with directories.
from test import hi

from collections import defaultdict  # An empty dictionary used to optimize the creation of bigram and trigram dictionaries.
hi()
alphabet = ["A", "B", "C", "D", "E", "F",  # An alphabet used for key generation.
            "G", "H", "I", "J", "K", "L", 
            "M", "N", "O", "P", "Q", "R", 
            "S", "T", "U", "V", "W", "X", 
            "Y", "Z", "_"               ]


#______________SAMPLE ELEMENTS FOR VALIDATION CHECKING______________#
#0000000000000000000000000000000000000000000000000000000000000000#|#|---
with open("bigram_matice.txt",  "r", encoding="utf-8") as file:  #|#| > Sample dictionary of bigram matrix {BM_rel}.
    BM_rel    = ast.literal_eval(file.read())                    #|#| 
#----------------------------------------------------------------#|#|---
with open("trigram_matice.txt", "r", encoding="utf-8") as file:  #|#| > Sample dictionary of trigram matrix {TM_rel}.
    TM_rel    = ast.literal_eval(file.read())                    #|#| 
#----------------------------------------------------------------#|#|---
with open("krakaWORDS.txt",     "r", encoding="utf-8") as file:  #|#| > Dictionary of existing words from the sample {words_rel}.
    words_rel = ast.literal_eval(file.read())                    #|#| 
#0000000000000000000000000000000000000000000000000000000000000000#|#|---


#_________REPLACEMENT OF TWO KEY VALUES_________#
#00000000000000000000000000000000000000000000#|#|---
def random_sample(key):                      #|#| > Generation of two random numbers {num1, num2} 
    num1 = random.randint(0, 26)             #|#| within the range of the alphabet elements list.
    num2 = random.randint(0, 26)             #|#| 
#--------------------------------------------#|#|---
    while num2 == num1:                      #|#| > Replacing one of the generated numbers with a different 
        num2 = random.randint(0, 26)         #|#|  number if they are the same, in order to avoid meaningless iterations.
#--------------------------------------------#|#|---
    char1 = key[num1]                        #|#| > Retrieving key values {char1, char2} based on the selected generated numbers
    char2 = key[num2]                        #|#|  in the order of the list.
#--------------------------------------------#|#|---
    key[num2] = char1                        #|#| > Swapping the two retrieved elements in the list of elements.
    key[num1] = char2                        #|#|
#--------------------------------------------#|#|---
    return key                               #|#| > Returning a new {key} with two modified elements.
#00000000000000000000000000000000000000000000#|#|---


#_____________CREATION OF A NEW KEY_____________#
#00000000000000000000000000000000000000000000#|#|---
def key_create(key):                         #|#| > Initialization of a dictionary {key_decrypt} for substitute decryption.
    key_decrypt = {}                         #|#| > Initialization of an index synchronization counter {cnt} for two lists.
    cnt = 0                                  #|#|
#--------------------------------------------#|#|---
    while cnt < len(key):                    #|#|
        key_decrypt[key[cnt]]= alphabet[cnt] #|#|
        cnt += 1                             #|#|
#--------------------------------------------#|#|---
    return key_decrypt                       #|#|
#00000000000000000000000000000000000000000000#|#|---


#__________CREATION OF A NEW CANDIDATE__________#
#00000000000000000000000000000000000000000000#|#|---
def write_candidate(key, text_decrypted):    #|#|
    new_text = ""                            #|#|
#--------------------------------------------#|#|---
    for i in text_decrypted:                 #|#|
        if i in key:                         #|#|
            new_text += key[i]               #|#|
#--------------------------------------------#|#|---
    return new_text                          #|#|
#00000000000000000000000000000000000000000000#|#|---


#_____________CREATION OF A BIGRAM______________#
#00000000000000000000000000000000000000000000#|#|---
def get_bigrams(text_decrypted):             #|#|
    bigram = defaultdict(int)                #|#|
#--------------------------------------------#|#|---
    for i in range(len(text_decrypted) -1):  #|#|
        bigram[text_decrypted[i]    +        #|#|
                   text_decrypted[i+1]] += 1 #|#|
#--------------------------------------------#|#|---
    return bigram                            #|#|
#00000000000000000000000000000000000000000000#|#|---


#_____________CREATION OF A TRIGRAM_____________#
#00000000000000000000000000000000000000000000#|#|---
def get_trigrams(text_decrypted):            #|#|
    trigram = defaultdict(int)               #|#|
#--------------------------------------------#|#|---
    for i in range(len(text_decrypted) -2):  #|#|
        trigram[   text_decrypted[i]    +    #|#|
                   text_decrypted[i+1]  +    #|#|
                   text_decrypted[i+2]] += 1 #|#|
#--------------------------------------------#|#|---
    return trigram                           #|#|
#00000000000000000000000000000000000000000000#|#|---


#__________CALCULATE VALIDATION POINTS__________#
#00000000000000000000000000000000000000000000#|#|---
def plausibility(bigram, trigram):           #|#|
    p = 0                                    #|#|
#--------------------------------------------#|#|---
    for i in bigram:                         #|#|
        p += (math.log(BM_rel[i]) *          #|#|
                       bigram[i])            #|#|
#--------------------------------------------#|#|---
    for i in trigram:                        #|#|
        p += (math.log(TM_rel[i]) *          #|#|
                      trigram[i])            #|#|
#--------------------------------------------#|#|---
    return p                                 #|#|
#00000000000000000000000000000000000000000000#|#|---


#__________ADDITIONAL VALIDATION CHECK__________#
#00000000000000000000000000000000000000000000#|#|---
def word_valid(p_current, decrypted_text):   #|#| 
    words = decrypted_text.split("_")        #|#|
    p_multipl = 1                            #|#|
#--------------------------------------------#|#|---
    for i in words:                          #|#|
        if (len(i) > 2 and                   #|#|
                i in words_rel[i[0:2]]):     #|#|
                     p_multipl += 0.2        #|#|
#--------------------------------------------#|#|---
    return (p_current * p_multipl)           #|#|
#00000000000000000000000000000000000000000000#|#|---


#_______________________SUBSTITUTION CIPHER CRACKING_______________________#
#00000000000000000000000000000000000000000000000000000000000000000000000#|#|---
def prolom_substitute(text, iter, word_val):                            #|#|
    current_key = alphabet.copy()                                       #|#|
    random.shuffle(current_key)                                         #|#|
#-----------------------------------------------------------------------#|#|---
    decrypted_current = write_candidate(key_create(current_key), text)  #|#|
    bigram_current = get_bigrams(decrypted_current)                     #|#|
    trigram_current = get_trigrams(decrypted_current)                   #|#|
    p_current = plausibility(bigram_current, trigram_current)           #|#|
#-----------------------------------------------------------------------#|#|---
    best_p = p_current                                                  #|#|
    best_text = decrypted_current                                       #|#|
    best_key = current_key.copy()                                       #|#|
#-----------------------------------------------------------------------#|#|---
    for i in range(1, iter+1):                                          #|#|
        candidate_key = random_sample(current_key.copy())               #|#|
        decryptor = key_create(candidate_key)                           #|#|
        decrypted_candidate = write_candidate(decryptor, text)          #|#|
        bigram_candidate = get_bigrams(decrypted_candidate)             #|#|
        trigram_candidate = get_trigrams(decrypted_candidate)           #|#|
        p_candidate = plausibility(bigram_candidate, trigram_candidate) #|#|
        if word_val == "on":                                            #|#|
            p_candidate = word_valid(p_candidate, decrypted_candidate)  #|#|
        q = p_candidate / p_current                                     #|#|
#-----------------------------------------------------------------------#|#|---
        if p_candidate > best_p:                                        #|#|
            best_p = p_candidate                                        #|#|
            best_key = candidate_key.copy()                             #|#|
            best_text = decrypted_candidate                             #|#|
#-----------------------------------------------------------------------#|#|---
        if q > 1:                                                       #|#|
            current_key = candidate_key.copy()                          #|#|
            p_current = p_candidate                                     #|#|
        elif random.randint(1, 1000) < 5:                               #|#|
            current_key = candidate_key.copy()                          #|#|
            p_current = p_candidate                                     #|#|
#-----------------------------------------------------------------------#|#|---
        if i % 1000 == 0:                                               #|#|
            print(f"Iter: {i}\n" +                                      #|#|
                  f"Plausibility: {p_current:.2f}\n----------------")   #|#|
#-----------------------------------------------------------------------#|#|---
    print(f"LAST PLAUSIBILITY: {p_current:.3f}\n" +                     #|#|
              f"HIGHEST PLAUSIBILITY: {best_p:.3f}")                    #|#|
#-----------------------------------------------------------------------#|#|---
    return [best_text, best_key]                                        #|#|
#00000000000000000000000000000000000000000000000000000000000000000000000#|#|---


#______________________PROGRAM INITIALIZATION_______________________#
#0000000000000000000000000000000000000000000000000000000000000000#|#|---
for i in os.listdir("Testovaci_soubory"):                        #|#|
    with open(f"Testovaci_soubory/{i}",                          #|#|
               "r", encoding="utf-8") as file:                   #|#|
        cipher = file.read()                                     #|#|
#----------------------------------------------------------------#|#|---
    parts = i.split("_")                                         #|#|
    mult = 20000                                                 #|#|
    smallCypr = "off"                                            #|#|
    if int(parts[1]) < 1000:                                     #|#|
        mult += 10000                                            #|#|
        smallCypr = "on"                                         #|#|
#----------------------------------------------------------------#|#|---
    decrypted = prolom_substitute(cipher, mult, smallCypr)       #|#|
#----------------------------------------------------------------#|#|---
    filepart = "_".join(parts[0:-1])                             #|#|
    with open(f"Decrypted_text/{filepart}_plaintext.txt",        #|#|
               "w", encoding="utf-8") as file:                   #|#|
        file.write(decrypted[0])                                 #|#|
    with open(f"Decrypted_keys/{filepart}_key.txt",              #|#|
               "w", encoding="utf-8") as file:                   #|#|
        file.write("".join(decrypted[1]))                        #|#|
#0000000000000000000000000000000000000000000000000000000000000000#|#|---