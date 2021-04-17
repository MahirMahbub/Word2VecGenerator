import glob
import multiprocessing
import pickle


from bangla_stemmer.resources import grammar
from bangla_stemmer.stemmer import stemmer
from bangla_stemmer.stemmer.stemmer import BanglaStemmer

from gensim.models import Word2Vec, FastText
# %%
word = 'কবিগুলিকে'
stm = BanglaStemmer().stem(['কবিরগুলিকে', 'আমাকে', 'নামাবার'])
print(stm)
# %%
from os.path import dirname, abspath
from typing import Dict, List
import re
# from . import grammer
# from ..resources import grammar



# d = dirname(dirname(abspath(__file__)))

class BanglaStemmer:
    first_dict: Dict[str, List[str]]
    second_dict: Dict[str, List[str]]
    third_dict: Dict[str, List[str]]
    fourth_dict: Dict[str, List[str]]


    def __init__(self):
        self.grammarParser()


    def grammarParser(self):
        self.first_dict = grammar.sp_initial_dict
        self.second_dict = grammar.con_rep_dict
        self.third_dict = grammar.obv_rep_dict
        self.fourth_dict = grammar.sp_final_dict


    def checklen(self, word):
        skip_wrd = ['া', 'ি', 'ী', 'ু', 'ূ', 'ৃ', 'ে', 'ৈ', 'ো', 'ৌ']
        len = 0
        for ltr in word:
            if ltr in skip_wrd:
                pass
            else:
                len += 1
        return len


    def dot_replace(self, word, initial_index, rplc):
        wrd = word[0:initial_index]
        for i in range(len(rplc)):
            if rplc[i] == '.':
                wrd += word[initial_index + i]
            else:
                wrd += rplc[i]
        return wrd


    def dirrect_replace(self, word, initial_index, rplc):
        wrd = word[0:initial_index]
        wrd += rplc
        return wrd


    def apply_frth_rule(self, word):
        grep = word
        for rules in self.fourth_dict:
            result = re.search(rules, word)
            if result:
                # print('applied fourth rules..')
                initial_index = result.span()[0]
                final_index = result.span()[1]
                wordlen = len(word)
                if final_index == wordlen:
                    rigid_wordlen = self.checklen(grep[0:initial_index])
                    if rigid_wordlen > 1:
                        rplc = self.fourth_dict[rules][1]
                        if '.' in rplc:
                            grep = self.dot_replace(word, initial_index, rplc)
                        else:
                            grep = self.dirrect_replace(word, initial_index, rplc)
                    elif rigid_wordlen == 1:
                        rplc = self.fourth_dict[rules][0]
                        if '.' in rplc:
                            grep = self.dot_replace(word, initial_index, rplc)
                        else:
                            grep = self.dirrect_replace(word, initial_index, rplc)
                    else:
                        pass
                else:
                    pass
                break
            else:
                pass
        return grep


    def apply_thrd_rule(self, word):
        grep = word
        for rules in self.third_dict:
            result = re.search(rules, word)
            if result:
                # print('applied third rules..')
                initial_index = result.span()[0]
                final_index = result.span()[1]
                wordlen = len(word)
                if final_index == wordlen:
                    rigid_wordlen = self.checklen(grep[0:initial_index])
                    if rigid_wordlen > 1:
                        rplc = self.third_dict[rules][1]
                        if '.' in rplc:
                            grep = self.dot_replace(word, initial_index, rplc)
                        else:
                            grep = self.dirrect_replace(word, initial_index, rplc)
                    elif rigid_wordlen == 1:
                        rplc = self.third_dict[rules][0]
                        if '.' in rplc:
                            grep = self.dot_replace(word, initial_index, rplc)
                        else:
                            grep = self.dirrect_replace(word, initial_index, rplc)
                    else:
                        pass
                else:
                    pass
                break
            else:
                pass
        grep = self.apply_frth_rule(grep)
        return grep


    def apply_scnd_rule(self, word):
        grep = word
        for rules in self.second_dict:
            result = re.search(rules, word)
            if result:
                # print('applied second rules..')
                initial_index = result.span()[0]
                final_index = result.span()[1]
                wordlen = len(word)
                if final_index == wordlen:
                    rigid_wordlen = self.checklen(grep[0:initial_index])
                    if rigid_wordlen > 1:
                        rplc = self.second_dict[rules][1]
                        if '.' in rplc:
                            grep = self.dot_replace(word, initial_index, rplc)
                        else:
                            grep = self.dirrect_replace(word, initial_index, rplc)
                    elif rigid_wordlen == 1:
                        rplc = self.second_dict[rules][0]
                        if '.' in rplc:
                            grep = self.dot_replace(word, initial_index, rplc)
                        else:
                            grep = self.dirrect_replace(word, initial_index, rplc)
                    else:
                        pass
                else:
                    pass
                break
            else:
                pass
        grep = self.apply_thrd_rule(grep)
        return grep


    def apply_frst_rule(self, word):
        grep = word
        for rules in self.first_dict:
            result = re.search(rules, word)
            if result:
                initial_index = result.span()[0]
                final_index = result.span()[1]
                wordlen = len(word)
                if final_index == wordlen:
                    rigid_wordlen = self.checklen(grep[0:initial_index])
                    if rigid_wordlen > 1:
                        rplc = self.first_dict[rules][1]
                        if '.' in rplc:
                            grep = self.dot_replace(word, initial_index, rplc)
                        else:
                            grep = self.dirrect_replace(word, initial_index, rplc)
                    elif rigid_wordlen == 1:
                        rplc = self.first_dict[rules][0]
                        if '.' in rplc:
                            grep = self.dot_replace(word, initial_index, rplc)
                        else:
                            grep = self.dirrect_replace(word, initial_index, rplc)
                    else:
                        pass
                else:
                    pass
                break
            else:
                pass
        grep = self.apply_scnd_rule(grep)
        return grep


    def stem(self, wordarg):
        stemlist = []
        stemword = ''
        if isinstance(wordarg, list):
            for word in wordarg:
                stemlist.append(self.apply_frst_rule(word))
            return stemlist
        elif isinstance(wordarg, str):
            stemword = self.apply_frst_rule(wordarg)
            return stemword



# %%

files = glob.glob("phrase_data/*.pkl")
# %%
for file in files:
    pkl_file = open(file, 'rb')
    file_data = pickle.load(pkl_file)
    with open("raw_corpus.txt", encoding="utf-8", mode="a+") as f:

        for line in file_data:
            if len(line) > 4:
                stri = " ".join(
                    [i.replace('“', "").
                         replace('"', "").
                         replace("–", "\n").
                         replace("	", " ").
                         replace("…", " ").
                         replace("×", "").
                         replace("#", "").
                         replace("|", "\n").
                         replace("৷", "\n").
                         replace("Ñ", "").
                         replace("=", " ").
                         replace("”", "") for i
                     in line])+"\n"
                stri = stri.replace(" _ ", " ").replace(" _", " ").replace("_ ", " ").replace("    ", " "). \
                    replace("  "," ").replace(
                    "   ", " ")
                f.write(stri.lstrip())
                stris = stri.split("\n")
                for l in stris:
                    l_list = BanglaStemmer().stem(l.split(" "))
                    if len(l_list) > 4:
                        data = f.write(" ".join(l_list).lstrip() + "\n")
                        if "_" in l:
                            ll = l.replace("_", " ")
                            ll_list = BanglaStemmer().stem(ll.split(" "))
                            data = f.write(" ".join(ll_list).lstrip() + "\n")

# %%
from gensim.models.callbacks import CallbackAny2Vec



class MonitorCallback(CallbackAny2Vec):

    def on_epoch_end(self, model):
        print("Model loss:", model.get_latest_training_loss())



monitor = MonitorCallback()  # print loss



# %%

def embedding(algorithm='word2vec', alg_type="skipgram", corpus_file="corpus_stem.txt", vector_size=300, window=5, min_count=1,
              workers=int(multiprocessing.cpu_count()) - 1, hs=0, epochs=3, compute_loss=True, callbacks=None):
    if callbacks is None:
        callbacks = [monitor]
    if algorithm == 'word2vec':
        if alg_type == 'cbow':
            model = Word2Vec(corpus_file=corpus_file, vector_size=vector_size, window=window, min_count=min_count,
                             workers=workers,
                             sg=0, hs=hs, epochs=epochs, compute_loss=compute_loss, callbacks=callbacks)
            return model
        elif alg_type == 'skipgram':
            model = Word2Vec(corpus_file=corpus_file, vector_size=vector_size, window=window, min_count=min_count,
                             workers=workers,
                             sg=1, hs=hs, epochs=epochs, compute_loss=compute_loss, callbacks=callbacks)
    elif algorithm == 'fastText':
        if alg_type == 'cbow':
            model = FastText(corpus_file=corpus_file, vector_size=vector_size, window=window, min_count=min_count,
                             workers=workers,
                             sg=0, hs=hs, epochs=epochs)
            return model
        elif alg_type == 'skipgram':
            model = FastText(corpus_file=corpus_file, vector_size=vector_size, window=window, min_count=min_count,
                             workers=workers,
                             sg=1, hs=hs, epochs=epochs)
    return model



# %%

model = embedding(alg_type='skipgram', min_count = 2, callbacks=[monitor])
# %%
model.save("word2vec_stem_skipgram_v300_e3_w3_min2.model")
# %%
val1 = model.wv.most_similar(BanglaStemmer().stem("বাংলাদেশ"), topn=15)
print(val1)
# %%

print(model.wv.most_similar(positive=[BanglaStemmer().stem("আর্জেন্টিনা"), BanglaStemmer().stem("ঢাকা")], negative=[BanglaStemmer().stem("বাংলাদেশ")]))
# %%
from gensim.models import Word2Vec
model = Word2Vec.load("word2vec_stem_skipgram_v300_e3_w3_min2.model")
# %%
print(model.wv.vectors.shape)
# %%

            # f.writelines()



        
        