# converts pdf, returns its text content as a string
# from https://www.binpress.com/tutorial/manipulating-pdfs-with-python/167
# pip install pdfminer.six
from io import StringIO
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
import pikepdf
import numpy

def shan_convert(pdf_path):    
    fp = open(pdf_path, 'rb')
    parser = PDFParser(fp)
    document = PDFDocument(parser)
    if not document.is_extractable:
        temp_file = pikepdf.open(pdf_path)
        temp_path = pdf_path[:-4] +"shan_temp" +".pdf"          
        temp_file.save(temp_path)
        fp = open(temp_path, 'rb')
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)   
    pagenos=set()  
    for page in PDFPage.get_pages(fp, pagenos):
        interpreter.process_page(page)
    text = retstr.getvalue()
    fp.close()
    device.close()
    retstr.close()
    return text

# converts all pdfs in directory pdfDir, saves all resulting txt files to txtdir
def shan_pdf_to_txt_single(pdf_file, txt_file):    
    try : 
        text = shan_convert(pdf_file)  # get string of text content of pdf
        f = open(txt_file,'w',encoding='utf-8')
        f.write(text)
        f.close()
        return("success")
    except: 
        return(pdf_file)
        
        
shan_pdf_to_txt = numpy.vectorize(shan_pdf_to_txt_single,otypes=[str])












