import re

def shan_keep(filter,dat):
    keep = []
    for part in dat:
        if str(filter) in part:
            keep.append(part)
    return keep