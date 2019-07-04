from src.soundshapecode import ssc
from src.soundshapecode.ssc import getHanziStrokesDict, getHanziStructureDict, getHanziSSCDict
from src.soundshapecode.variant_kmp import VatiantKMP
from src.soundshapecode.ssc_similarity.compute_ssc_similarity import computeSSCSimilaruty
import jieba.analyse
SIMILARITY_THRESHOLD = 0.8
topK = 10
SSC_ENCODE_WAY = 'ALL'  # 'ALL','SOUND','SHAPE'
# SSC_ENCODE_WAY = 'SOUND'  # 'ALL','SOUND','SHAPE'

class Similarity:
    def __init__(self):
        getHanziStrokesDict()
        getHanziStructureDict()
        # generateHanziSSCFile()#生成汉子-ssc映射文件
        getHanziSSCDict()
    # 计算单字相似度
    def Similarity_between_word(self, str1, str2):
        chi_word1_ssc = ssc.getSSC(str1, SSC_ENCODE_WAY)
        chi_word2_ssc = ssc.getSSC(str2, SSC_ENCODE_WAY)
        return computeSSCSimilaruty(chi_word1_ssc[0],chi_word2_ssc[0],SSC_ENCODE_WAY)

if __name__ == "__main__":
    s1 = "产"
    s2 = "産"
    s = Similarity()
    print(s.Similarity_between_word(s1, s2))
