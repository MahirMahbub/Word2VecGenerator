import numpy

# cosine_similarity = numpy.dot(model['spain'], model['france']) / (
#             numpy.linalg.norm(model['spain']) * numpy.linalg.norm(model['france']))
# %%
from gensim.models import Word2Vec

model = Word2Vec.load("temp models/word2vec_stem_skipgram_v300_e3_w3_min2.model")

# %%
def restrict_w2v(w2v):
    new_vectors = []
    new_index2entity = []
    # len(w2v.wv.index_to_key)
    for i in range(len(w2v.wv.index_to_key)):
        word = w2v.wv.index_to_key[i]


        # vocab = w2v.wv.key_to_index[word]
        # vec_norm = w2v.wv.vectors_norm[i]
        # print(vec)
        if not "_" in word:
            vec = w2v.wv[word]
            # vocab. = len(new_index2entity)
            new_index2entity.append(word)
            # new_vocab[word] = vocab
            new_vectors.append(vec)
        del word
            # new_vectors_norm.append(vec_norm)

    # w2v.vocab = new_vocab
    #print(w2v.wv.index)
    # w2v.wv.index = len(new_index2entity)
    # print(w2v.wv.index)
    w2v.wv.vectors = new_vectors
    #print(len(w2v.wv.index_to_key))
    w2v.wv.index_to_key = new_index2entity
    del new_vectors
    del new_index2entity
    # w2v.wv.vectors_norm = new_vectors_norm
    return w2v

restrict_w2v(model)

#%%
model.save("word2vec_discard_stem_skipgram_v300_e3_w3_min2.model")
# #%%
# new_vocab = []
# for word in vocab:
#     if "_" in word:
#         # new_vocab.append(word)
#         del model.wv.key_to_index[word]
# model.wv.index_to_key = new_vocab
# print(model.wv.vectors.shape)

#%%
print(model.wv["ইংল্যান্ড"])
#%%

from bangla_stemmer.stemmer.stemmer import BanglaStemmer
print(model.wv.similar_by_vector("ইংল্যান্ড"))
# %%
import pandas as pd

df = pd.read_csv("Evaluation_datasets/Synonym_bn.txt", header=None)
# %%
print(df)
from bangla_stemmer.stemmer.stemmer import BanglaStemmer

one = BanglaStemmer().stem(list(df[0]))
two = BanglaStemmer().stem(list(df[1]))
three = BanglaStemmer().stem(list(df[2]))
four = BanglaStemmer().stem(list(df[3]))
five = BanglaStemmer().stem(list(df[4]))
six = BanglaStemmer().stem(list(df[5]))
synonyms = list(zip(one, two, three, four, five, six))

# %%
print(synonyms)
#%%
count = 0
total = 0
for synonym in synonyms:
    max = 0
    val = ""
    for i in range(1, 5):
        # print(model.wv[synonym[0]])
        try:
            cosine_similarity = numpy.dot(model.wv[synonym[0]], model.wv[synonym[i]]) / (
                    numpy.linalg.norm(model.wv[synonym[0]]) * numpy.linalg.norm(model.wv[synonym[i]]))
        except:
            break
        # print(cosine_similarity)
        if cosine_similarity > max:
            max = cosine_similarity
            val = synonym[i]
    if val == synonym[5] and i==4:
        count += 1
    if i==4:
        total += 1
print((count / total) * 100)
print(total)
# %%
import pandas as pd

df = pd.read_csv("Evaluation_datasets/Antonym_bn.txt", header=None)
# %%
print(df)
from bangla_stemmer.stemmer.stemmer import BanglaStemmer

one = BanglaStemmer().stem(list(df[0]))
two = BanglaStemmer().stem(list(df[1]))
three = BanglaStemmer().stem(list(df[2]))
four = BanglaStemmer().stem(list(df[3]))
five = BanglaStemmer().stem(list(df[4]))
six = BanglaStemmer().stem(list(df[5]))
antonyms = list(zip(one, two, three, four, five, six))
count = 0
total = 0
for antonym in antonyms:
    min = 1000
    val = ""
    for i in range(1, 5):
        # print(model.wv[synonym[0]])
        try:
            cosine_similarity = numpy.dot(model.wv[antonym[0]], model.wv[antonym[i]]) / (
                    numpy.linalg.norm(model.wv[antonym[0]]) * numpy.linalg.norm(model.wv[antonym[i]]))
        except:
            break
        # print(cosine_similarity)
        if cosine_similarity < min:
            min = cosine_similarity
            val = antonym[i]
    if val == antonym[5] and i==4:
        count += 1
    if i==4:
        total += 1
print((count / total) * 100)

# %%
import pandas as pd

df = pd.read_csv("Evaluation_datasets/Analogy_bn.txt", header=None, delimiter=" ")
# %%
print(df)
from bangla_stemmer.stemmer.stemmer import BanglaStemmer
#%%
one = BanglaStemmer().stem(list(df[0]))
two = BanglaStemmer().stem(list(df[1]))
three = BanglaStemmer().stem(list(df[2]))
four = BanglaStemmer().stem(list(df[3]))
#%%
analogys = list(zip(one, two, three, four))
count = 0
total = 0
split=-1

#%%
for analogy in analogys:
    val = ""

    if total%237 == 0:
        split+=1
        print(split*10, "% Done.....")
    try:
        val = model.wv.most_similar(positive=[analogy[1], analogy[2]],
                                    negative=[analogy[0]], topn=4)
    except:
        continue
    total += 1

    value = [v[0] for v in val]

    for s in value:
        if analogy[3] in s:
            count+=1
            break

print(count, total)
print((count/total)*100)

#%%
model.wv.most_similar(positive=[BanglaStemmer().stem("ইংল্যান্ড"), BanglaStemmer().stem("এথেন্স")],
                      negative=[BanglaStemmer().stem("গ্রীস")])
