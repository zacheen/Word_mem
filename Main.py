import json
from datetime import datetime,timedelta 
from random import randrange
import Settings as SETT
import tkinter as tk

from Util import *
class Words :
    def __init__(self):
        self.now_time = datetime.now()
        fr = open(SETT.word_file_path, "r")
        self.old_word_list = json.loads(fr.read())         # 沒有超過日期的單字
        print("總共讀取單字數量 : ", len(self.old_word_list))
        self.time_past_list = []  # 不能用 deque 因為要 pop  # 超過日期的單字
        self.new_word_list = []
        indx = 0
        for _ in range(len(self.old_word_list)):
            word_last_date = self.old_word_list[indx]["date"]
            word_last_date = datetime.strptime(word_last_date, SETT.DATE_FORMAT)
            if word_last_date < self.now_time :
                self.time_past_list.append(self.old_word_list.pop(indx))
            else :
                indx += 1

    # 方法1 : 隨機直到日期以內
    # 方法2 : 先挑出日期以內再隨機 (但是我希望可以不要弄亂順序)
    def random_within_date(self):
        NEAR_FIRST = 100 # 最近看過的項目優先隨機到
        rand_range = len(self.time_past_list)
        if NEAR_FIRST > 0 :
            rand_range = min(rand_range, NEAR_FIRST)
        return self.time_past_list.pop(randrange(rand_range))
    
    def add_word(self, item):
        self.new_word_list.insert(0,item) # ?? 有可能會花很久

    def save(self, random_word = None):
        if random_word == None :
            random_word = []
        else :
            random_word = [random_word]
        all_words = self.new_word_list + random_word + self.time_past_list + self.old_word_list
        print("總共寫入單字數量 : ", len(all_words))
        with open(SETT.word_file_path, "w", encoding='UTF-8') as fw:
            json.dump(all_words, fw, indent = 4, ensure_ascii=False)
        # 備份
        date_str = datetime.now().strftime(r"_%Y_%m_%d_%H_%M")
        with open(SETT.word_file_path.replace(".json", date_str+".json"), "w", encoding='UTF-8') as fw:
            json.dump(all_words, fw, indent = 4, ensure_ascii=False)

if __name__ == "__main__" :
    words = Words()
    
    import atexit
    def when_exit():
        global rand_word
        words.save(rand_word)
    atexit.register(when_exit)

    # UI 介面
    window = tk.Tk()
    window.title('word_mem')
    # window.state("zoomed") # 有BUG 會直接點到後面
    window.geometry("900x500+350+100")
    word_show_weight = 0.4

    show_txt = tk.Button(window,                 # 文字標示所在視窗
        text = '英文單字',  # 顯示文字
        bg = '#EEBB00',         #  背景顏色
        font = ('Arial', 15),   # 字型與大小
        width = 15, height = 2,  # 文字標示尺寸  
        command = lambda : word_to_sound(rand_word["eng"]),
    )
    show_txt.place(relx=0,rely=0,relheight=word_show_weight,relwidth=1)

    def random_a_word():
        global rand_word
        rand_word = words.random_within_date()
        show_str = rand_word["eng"]
        show_txt.config(text = show_str )
        word_to_sound(show_str)
        print(rand_word)

    # 按鈕初始化
    button_show_ans = tk.Button(window,text = '顯示翻譯',font = ('黑體', 15))
    button_test_pass = tk.Button(window,text = '知道',font = ('黑體', 15))
    button_test_fail = tk.Button(window,text = '不知道',font = ('黑體', 15))

    button_status = 2 # 2 : init / 1 : show ans / 0 : Know
    def switch_button():
        global button_status
        if button_status > 0:  
            # change to show ans
            if button_status != 2 :
                button_test_pass.place_forget()
                button_test_fail.place_forget()
            random_a_word()
            button_show_ans.place(relx=0,rely=word_show_weight,relheight=1-word_show_weight,relwidth=1)
            button_status = 0
        else :
            # change to know
            show_str = rand_word["chi"]
            if rand_word["association"] != "no" :
                show_str += "\n" +rand_word["association"]
            show_txt.config(text=show_str)
            button_test_pass.place(relx=0,rely=word_show_weight,relheight=1-word_show_weight,relwidth=0.5)
            button_test_fail.place(relx=0.5,rely=word_show_weight,relheight=1-word_show_weight,relwidth=0.5)
            button_show_ans.place_forget()
            button_status = 1
        print("switch finish now button_status : ",button_status)
    switch_button()
    
    # 按鈕 function
    def test_pass(word):
        print(word["status"])
        print(SETT.DAYS[word["status"]])
        word["date"] = (datetime.now() + timedelta(days=SETT.DAYS[word["status"]])).strftime(SETT.DATE_FORMAT)
        word["status"] = min(word["status"]+1, len(SETT.DAYS)-1)
        words.add_word(rand_word)
        switch_button()

    def test_fail(word):
        next_day = 1
        if word["status"] > 11 :
            # 如果已經進入長期記憶 又錯誤的話要確認有沒有進入長期記憶
            # 因此要延後幾天再確認一次
            next_day = 7
        word["date"] = (datetime.now() + timedelta(days=next_day)).strftime(SETT.DATE_FORMAT)
        word["status"] = max(word["status"]-1, 0)
        words.add_word(rand_word)
        switch_button()

    def show_ans():
        switch_button()

    button_show_ans.config(command = show_ans)
    button_test_pass.config(command = lambda : test_pass(rand_word))
    button_test_fail.config(command = lambda : test_fail(rand_word))
    
    # # << 執行主程式 >>
    window.mainloop()
