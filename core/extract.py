import pandas as pd
import fitz
import re
import sys
import logging
class Extract:

    FILE:str
    BEGIN_PAGE:int
    END_PAGE:int
    allText:str
    doc:fitz.Document

    def __init__(self,FILE:str):
        self.FILE=FILE
        self.__openFile()
        self.BEGIN_PAGE=0
        self.END_PAGE=self.doc.page_count
        self.allText=""

    def __openFile(self):
        try:
            self.doc=fitz.open("./source/Windows/"+self.FILE+".pdf")
        except:
            print("El error fue: "+str(sys.exc_info()[0]))
            exit(1)


    def __getSections(self):
        for i in range(self.BEGIN_PAGE,self.END_PAGE):
            page=self.doc.load_page(i)
            self.allText+=page.get_text("")
        PATTERN_SUBSTRACT_INDEX=re.compile(r"\nOverview \n(.*)\nAppendix: Summary Table", re.DOTALL)
        self.allText=PATTERN_SUBSTRACT_INDEX.findall(self.allText)[0]
        PATTERN_SECTIONS = re.compile(r'(\n\d+\.[\.\d]+ \(\w{2}\).*?)(?=\n\d+\.[\.\d]+ \(\w{2}\)|$)', re.DOTALL)
        return PATTERN_SECTIONS.findall(self.allText)
    
    def __extractRow(self, text:str):
        patternTitle = re.compile(r'[\.\d]+ \(\w{2}\)(.*?)Profile Applicability:', re.DOTALL)
        patternDescription = re.compile(r'Description: \n(.*?)\nRationale:', re.DOTALL)
        patternAudit = re.compile(r'\nAudit: \n(.*?)\nRemediation:', re.DOTALL)
        patternRemediation = re.compile(r'Remediation: \n(.*?)\n(Default Value|CIS Controls)', re.DOTALL)

        IDCS=re.search(r"[\.\d]+", text).group(0)+""
        Level=re.search(r"[\.\d]+ (\(\w{2}\))", text).group(1)+""
        Title=patternTitle.search(text).group(1)
        Description=patternDescription.search(text).group(1)
        Audit=patternAudit.search(text).group(1)
        Remediation=patternRemediation.search(text).group(1)

        return IDCS, Level, Title, Description, Audit, Remediation
    
    def __createDF(self, sections:list):
        df=pd.DataFrame(columns=["IDCIS", "Level", "Title", "Description", "Audit", "Remediation"])
        i=0
        for section in sections:
            row=Row(*self.__extractRow(section))
            df.loc[i]=row.to_dict()
            i+=1
        return df

    def __toExcel(self, df:pd.DataFrame):
        try:
            df.to_excel("output/Windows/extracted/"+self.FILE+"_extracted"+".xlsx", index=False)
        except:
            print("El error fue: "+str(sys.exc_info()[0]))
            exit(1)

    def extraer(self):
        sections=self.__getSections()
        df=self.__createDF(sections)
        self.__toExcel(df)

class Row:
    """
    Esta clase representa una fila o control con la información de un control
    """
    def __init__(self, IDCIS, Level, Title, Description, Audit, Remediation):
        self.IDCIS:str = IDCIS
        self.Level:str = Level
        self.Title:str = Title
        self.Description:str = Description
        self.Audit:str = Audit
        self.Remediation:str= Remediation
    
    def to_dict(self):
        return {"IDCIS":self.IDCIS, "Level":self.Level, "Title":self.Title, "Description":self.Description, "Audit":self.Audit, "Remediation":self.Remediation}
