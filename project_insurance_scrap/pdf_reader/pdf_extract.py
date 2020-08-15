import pdfplumber
import pandas as pd
import numpy as np

###########################################################
# extract char feature   
def pdf_extract_word(filename):
    result = pd.DataFrame()
    def extract_word_single(page):
        output = pd.DataFrame(page.chars)
        return output
    fun =np.vectorize(extract_word_single,otypes=[list])
    with pdfplumber.open(filename) as pdf:       
        result = pd.concat(fun(pdf.pages))
        result = result.reset_index()
        result = result.drop(columns = ['index']) 
        result = result.astype({'adv':'float','bottom':'float','doctop':'float','fontname':'str',
                                'height':'float','object_type':'str','page_number':'int','size':'float',
                                'text':'str','top':'float','upright':'int','width':'float',
                                'x0':'float','x1':'float','y0':'float','y1':'float',
                                    'text':'str'})
        result = result.rename(columns = {'bottom':'y_bottom','page_number':'page'})
        return result    

###########################################################
# extract table feature
def pdf_extract_cell(filename ,method = "line"):
    shan_settings_text={
    "vertical_strategy": "text", 
    "horizontal_strategy": "text",
    "keep_blank_chars": True,
    "text_x_tolerance": 8,
    "text_y_tolerance": 5,
    }
    shan_settings_custom={
    "vertical_strategy": "text", 
    "horizontal_strategy": "text",
    "keep_blank_chars": False,
    "snap_tolerance": 8 ,
    "text_x_tolerance": 3,
    "text_y_tolerance": 5,
    }
    shan_settings_line={
    "vertical_strategy": "lines", 
    "horizontal_strategy": "lines",
    "snap_tolerance": 6,
    "join_tolerance": 10,
    "edge_min_length": 5,
    }
    pdf = pdfplumber.open(filename)
    tall = np.cumsum([page.height for page in pdf.pages])
    tall = np.append(0,tall[0:len(tall)-1])
    tol_pages = len(pdf.pages)
    result = pd.DataFrame()
    for select_page in range(0,tol_pages):
        pages = pdf.pages[select_page]    
        output = pd.DataFrame()
        if method == "line":
            find_tables = pages.find_tables(table_settings = shan_settings_line)
        elif method =="text":
            find_tables = pages.find_tables(table_settings = shan_settings_text)
        elif method =="custom":
            find_tables = pages.find_tables(table_settings = shan_settings_custom)     
        else:
            return "no such method!"
        for select_table in range(0,len(find_tables)):
            dat = pd.DataFrame(find_tables[select_table].cells,columns=['left','top','right','bottom'])
            dat['table'] = select_table + 1
            dat['page'] = select_page + 1
            dat['cell'] = range(1,len(dat)+1)
            output = pd.concat([output,dat])
        result = pd.concat([result,output])
    result = result.astype({'left':'float', 'top':'float',
                            'right':'float', 'bottom':'float',
                            'cell':'int'})
    result = result.reset_index()
    result = result.drop(columns = ['index'])     
    return result
    
#############################
# extract raw lines
def pdf_extract_line(filename):     
    def extract_line_single(page):
        output = pd.DataFrame(page.edges)
        if( len(output)>0 ):
            output['doc_y'] = output.doctop+output.bottom-output.top    
            output = output[['x0','x1','y0','y1','orientation','doc_y','page_number','evenodd']]
            output = output.astype({'doc_y':'float', 'evenodd':'bool',
                                    'orientation':'str', 'page_number':'str' ,
                                    'x0':'float', 'x1':'float', 'y0':'float', 'y1':'float'})
        return output
    fun =np.vectorize(extract_line_single,otypes=[list])
    with pdfplumber.open(filename) as pdf:
        result = pd.concat(fun(pdf.pages))
        result.index =range(0,len(result))
        return result
           
