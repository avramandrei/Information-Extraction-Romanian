# 0 - PAD
# 1 - UNK


def create_vocabularies(conllup_sentences):
    w2i = {}
    i2w = {}

    counter = 2

    for conllup_sentence in conllup_sentences:
        for token in conllup_sentence.tokens:
            word = token.word

            if word not in w2i.keys():
                w2i[word] = counter
                i2w[counter] = word
                counter += 1

    return w2i, i2w