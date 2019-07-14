import re

# keep word that has select attr
def str_keep(word_to_keep,dat):
    keep = []
    for part in dat:
        if word_to_keep in part:
            keep.append(part)
    return keep


def str_extract(extract,dat):
    keep = []
    for part in dat:
        if str(filter) in part:
            keep.append(part)
    return keep


