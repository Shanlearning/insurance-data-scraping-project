import numpy
import re


def str_detect_single(pattern,dat):
    return(re.findall(pattern,dat) != [])

str_detect_vectorized = numpy.vectorize(str_detect_single,otypes=[bool],doc='dectect if pattern is in dat' )

