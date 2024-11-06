# 這是把舊的格式(txt)轉換成新的格式(json)
import json

word_file_path = r"D:\dont_move\word\to_convert.txt"
fr = open(word_file_path, "r")
all_content = fr.readlines()
read_indx = 0
def next_line():
    global read_indx
    if read_indx >= len(all_content):
        raise IndexError 
    ret = all_content[read_indx]
    read_indx += 1
    return ret.strip()

all_word = []
while True :
    # split_method = "sound"
    split_method = "translate"
    try :
        if split_method == "sound" :
            read_line = next_line()
            read_line = read_line.split(" ")
            # print(read_line)
            eng_word = read_line[0]
            if len(read_line) > 1 :
                sound = read_line[1]
            else :
                sound = ""
            
            each_Word = \
            {
                "association": "",
                "similar": [
                ],
                "each_T": [
                    {
                        "eng": eng_word,
                        "chi": "",
                        "status": 0,
                        "date": "2020/01/01",
                        "ex": [],
                        "sound": sound,
                        "type": "sound"
                    }
                ]
            }
        elif split_method == "translate" :
            read_line = next_line()
            read_line = read_line.split("\t")
            # print(read_line)
            eng_word = read_line[2] # " ".join(read_line[:-1])
            chi_word = read_line[3]
            
            # chi_word = chi_word.replace("(","").replace(")","")
            each_Word = \
            {
                "association": "",
                "similar": [
                ],
                "each_T": [
                    {
                        "eng": eng_word,
                        "chi": chi_word,
                        "status": 7,
                        "date": "2020/01/01",
                        "ex": [],
                        "sound": "",
                        "type": "chi"
                    }
                ]
            }
        all_word.append(each_Word)
    except IndexError :
        break

fr.close()

with open(word_file_path.replace(".txt",".json"), "w", encoding='UTF-8') as fw:
    json.dump(all_word, fw, indent = 4, ensure_ascii=False)