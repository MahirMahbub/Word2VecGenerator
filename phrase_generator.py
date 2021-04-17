import pickle

import dask
from dask.diagnostics import ProgressBar
from gensim.sklearn_api import PhrasesTransformer



def write_in_pkl(data, filename):
    print(filename)
    outfile = open(filename, 'wb')
    pickle.dump(data, outfile)
    outfile.close()
    return data



def load_data():
    file_names = [r"output_final/bangla_books.pkl", r"output_final/banglapedia.pkl",
                  r"output_final/bnwiki.pkl", r"output_final/ittefaq.pkl",
                  r"output_final/kalerkantho.pkl", r"output_final/prothomalo.pkl",
                  r"output_final/sachalayatan.pkl", r"output_final/somewherein.pkl"]
    # total_data = []
    # for file_name in file_names[7:8]:
    pkl_file = open(file_names[7], 'rb')
    file_data = pickle.load(pkl_file)
    # for data in file_data:
    #     data[:] = [i.replace('\u200c', "") for i in data if i!= ""]
    # total_data += file_data
    print(file_names[7], " loading_complete.....")
    # random.shuffle(total_data)
    return file_data



@dask.delayed
def phrase_detector(data):
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
    bigram_transformer = PhrasesTransformer(min_count=5, threshold=20.0, progress_per=10000,
                                            connector_words=frozenset(connectors))
    data = bigram_transformer.fit_transform(data)
    return data



def main(dat):
    dat = phrase_detector(dat).compute()
    return dat



# write_in_pkl(total_data,r"output_final/newspapers.pkl")

if __name__ == "__main__":
    dat = load_data()
    split_size = 20
    split = int(len(dat) / split_size)
    # print(type(split))
    iterator = 0

    for i in range(split_size):
        print("Progress:", (i + 1) * 5, "%: ", ((i + 1) * 5) * "*")
        if ((iterator + split) > len(dat)):
            data = dat[iterator:]
        else:
            data = dat[iterator:(iterator + split)]
        iterator += split
        data = main(data)
        write_in_pkl(data, r"phrase_data/" + "part_" + str(i) + "_bangla_blogs_somewherein.pkl")
