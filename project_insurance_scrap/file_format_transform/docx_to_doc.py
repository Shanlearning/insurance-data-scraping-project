import sys
import pickle
import re
import codecs
import string
import shutil
from win32com import client as wc
import docx

def docx2doc_single(docx_name,doc_name):   
    word = wc.Dispatch('Word.Application')
    doc = word.Documents.Open(docx_name)        # 目标路径下的文件
    doc.SaveAs(doc_name, 12, False, "", True, "", False, False, False, False)  # 转化后路径下的文件    
    doc.Close()
    word.Quit()
    


