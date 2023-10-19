word_file_path = r"D:\dont_move\word\toeic.json"
NEAR_FIRST = 150
# word_file_path = r"D:\dont_move\word\gre.json"
# NEAR_FIRST = 50
DAYS = [0,1,1,1,3,5,7,14,21,31,31,45,90,180] # 365 感覺沒有必要了
long_term_mem_threshold = DAYS.index(7)
print("long_term indx :", long_term_mem_threshold)
DATE_FORMAT = r"%Y/%m/%d"
PLAY_SOUND = True
# PLAY_SOUND = False
