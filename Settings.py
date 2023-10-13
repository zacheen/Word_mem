word_file_path = r"D:\dont_move\word\gre.json"
DAYS = [0,1,1,1,3,5,7,14,21,31,31,45,90,180] # 365 感覺沒有必要了
long_term_mem_threshold = DAYS.index(7)
print("long_term indx :", long_term_mem_threshold)
DATE_FORMAT = r"%Y/%m/%d"