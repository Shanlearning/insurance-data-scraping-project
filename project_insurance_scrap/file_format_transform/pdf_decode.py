import pikepdf
import numpy
import os

def pdf_decode_single(old_path,new_path):
    try:
        pdf = pikepdf.open(old_path)     
        pdf.save(new_path)
        pdf.close       
        return "success! " + new_path
    except:        
        return "fail " + old_path
    
def pdf_folder_decode(pdf_folder):
    pdf_folder = os.path.abspath(pdf_folder)
    pdf_decode_vectorized = numpy.vectorize(pdf_decode_single,otypes=[str])   
    os_path_join = numpy.vectorize(os.path.join,otypes=[str])
    if not os.path.exists(pdf_folder+"_decode"):
        os.makedirs(pdf_folder+"_decode")
    else:
        return (pdf_folder+"_decode already exists!")
    old_path = os_path_join(pdf_folder,os.listdir(pdf_folder))
    new_path = os_path_join(pdf_folder+"_decode",os.listdir(pdf_folder))
    return pdf_decode_vectorized(old_path,new_path)
     