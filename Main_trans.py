import json
import sys
import os
from datetime import datetime,timedelta 
import time
from random import randrange,choices
import copy
import Settings as SETT
import tkinter as tk
import tkinter.messagebox as messagebox

import Util

def til_the_end():
    messagebox.showinfo(title = 'Finish', # 視窗標題
        message = 'Congrats! Until the end!')   # 訊息內容
    print("今日進度已完成!")
    sys.exit()

# 寫入今日錯誤紀錄 (紀錄的日期是隔天)
wrong_word_list = []
again_word_list = []
def add_wrong_word(word, word_list):
    new_wrong_word = copy.deepcopy(word)
    # 這裡改錯誤的那個單字的 info
    new_wrong_word["each_T"][rand_word_indx]["date"] = datetime.now().strftime(SETT.DATE_FORMAT)
    new_wrong_word["each_T"][rand_word_indx]["status"] = min(new_wrong_word["each_T"][rand_word_indx]["status"], SETT.WRONG_STATUS)
    word_list.append(new_wrong_word)

    # 從所有的單字中找出 similar 連結的單字
    for each_related in all_related :
        this_eng_word = word["each_T"][rand_word_indx]["eng"]
        sim_res = each_related.ger_related(this_eng_word)
        for each_sim in sim_res :
            if each_sim == this_eng_word :
                continue
            # 相似的也參與錯誤考試中
            if each_sim in all_word_map :
                word_whole = copy.deepcopy(all_word_map[each_sim])
                for each_w in word_whole["each_T"] :
                    if each_w["eng"] == each_sim :
                        each_w["date"] = datetime.now().strftime(SETT.DATE_FORMAT)
                        each_w["status"] = min(SETT.WRONG_STATUS, each_w["status"])
                word_list.append(word_whole)
            # else # 不用 else 因為通常是很簡單的

def write_wrong_word(wrong_word_list, file_path):
    if SETT.TEST_FAIL :
        return

    read_date = ""
    # 讀取檔案的日期
    fr = None
    if os.path.isfile(file_path) :
        fr = open(file_path, "r", encoding='UTF-8')
        read_date = fr.readline()

        old_wrong_word_list = json.loads(fr.read())
        wrong_word_list = old_wrong_word_list + wrong_word_list

        fr.close()
    
    fw = open(file_path, "w", encoding='UTF-8')
    if read_date == "" :
        read_date = (datetime.now() + timedelta(days=1)).strftime(SETT.DATE_FORMAT)+"\n"
    fw.write(read_date)
    json.dump(wrong_word_list, fw, indent = 4, ensure_ascii=False)
    fw.close()
                    
all_word_map = {}
class Words :
    def __init__(self, Settings, main_type = "trans"):
        self.word_file_path = Settings.word_file_path
        self.NEAR_FIRST = Settings.NEAR_FIRST
        self.weight = Settings.weight
        self.now_time = datetime.now()
        fr = open(self.word_file_path, "r", encoding='UTF-8')
        # 練習錯誤的檔案 第一行用來紀錄的日期 所以要排除
        if SETT.TEST_FAIL :
            read_date = datetime.strptime(fr.readline()[:-1], SETT.DATE_FORMAT)
            self.another_day = read_date < datetime.now()
        self.old_word_list = json.loads(fr.read())         # 沒有超過日期的單字
        fr.close()
        self.new_word_list = []

        status_count = 0
        know_count = 0
        del_list = []
        for indx in range(len(self.old_word_list)-1,-1,-1):
            # 確認沒有重複的
            for each_word in self.old_word_list[indx]["each_T"] :
                if each_word["eng"] in all_word_map :
                    if main_type == "trans" and each_word["chi"] != "@" :
                        print("same!! :", each_word["eng"])
                        if SETT.TEST_FAIL or SETT.DEL_DUPLICATE :
                            del_list.append(indx)
                else :
                    all_word_map[each_word["eng"]] = self.old_word_list[indx]

            # # 處理每個組合
            if main_type == "trans":
                if 'other' in self.old_word_list[indx] : # 刪除 'other'
                    del(self.old_word_list[indx]['other'])
                if "similar" in self.old_word_list[indx] : # 刪除 'similar'
                    del(self.old_word_list[indx]['similar'])

            # # 處理每個字
            del_this_word = SETT.TEST_FAIL
            for each_word in self.old_word_list[indx]["each_T"] :
                if main_type == "trans":
                    if "ex" not in each_word:
                        each_word["ex"] = []
                    if "sound" not in each_word:
                        each_word["sound"] = ""
                    if "type" not in each_word:
                        each_word["type"] = "eng"
                    if "def" not in each_word:
                        each_word["def"] = []
                    if SETT.TEST_FAIL :
                        if "2099" in each_word["date"] :
                            pass
                        elif each_word["status"] <= SETT.WRONG_WORD_PASS:
                            del_this_word = False
                        elif SETT.CLEAR_PASS :
                            pass
                        elif not self.another_day :
                            del_this_word = False    
                else :
                    if "ex" not in each_word:
                        each_word["ex"] = []
                    if type(each_word["ex"]) != type([]) :
                        each_word["ex"] = [each_word["ex"]]
            
            if del_this_word :
                del_list.append(indx)

            # 計算狀態 (同字根的單字只計算第一個)
            if self.old_word_list[indx]['each_T'][0]["status"] >= SETT.long_term_mem_threshold :
                know_count += 1
            status_count += self.old_word_list[indx]['each_T'][0]["status"]
        
        if SETT.TEST_FAIL :
            del_list = list(set(del_list))
            del_list.reverse()
            print("del_list :",del_list)
            for indx in del_list :
                del(self.old_word_list[indx])

        # 找 random 起使位置
        self.start_indx = len(self.old_word_list)
        break_flag = False
        for indx in range(len(self.old_word_list)):
            for each_word in self.old_word_list[indx]['each_T'] :
                word_last_date = each_word["date"]
                word_last_date = datetime.strptime(word_last_date, SETT.DATE_FORMAT)
                if word_last_date < self.now_time :
                    self.start_indx = indx
                    break_flag = True
                    break
            if break_flag :
                break
        
        if len(self.old_word_list) != 0 :
            print(f"--  {self.word_file_path}  --------------------------------")
            print("今日已讀單字 :", self.start_indx) # 有點不准，不過不會差太多
            print("總共讀取單字數量 :", len(self.old_word_list))
            # print("學會單字數量 :", know_count)
            # print("錯誤單字數量 :", len(self.old_word_list) - know_count)
            print("status 平均 :", status_count / len(self.old_word_list))

    # 方法1 : 隨機直到日期以內
    # 方法2 : 先挑出日期以內再隨機 (但是我希望可以不要弄亂順序)
    def random_within_date(self):
        rand_range = len(self.old_word_list)
        if self.NEAR_FIRST > 0 :
            rand_range = min(rand_range, self.NEAR_FIRST+self.start_indx)
        if self.start_indx == rand_range :
            return None, -1
        now_indx = randrange(self.start_indx, rand_range)
        rand_indx_mem = now_indx
        while len(self.old_word_list) > self.start_indx :
            for indx, this_word in enumerate(self.old_word_list[now_indx]["each_T"]) :
                word_last_date = this_word["date"]
                word_last_date = datetime.strptime(word_last_date, SETT.DATE_FORMAT)
                if word_last_date <= self.now_time :
                    self.last_rand_indx = now_indx
                    # print("rand",self.start_indx, rand_range, now_indx)
                    return self.old_word_list.pop(now_indx), indx
            if SETT.TEST_FAIL == False:
                self.old_word_list.insert(0,(self.old_word_list.pop(now_indx)))
                self.start_indx += 1
            now_indx += 1
            if now_indx == len(self.old_word_list) :
                now_indx = self.start_indx
            if SETT.TEST_FAIL and rand_indx_mem == now_indx :
                break
        return None, -1
    
    def add_word_first(self, item):
        self.new_word_list.insert(0,item)

    def add_word_last(self, item):
        self.old_word_list.append(item)

    def insert_back(self, random_word = None):
        if random_word != None :
            self.old_word_list.insert(self.last_rand_indx, random_word)

    def save(self):
        all_words = self.new_word_list + self.old_word_list
        print(f"--  {self.word_file_path}  --------------------------------")
        status_count = 0
        know_count = 0
        if len(self.old_word_list) != 0 :
            print("總共寫入單字數量 :", len(all_words))
            for indx in range(len(all_words)):
                if all_words[indx]['each_T'][0]["status"] >= SETT.long_term_mem_threshold :
                    know_count += 1
                status_count += all_words[indx]['each_T'][0]["status"]
            print("今日已讀單字 :", self.start_indx)
            # print("學會單字數量 :", know_count)
            # print("錯誤單字數量 :", len(all_words) - know_count)
            print("status 平均 :", status_count / len(all_words))

        # 寫入
        with open(self.word_file_path, "w", encoding='UTF-8') as fw:
            if SETT.TEST_FAIL :
                fw.write((datetime.now() + timedelta(days=1)).strftime(SETT.DATE_FORMAT)+"\n")
            json.dump(all_words, fw, indent = 4, ensure_ascii=False)
        # 備份
        if not SETT.TEST_FAIL :
            date_str = datetime.now().strftime(r"_%Y_%m_%d_%H_%M")
            with open(self.word_file_path.replace(r"\word",r"\word_backup").replace(".json", date_str+".json"), "w", encoding='UTF-8') as fw:
                json.dump(all_words, fw, indent = 4, ensure_ascii=False)

small_dict = {}
class Related(Util.UF_find_relate) :
    def __init__(self, related_file_path):
        super().__init__()
        fr = open(related_file_path, "r", encoding='UTF-8')
        last_related_word = ""
        for each_word in fr:
            if "-----" in each_word :
                break
            if each_word == "" :
                continue
            # 處理單字
            each_word_split = each_word.split(" / ")
            this_word = each_word_split[0].strip()
            if len(each_word_split) >= 2 :
                small_dict[this_word] = each_word_split[1].strip()

            if this_word == "":
                last_related_word = ""
            else :
                if last_related_word == "" :
                    last_related_word = this_word
                else :
                    self.union(this_word, last_related_word)
        fr.close()

def add_new_word(word_file_path, word):
    word_file_path = word_file_path.replace(".","_new.")
    print(word_file_path)
    file_word_list = []
    if os.path.isfile(word_file_path) :
        with open(word_file_path, "r", encoding='UTF-8') as fr :
            file_word_list = json.loads(fr.read())
    file_word_list.append(word)
    with open(word_file_path, "w", encoding='UTF-8') as fw :
        json.dump(file_word_list, fw, indent = 4, ensure_ascii=False)

def get_new_word(rand_json):
    rand_word = None
    new_word_path = rand_json.word_file_path.replace(".","_new.")
    if os.path.isfile(new_word_path) :
        with open(new_word_path, "r", encoding='UTF-8') as new_fr:
            new_word_file = json.loads(new_fr.read())
            if new_word_file :
                try :
                    rand_word = new_word_file.pop(0)
                except :
                    return None # 有檔案 但是裡面沒有單字了
                with open(new_word_path, "w", encoding='UTF-8') as new_fw:
                    json.dump(new_word_file, new_fw, indent = 4, ensure_ascii=False)
                rand_json.last_rand_indx = 0
    return rand_word

def random_a_word():
    global rand_word
    global rand_word_indx
    global rand_json
    global rand_weights
    while all_json :
        rand_json = choices(all_json, weights=rand_weights, k = 1)[0]
        rand_word, rand_word_indx = rand_json.random_within_date()
        if rand_word == None :
            # 查看有沒有新的單字
            rand_word = get_new_word(rand_json)
            if rand_word != None :
                break
            # 會執行到這裡代表沒有新的單字
            print(rand_json.word_file_path, "已結束")
            rand_json.save()
            all_json.remove(rand_json)
            rand_weights = tuple(each_json.weight for each_json in all_json)
            if SETT.STRICT_WEI :
                if sum(rand_weights) == 0 :
                    break
        else :
            break
    if rand_word == None :
        til_the_end()

def test_the_word():
    global rand_word_chi
    if "chi" in rand_word["each_T"][rand_word_indx] :
        rand_word_chi = rand_word["each_T"][rand_word_indx]["chi"]
    else :
        rand_word_chi = ""
    if rand_word_chi == "@" :
        this_eng = rand_word["each_T"][rand_word_indx]["eng"]
        for each_w in all_word_map[this_eng]["each_T"] : 
            if each_w["eng"] == this_eng :
                rand_word_chi = each_w["chi"]
    
    show_str = ""
    if rand_word["each_T"][rand_word_indx]["type"] == "sound" :
        show_str = "(SOUND!!) " + rand_word["each_T"][rand_word_indx]["eng"]
    elif rand_word["each_T"][rand_word_indx]["type"] == "spell" :
        show_str = "(sound only)"
        play_word_eng(False)
    elif rand_word["each_T"][rand_word_indx]["type"] == "eng" :
        show_str = rand_word_chi + " (eng) " + str(len(rand_word["each_T"]))
    else :
        # 如果等級滿了就練英文聽力 (聽到要知道是什麼單字)
        if not Util.no_network and rand_word["each_T"][rand_word_indx]["status"] >= SETT.FULL_LEVEL and randrange(0,2) == 0 :
            show_str = "(sound only)"
            play_word_eng(False)
            # There's still a chance that the first one might encounter bugs, but it rarely occurs.
            time.sleep(0.2)
            if Util.no_network : 
                show_str = rand_word["each_T"][rand_word_indx]["eng"] + " (Chi)"
        else :
            show_str = rand_word["each_T"][rand_word_indx]["eng"] + " (Chi)"
    show_txt.config(text = show_str)

def play_word_eng(other = False, play_word = None, play_word_indx = None):
    if play_word == None :
        play_word = rand_word
        play_word_indx = rand_word_indx
    eng_and_other = ""
    if "sound" in play_word["each_T"][play_word_indx] :
        eng_and_other = play_word["each_T"][play_word_indx]["sound"]
    if eng_and_other == "" :
        eng_and_other = play_word["each_T"][play_word_indx]["eng"]

    if other :
        for indx, each_word in enumerate(play_word["each_T"]) :
            if indx != play_word_indx :
                eng_and_other += " , " + (each_word["sound"] if each_word["sound"] != "" else each_word["eng"])
    Util.word_to_sound(eng_and_other)

if __name__ == "__main__" :
    all_json = [Words(each_json_file) for each_json_file in SETT.all_json_files]
    rand_weights = tuple(each_json.weight for each_json in all_json)
    print("rand_weights :",rand_weights)

    # similar set 讀取有相關的單字
    all_related = [Related(each_related_file) for each_related_file in SETT.all_related_files]
    
    import atexit
    def when_exit():
        global rand_word
        global rand_json
        rand_json.insert_back(rand_word)
        for each_json in all_json : each_json.save()
        write_wrong_word(wrong_word_list, SETT.WRONG_WORD_PATH)
        write_wrong_word(again_word_list, SETT.AGAIN_WORD_PATH)
    atexit.register(when_exit)

    # UI 介面
    window = tk.Tk()
    window.title('word_mem')
    def detect_focus(event):
        if event.widget == window:
            # print("gained the focus")
            window.isfocus = True
    def detect_unfocus(event):
        if event.widget == window:
            # print("lost the focus")
            window.isfocus = False
    window.bind("<FocusIn>", detect_focus)
    window.bind("<FocusOut>", detect_unfocus)
    # window.state("zoomed") # 有BUG 會直接點到後面
    window.geometry("1350x650+100+50")
    word_show_weight = 0.5

    show_txt = tk.Button(window,                 # 文字標示所在視窗
        text = '英文單字',  # 顯示文字
        bg = '#EEBB00',         #  背景顏色
        font = ('Arial', 20),   # 字型與大小
        width = 15, height = 2,  # 文字標示尺寸  
        command = lambda : play_word_eng(False),
    )
    show_txt.place(relx=0,rely=0,relheight=word_show_weight,relwidth=1)
    
    # 按鈕初始化
    button_show_ans = tk.Button(window,text = '顯示翻譯(up)',font = ('黑體', 15))
    button_test_pass = tk.Button(window,text = '知道(left)',font = ('黑體', 15))
    button_test_again = tk.Button(window,text = '沒有及時反應',font = ('黑體', 15))
    button_test_hard = tk.Button(window,text = '難且不常出現',font = ('黑體', 15))
    button_test_fail = tk.Button(window,text = '不知道(right)',font = ('黑體', 15))

    button_status = 2 # 2 : init / 1 : show ans / 0 : Know
    def switch_button():
        global button_status
        if button_status > 0:  
            # change to show ans
            if button_status != 2 :
                button_test_pass.place_forget()
                button_test_again.place_forget()
                button_test_hard.place_forget()
                button_test_fail.place_forget()
            random_a_word()
            test_the_word()
            button_show_ans.place(relx=0,rely=word_show_weight,relheight=1-word_show_weight,relwidth=1)
            button_status = 0
        else :
            # change to know
            show_str = ""
            # include type "eng", "chi", "sound", "spell"("sound", "spell" 是因為說不定有中文)
            eng_str = rand_word["each_T"][rand_word_indx]["eng"]
            chi_str = rand_word["each_T"][rand_word_indx]["chi"]
            if chi_str == "@" :
                chi_str = rand_word_chi
            show_str = f'{eng_str} {chi_str} ({rand_word["each_T"][rand_word_indx]["status"]})'
            if rand_word["association"] :
                show_str += "\n" +rand_word["association"]
            if len(rand_word["each_T"]) > 1 :
                for indx, each_word in enumerate(rand_word["each_T"]) :
                    if indx != rand_word_indx :
                        show_str += "\n" + each_word["eng"] + " " + each_word["chi"]
            if "def" in rand_word["each_T"][rand_word_indx] :
                for each_def in rand_word["each_T"][rand_word_indx]["def"] :
                    show_str += "\n" + each_def
            if "ex" in rand_word["each_T"][rand_word_indx] :
                for indx, each_ex in enumerate(rand_word["each_T"][rand_word_indx]["ex"]) :
                    if "'" not in each_ex :
                        each_ex = each_ex.replace(eng_str,f"'{eng_str}'")
                        rand_word["each_T"][rand_word_indx]["ex"][indx] = each_ex
                    show_str += "\n" + each_ex
            
            for each_related in all_related :
                this_eng_word = rand_word["each_T"][rand_word_indx]["eng"]
                sim_res = each_related.ger_related(this_eng_word)
                if len(sim_res) >= 2 :
                    show_str += "\n" + "similar : "
                    for each_sim in sim_res :
                        if each_sim == this_eng_word :
                            continue
                        chi = small_dict.get(each_sim, None)
                        if chi != None :
                            show_str += "\n" + each_sim + " " + chi
                        elif each_sim in all_word_map :
                            for each_type in all_word_map[each_sim]["each_T"] :
                                if each_type["eng"] == each_sim :
                                    show_str += "\n" + each_sim + " " + each_type["chi"]
                                    break
                        else :
                            show_str += "\n" + each_sim
            
            show_txt.config(text=show_str)
            place_weight = [2,1,1,2]
            weight_sum = sum(place_weight)
            place_weight = [each_weight / weight_sum for each_weight in place_weight]
            relx_pos = []
            total_relx = 0.0
            for percentage in place_weight :
                relx_pos.append(total_relx)
                total_relx += percentage
            button_test_pass.place(relx=relx_pos[0],rely=word_show_weight,relheight=1-word_show_weight,relwidth=place_weight[0])
            button_test_again.place(relx=relx_pos[1],rely=word_show_weight,relheight=1-word_show_weight,relwidth=place_weight[1])
            button_test_hard.place(relx=relx_pos[2],rely=word_show_weight,relheight=1-word_show_weight,relwidth=place_weight[2])
            button_test_fail.place(relx=relx_pos[3],rely=word_show_weight,relheight=1-word_show_weight,relwidth=place_weight[3])
            button_show_ans.place_forget()
            button_status = 1
    switch_button()
    
    # 按鈕 function
    def test_pass(word):
        if SETT.TEST_FAIL :
            word["each_T"][rand_word_indx]["status"] = min(word["each_T"][rand_word_indx]["status"]+1, SETT.FULL_LEVEL)
            if word["each_T"][rand_word_indx]["status"] > SETT.WRONG_WORD_PASS :
                word["each_T"][rand_word_indx]["date"] = (datetime.now() + timedelta(days=1)).strftime(SETT.DATE_FORMAT)
            rand_json.insert_back(word)
        else :
            word["each_T"][rand_word_indx]["status"] = min(word["each_T"][rand_word_indx]["status"]+1, SETT.FULL_LEVEL)
            shift_days = SETT.DAYS[word["each_T"][rand_word_indx]["status"]]
            if word["each_T"][rand_word_indx]["status"] > (SETT.long_term_mem_threshold+2) :
                shift_days += randrange(0,4)
            elif word["each_T"][rand_word_indx]["status"] > 4 :
                shift_days += randrange(-1,2)
            word["each_T"][rand_word_indx]["date"] = (datetime.now() + timedelta(days=shift_days)).strftime(SETT.DATE_FORMAT)
            
            # 如果前一個單字已經 滿state
            if word["each_T"][rand_word_indx]["status"] >= SETT.D49_indx :
                next_indx = rand_word_indx + 1
                if next_indx == len(word["each_T"]) :
                    next_indx = 0
                # 1. 可以開始背下一個單字
                if "2099" in word["each_T"][next_indx]["date"] :
                    print("full next word :", word["each_T"][next_indx]["eng"] )
                    word["each_T"][next_indx]["date"] = (datetime.now() + timedelta(days=1)).strftime(SETT.DATE_FORMAT)
                    if word["each_T"][next_indx]["status"] == 0:
                        word["each_T"][next_indx]["status"] = 7
                # 2. 如果有其他 滿state 的單字, 全部一起更新日期 並把下一個單字設定比較前面
                rand_days = randrange(0,4)
                for i in range(len(word["each_T"])) :
                    if word["each_T"][i]["status"] >= SETT.FULL_LEVEL : # 滿等才需要因為其他正確跟著改日期
                        shift_days = SETT.DAYS[word["each_T"][i]["status"]] + rand_days
                        if i == next_indx :
                            shift_days -= 1
                        word["each_T"][i]["date"] = (datetime.now() + timedelta(days=shift_days)).strftime(SETT.DATE_FORMAT)

            rand_json.add_word_first(word)
        switch_button()

    def test_again(word):
        if SETT.TEST_FAIL :
            # Sometimes, the same word might appear twice.
            rand_json.insert_back(word)
        else :
            word["each_T"][rand_word_indx]["status"] = max(word["each_T"][rand_word_indx]["status"]-1, 0)
            shift_days = SETT.DAYS[word["each_T"][rand_word_indx]["status"]]
            word["each_T"][rand_word_indx]["date"] = (datetime.now() + timedelta(days=shift_days)).strftime(SETT.DATE_FORMAT)
            add_wrong_word(word, again_word_list)
            rand_json.add_word_first(word)
        switch_button()

    def test_fail(word):
        if SETT.TEST_FAIL :
            word["each_T"][rand_word_indx]["status"] = max(word["each_T"][rand_word_indx]["status"]-2, 0)
            rand_json.insert_back(word)
        else :
            word["each_T"][rand_word_indx]["status"] = max(word["each_T"][rand_word_indx]["status"]-2, 0)
            shift_days = SETT.DAYS[word["each_T"][rand_word_indx]["status"]]
            word["each_T"][rand_word_indx]["date"] = (datetime.now() + timedelta(days=shift_days)).strftime(SETT.DATE_FORMAT)
            add_wrong_word(word, wrong_word_list)
            rand_json.add_word_first(word)
        switch_button()

    def test_hard(word):
        word["each_T"][rand_word_indx]["date"] = (datetime.now() + timedelta(days=1)).strftime(SETT.DATE_FORMAT)
        word["each_T"][rand_word_indx]["status"] = max(word["each_T"][rand_word_indx]["status"]-1, 0)
        add_new_word(rand_json.word_file_path, word)
        switch_button()

    def show_ans():
        play_word_eng(True)
        switch_button()

    button_show_ans.config(command = show_ans)
    button_test_pass.config(command = lambda : test_pass(rand_word))
    button_test_again.config(command = lambda : test_again(rand_word))
    button_test_hard.config(command = lambda : test_hard(rand_word))
    button_test_fail.config(command = lambda : test_fail(rand_word))

    # 按鍵偵測
    from pynput import keyboard
    def on_release(key):
        if not window.isfocus :
            return
        if button_status > 0:
            if key == keyboard.Key.left:
                test_pass(rand_word)
            elif key == keyboard.Key.right:
                test_fail(rand_word)
            elif key == keyboard.Key.up:
                play_word_eng(True)
            elif key == keyboard.Key.down:
                test_again(rand_word)
        else :
            if key == keyboard.Key.up:
                show_ans()
            elif key == keyboard.Key.left or key == keyboard.Key.right :
                play_word_eng(False)
    # Collect events until released
    listener = keyboard.Listener(on_release=on_release)
    listener.start()
    
    # # << 執行主程式 >>
    window.mainloop()

    listener.stop()