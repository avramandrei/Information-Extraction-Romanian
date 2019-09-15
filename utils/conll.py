import sys


class Token(object):
    def __init__(self, index=-1, word="_", lemma="_", upos="_", xpos="_", feats="_", head="_", deprel="_", deps="_",
                 misc="_"):
        self.index, self.is_compound_entry = self._int_try_parse(index)
        self.word = word
        self.lemma = lemma
        self.upos = upos
        self.xpos = xpos
        self.feats = feats
        self.head, _ = self._int_try_parse(head)
        self.deprel = deprel
        self.deps = deps
        self.misc = misc

    def _int_try_parse(self, value):
        try:
            return int(value), False
        except ValueError:
            return value, True


class CONLLSentence(object):
    def __init__(self, tokens=None):
        self.tokens = []
        if tokens != None:
            self.tokens = tokens

    def __repr__(self):
        sentence = ""
        for token in self.tokens:
            sentence += token.word
            if not "SpaceAfter=No" in token.misc:
                sentence += " "
        return sentence

    def to_text(self):
        lines = []
        for token in self.tokens:
            lines.append("{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(
                token.index,
                token.word,
                token.lemma,
                token.upos,
                token.xpos,
                token.feats,
                token.head,
                token.deprel,
                token.deps,
                token.misc,
            ))
        return lines


def read_file(filename):
    with open(filename, "r", encoding="utf8") as f:
        lines = f.readlines()
    dataset = []
    tokens = []

    for line in lines:
        if line.startswith("\n"):
            dataset.append(tokens)
            tokens = []
            continue

        if line.strip() == "":
            if len(tokens) > 0:
                dataset.append(CONLLSentence(tokens=tokens))
                continue

        parts = line.strip().split("\t")
        if len(parts) != 10:
            print("ERROR processing line: [" + line.strip() + "], not a valid conll format!")
            sys.exit(0)

        token = Token(index=int(parts[0]), word=parts[1], lemma=parts[2], upos=parts[3], xpos=parts[4], feats=parts[5],
                      head=parts[6], deprel=parts[7], deps=parts[8], misc=parts[9])
        tokens.append(token)

    return dataset