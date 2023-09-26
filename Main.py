import json
from datetime import datetime,timedelta 
from random import randrange
import Settings as SETT
import tkinter as tk

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
        return self.time_past_list.pop(randrange(len(self.time_past_list)))
    
    def add_word(self, item):
        self.new_word_list.insert(0,item) # ?? 有可能會花很久

    def save(self, random_word = None):
        if random_word == None :
            random_word = []
        else :
            random_word = [random_word]
        all_words = self.new_word_list + random_word + self.time_past_list + self.old_word_list
        print("總共寫入單字數量 : ", len(all_words))
        with open(SETT.word_file_path.replace(".json","_after.json"), "w", encoding='UTF-8') as fw:
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
    window.title('Hello World')
    window.state("zoomed")
    word_show_weight = 0.2

    show_txt = tk.Label(window,                 # 文字標示所在視窗
        text = '英文單字',  # 顯示文字
        bg = '#EEBB00',         #  背景顏色
        font = ('Arial', 12),   # 字型與大小
        width = 15, height = 2  # 文字標示尺寸   
    )
    show_txt.place(relx=0,rely=0,relheight=word_show_weight,relwidth=1)

    def random_a_word():
        global rand_word
        rand_word = words.random_within_date()
        show_txt.config(text=rand_word["eng"])
        print(rand_word)

    # 按鈕初始化
    button_show_ans = tk.Button(window,text = '顯示翻譯')
    button_test_pass = tk.Button(window,text = '知道',)
    button_test_fail = tk.Button(window,text = '不知道')

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
            show_txt.config(text=rand_word["chi"])
            button_test_pass.place(relx=0,rely=word_show_weight,relheight=1-word_show_weight,relwidth=0.5)
            button_test_fail.place(relx=0.5,rely=word_show_weight,relheight=1-word_show_weight,relwidth=0.5)
            button_show_ans.place_forget()
            button_status = 1
        print("switch finish now button_status : ",button_status)
    switch_button()
    
    # 按鈕 function
    def test_pass(word):
        switch_button()
        word["date"] = (datetime.now() + timedelta(days=SETT.DAYS[word["status"]])).strftime(SETT.DATE_FORMAT)
        word["status"] = min(word["status"]+1, len(SETT.DAYS)-1)
        words.add_word(rand_word)

    def test_fail(word):
        switch_button()
        word["date"] = (datetime.now() + timedelta(days=1)).strftime(SETT.DATE_FORMAT)
        word["status"] = max(word["status"]-1, 0)
        words.add_word(rand_word)

    def show_ans():
        switch_button()

    button_show_ans.config(command = show_ans)
    button_test_pass.config(command = lambda : test_pass(rand_word))
    button_test_fail.config(command = lambda : test_fail(rand_word))
    
    # # << 執行主程式 >>
    window.mainloop()
