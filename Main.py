import json
import sys
import os
from datetime import datetime,timedelta 
from random import randrange,choices
import copy
import Settings as SETT
import tkinter as tk
import tkinter.messagebox as messagebox

from Util import *

def til_the_end():
    messagebox.showinfo(title = 'Finish', # 視窗標題
        message = 'Congrats! Until the end!')   # 訊息內容
    print("今日進度已完成!")
    sys.exit()

# 寫入今日錯誤紀錄 (紀錄的日期是隔天)
wrong_word_list = []
def add_wrong_word(word):
    global wrong_word_list
    new_wrong_word = copy.deepcopy(word)
    new_wrong_word["date"] = datetime.now().strftime(SETT.DATE_FORMAT)
    new_wrong_word["status"] = min(new_wrong_word["status"], 5)
    wrong_word_list.append(new_wrong_word)

def write_wrong_word():
    if SETT.TEST_FAIL :
        return
    global wrong_word_list
    another_day = True
    # 讀取檔案的日期
    fr = None
    if os.path.isfile(SETT.WRONG_WORD_PATH) :
        fr = open(SETT.WRONG_WORD_PATH, "r")
        wrong_date = fr.readline()
        wrong_date = datetime.strptime(wrong_date[:-1], SETT.DATE_FORMAT)
        if wrong_date > datetime.now() :
            another_day = False
    
    if another_day or fr == None :
        pass
    else :
        old_wrong_word_list = json.loads(fr.read())
        wrong_word_list = old_wrong_word_list + wrong_word_list
    if fr :
        fr.close()
    
    fw = open(SETT.WRONG_WORD_PATH, "w", encoding='UTF-8')
    fw.write((datetime.now() + timedelta(days=1)).strftime(SETT.DATE_FORMAT)+"\n")
    json.dump(wrong_word_list, fw, indent = 4, ensure_ascii=False)
    fw.close()
        
class Words :
    def __init__(self, Settings):
        self.word_file_path = Settings.word_file_path
        self.NEAR_FIRST = Settings.NEAR_FIRST
        self.weight = Settings.weight
        self.now_time = datetime.now()
        fr = open(self.word_file_path, "r", encoding='UTF-8')
        # 排除錯誤檔案 第一行紀錄的日期
        if SETT.TEST_FAIL :
            self.read_date = fr.readline()
        self.old_word_list = json.loads(fr.read())         # 沒有超過日期的單字
        fr.close()
        self.new_word_list = []
        # 找 random 起使位置
        self.start_indx = len(self.old_word_list)
        for indx in range(len(self.old_word_list)):
            word_last_date = self.old_word_list[indx]["date"]
            word_last_date = datetime.strptime(word_last_date, SETT.DATE_FORMAT)
            if word_last_date < self.now_time :
                self.start_indx = indx
                break
        print(f"--  {self.word_file_path}  --------------------------------")
        print("今日已讀單字 :", self.start_indx) # 有點不准，不過差不多啦

        # 處理每個字
        status_count = 0
        know_count = 0
        for indx in range(len(self.old_word_list)):
            # if self.old_word_list[indx]["association"] == "no":
            #     self.old_word_list[indx]["association"] = ""
            if self.old_word_list[indx]["status"] >= SETT.long_term_mem_threshold :
                know_count += 1
            status_count += self.old_word_list[indx]["status"]
        print("總共讀取單字數量 :", len(self.old_word_list))
        # print("學會單字數量 :", know_count)
        # print("錯誤單字數量 :", len(self.old_word_list) - know_count)
        # print("status 總和 :", status_count)
        print("status 平均 :", status_count / len(self.old_word_list))

    # 方法1 : 隨機直到日期以內
    # 方法2 : 先挑出日期以內再隨機 (但是我希望可以不要弄亂順序)
    def random_within_date(self):
        rand_range = len(self.old_word_list)
        if self.NEAR_FIRST > 0 :
            rand_range = min(rand_range, self.NEAR_FIRST+self.start_indx)
        if self.start_indx == rand_range :
            return None
        now_indx = randrange(self.start_indx, rand_range)
        while len(self.old_word_list) > self.start_indx :
            word_last_date = self.old_word_list[now_indx]["date"]
            word_last_date = datetime.strptime(word_last_date, SETT.DATE_FORMAT)
            if word_last_date < self.now_time :
                self.last_rand_indx = now_indx
                # print("rand",self.start_indx, rand_range, now_indx)
                return self.old_word_list.pop(now_indx)
            else :
                self.old_word_list.insert(0,(self.old_word_list.pop(now_indx)))
                self.start_indx += 1
                now_indx += 1
            if now_indx == len(self.old_word_list) :
                now_indx = self.start_indx
        return None
    
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
        print("總共寫入單字數量 :", len(all_words))
        for indx in range(len(all_words)):
            if all_words[indx]["status"] >= SETT.long_term_mem_threshold :
                know_count += 1
            status_count += all_words[indx]["status"]
        print("今日已讀單字 :", self.start_indx)
        # print("學會單字數量 :", know_count)
        # print("錯誤單字數量 :", len(all_words) - know_count)
        # print("status 總和 :", status_count)
        print("status 平均 :", status_count / len(all_words))
        # 寫入
        with open(self.word_file_path, "w", encoding='UTF-8') as fw:
            if SETT.TEST_FAIL :
                fw.write(self.read_date)
            json.dump(all_words, fw, indent = 4, ensure_ascii=False)
        # 備份
        if not SETT.TEST_FAIL :
            date_str = datetime.now().strftime(r"_%Y_%m_%d_%H_%M")
            with open(self.word_file_path.replace(r"\word",r"\word\backup").replace(".json", date_str+".json"), "w", encoding='UTF-8') as fw:
                json.dump(all_words, fw, indent = 4, ensure_ascii=False)

def add_new_word(word_file_path, word):
    word_file_path = word_file_path.replace(".","_new.")
    print(word_file_path)
    file_word_list = []
    if os.path.isfile(word_file_path) :
        with open(word_file_path, "r") as fr :
            file_word_list = json.loads(fr.read())
    file_word_list.append(word)
    with open(word_file_path, "w") as fw :
        json.dump(file_word_list, fw, indent = 4, ensure_ascii=False)

if __name__ == "__main__" :
    all_json = [Words(each_json_file) for each_json_file in SETT.all_json_files]
    rand_weights = tuple(each_json.weight for each_json in all_json)
    print("rand_weights :",rand_weights)
    
    import atexit
    def when_exit():
        global rand_word
        rand_json.insert_back(rand_word)
        for each_json in all_json : each_json.save()
        write_wrong_word()
    atexit.register(when_exit)

    # UI 介面
    window = tk.Tk()
    window.title('word_mem')
    # window.state("zoomed") # 有BUG 會直接點到後面
    window.geometry("1350x650+100+50")
    word_show_weight = 0.5

    show_txt = tk.Button(window,                 # 文字標示所在視窗
        text = '英文單字',  # 顯示文字
        bg = '#EEBB00',         #  背景顏色
        font = ('Arial', 20),   # 字型與大小
        width = 15, height = 2,  # 文字標示尺寸  
        command = lambda : word_to_sound(rand_word["eng"]),
    )
    show_txt.place(relx=0,rely=0,relheight=word_show_weight,relwidth=1)

    def random_a_word():
        global rand_word
        global rand_json
        global rand_weights
        while all_json :
            rand_json = choices(all_json, weights=rand_weights, k = 1)[0]
            rand_word = rand_json.random_within_date()
            if rand_word == None :
                # 查看有沒有新的單字
                new_word_path = rand_json.word_file_path.replace(".","_new.")
                # print("new_word_path :",new_word_path)
                if os.path.isfile(new_word_path) :
                    with open(new_word_path, "r", encoding='UTF-8') as new_fr:
                        new_word_file = json.loads(new_fr.read())
                        if new_word_file :
                            rand_word = new_word_file.pop(0)
                            with open(new_word_path, "w", encoding='UTF-8') as new_fw:
                                json.dump(new_word_file, new_fw, indent = 4, ensure_ascii=False)
                            rand_json.last_rand_indx = 0
                            break
                # 會執行到這裡代表沒有新的單字
                print(rand_json.word_file_path, "已結束")
                rand_json.save()
                all_json.remove(rand_json)
                rand_weights = tuple(each_json.weight for each_json in all_json)
            else :
                break
        if rand_word == None :
            til_the_end()
        show_str = rand_word["eng"]
        # word_to_sound(show_str) # 出現新單字要不要順便聽發音
        show_txt.config(text = show_str )

    def play_word_and_other():
        eng_and_other = rand_word["eng"]
        eng_and_other =  " ' ' ".join([eng_and_other] + [each_other.split(" ")[0] for each_other in rand_word["other"]])
        word_to_sound(eng_and_other)
    
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
            button_show_ans.place(relx=0,rely=word_show_weight,relheight=1-word_show_weight,relwidth=1)
            button_status = 0
        else :
            # change to know
            show_str = f'{show_txt.cget("text")} {rand_word["chi"]} ({rand_word["status"]})'
            if rand_word["association"] :
                show_str += "\n" +rand_word["association"]
            if "other" in rand_word and len(rand_word["other"])>0 :
                show_str += "\n" + "other type : "
                for other_type in rand_word["other"] :
                    show_str += "\n" + other_type
            if "similar" in rand_word and len(rand_word["similar"])>0 :
                show_str += "\n" + "similar : "
                for other_type in rand_word["similar"] :
                    show_str += "\n" + other_type
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
        # print("switch finish now button_status :",button_status)
    switch_button()
    
    # 按鈕 function
    def test_pass(word):
        # word["status"] = min(max(word["status"]+1,long_term_mem_threshold+2), len(SETT.DAYS)-1) # 很久沒有測驗 通過就直接算會了
        if SETT.TEST_FAIL :
            word["status"] = min(word["status"]+1, len(SETT.DAYS)-1)
            if word["status"] > SETT.WRONG_WORD_PASS :
                word["date"] = (datetime.now() + timedelta(days=1)).strftime(SETT.DATE_FORMAT)
            rand_json.insert_back(word)
        else :
            word["status"] = min(word["status"]+1, len(SETT.DAYS)-1)
            shift_days = SETT.DAYS[word["status"]]
            if word["status"] > (SETT.long_term_mem_threshold+2) :
                shift_days += randrange(0,4)
            word["date"] = (datetime.now() + timedelta(days=shift_days)).strftime(SETT.DATE_FORMAT)
            rand_json.add_word_first(word)
        switch_button()

    def test_again(word):
        word["status"] = max(word["status"]-1, 0)
        shift_days = SETT.DAYS[word["status"]]
        word["date"] = (datetime.now() + timedelta(days=shift_days)).strftime(SETT.DATE_FORMAT)
        rand_json.add_word_first(word)
        switch_button()

    def test_fail(word):
        if SETT.TEST_FAIL :
            word["status"] = max(word["status"]-2, 0)
            rand_json.insert_back(word)
        else :
            word["status"] = max(word["status"]-2, 0)
            shift_days = SETT.DAYS[word["status"]]
            word["date"] = (datetime.now() + timedelta(days=shift_days)).strftime(SETT.DATE_FORMAT)
            add_wrong_word(word)
            rand_json.add_word_first(word)
        switch_button()

    def test_hard(word):
        word["date"] = (datetime.now() + timedelta(days=1)).strftime(SETT.DATE_FORMAT)
        word["status"] = max(word["status"]-1, 0)
        # rand_json.add_word_last(word)
        add_new_word(rand_json.word_file_path, word)
        switch_button()

    def show_ans():
        play_word_and_other()
        switch_button()

    button_show_ans.config(command = show_ans)
    button_test_pass.config(command = lambda : test_pass(rand_word))
    button_test_again.config(command = lambda : test_again(rand_word))
    button_test_hard.config(command = lambda : test_hard(rand_word))
    button_test_fail.config(command = lambda : test_fail(rand_word))

    # 按鍵偵測
    from pynput import keyboard
    def on_release(key):
        if button_status > 0:
            if key == keyboard.Key.left:
                test_pass(rand_word)
            elif key == keyboard.Key.right:
                test_fail(rand_word)
            elif key == keyboard.Key.up:
                play_word_and_other()
            elif key == keyboard.Key.down:
                test_again(rand_word)
        else :
            if key == keyboard.Key.up:
                show_ans()
            elif key == keyboard.Key.left or key == keyboard.Key.right :
                word_to_sound(rand_word["eng"])
    # Collect events until released
    listener = keyboard.Listener(on_release=on_release)
    listener.start()
    
    # # << 執行主程式 >>
    window.mainloop()

    listener.stop()