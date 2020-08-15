import os
import shutil
import numpy as np
from win32com import client
import pikepdf
import re
from collections import Counter 
from itertools import tee, count

def os_walk_path(path,limit="all"):
    if not os.path.exists(path):
       return "path do not exist"
    output = []
    if limit =="all":
        for root,dirs,names in os.walk(path):
            for filename in names:
                output.append(str(os.path.join(root,filename)))
        return output
    else:
        for root,dirs,names in os.walk(path):
            for filename in names:   
                if len(re.findall(os.path.splitext(filename)[1].lower(),limit.lower()))>0: 
                    output.append(str(os.path.join(root,filename)))
        return output
    
# os gather will decode pdf, transfer docx and doc file into pdf file
def os_gather_files(from_files:str,to_path:str):
    def doc2pdf_single(doc_name, pdf_name):
        if len(re.findall(os.path.splitext(pdf_name)[1].lower(),".doc^x|docx")) > 0 :
            pdf_name = os.path.splitext(pdf_name)[0] +".pdf"
        word = client.DispatchEx("Word.Application")
        if os.path.exists(pdf_name):
            os.remove(pdf_name)
        worddoc = word.Documents.Open(doc_name,ReadOnly = 1)
        worddoc.SaveAs(pdf_name, FileFormat = 17)
        worddoc.Close()
    
    os_path_join = np.vectorize(os.path.join,otypes=[str])    
    
    def os_copy_file_single(from_file:str,to_file:str):
        try: 
            if len(re.findall(os.path.splitext(from_file)[1].lower(),".pdf")) > 0 :    
                pdf = pikepdf.open(from_file)     
                pdf.save(to_file)
                pdf.close  
            elif len(re.findall(os.path.splitext(from_file)[1].lower(),".doc|.docx")) > 0 : 
                doc2pdf_single(from_file, to_file)
            else:
                shutil.copy(from_file, to_file)
            return "success! " + to_file
        except:
            return "fail! " + from_file
        
    def uniquify(seq, suffs = count(1)):
        """Make all the items unique by adding a suffix (1, 2, etc).
        
        `seq` is mutable sequence of strings.
        `suffs` is an optional alternative suffix iterable.
        """
        not_unique = [k for k,v in Counter(seq).items() if v>1] # so we have: ['name', 'zip']
        # suffix generator dict - e.g., {'name': <my_gen>, 'zip': <my_gen>}
        suff_gens = dict(zip(not_unique, tee(suffs, len(not_unique))))  
        for idx,s in enumerate(seq):
            try:
                suffix = str(next(suff_gens[s]))
            except KeyError:
                # s was unique
                continue
            else:
                seq[idx] += suffix
    
    def str_c(*pattern,sep=""):
        def str_c_single(*pattern,sep=""):
            output = pattern[0]
            for i in range(1,len(pattern)):
                output = output+sep+pattern[i]
            return output
        fun =  np.vectorize(str_c_single,excluded=['pattern'],otypes=[str])
        return fun(*pattern).tolist()
    
    os_path_copy = np.vectorize(os_copy_file_single,otypes=[str])
    
    to_path = os.path.abspath(to_path)
    if not os.path.exists(to_path):
        os.makedirs(to_path)
    to_file_name = os_get_file_name(os_remove_suffix_name(from_files))
    uniquify(to_file_name, (f'_{x!s}' for x in range(1, 100)))
    to_file_suffix = os_get_suffix_name(from_files)
    to_file_name = str_c(to_file_name,to_file_suffix)
    to_files = os_path_join(to_path,to_file_name)
    return os_path_copy(from_files,to_files)

def os_make_dir(pathlist):
    for path in pathlist:
        isExists=os.path.exists(path)
        if not isExists:
            os.makedirs(path)

def os_get_suffix_name(file_path:str):  
    def os_get_suffix_name_single(file_path:str):
        return os.path.splitext(file_path)[1]
    fun = np.vectorize(os_get_suffix_name_single,otypes=[str])
    return fun(file_path).tolist()

def os_remove_suffix_name(file_path:str):
    def os_remove_suffix_name_single(file_path:str):
        return os.path.splitext(file_path)[0]
    fun = np.vectorize(os_remove_suffix_name_single,otypes=[str])
    return fun(file_path).tolist()

def os_get_file_name(file_path:str):
    def os_get_file_name_single(file_path:str):
        return os.path.split(file_path)[1]
    fun = np.vectorize(os_get_file_name_single,otypes=[str])
    return fun(file_path).tolist()

def os_remove_file_name(file_path:str):
    def os_remove_file_name_single(file_path:str):
        return os.path.split(file_path)[0]
    fun = np.vectorize(os_remove_file_name_single,otypes=[str])
    return fun(file_path).tolist()





