import re
# keep word that has select attr

def str_detect_single(pattern,dat):
    return(re.findall(pattern,dat) != [])

def which(dat):
    if type(dat) == bool:
        return 0
    elif type(dat) == list:
        output = []
        for i in range(0, len(dat) ):
            if dat[i] == True:
                output.append(i)
        return output

def str_detect(pattern,dat):
    if type(dat) == str:
        return str_detect_single(pattern,dat)
    elif type(dat) == list:
        output = []
        for part in dat:
            output.extend([str_detect_single(pattern,part)])
        return output

def str_keep(pattern, dat):
    if type(dat) == str:
        if str_detect(pattern,dat) == True:
            return dat
        else:
            return ""
    elif type(dat) == list:
        keep = []
        det = str_detect(pattern ,dat )
        for i in range(0,len(det)):
            if det[i] == True:
                keep.append(dat[i])
        return keep

def str_extract(pattern, dat):
    output =[]
    if type(dat) == str:
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


