from keras.layers import Input, Embedding, LSTM, Bidirectional, TimeDistributed, Dense
from keras_contrib.layers import CRF
import keras


def NamedEntityRecognizer(seq_len, voc_dim, emb_dim, n_class):
    print("Initializing the Named Entity Recognizer...")

    inputs = Input((seq_len, ))

    embeddings = Embedding(voc_dim + 2, emb_dim)(inputs)

    bilstm = Bidirectional(LSTM(units=50, return_sequences=True, recurrent_dropout=0.1))(embeddings)

    hidden = TimeDistributed(Dense(150, activation="relu"))(bilstm)

    outputs = CRF(n_class)(hidden)

    return keras.Model(inputs=inputs, outputs=outputs)