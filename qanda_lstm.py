"""

A simple LSTM model to generate QANDA scripts

"""

from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout, LSTM
from keras.optimizers import RMSprop
from tqdm import tqdm
import numpy as np
import random
import sys

# get qanda transcripts
print('Welcome to QANDAbot')
text = open('qanda_transcripts.txt', 'r').read().lower()
print('Corpus length (millions chars): ', len(text)/1e6)

chars = sorted(list(set(text)))
char_indices = dict((c, i) for i, c in enumerate(chars))
indices_char = dict((i, c) for i, c in enumerate(chars))

batch_size = 128
maxlen = 30
step = 3
sentences = []
next_chars = []
for i in tqdm(range(0, len(text) - maxlen, step)):
    sentences.append(text[i: i+maxlen])
    next_chars.append(text[i+maxlen])
print('Number of sequences: ', len(sentences))
print('')
print('Vectorization')
print('')
X = np.zeros((len(sentences), maxlen, len(chars)), dtype=np.bool)
y = np.zeros((len(sentences), len(chars)), dtype=np.bool)
for i, sentence in tqdm(enumerate(sentences)):
    for t, char in enumerate(sentence):
        X[i, t, char_indices[char]] = 1
    y[i, char_indices[next_chars[i]]] = 1

# build the model
print('Building model')
model = Sequential()
model.add(LSTM(512, input_shape=(maxlen, len(chars)),
    return_sequences = True, stateful=True,
    batch_input_shape = (128, maxlen, len(chars))))
model.add(LSTM(512, input_shape=(maxlen, len(chars)),
    return_sequences = False, stateful=True))
model.add(Dense(len(chars)))
model.add(Activation('softmax'))
optimizer = RMSprop(lr=0.01)
model.compile(loss='categorical_crossentropy', optimizer=optimizer)

# to make the sample sizes divisible by batch_size for stateful RNN
n_sentences = (len(sentences) // batch_size) * batch_size
X = X[0:n_sentences]
y = y[0:n_sentences]

def sample(preds, temperature=1.0):
    # helper function for index sampling
    preds = np.asarray(preds).astype('float32')
    preds = np.log(preds) / temperature
    exp_preds = np.exp(preds)
    preds = exp_preds / np.sum(preds)
    probas = np.random.multinomial(1, preds, 1)
    return np.argmax(probas)

# train the model, output generated text after each iteration
for iteration in tqdm(range(1, 60)):
    print()
    print('-'*50)
    print('Iteration', iteration)
    model.fit(X, y, batch_size = 128, nb_epoch=1, shuffle=False)
    model.reset_states()
    start_index = random.randint(0, len(text) - maxlen - 1)
    model.save('qanda_bot.h5')
    for diversity in [0.2, 0.5, 1.0, 1.2]:
        print()
        print('---------- diversity:', diversity)

        generated = ''
        sentence = text[start_index: start_index + maxlen]
        generated += sentence
        print('--------------- Generating with seed: "' + sentence + '"')
        sys.stdout.write(generated)

        for i in range(400):
            x = np.zeros((1, maxlen, len(chars)))
            for t, char in enumerate(sentence):
                x[0, t, char_indices[char]] = 1

            preds = model.predict(x, verbose=0)[0]
            next_index = sample(preds, diversity)
            next_char = indices_char[next_index]

            generated += next_char
            sentence = sentence[1:] + next_char

            sys.stdout.write(next_char)
            sys.stdout.flush()
        print()            






    

