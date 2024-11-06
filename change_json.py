import json

file_path = r"D:\dont_move\word\typo.json"
fr = open(file_path, "r", encoding='UTF-8')
all_word = json.loads(fr.read())
fr.close()

new_all_word = []
for each_item in all_word :
    each_item["eng"] = each_item["correct"]
    del(each_item["correct"])
    if each_item["wrong"] == each_item["eng"] :
        each_item["wrong"] = ""
    each_item["date"] = "2024/09/10"
    each_item["status"] = 3
    new_item = {}
    new_item["each_T"] = [each_item]
    new_all_word.append(new_item)

fw = open(file_path, "w", encoding='UTF-8')
json.dump(new_all_word, fw, indent = 4, ensure_ascii=False)