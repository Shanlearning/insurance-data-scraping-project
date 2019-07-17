import numpy
import re
# import project_insurance_scrap.scrap_functions as shan
import project_insurance_scrap.scrap_basic_functions as shanbasic

def str_detect(pattern,dat):
    return shanbasic.str_detect_vectorized(pattern,dat).tolist()
# keep word that has select attr

def str_keep(pattern, dat):
    output = shanbasic.str_keep_vectorized(pattern,dat).tolist()
    if type(output) == list:
        output = list(filter(lambda a: a != "", output))
        if len(output) == 1:
            output = output[0]
    return output

def str_drop(pattern, dat):
    output = shanbasic.str_drop_vectorized(pattern,dat).tolist()
    if type(output) == list:
        output = list(filter(lambda a: a != "", output))
        if len(output) == 1:
            output = output[0]
    return output

def str_extract(pattern, dat):
    return shanbasic.str_extract_vectorized(pattern,dat).tolist()

def which(dat):
    if type(dat) == bool:
        if dat == True:
            return [0]
        else:
            return []
    elif type(dat) == list:
        output = []
        for i in range(0, len(dat) ):
            if dat[i] == True:
                output.append(i)
        return output

def keep(TorF, dat):
    output = shanbasic.keep_vectorized(TorF,dat).tolist()
    if type(output) == list:
        output = list(filter(lambda a: a != None, output))
        if len(output) == 1:
            output = output[0]
    return output



#def str_replace

#def str_replace_all

#def str_extract_all

#def str_split


