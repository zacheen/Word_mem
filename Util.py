import threading
import Settings as SETT

import requests
no_network = False
def word_to_sound(word, language = "en"):
    # print("play :", word)
    if SETT.PLAY_SOUND != True :
        return
    class My_thread (threading.Thread):   #繼承父類threading.Thread
        def run(self): #把要執行的代碼寫到run函數里面 線程在創建後會直接運行run函數     
            global no_network
            print("no_network in word_to_sound :",no_network)
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