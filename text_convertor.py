import fitz  

with fitz.open("book/Krakatit.pdf") as doc:
    text = ""
    for page in doc:
        text += page.get_text().upper() + "\n"

replacer = {"Á": "A",
            "Č": "C",
            "Ď": "D",
            "É": "E",
            "Ě": "E",
            "Í": "I",
            "Ň": "N",
            "Ó": "O",
            "Ř": "R",
            "Š": "S",
            "Ť": "T",
            "Ú": "U",
            "Ů": "U",
            "Ý": "Y",
            "Ž": "Z",
            " ": "_",}

abc = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "_"]

fin_text = ""
text = text.replace("\n", " ")

for veo in replacer:
    text = text.replace(veo, replacer[veo])

for veo in text:
    if veo in abc:
        fin_text += veo
        if len(fin_text) > 1 and fin_text[-2] == "_" and veo == "_":
            fin_text = fin_text[0:-1]

with open("krakatit.txt", "w", encoding="utf-8") as file:
    file.write(fin_text)