import networkx as nx


def extract_node(conllup_sentence, pos_entity_1, pos_entity_2, nsubj=True):
    if nsubj is True and conllup_sentence.tokens[pos_entity_1[0][0]-1].deprel not in ["nsubj", "nsubj:pass"]:
        return None, None, None

    graph = nx.Graph()
    root = (0, "root")
    graph.add_node(root)

    for token in conllup_sentence.tokens:
        graph.add_edge((token.index, token.word),
                       (token.head, conllup_sentence.tokens[token.head-1].word),
                       attr=token.deprel)

    source_node = (pos_entity_1[0][0], conllup_sentence.tokens[pos_entity_1[0][0]-1].word)
    target_node = (pos_entity_2[0][0], conllup_sentence.tokens[pos_entity_2[0][0]-1].word)

    prep_path = [node for node in nx.shortest_path(graph, source=source_node, target=target_node)]

    path = list()
    for node in prep_path:
        if node[0] not in pos_entity_1[0] and node[0] not in pos_entity_2[0]:
            path.append(node)

    if len(path) > 0:
        subject = pos_entity_1[1], " ".join(conllup_sentence.tokens[i - 1].word for i in pos_entity_1[0])
        predicate = " ".join(node[1] for node in path)
        object = pos_entity_2[1], " ".join(conllup_sentence.tokens[i - 1].word for i in pos_entity_2[0])

        return subject, predicate, object

    return None, None, None
