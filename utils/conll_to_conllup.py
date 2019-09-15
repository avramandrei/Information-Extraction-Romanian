import json
from utils.conllup import CONLLUPSentence, Token
import numpy as np


def conll2conllup(conll_sentences, pred, ent2oh_path):
    with open(ent2oh_path, "r") as file:
        entity2onehot = json.load(file)

    conllup_sentences = list()

    for sent_id, tokens in enumerate(conll_sentences):
        conllup_tokens = []
        prev_entity = "O"
        counter = 0

        for token_id, token in enumerate(tokens):

            for gold_entity, gold_value in entity2onehot.items():
                if np.argmax(gold_value) == np.argmax(pred[sent_id][token_id]):
                    entity = gold_entity

            if entity is not "O":
                if prev_entity == "O":
                    counter += 1
                    parseme_mwe = str(counter) + ":" + entity
                else:
                    parseme_mwe = str(counter)
            else:
                parseme_mwe = "*"

            prev_entity = entity

            conllup_tokens.append(
                Token(index=token.index,
                      word=token.word,
                      lemma=token.lemma,
                      upos=token.upos,
                      xpos=token.xpos,
                      feats=token.attrs,
                      head=token.head,
                      deprel=token.label,
                      deps=token.deps,
                      misc=token.space_after,
                      parseme_mwe=parseme_mwe
                      )
            )

        conllup_sentences.append(CONLLUPSentence(id=sent_id, tokens=conllup_tokens))

    return conllup_sentences
