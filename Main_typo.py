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
import Main_trans
import random

def til_the_end():
    print("今日進度已完成!")
    sys.exit()

import ctypes,sys
STD_OUTPUT_HANDLE = -11
std_out_handle = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)

def set_cmd_text_color(color, handle=std_out_handle):
    Bool = ctypes.windll.kernel32.SetConsoleTextAttribute(handle, color)
    return Bool

#reset white
FOREGROUND_WHITE = 0x0f # white.
def resetColor():
    set_cmd_text_color(FOREGROUND_WHITE)

FOREGROUND_DARKRED = 0x04 # dark red.
def printDarkRed(mess):
    sys.stdout.flush()
    set_cmd_text_color(FOREGROUND_DARKRED)
    sys.stdout.write(mess)
    sys.stdout.flush()
    resetColor()

all_word_map = {}
if __name__ == "__main__" :
    all_json = [Main_trans.Words(each_json_file, "typo") for each_json_file in SETT.type_files]
    rand_weights = tuple(each_json.weight for each_json in all_json)

    import atexit
    def when_exit():
        global rand_word
        rand_json.insert_back(rand_word)
        print("save back :", rand_word)
        for each_json in all_json : each_json.save()
        # write_wrong_word(wrong_word_list, SETT.WRONG_WORD_PATH)
        # write_wrong_word(again_word_list, SETT.AGAIN_WORD_PATH)
    atexit.register(when_exit)

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
                rand_word = Main_trans.get_new_word(rand_json)
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
        possible_method = [0]
        # 曾經打錯過
        if rand_word["each_T"][rand_word_indx]["wrong"] != "" :
            possible_method.append(1) # 印出錯誤
            possible_method.append(2) # 用聽的
        # 有例子
        if len(rand_word["each_T"][rand_word_indx]["ex"]) > 0:
            possible_method.append(4)
            possible_method.remove(0)

        rand_method = choices(possible_method, k=1)[0]
        # print("possible_method : ",possible_method, rand_method)
        show_str = ""
        if rand_method == 0 :
            show_str += rand_word["each_T"][rand_word_indx]["eng"]
        elif rand_method == 1 :
            show_str += rand_word["each_T"][rand_word_indx]["wrong"]
        elif rand_method == 2 :
            show_str += "(spell)"
            Main_trans.play_word_eng(False, rand_word, rand_word_indx)
        elif rand_method == 4 :
            show_str += choices(rand_word["each_T"][rand_word_indx]["ex"], k = 1)[0]

        return show_str + " : "

    def test_pass(word):
        word["each_T"][rand_word_indx]["status"] = min(word["each_T"][rand_word_indx]["status"]+1, SETT.FULL_LEVEL)
        shift_days = SETT.DAYS[word["each_T"][rand_word_indx]["status"]]
        if word["each_T"][rand_word_indx]["status"] > (SETT.long_term_mem_threshold+2) :
            shift_days += randrange(0,4)
        elif word["each_T"][rand_word_indx]["status"] > 3 :
            shift_days += randrange(-1,2)
        word["each_T"][rand_word_indx]["date"] = (datetime.now() + timedelta(days=shift_days)).strftime(SETT.DATE_FORMAT)
        
        # 如果前一個單字已經 滿state
        if word["each_T"][rand_word_indx]["status"] >= SETT.D45_indx :
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

    def test_fail(word):
        word["each_T"][rand_word_indx]["status"] = max(word["each_T"][rand_word_indx]["status"]-2, 0)
        shift_days = SETT.DAYS[word["each_T"][rand_word_indx]["status"]]
        word["each_T"][rand_word_indx]["date"] = (datetime.now() + timedelta(days=shift_days)).strftime(SETT.DATE_FORMAT)
        rand_json.add_word_first(word)

        #Practice again
        cor = word["each_T"][rand_word_indx]["eng"]
        while True :
            type_in = input("Practice again : ")
            if type_in == "C" or type_in == cor :
                break
            print("正確 : "+cor)
            print("輸入 : "+type_in)

    while True :
        random_a_word()
        show_str = test_the_word()
        try :
            type_in = input(show_str)
        except KeyboardInterrupt :
            sys.exit()

        if type_in == rand_word["each_T"][rand_word_indx]["eng"] :
            print("the same")
            test_pass(rand_word)
        elif type_in == "C" :
            test_pass(rand_word)
        else :
            cor = rand_word["each_T"][rand_word_indx]["eng"]
            print("正確 : "+cor)
            print("輸入 : ", end="")
            same = True
            for each_word_index in range(min(len(cor), len(type_in))) :
                if type_in[each_word_index] == cor[each_word_index]:
                    print(type_in[each_word_index], end="")
                else:
                    printDarkRed(type_in[each_word_index])
                    same = False
            print("")
            test_fail(rand_word)