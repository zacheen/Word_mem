import threading
import Settings as SETT

class UF_find_relate:
    def __init__(self):
        self.id = {}
        self.set_member = {}
        print("set_member :",self.set_member)
    
    # won't dirrectly use this function
    # because when using "union" it will be adding automatically
    # if only one item needs to be added, it means that no other is related to this item, so no related result
    def add_item(self, item):
        self.id[item] = item
        self.set_member[item] = set([item])

    # if a new item appears, add it automatically
    def union(self, i1, i2):
        f1 = self.find(i1)
        if f1 == None :
            self.add_item(i1)
            f1 = i1
        f2 = self.find(i2)
        if f2 == None :
            self.add_item(i2)
            f2 = i2
        
        if f1 == f2:
            return
        self.set_member[f1] = self.set_member[f2] | self.set_member[f1]
        del(self.set_member[f2])
        self.id[f2] = f1

    # if the item didn't save in list, return None
    def find(self, item):
        res = self.id.get(item, None)
        if res == None :
            return None
        if res != item:
            self.id[item] = self.find(res)
        return self.id[item]
    
    def ger_related(self, item):
        ret = self.find(item)
        if ret == None :
            return set([item])
        return self.set_member[ret]

import requests
no_network = False
def word_to_sound(word, language = "en"):
    # print("play :", word)
    if SETT.PLAY_SOUND != True :
        return
    class My_thread (threading.Thread):   #繼承父類threading.Thread
        def run(self): #把要執行的代碼寫到run函數里面 線程在創建後會直接運行run函數     
            global no_network
            url = f"http://translate.google.com/translate_tts?client=tw-ob&ie=UTF-8&tl={language}&q={word}"
            try :
                response = requests.get(url)
                play_byte_mp3(response.content)
                if no_network :
                    no_network = False
                    print("change back to have network")
            except requests.exceptions.ConnectionError :
                if not no_network :
                    no_network = True
                    print("change to no network")
    My_thread().start()

from pygame import mixer
from pygame import time as pygame_time
import time
from io import BytesIO
mixer.init()
def play_byte_mp3(byte_mp3):
    mp3_stream = BytesIO(byte_mp3)
    sound = mixer.Sound(mp3_stream)
    time.sleep(0.3)
    sound.play()
    pygame_time.wait(int(sound.get_length() * 1000))

if __name__ == "__main__" :
    word_to_sound("word ' ' word")
    # word_to_sound("word word")
    # word_to_sound("word ' ' ' ' word")