# True False
TEST_FAIL = True
TEST_FAIL = False
CLEAR_PASS = False
DEL_DUPLICATE = False
class Json_file:
    def __init__(self, word_file_path, NEAR_FIRST, weight = 1):
        self.word_file_path = word_file_path
        self.NEAR_FIRST = NEAR_FIRST
        self.weight = weight

class Related_file:
    def __init__(self, related_file_path):
        self.related_file_path = related_file_path

DAYS = [0,1,1,2,3,4,5,7,10,15,22,33,49,75,120] # 180 天感覺有時候都忘了
long_term_mem_threshold = DAYS.index(7)
D49_indx = DAYS.index(49)
FULL_LEVEL = len(DAYS) - 1
print("long_term indx :", long_term_mem_threshold)
DATE_FORMAT = r"%Y/%m/%d"
PLAY_SOUND = True
WRONG_WORD_PATH = r"G:\我的雲端硬碟\__wrong_word.txt"
AGAIN_WORD_PATH = r"G:\我的雲端硬碟\__again_word.txt"
WRONG_WORD_PASS = 6
WRONG_STATUS = 5

if TEST_FAIL :
    all_json_files = [
        Json_file(WRONG_WORD_PATH, 200, 1),
        Json_file(AGAIN_WORD_PATH, 200, 1),
        ]
else :
    all_json_files = [
        Json_file(r"D:\dont_move\word\toeic.json", 150, 2),
        Json_file(r"D:\dont_move\word\toelf.json", 150, 2),
        Json_file(r"D:\dont_move\word\gre.json", 150, 2),
        Json_file(r"D:\dont_move\word\math.json", 150, 2),
        # Json_file(r"D:\dont_move\word\Sound.json", 150, 1),
        Json_file(r"D:\dont_move\word\Chi_To_Eng.json", 150, 1),
        # Json_file(r"D:\dont_move\word\gre_new.json", 150, 0),
        ]
STRICT_WEI = False

type_files = [
    Json_file(r"D:\dont_move\word\typo.json", 150, 1),
]

all_related_files = [
   r"D:\dont_move\word\word_similar.txt",
]