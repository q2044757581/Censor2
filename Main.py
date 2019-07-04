import time

from DFA import DFAFilter
from Fast_DFA import Fast_DFAFilter
from Pure_DFA import Pure_DFAFilter

gfw1 = Pure_DFAFilter()
gfw2 = Fast_DFAFilter()
gfw3 = DFAFilter()



if __name__ == "__main__":
    while(True):
        a = input("输入检测程度, 1~3:")
        text = input("输入检测文本: ")
        if a == "1":
            time1 = time.time()
            result = gfw1.DFA(text)
            time2 = time.time() - time1
            print(result, time2)
        elif a == "2":
            time1 = time.time()
            result = gfw2.DFA(text)
            time2 = time.time() - time1
            print(result, time2)
        else:
            time1 = time.time()
            result = gfw3.DFA(text)
            time2 = time.time() - time1
            print(result, time2)