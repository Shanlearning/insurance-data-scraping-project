import numpy
import re


def str_detect_single(pattern,dat):
    return(re.findall(pattern,dat) != [])

str_detect_vectorized = numpy.vectorize(str_detect_single,otypes=[bool])

def str_keep_single(pattern, dat):
    dat = str(dat)
    if re.findall(pattern,dat) != []:
        return dat
    else:
        return ""

str_keep_vectorized = numpy.vectorize(str_keep_single,otypes=[str], excluded=['dat'])

def str_drop_single(pattern, dat):
    dat = str(dat)
    if re.findall(pattern,dat) == []:
        return dat
    else:
        return ""

str_drop_vectorized = numpy.vectorize(str_drop_single,otypes=[str], excluded=['dat'])

def keep_TF_single(TorF, dat):
    if TorF == True:
        return dat

keep_vectorized = numpy.vectorize(keep_TF_single)


def str_extract_single(pattern, dat):
    output = re.findall(pattern, dat)
    if output != []:
        output = output[0]
    else:
        output = ""
    return output

str_extract_vectorized = numpy.vectorize(str_extract_single,otypes=[str], excluded=['dat'])
