import morfeusz2

def forms_generator(words):

    morf = morfeusz2.Morfeusz()
    forms = []
    for word in words:
        generated = morf.generate(word)
        for gen in generated:
            form = gen[0]
            if form not in forms:
                forms.append(form)
    return forms
