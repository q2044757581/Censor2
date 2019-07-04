# -*- coding:utf-8 -*-
# DFA算法
import re
import time
from copy import deepcopy

from src.Similarity.run import Similarity

class Fast_DFAFilter(object):
    def __init__(self):
        self.keyword_chains = {}  # 关键词链表
        self.delimit = '\x00'  # 限定
        self.similarity = Similarity()
        path = "CensorWords.txt"
        self.parse(path)

    def add(self, keyword):
        keyword = keyword.lower()  # 关键词英文变为小写
        chars = keyword.strip()  # 关键字去除首尾空格和换行
        if not chars:  # 如果关键词为空直接返回
            return
        level = self.keyword_chains
        # 遍历关键字的每个字
        for i in range(len(chars)):
            # 如果这个字已经存在字符链的key中就进入其子字典
            if chars[i] in level:
                level = level[chars[i]]
            else:
                if not isinstance(level, dict):
                    break
                for j in range(i, len(chars)):
                    level[chars[j]] = {}
                    last_level, last_char = level, chars[j]
                    level = level[chars[j]]
                last_level[last_char] = {self.delimit: 0}
                break
        if i == len(chars) - 1:
            level[self.delimit] = 0

    def parse(self, path):
        with open(path, encoding='utf-8') as f:
            for keyword in f:
                self.add(str(keyword).strip())
        # print(self.keyword_chains)
    def if_in_Dict(self, char, level):
        max_sim = -1
        max_char = ""
        for key in level.keys():
            temp = self.similarity.Similarity_between_word(char, key)
            if temp > max_sim:
                max_sim = temp
                max_char = key
        return max_char, max_sim

    def is_Chinese(self, word):
        for ch in word:
            if '\u4e00' <= ch <= '\u9fff':
                return True
        return False

    def filter(self, message, repl="*"):
        has_problem = 0
        original_message = deepcopy(message)
        message = message.lower()
        ret = []
        start = 0
        while start < len(message):
            level = self.keyword_chains
            step_ins = 0
            for char in message[start:]:
                if self.is_Chinese(char):  # 中文
                    max_char, max_sim = self.if_in_Dict(char, level)
                    if max_sim >= 0.9:
                        step_ins += 1
                        if self.delimit not in level[max_char]:
                            level = level[max_char]
                        else:
                            has_problem += 1
                            ret.append(repl * step_ins)
                            start += step_ins - 1
                            break
                    else:
                        ret.append(original_message[start])
                        break
                else:
                    if char in level:  # 字母、数字或符号
                        step_ins += 1
                        if self.delimit not in level[char]:
                            level = level[char]
                        else:
                            has_problem += 1
                            ret.append(repl * step_ins)
                            start += step_ins - 1
                            break
                    else:
                        ret.append(original_message[start])
                        break
            else:
                ret.append(original_message[start])
            start += 1

        return ''.join(ret), has_problem
    def DFA(self, text):
        # 如果再全保留情况下只有2个以下敏感词的话，可以允许发送打码后的评论， 如果其他情况下有敏感词，说明是蓄意的，不允许发送
        encode_way = "ALL"
        max_score = 0
        tmp_text = deepcopy(text)
        time3 = time.time()
        result1, define1 = self.filter(tmp_text)  # 全保留
        # print(result1, define1)
        _tmp_text = "".join(re.findall(r'[\u4e00-\u9fa5a-zA-Z0-9]', tmp_text))  # 去符号
        if len(_tmp_text) == len(text):
            _tmp_text = ""
        result2, define2 = self.filter(_tmp_text)
        # print(result2, define2)
        tmp_text1 = re.sub(r'[a-zA-Z0-9]', "", tmp_text)  # 纯中文
        if len(tmp_text1) == len(text):
            tmp_text1 = ""
        result3, define3 = self.filter(tmp_text1)

        Dict = {}
        if define1 == 0:
            if max(define2, define3) > 0:
                Dict["sentence"] = ""
                Dict["WordsNum"] = max(define2, define3)
            else:
                Dict["sentence"] = text
                Dict["WordsNum"] = 0
        elif define1 <= 2:
            if max(define2, define3) > define1:
                Dict["sentence"] = ""
                Dict["WordsNum"] = max(define2, define3)
            else:
                Dict["sentence"] = result1
                Dict["WordsNum"] = define1
        else:
            Dict["sentence"] = ""
            Dict["WordsNum"] = max(define1, define2, define3)
        return Dict

if __name__ == "__main__":
    text = "我去到阴道里面,卧槽, 贼爽666"
    gfw = Fast_DFAFilter()
    time1 = time.time()
    result = gfw.DFA(text)
    time2 = time.time() - time1
    print(result, time2)