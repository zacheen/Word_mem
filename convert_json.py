# 這是把舊的格式(txt)轉換成新的格式(json)
import json

word_file_path = r"D:\dont_move\word\gre_test.txt"
fr = open(word_file_path, "r")
all_word = []
for lines in fr :
    lines = lines.strip()
    w_info = lines.split("\t")
    if len(w_info) == 1 :
        continue
    print(w_info)
    each_Word = {
        "date" : w_info[0],
        "status" : int(w_info[1]),
        "eng" : w_info[2],
        "chi" : w_info[3],
        "association" : w_info[4]}
    all_word.append(each_Word)

fr.close()

with open(word_file_path.replace(".txt",".json"), "w", encoding='UTF-8') as fw:
    json.dump(all_word, fw, indent = 4, ensure_ascii=False)