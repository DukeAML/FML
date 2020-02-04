
#notes: figure out how to import word2vec embeddings
#pre-process -- text -> onehot --> padding? --> embed --> concat --> lstm
#                                                     --> numeric input

#create second model w/ NLP pipeline
vocab_size = 1000 #revisit

model_inputN = layers.Input(shape = (19,125)) #numeric
#text input 
model_inputT = layers.Input(shape = (19,200)) #assuming we have ~200 words per time-step

embed = layers.Embedding(vocab_size, 64, input_length=(19,200))(model_inputT) #embedding for text
concat = layers.Concatenate(axis =1, [embed, model_inputN]  )()
lstm = layers.LSTM(125, dropout = .2)(concat)