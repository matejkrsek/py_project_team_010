ciper = "IUDEZKJUHEUFKSEVIUUXAKBUDEUBSKMEFLUNIFUPKVAEUMULFAWNLUNIFUMRPRHUNEPUMRJUBKUDEUHNEHNRUNKUHEUJLHEDRUYIMARNUKBRUIULPESINUHEUJISWUPKBESIUJISRBFWUIUFUZEZISEYEZRUFKSEVISUDRUJRAZEUIUTSIPRSUDRUAKYXKLNIZKLUTARMLUISEUDETKUKBRUHEUMWNAEHNRSWUXAEHUDEDRUTSIMLUPKUX"
keyt = list("IVBPE_QTRDFSJZKXCAHNLMGOWYU")
kon = ['V', 'L', 'Z', 'O', 'D', 'T', 'Q', 'H', 'U', 'X', 'W', 'S', 'E', 'R', 'M', 'C', 'F', 'K', 'N', 'Y', 'I', 'B', 'J', 'G', 'P', '_', 'A']


abc = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "_"]



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

dec = key_update(keyt)
texe = text_update(dec, ciper)
print(texe)


# Замена нулей
def null_defender(dct):
    for i in dct:
        if dct[i] == 0:
            dct[i] = 1
    return dct


"""
with open(f"Testovaci_soubory/text_250_sample_3_ciphertext.txt", "r", encoding="utf-8") as file:
    cipher = file.read()
decrypted = decrypt(cipher, 3, "on")
with open(f"text_250_sample_3_plaintext.txt", "w", encoding="utf-8") as file:
        file.write(decrypted[0])
with open(f"text_250_sample_3_key.txt", "w", encoding="utf-8") as file:
    file.write("".join(decrypted[1]))
"""