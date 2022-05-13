import random

def create_typos_list(words):
    global_typos = []
    for word in words:
        local_typos = []
        while len(local_typos) < 5:
            typo = generate_typos(word)
            if typo in local_typos or typo == word:
                pass
            else:
                local_typos.append(typo)
        for local in local_typos:
            global_typos.append(local)
    for glob in global_typos:
        words.append(glob)
    return words

def generate_typos(word, prob=0.05):
    keyApprox = {}
    keyApprox['q'] = "qwasedzx"
    keyApprox['w'] = "wqesadrfcx"
    keyApprox['e'] = "eęwrsfdqazxcvgt"
    keyApprox['r'] = "retdgfwsxcvgt"
    keyApprox['t'] = "tryfhgedcvbnju"
    keyApprox['y'] = "ytugjhrfvbnji"
    keyApprox['u'] = "uóyihkjtgbnmlo"
    keyApprox['i'] = "iuojlkyhnmlp"
    keyApprox['o'] = "oóipklujm"
    keyApprox['p'] = "plo['ik"

    keyApprox['a'] = "aąqszwxwdce"
    keyApprox['s'] = "sśwxadrfv"
    keyApprox['d'] = "decsfaqgbv"
    keyApprox['f'] = "fdgrvwsxyhn"
    keyApprox['g'] = "gtbfhedcyjn"
    keyApprox['h'] = "hyngjfrvkim"
    keyApprox['j'] = "jhknugtblom"
    keyApprox['k'] = "kjlinyhn"
    keyApprox['l'] = "lłokmpujn"

    keyApprox['z'] = "zźaxsvde"
    keyApprox['x'] = "xzcsdbvfrewq"
    keyApprox['c'] = "cćxvdfzswergb"
    keyApprox['v'] = "vcfbgxdertyn"
    keyApprox['b'] = "bvnghcftyun"
    keyApprox['n'] = "nńbmhjvgtuik"
    keyApprox['m'] = "mnkjloik"
    keyApprox[' '] = " "

    keyApprox['ś'] = "s"
    keyApprox['ź'] = "z"
    keyApprox['ń'] = "n"
    keyApprox['ć'] = "c"
    keyApprox['ę'] = "e"
    keyApprox['ą'] = "a"
    keyApprox['ł'] = "l"
    keyApprox['ó'] = "uo"

    probOfTypo = int(prob * 100)
    buttertext = ""
    for letter in word:
        lcletter = letter.lower()
        if not lcletter in keyApprox.keys():
            newletter = lcletter
        else:
            if random.choice(range(0, 100)) <= probOfTypo:
                newletter = random.choice(keyApprox[lcletter])
            else:
                newletter = lcletter
        # go back to original case
        if not lcletter == letter:
            newletter = newletter.upper()
        buttertext += newletter

    return buttertext
