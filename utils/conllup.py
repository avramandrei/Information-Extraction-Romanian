import sys
import os


class Token(object):
    def __init__(self, index=-1, word="_", lemma="_", upos="_", xpos="_", feats="_", head="_", deprel="_", deps="_",
                 misc="_", parseme_mwe="_"):
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
        self.parseme_mwe = parseme_mwe

    def _int_try_parse(self, value):
        try:
            return int(value), False
        except ValueError:
            return value, True


class CONLLUPSentence(object):
    def __init__(self, id=None, tokens=None):
        self.tokens = []
        self.id = id
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
        if self.id != None:
            lines.append("# sent_id = {}\n".format(self.id))
        lines.append("# text = {}\n".format(self))
        for token in self.tokens:
            lines.append("{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(
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
                token.parseme_mwe
            ))
        return lines


def read_file(filename):
    with open(filename, "r", encoding="utf8") as f:
        lines = f.readlines()
    dataset = []
    tokens = []

    for line in lines:
        if line.startswith("#"):
            if "sent_id" in line:
                sentence_id = line.replace("# sent_id = ", "").strip()
                tokens = []
                continue
            continue

        if line.strip() == "":
            if len(tokens) > 0:
                dataset.append(CONLLUPSentence(id=sentence_id, tokens=tokens))
                continue

        parts = line.strip().split("\t")
        if len(parts) != 11:
            print("ERROR processing line: [" + line.strip() + "], not a valid conllup format!")
            sys.exit(0)

        token = Token(index=int(parts[0]), word=parts[1], lemma=parts[2], upos=parts[3], xpos=parts[4], feats=parts[5],
                      head=parts[6], deprel=parts[7], deps=parts[8], misc=parts[9], parseme_mwe=parts[10])
        tokens.append(token)

    return dataset


def write_file(output_path, conllupdataset):
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    conllup_file_handle = open(os.path.join(output_path, "output.conllup"), "w", encoding='utf-8')
    conllup_file_handle.write("# global.columns = ID FORM LEMMA UPOS XPOS FEATS HEAD DEPREL DEPS MISC PARSEME:MWE\n")
    for sentence_id, sentence in enumerate(conllupdataset):
        for line in sentence.to_text():
            conllup_file_handle.write(line)
        conllup_file_handle.write("\n")
    conllup_file_handle.close()


def extract_entities(conllup_sentences):
    all_sen_entity_list = list()

    for sentence in conllup_sentences:
        sen_entity_list = list()
        entity_pos = list()
        past_entity = None

        for token in sentence.tokens:
            entity = token.parseme_mwe

            if ":" in entity:
                if len(entity_pos) > 0 and past_entity is not None:
                    sen_entity_list.append((entity_pos, past_entity))

                entity_pos = list()
                entity_pos.append(token.index)
                past_entity = entity[2:]
            elif entity is not "*":
                entity_pos.append(token.index)

        if past_entity is not None:
            sen_entity_list.append((entity_pos, past_entity))

        all_sen_entity_list.append(sen_entity_list)

    return all_sen_entity_list
