import pandas as pd
import re
import sys
class Clean:
    FILE:str
    DF:pd.DataFrame
    def __init__(self,FILE:str):
        self.FILE=FILE
        self.__createDF()

    def __createDF(self):
        try:
            self.DF=pd.read_excel("output/Windows/extracted/"+self.FILE+"_extracted"+".xlsx")
        except:
            print("El error abriendo el archivo fue: "+str(sys.exc_info()[0]))
            exit(1)

    def __cleanColumns(self):
        PATTERN_REMEDIATION= re.compile(r'(.*?)(\nNote|$)', re.DOTALL)
        PATTERN_STATE=re.compile(r'(\nThe recommended .*?|$)(Note|Important|$)', re.DOTALL)
        PATTERN_DESCRIPTION=re.compile(r'(.*?)(\nThe recommended|Note|$)', re.DOTALL)

        self.DF['Title']=self.DF['Title'].str.replace('(Automated)','')
        self.DF['Title']=self.DF['Title'].str.strip()
        PATTERN_EXTRACT_ADD=re.compile(r'\((MS only|DC only)\)',re.DOTALL)
        self.DF['MS/DC']=self.DF['Title'].apply(
            lambda x:
                PATTERN_EXTRACT_ADD.findall(x)[0] if len(PATTERN_EXTRACT_ADD.findall(x))>0 
                else 'None')
        self.DF['Title']=self.DF['Title'].str.replace('(MS only)','')
        self.DF['Title']=self.DF['Title'].str.replace('(DC only)','')
        self.DF['Audit']=self.DF['Audit'].apply(lambda x: re.compile(r'Page \d+', re.DOTALL).sub('',x))
        self.DF['Audit']=self.DF['Audit'].str.strip()
        self.DF['Remediation']=self.DF['Remediation'].apply(lambda x: PATTERN_REMEDIATION.findall(x)[0][0])
        self.DF['Remediation']=self.DF['Remediation'].apply(lambda x: re.compile(r'Page \d+', re.DOTALL).sub('',x))
        self.DF['Remediation']=self.DF['Remediation'].str.strip()
        self.DF['State']=self.DF['Description'].apply(lambda x: PATTERN_STATE.search(x).group(1))
        self.DF['State']=self.DF['State'].apply(lambda x: re.compile(r'Page \d+', re.DOTALL).sub('',x))
        self.DF['State']=self.DF['State'].str.strip()
        self.DF['Description']=self.DF['Description'].apply(lambda x: re.compile(r'Page \d+', re.DOTALL).sub('',x))
        self.DF['Description']=self.DF['Description'].apply(lambda x: PATTERN_DESCRIPTION.search(x).group(1))
        self.DF['Description']=self.DF['Description'].str.strip()
        
    def __createDFFinal(self):
        DF_final=pd.DataFrame(columns=["IDCIS", "Parametro", "MS/DS", "Descripción", "Procedimiento de implementación", "Procedimiento de verificación", "Config implementación", "Config verificación"])
        DF_final['IDCIS']=self.DF['IDCIS']
        DF_final['Parametro']=self.DF['Title']
        DF_final['MS/DS']=self.DF['MS/DC']
        DF_final['Descripción']=self.DF['Description']

        PATTERN_DIV_REMEDIATION=re.compile(r'(: \n)', re.DOTALL)
        DF_final['Procedimiento de implementación']=self.DF['Remediation'].apply(lambda x: "".join(PATTERN_DIV_REMEDIATION.split(x)[:-1]))
        DF_final['Config implementación']=self.DF['Remediation'].apply(lambda x: PATTERN_DIV_REMEDIATION.split(x)[-1])

        PATTERN_DIV_AUDIT=re.compile(r'(: \n)', re.DOTALL)
        DF_final['Procedimiento de verificación']=self.DF['Audit'].apply(lambda x: "".join(PATTERN_DIV_AUDIT.split(x)[:-1]))
        DF_final['Procedimiento de verificación']=self.DF['Audit'].apply(
            lambda x:
            "".join(PATTERN_DIV_AUDIT.split(x)[:-1]) if len(PATTERN_DIV_AUDIT.split(x))>1 
            else x)
        DF_final['Config verificación']=self.DF['Audit'].apply(
            lambda x:
            PATTERN_DIV_AUDIT.split(x)[-1] if len(PATTERN_DIV_AUDIT.split(x))>1
            else "")

        DF_final['Procedimiento de implementación']=self.DF['State']+" "+DF_final['Procedimiento de implementación']
        DF_final.replace('\n','', regex=True, inplace=True)

        return DF_final

    def __toExcel(self,df:pd.DataFrame):
        try:
            df.to_excel("output/Windows/clean/"+self.FILE+"_clean"+".xlsx", index=False)
        except:
            print("El error creando el archivo clean fue: "+str(sys.exc_info()[0]))
            exit(1)

    def limpiar(self):
        self.__cleanColumns()
        DF_final=self.__createDFFinal()
        self.__toExcel(DF_final)