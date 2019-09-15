from utils.conllup import read_file
from utils.vocabulary import create_vocabularies
import numpy as np
import json


def create_x_from_conll(conll_sentences, w2i, seq_len):
    X = []

    for conll_sentence in conll_sentences:
        X_sentence = []

        for token in conll_sentence:
            word = token.word

            try:
                X_sentence.append(w2i[word])
            except KeyError:
                X_sentence.append(1)

        curr_seq_len = len(X_sentence)

        if curr_seq_len < seq_len:
            for i in range(curr_seq_len, seq_len):
                X_sentence.append(0)

            X.append(X_sentence)

    return np.array(X)


def create_xy_from_conllup(conllup_sentences, w2i, seq_len):
    X = []
    y = []

    with open("models/ent2oh.json", "r") as file:
        entity2onehot = json.load(file)

    for conllup_sentence in conllup_sentences:
        X_sentence = []
        y_sentence = []

        for token in conllup_sentence.tokens:
            word = token.word
            entity = token.parseme_mwe

            X_sentence.append(w2i[word])

            if entity == "*":
                onehot = entity2onehot["O"]
                y_sentence.append(onehot)
            elif ":" in entity:
                onehot = entity2onehot[entity.split(":")[1]]
                y_sentence.append(onehot)
                prev_onehot = onehot
            else:
                y_sentence.append(prev_onehot)

        assert len(X_sentence) == len(y_sentence)

        curr_seq_len = len(X_sentence)

        if curr_seq_len < seq_len:
            for i in range(curr_seq_len, seq_len):
                X_sentence.append(0)
                y_sentence.append(entity2onehot["O"])

            X.append(X_sentence)
            y.append(y_sentence)

    return np.array(X), np.array(y)


def load_data_from_conllup(path, seq_len):
    print("Loading data...")

    conllup_sentences = read_file(path)

    w2i, i2w = create_vocabularies(conllup_sentences)

    X, y = create_xy_from_conllup(conllup_sentences, w2i, seq_len)

    return X, y, w2i, i2w


def load_data_from_conll(path, seq_len):
    pass