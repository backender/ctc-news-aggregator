import re
def removeNonAscii(s):
    text="".join(i for i in s if ord(i)<128)
    return text.decode('utf-8','ignore').encode("utf-8")
def aboutBitcoin(text):
    text=text.lower()
    filter='bitcoin'
    if filter in text:
        return True
    else: return False
def aboutEthereum(text):
    text=text.lower()
    filter='ethereum'
    if filter in text:
        return True
    else: return False# -*- coding: utf-8 -*-
def textPreprocessing(text):
    text=removeNonAscii(re.sub('\<(.*?)\>',' ',text))
    text=text.replace('\n', ' ')
    text=text.replace('\r',' ')
    text=re.sub(r'\W+', ' ', text)
    return text