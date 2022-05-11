def find_synonyms(words):
    global_synonyms = []
    for word in words:
        local_synonyms = []
        word = word.lower()
        with open('thesaurus_full.txt', 'r', encoding='utf-8') as f:
            for line in f:
                dict_word = line.split(';')
                if dict_word[0] == word:
                    local_synonyms.append(dict_word)
        synonyms = [item for sublist in local_synonyms for item in sublist]
        local_synonyms = words_filter(synonyms)
        for local in local_synonyms:
            global_synonyms.append(local)
    for glo in global_synonyms:
        words.append(glo)
    return words

def words_filter(syn):
    syn = [word.strip() for word in syn]
    syn = [syn.remove(word) if ' ' in word else word for word in syn]
    syn = [word for word in syn if word is not None]
    return syn