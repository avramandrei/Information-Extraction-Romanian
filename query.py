from rdflib import Graph
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("graphpath")
    parser.add_argument("sqlout")
    parser.add_argument("--subj")
    parser.add_argument("--pred")

    args = parser.parse_args()

    store = Graph()
    store.load(args.graphpath)

    with open(args.sqlout, "w", encoding='utf-8') as file:
        if args.subj and args.pred:
            query = 'SELECT ?subj_words ?pred_words ?obj_words ' \
                    'WHERE { ?relation relation:subject ?subj .' \
                    '        ?subj entity:words ?subj_words .' \
                    '' \
                    '        ?relation relation:predicate ?pred_words .' \
                    '' \
                    '        ?relation relation:object ?obj .' \
                    '        ?obj entity:words ?obj_words .' \
                    'FILTER ( regex( ?subj_words, "' + args.subj + '") && ' \
                    '         regex( ?pred_words, "' + args.pred + '") ) }' \

            for row in store.query(query):
                file.write("Subject: {}\nPredicate: {}\nObject: {}\n\n".format(
                            row.subj_words, row.pred_words, row.obj_words
                ))
        elif args.subj:
            query = 'SELECT ?subj_words ?pred_words ?obj_words ' \
                    'WHERE { ?relation relation:subject ?subj .' \
                    '        ?subj entity:words ?subj_words .' \
                    '' \
                    '        ?relation relation:predicate ?pred_words .' \
                    '' \
                    '        ?relation relation:object ?obj .' \
                    '        ?obj entity:words ?obj_words .' \
                    'FILTER ( regex( ?subj_words, "' + args.subj + '")) }' \

            for row in store.query(query):
                file.write("Subject: {}\nPredicate: {}\nObject: {}\n\n".format(
                            row.subj_words, row.pred_words, row.obj_words
                ))
        elif args.pred:
            query = 'SELECT ?subj_words ?pred_words ?obj_words ' \
                    'WHERE { ?relation relation:subject ?subj .' \
                    '        ?subj entity:words ?subj_words .' \
                    '' \
                    '        ?relation relation:predicate ?pred_words .' \
                    '' \
                    '        ?relation relation:object ?obj .' \
                    '        ?obj entity:words ?obj_words .' \
                    'FILTER ( regex( ?pred_words, "' + args.pred + '")) }' \

            for row in store.query(query):
                file.write("Subject: {}\nPredicate: {}\nObject: {}\n\n".format(
                            row.subj_words, row.pred_words, row.obj_words
                ))
        else:
            raise ValueError("Your must specify either the subject or relation")


