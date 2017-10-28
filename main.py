#!usr/bin/python
# -*- coding=utf-8 -*-
import sys
try:
    from ssrParse2 import ssrParse
except:
    from ssrParse3 import ssrParse

def test():
    pythonVersion = int(sys.version_info.major)
    ssrList = ssrParse.parseSubscribe(sys.argv[1])
    info = ssrParse()
    for item in ssrList:
        if len(item) > 0:
            info.decode(item)
            dict = info.format()
            for key in dict.keys():
                if pythonVersion == 2:
                    print(":".join([key, str(dict[key]).decode("utf-8")]))
                elif pythonVersion == 3:
                    print(":".join([key, str(dict[key])]))
            print ("\n")

if __name__ == '__main__':
    test()