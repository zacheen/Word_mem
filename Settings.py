TEST_FAIL = True
TEST_FAIL = False
class Json_file:
    def __init__(self, word_file_path, NEAR_FIRST, weight = 1):
        self.word_file_path = word_file_path
        self.NEAR_FIRST = NEAR_FIRST
        self.weight = weight

DAYS = [0,1,1,1,2,3,5,7,15,23,31,31,45,90,180] # 365 感覺沒有必要了
long_term_mem_threshold = DAYS.index(7)
print("long_term indx :", long_term_mem_threshold)
DATE_FORMAT = r"%Y/%m/%d"
PLAY_SOUND = True
# PLAY_SOUND = False
WRONG_WORD_PATH = r"G:\我的雲端硬碟\__wrong_word.txt"
AGAIN_WORD_PATH = r"G:\我的雲端硬碟\__again_word.txt"
WRONG_WORD_PASS = 6

if TEST_FAIL :
    all_json_files = [
        Json_file(WRONG_WORD_PATH, 200, 1),
        ]
else :
    all_json_files = [
        Json_file(r"D:\dont_move\word\toeic.json", 150, 2),
        Json_file(r"D:\dont_move\word\toelf.json", 150, 2),
        Json_file(r"D:\dont_move\word\gre.json", 150, 2),
        Json_file(r"D:\dont_move\word\gre_new.json", 150, 0),
        ]