import  os
from win32com import client

def doc2pdf_single(doc_name, pdf_name):
    try:
        word = client.DispatchEx("Word.Application")
        if os.path.exists(pdf_name):
            os.remove(pdf_name)
        worddoc = word.Documents.Open(doc_name,ReadOnly = 1)
        worddoc.SaveAs(pdf_name, FileFormat = 17)
        worddoc.Close()
        os.remove(doc_name)
        return pdf_name
    except:
        return "failed"