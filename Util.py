import threading

import requests
def word_to_sound(word, language = "en"):
    class My_thread (threading.Thread):   #繼承父類threading.Thread
        def run(self): #把要執行的代碼寫到run函數里面 線程在創建後會直接運行run函數     
            url = f"http://translate.google.com/translate_tts?client=tw-ob&ie=UTF-8&tl={language}&q={word}"
            response = requests.get(url)
            play_byte_mp3(response.content)
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