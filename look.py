import random
import math
import ast

cprtext = "ABM_DEAOMARDHMAVA_VNAERDALD_UAOMAZDNYPAA_VZHBDSVANDAYVWAWIOPABCKVBMARDLMABSDBMAYDOPAXDAWMRDZACYVSANDAYUNDACMWPBSVAHSVBMIAYDOPAXDAWMRDZAMYDBKDSAOBUKWVABPNWMZUSA_ABM_IAVACMNYVBUSANDACKDOAWMSVAXDOAKDWSAZHKVCYUBDACMXDODNACKDNDAERDAIXDSVANABM_DEAOBVAWKMWPA_CDYACMXOAEINUEDAOVSAOMBD_IAYDAVNCMRALSU_AWAHKVRUZUEAWVEAZHZDNA_CVYWPANWKUCDSA_ILPA_CVYWPANAYDLMIANDAERMIARDRUAVRUAOMCKDOIAVRUA_CVYWPAZMCVWAEUARDKM_IEUNAEINUEAYMAIODSVYAVLPNABUODSAVLPALPSMAXUNYMA_DAXNDEAYDAEDSVAKVOVAEPNSUNA_DALPZHAEMHSVAXDNYDAXDORMIANSPNDYAZMNAEUAKDWSA_CVYWPARDEI_DNALIOALPNAEINDSABPOVYAYMAZMARDZHZDNAVARDNEUNARDLMALPAYDAMOBD_SUAVAXVAANCINYUSVAKIZDAOMAWSURVABUOUNAUARVAYMAXNDEAEPNSDSVA_DALPZHANSVANAYDLMIAOMCKDOIAOMBDOSVALPZHAYMAOMBDOSVALPZHAYMAXUNYDAVSDAAYPAXNUAYVEARDWODA_VNRMILDRAXOUAWARUAHSDOARUWOPAEDARDRVCVOSMACYVYANDAYDARVAYMAWOP_AXDAZSMBDWACKURZD_RVAEPNSUANUA_DAXDARVANBDYDANVEAEVNAXUAKVOACMHSDOSARVARUAIYKP_RDRPEVAMZUEVACKDZDAXDRARDOMBDOSA_VCKUYAAYVWABUOUNABPODZHSVAYPARDIEUNAVRUASHVYAYPAEUSPAVSDACMZHMCAWOP_AXNDEANUAYMACVW"

with open("bigram_matice.txt", "r", encoding="utf-8") as file:
    ref = ast.literal_eval(file.read())

# Алфавит
abc = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "_"]

# Подготовка биграмм из текста
def get_bigrams(text):
    return [text[i] + text[i+1] for i in range(len(text) - 1)]

# Построение частотной матрицы (как словаря)
def transition_matrix(bigrams):
    mat = {a + b: 0 for a in abc for b in abc}
    for bg in bigrams:
        if bg in mat:
            mat[bg] += 1
    for k in mat:
        if mat[k] == 0:
            mat[k] = 1e-6  # защита от log(0)
    return mat

# Функция вероятности (log-подобие)
def plausibility(text, TM_ref):
    bigrams_obs = get_bigrams(text)
    TM_obs = transition_matrix(bigrams_obs)
    score = 0
    for bg in TM_obs:
        if TM_ref[bg] == 0:
            TM_ref[bg] = 1
        score += math.log(TM_ref[bg]) * TM_obs[bg]
    return score

# Дешифровка по ключу
def substitute_decrypt(ciphertext, key):
    decoder = {k: v for k, v in zip(key, abc)}
    return "".join(decoder.get(c, c) for c in ciphertext)

# Алгоритм расшифровки с симулированным отжигом
def decrypt(ciphertext, TM_ref, iterations=50000, start_key=None):
    if start_key is None:
        current_key = abc.copy()
        random.shuffle(current_key)
    else:
        current_key = start_key.copy()

    decrypted = substitute_decrypt(ciphertext, current_key)
    p_current = plausibility(decrypted, TM_ref)

    for i in range(1, iterations + 1):
        candidate_key = current_key.copy()
        a, b = random.sample(range(len(abc)), 2)
        candidate_key[a], candidate_key[b] = candidate_key[b], candidate_key[a]

        candidate_decrypted = substitute_decrypt(ciphertext, candidate_key)
        p_candidate = plausibility(candidate_decrypted, TM_ref)

        q = p_candidate / p_current

        if q > 1 or random.random() < 0.01:
            current_key = candidate_key
            p_current = p_candidate

        if i % 1000 == 0:
            print(f"Iter {i} | Plausibility: {p_current:.2f}")

    best_decrypted = substitute_decrypt(ciphertext, current_key)
    return current_key, best_decrypted, p_current

enid = decrypt(cprtext, ref)
print(enid[0])