import pickle
import random

import numpy as np
from gensim.sklearn_api import PhrasesTransformer
def write_in_pkl(data, filename):
    print(filename)
    outfile = open(filename, 'wb')
    pickle.dump(data, outfile)
    outfile.close()
    return data

file_names = [r"output/bangla_books.pkl", r"output/banglapedia.pkl",
              r"output/bnwiki.pkl", r"output/ittefaq.pkl",
              r"output/kalerkantho.pkl", r"output/prothomalo.pkl",
              r"output/sachalayatan.pkl", r"output/somewherein.pkl"]

for file_name in file_names:
    total_data = []
    pkl_file = open(file_name, 'rb')
    file_data = pickle.load(pkl_file)

    # final_list = []
    for list_2d in file_data:
        total_data += list(list_2d)
    print(file_name, " loading_complete.....")
    for data in total_data:
        data[:] = [i.replace("\xa0","") for i in data if i.replace("\xa0","").replace('°', "")!=""]

    write_in_pkl(total_data, file_name.replace("output", "output_final"))
    del total_data
    del file_data
    del pkl_file
#
# random.shuffle(total_data)
# connectors = [
#         "কারন", "যেহেতু", "অতএব", "সুতরাং", "কে", "যে", "কেকে", "এবং", "ও", "কিন্তু", "তথাপি", "যে", "যা", "যাতে",
#         "ফলে", "এমনকি", "প্রথমত", "প্রায়ই", "মাঝে মাঝে", "আরো", "অধিকতর", "যেটি", "যা", "যেন", "যদিও", "যাতে",
#         "সত্ত্বেও", "সত্বেও", "যখন", "অনুরূপভাবে", "একইভাবে", "অতএব", "সুতরাং", "যাতে", "যেন", "প্রথমত",
#         "বরং", "চেয়ে", "তেমনই", "যাইহোক", "প্রকৃতপক্ষে", "যেহেতু", "সাধারনত", "শুধু", "কেবল", "একমাত্র", "প্রথমত",
#         "পরিশেষে", "তাছাড়া", "অধিকন্তু", "উপরন্তু", "এমনি", "এটিও", "এবং", "ও", "পাশাপাশি", "অধিকন্তু", "দুঃখজনকভাবে",
#         "আসলে", "অত:পর", "সুতরাং", "যথা",
#         "যেমন", "লক্ষণীয়ভাবে", "মোটামুটি", "দুয়ের যে কোন একটি", "দুটির যে কোন একটি", "দুয়ের কোনটি নয়",
#         "দুটির কোনটি নয়", "যাহাই ঘটুক না কেন", "অতিরিক্ত আরো", "অতিরিক্ত", "এ বিষয়ে", "বাস্তবিকপক্ষে", "সেই সঙ্গে",
#         "তবু", "তথাপি", "তবুও", "তারপরও", "যদি", "অপেক্ষাকৃত", "সত্যি বলতে", "যাই ঘটুক না কেন",
#         "যদি আপনি চান", "না বললেও চলে", "এ ব্যাপারে যতটুকু বলা যায়", "আমার জানা মতে", "কেন যে", "অন্যদিকে", "মোটের উপর",
#         "খোলাখুলি ভাবে বলা যায়", "সত্যিকার ব্যাপার হলো", "সংক্ষেপে বলতে গেলে", "যদিও", "ঘটনাক্রমে", "তারপর", "তখন",
#         "থেকে", "কিছুক্ষণের জন্য", "জন্য", "উদ্দেশ্যে", "উদ্দেশ্য", "জন্যে", "জন্য",
#         "হঠাৎ", "যদিও না", "সর্বপরি", "ঊদাহরনস্বরূপ", "উদাহরনস্বরূপ", "ঊদাহরন", "উদাহরন", "পরিবর্তে", "এইভাবে",
#         "দূর্ভাগ্যবশত", "একদা", "ধিরে ধিরে", "মাঝে মাঝে", "পর্যন্ত", "যতক্ষন পর্যন্ত", "যতক্ষন পর্যন্ত না",
#         "যেন মনে হয়", "এমন যদিও হয়ও",
#         "হতে না হতেই", "হতে", "আজ না হোক কাল", "আর কোন কিন্তু নয়", "উপলক্ষ্যে", "উপলক্ষ্য", "বিশ্বস্ত সূত্রে",
#         "আপনারা জানেন", "কারণে", "বিনা দ্ধাবিধায়", "প্রথমেই", "আশ্চর্যজনকভাবে", "আশ্চর্যের ব্যাপার হলো",
#         "আশ্চর্যের ব্যাপার",
#         "সত্য বলতে কি", "যদিও পারতাম", "যদি না", "এই শর্তে যে", "এই লোকটিই", "চিরতরে", "এমনটি যদিও",
#         "মূল কথায় ফিরে আসলে", "দৈনিক", "ভিতরে ঢুকে", "বলিলেন", "বললেন", "বললো", "দেখলো", "দেখো", "দেখ"
#     ]
# bigram_transformer = PhrasesTransformer(min_count=5, threshold=10.0, progress_per=10000,
#                                             connector_words=frozenset(connectors))
# data = bigram_transformer.fit_transform(final_list)
