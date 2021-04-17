import json
import pickle
import re

import dask



# @dask.delayed
from gensim.sklearn_api import PhrasesTransformer



def read_corpus(filename):
    # data = bag.read_text(filename, encoding="utf-8", linedelimiter=r"\n", blocksize=1)
    # return data
    pkl_file = open(filename, 'rb')
    file_data = pickle.load(pkl_file)
    #print(file_data)
    # df = pd.read_pickle(...)
    # ddf = dd.from_pandas(df, npartitions=8)
    pkl_file.close()
    return ''.join(file_data)



@dask.delayed
def clean_data(data):
    dirt = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ.-_/\~`*%$#@,:;1234567890<>(){}[]‘’''১২৩৪৫৬৭৮৯০"
    data = [char for char in data if char not in dirt]
    data = ''.join(data)
    data = data.split(" ")
    with open(r'data/words/stopwords-bn.json', encoding="utf-8") as f:
        stop_words = json.load(f)
        # print(stop_words)
        data = [i for i in data if i not in stop_words and i != ""]
    return ' '.join(data)



@dask.delayed
def tokenize_with_daari(corpus):
    corpus = corpus.replace('\n', ' ')
    corpus = re.split(r'।+|\?+|\!+', corpus)
    # corpus = [s for s in re.split('।|\?|\!',corpus) if s]

    data = [sentence.replace("\ufeff", "") for sentence in corpus]
    data = [dat.split(" ") for dat in data]
    connectors = [
        "কারন", "যেহেতু", "অতএব", "সুতরাং", "কে", "যে", "কেকে", "এবং", "ও", "কিন্তু", "তথাপি", "যে", "যা", "যাতে",
        "ফলে", "এমনকি", "প্রথমত", "প্রায়ই", "মাঝে মাঝে", "আরো", "অধিকতর", "যেটি", "যা", "যেন", "যদিও", "যাতে",
        "সত্ত্বেও", "সত্বেও", "যখন", "অনুরূপভাবে", "একইভাবে", "অতএব", "সুতরাং", "যাতে", "যেন", "প্রথমত",
        "বরং", "চেয়ে", "তেমনই", "যাইহোক", "প্রকৃতপক্ষে", "যেহেতু", "সাধারনত", "শুধু", "কেবল", "একমাত্র", "প্রথমত",
        "পরিশেষে", "তাছাড়া", "অধিকন্তু", "উপরন্তু", "এমনি", "এটিও", "এবং", "ও", "পাশাপাশি", "অধিকন্তু", "দুঃখজনকভাবে",
        "আসলে", "অত:পর", "সুতরাং", "যথা",
        "যেমন", "লক্ষণীয়ভাবে", "মোটামুটি", "দুয়ের যে কোন একটি", "দুটির যে কোন একটি", "দুয়ের কোনটি নয়",
        "দুটির কোনটি নয়", "যাহাই ঘটুক না কেন", "অতিরিক্ত আরো", "অতিরিক্ত", "এ বিষয়ে", "বাস্তবিকপক্ষে", "সেই সঙ্গে",
        "তবু", "তথাপি", "তবুও", "তারপরও", "যদি", "অপেক্ষাকৃত", "সত্যি বলতে", "যাই ঘটুক না কেন",
        "যদি আপনি চান", "না বললেও চলে", "এ ব্যাপারে যতটুকু বলা যায়", "আমার জানা মতে", "কেন যে", "অন্যদিকে", "মোটের উপর",
        "খোলাখুলি ভাবে বলা যায়", "সত্যিকার ব্যাপার হলো", "সংক্ষেপে বলতে গেলে", "যদিও", "ঘটনাক্রমে", "তারপর", "তখন",
        "থেকে", "কিছুক্ষণের জন্য", "জন্য", "উদ্দেশ্যে", "উদ্দেশ্য", "জন্যে", "জন্য",
        "হঠাৎ", "যদিও না", "সর্বপরি", "ঊদাহরনস্বরূপ", "উদাহরনস্বরূপ", "ঊদাহরন", "উদাহরন", "পরিবর্তে", "এইভাবে",
        "দূর্ভাগ্যবশত", "একদা", "ধিরে ধিরে", "মাঝে মাঝে", "পর্যন্ত", "যতক্ষন পর্যন্ত", "যতক্ষন পর্যন্ত না",
        "যেন মনে হয়", "এমন যদিও হয়ও",
        "হতে না হতেই", "হতে", "আজ না হোক কাল", "আর কোন কিন্তু নয়", "উপলক্ষ্যে", "উপলক্ষ্য", "বিশ্বস্ত সূত্রে",
        "আপনারা জানেন", "কারণে", "বিনা দ্ধাবিধায়", "প্রথমেই", "আশ্চর্যজনকভাবে", "আশ্চর্যের ব্যাপার হলো",
        "আশ্চর্যের ব্যাপার",
        "সত্য বলতে কি", "যদিও পারতাম", "যদি না", "এই শর্তে যে", "এই লোকটিই", "চিরতরে", "এমনটি যদিও",
        "মূল কথায় ফিরে আসলে", "দৈনিক", "ভিতরে ঢুকে", "বলিলেন", "বললেন", "বললো", "দেখলো", "দেখো", "দেখ"
    ]
    # bigram_transformer = PhrasesTransformer(min_count=5, connector_words=frozenset(connectors))
    # data = bigram_transformer.fit_transform(data)
    return data



# @dask.delayed
def write_in_pkl(data, filename):
    print(filename)
    outfile = open(filename, 'wb')
    pickle.dump(data, outfile)
    outfile.close()
    return data



def f(data):
    data = clean_data(data)
    data = tokenize_with_daari(data)

    return data



def main():
    file_names = [r"data/bangla_books.pkl", r"data/banglapedia.pkl",
                  r"data/bnwiki.pkl", r"data/ittefaq.pkl",
                  r"data/kalerkantho.pkl", r"data/prothomalo.pkl",
                  r"data/sachalayatan.pkl", r"data/somewherein.pkl"]
    total_data = []
    for file_name in file_names[7:]:
        file_data = read_corpus(file_name)
        print(file_name, " Loading Done.....")
        split_size = 100
        split = int(len(file_data) / split_size)
        # print(type(split))
        iterator = 0

        for i in range(split_size):
            if (i + 1) % 5 == 0:
                print("Progress:", (i + 1), "%: ", (i + 1) * "*")
            if ((iterator + split) > len(file_data)):
                data = file_data[iterator:]
            else:
                data = file_data[iterator:(iterator + split)]
            iterator += split
            data = dask.compute(f(data))
            total_data.extend(data)
        del file_data
    write_in_pkl(total_data, r"data/somewherein.pkl".replace("data", "output"))



if __name__ == '__main__':
    # with ProgressBar():
    main()

# print(read_corpus("D:\word2VecGenerator\data\input.txt").compute())
