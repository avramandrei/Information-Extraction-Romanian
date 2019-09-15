from keras.models import load_model
import os
from cube.api import Cube
from utils.conllup import write_file
import argparse
from keras_contrib.layers import CRF
from keras_contrib.losses import crf_loss
from keras_contrib.metrics import crf_accuracy
import json
from utils.load_data import create_x_from_conll
from utils.conll_to_conllup import conll2conllup
from utils.rdf import extract_node
from utils.conllup import read_file, extract_entities
from rdflib import Graph, Namespace, BNode, Literal
from rdflib.namespace import FOAF, DC, RDF

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

NER_PATH = os.path.join("resources", "roner.h5")
W2I_PATH = os.path.join("resources", "w2i.json")
I2W_PATH = os.path.join("resources", "i2w.json")
ENT2OH_PATH = os.path.join("resources", "ent2oh.json")
SEQ_LEN = 100  # this must be the same as the original NER sequence length


def create_conll_sentences(file_path):
    print("*"*25 + "  Working on transforming the input file '{}' to CoNLL format  ".format(file_path) + "*"*25 + "\n")

    print("Reading the input file...")
    with open(file_path, "r", encoding="utf-8") as file:
        text = file.read()

    print("Loading the 'ro' nlp-cube model...")

    cube = Cube(verbose=False)
    cube.load("ro")

    print("Creating the CoNLL sentences...")
    sentences = cube(text)

    print("\n" + "*"*124 + "\n")

    return sentences


def create_conllup_sentences(conll_sentences, output_path):
    print("*" * 26 + "  Working on transforming the CoNLL sentences to CoNLL-U Plus format  " + "*" * 27 + "\n")

    print("Loading the index vocabularies...")

    with open(W2I_PATH, "r", encoding="utf-8") as w2i_file:
        w2i = json.load(w2i_file)

    X = create_x_from_conll(conll_sentences, w2i, SEQ_LEN)

    print("Loadint the NER model...")

    custom_objects = {"CRF": CRF, "crf_loss": crf_loss, "crf_accuracy": crf_accuracy}
    ner = load_model(NER_PATH, custom_objects)

    print("Identifying the named entities...")
    pred = ner.predict(X)

    conllup_sentences = conll2conllup(conll_sentences, pred, ENT2OH_PATH)

    print("Saving the CoNLL-U Plus sentences...")
    write_file(output_path, conllup_sentences)

    print("\n" + "*" * 124 + "\n")

    return conllup_sentences


def create_rdf_graph(conllup_sentences, output_path):
    print("*" * 28 + "  Creating the RDF ontology graph from the CoNLL-U Plus sentences  " + "*" * 28 + "\n")
    store = Graph()
    ns_rel = Namespace("https://github.com/avramus/ppie-onto-api/")
    ns_entity = Namespace("https://github.com/dumitrescustefan/ronec/")

    store.bind("relation", ns_rel)
    store.bind("entity", ns_entity)

    entities_list = extract_entities(conllup_sentences)

    print("Extracting the Subject, Predicate, Object triplets from the CoNLL-U Plus sentences...")
    for i, conllup_sentence in enumerate(conllup_sentences):
        if len(entities_list[i]) > 1:
            for j in range(len(entities_list[i]) - 1):
                subject, predicate, object = extract_node(conllup_sentence, entities_list[i][j], entities_list[i][j+1])

                if subject is not None and predicate is not None and object is not None:
                    subj_entity = subject[0]
                    subj_words = subject[1]

                    pred_words = predicate

                    obj_entity = object[0]
                    obj_words = object[1]

                    node_rel = BNode()
                    store.add((node_rel, RDF.type, ns_rel.relation))

                    node_entity_subj = BNode()
                    node_entity_obj = BNode()

                    exec("store.add((node_entity_subj, RDF.type, ns_entity.{}))".format(subj_entity))
                    exec("store.add((node_entity_obj, RDF.type, ns_entity.{}))".format(obj_entity))

                    store.add((node_rel, ns_rel.subject, node_entity_subj))
                    store.add((node_rel, ns_rel.object, node_entity_obj))
                    store.add((node_rel, ns_rel.predicate, Literal(pred_words)))

                    store.add((node_entity_subj, ns_entity.words, Literal(subj_words)))
                    store.add((node_entity_obj, ns_entity.words, Literal(obj_words)))

    print("Saving the RDF ontology graph...")
    with open(os.path.join(output_path, "output_rdf.xml"), "wb") as file:
        file.write(store.serialize(format="pretty-xml"))

    print("\n" + "*" * 124 + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file_path", type=str)
    parser.add_argument("output_path", type=str)

    args = parser.parse_args()

    conll_sentences = create_conll_sentences(args.file_path)
    conllup_sentences = create_conllup_sentences(conll_sentences, args.output_path)
    create_rdf_graph(conllup_sentences, args.output_path)

    custom_objects = {"CRF": CRF, "crf_loss": crf_loss, "crf_accuracy": crf_accuracy}
    ner = load_model(os.path.join("models", "roner.h5"), custom_objects)
