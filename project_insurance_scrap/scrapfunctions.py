import re
import scrapy
# keep word that has select attr

#判断变量类型的函数
def getType(variate):
    type=None
    if isinstance(variate,int):
        type = "integer"
    elif isinstance(variate,str):
        type = "string"
    elif isinstance(variate,float):
        type = "float"
    elif isinstance(variate,list):
        type = "list"
    elif isinstance(variate,tuple):
        type = "tuple"
    elif isinstance(variate,dict):
        type = "dict"
    elif isinstance(variate,set):
        type = "set"
    return type

def str_detect_single(pattern,dat):
    return(re.findall(pattern,dat) == [])


def str_keep(pattern, dat):
    if getType(dat) == "string":
        if pattern in dat:
            return dat
        else:
            return ""
    elif getType(dat) == "list":
        keep = []
        for part in dat:
            if pattern in part:
                keep.append(part)
        return keep

def str_extract(pattern, dat):
    output =[]
    if getType(dat) == "string":
        output = re.findall(pattern, dat)
        if output != []:
            output = output[0]
        else:
            output = ""
    else:
        for part in dat:
            keep = re.findall(pattern,part)
            if keep != []:
                keep = keep[0]
            else:
                keep = ""
            output.append(keep)
    return output


#def str_replace

#def str_replace_all

#def str_extract_all

#def str_split


