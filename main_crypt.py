import random  # A library for randomizing numbers and elements.
import math    # A library for more complex mathematical calculations.
import ast     # A library used to safely convert a string from a file into a Python data structure.
import os      # A library for working with directories.

from collections import defaultdict  # An empty dictionary used to optimize the creation of bigram and trigram dictionaries.

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

#______________REFERENCE TEXT FOR NORMALIZED PLAUSIBILITY______________#
#0000000000000000000000000000000000000000000000000000000000000000#|#|---
with open("krakatit.txt", "r", encoding="utf-8") as file:        #|#| > Reference text for plausibility scoring.
    ref_text = file.read()                                       #|#| 
    ref_bigrams = defaultdict(int)                               #|#| 
    ref_trigrams = defaultdict(int)                              #|#| 
    for i in range(len(ref_text) - 1):                           #|#| 
        ref_bigrams[ref_text[i] + ref_text[i + 1]] += 1          #|#| 
    for i in range(len(ref_text) - 2):                           #|#| 
        ref_trigrams[ref_text[i] + ref_text[i + 1] + ref_text[i + 2]] += 1  #|#| 
        ref_plausibility = 0
    for bg in ref_bigrams:
        ref_plausibility += math.log(BM_rel[bg]) * ref_bigrams[bg]
    for tg in ref_trigrams:
        ref_plausibility += math.log(TM_rel[tg]) * ref_trigrams[tg]
    ref_plausibility_per_char = ref_plausibility / len(ref_text)  # > Průměrná plausibility na znak
 
#----------------------------------------------------------------#|#|---

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

#__________SCORE PLAUSIBILITY AS PERCENT__________#
#00000000000000000000000000000000000000000000#|#|---
def plausibility_score(p_current, text_length):                  #|#| > Skóre v % podle referenční hodnoty
    current_per_char = p_current / text_length                  #|#| > Intenzita plausibility na znak
    score = (current_per_char / ref_plausibility_per_char) * 100  #|#| > Porovnání s referencí
    return min(max(score, 0), 100)                               #|#| > Oříznuto na 0–100

#00000000000000000000000000000000000000000000#|#|---

#_______________________SUBSTITUTION CIPHER CRACKING_______________________#
#00000000000000000000000000000000000000000000000000000000000000000000000#|#|---
def prolom_substitute(text, iter, word_val):
    current_key = alphabet.copy()
    random.shuffle(current_key)
    decrypted_current = write_candidate(key_create(current_key), text)
    bigram_current = get_bigrams(decrypted_current)
    trigram_current = get_trigrams(decrypted_current)
    p_current = plausibility(bigram_current, trigram_current)

    best_p = p_current
    best_text = decrypted_current
    best_key = current_key.copy()

    for i in range(1, iter+1):
        candidate_key = random_sample(current_key.copy())
        decryptor = key_create(candidate_key)
        decrypted_candidate = write_candidate(decryptor, text)
        bigram_candidate = get_bigrams(decrypted_candidate)
        trigram_candidate = get_trigrams(decrypted_candidate)
        p_candidate = plausibility(bigram_candidate, trigram_candidate)

        if word_val == "on":
            p_candidate = word_valid(p_candidate, decrypted_candidate)

        q = p_candidate / p_current
        
        if p_candidate > best_p:
            best_p = p_candidate
            best_key = candidate_key.copy()
            best_text = decrypted_candidate

        if q > 1:
            current_key = candidate_key.copy()
            p_current = p_candidate
        elif random.randint(1, 1000) < 5:
            current_key = candidate_key.copy()
            p_current = p_candidate

        if i % 2000 == 0:
            print(f"Iter: {i}\nPlausibility: {p_current:.2f}\n----------------")

    #  Výpočet procenta validních slov v dešifrovaném textu
    words = best_text.split("_")
    valid_words = sum(1 for w in words if len(w) > 2 and w in words_rel.get(w[:2], []))
    word_percentage = (valid_words / len(words)) * 100 if words else 0

    print(f"📚 V dešivrovaném textu bylo rozpoznáno: {valid_words}/{len(words)} ({word_percentage:.2f}%) českých slov")
    print("Nejlepší nalezený klíč: " + "".join(best_key))

    return [best_text, best_key]

#00000000000000000000000000000000000000000000000000000000000000000000000#|#|---

#______________ENCRYPTION FUNCTION_______________#
#00000000000000000000000000000000000000000000#|#|---
def encrypt_text(plaintext, key):            #|#| > Funkce, která zašifruje vstupní text
    encryptor = {}                           #|#| > Inicializace šifrovacího slovníku
    cnt = 0                                  #|#| > Index synchronizace pro přiřazení znaků
#--------------------------------------------#|#|---
    while cnt < len(alphabet):               #|#| > Tvorba mapování znaků původní abecedy na šifrovací
        encryptor[alphabet[cnt]] = key[cnt]  #|#|
        cnt += 1                             #|#|
#--------------------------------------------#|#|---
    ciphertext = ""                          #|#| > Inicializace výsledného šifrovaného textu
    for char in plaintext:                   #|#|
        if char in encryptor:                #|#|
            ciphertext += encryptor[char]    #|#|
#--------------------------------------------#|#|---
    return ciphertext                        #|#| > Vrací zašifrovaný text
#00000000000000000000000000000000000000000000#|#|---

#_____________VERIFYING RECOVERED KEY_____________#
#00000000000000000000000000000000000000000000#|#|---
def verify_key(plaintext, recovered_key, original_cipher):      #|#| > Funkce ověřuje správnost nalezeného klíče
    test_cipher = encrypt_text(plaintext, recovered_key)        #|#| > Znovu zašifruje původní plaintext odhaleným klíčem
#--------------------------------------------#|#|---
    return test_cipher == original_cipher                       #|#| > Porovná s původním ciphertextem
#00000000000000000000000000000000000000000000#|#|---

#______________________PROGRAM INITIALIZATION_______________________#
#0000000000000000000000000000000000000000000000000000000000000000#|#|---
for i in os.listdir("Testovaci_soubory"):                        #|#|
    with open(f"Testovaci_soubory/{i}",                          #|#|
               "r", encoding="utf-8") as file:                   #|#|
        cipher = file.read()                                     #|#|
#----------------------------------------------------------------#|#|---
    parts = i.split("_")    #CHECK THESE 7 LINES, IVE GOT NO IDEA WHAT I DID WITH IT :D           #|#|
    mult = 20000                                                #|#|
    smallCypr = "off"       #u malé šifry se neupoužije slovník  #|#|
    if int(parts[1]) < 1000:                                     #|#|
        mult += 1000                                            #|#|
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