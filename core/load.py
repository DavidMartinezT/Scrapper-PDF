import pandas as pd
import re
import sys
import numpy as np
from deep_translator import GoogleTranslator
import time
pd.options.mode.chained_assignment = None 
class Load:
    FILE:str
    DF:pd.DataFrame
    LANGUAGE:str
    def __init__(self, FILE:str, LANGUAGE:str):
        self.FILE=FILE
        self.LANGUAGE=LANGUAGE
        self.__createDF()

    def __createDF(self):
        try:
            self.DF=pd.read_excel("output/Windows/clean/"+self.FILE+"_clean"+".xlsx")
            self.DF.fillna('',inplace=True)
        except:
            print("El error abriendo el archivo fue: "+str(sys.exc_info()[0]))
            exit(1)

    def __toSpanish(self):
        print("Traduciendo... esto puede tardar unos minutos")
        self.DF['Parametro']=self.DF['Parametro'].apply(lambda x: GoogleTranslator(source='auto', target='es').translate(x))
        self.DF['Descripción']=self.DF['Descripción'].apply(lambda x: GoogleTranslator(source='auto', target='es').translate(x))
        self.DF['Procedimiento de implementación']=self.DF['Procedimiento de implementación'].apply(lambda x: GoogleTranslator(source='auto', target='es').translate(x))
        self.DF['Procedimiento de verificación']=self.DF['Procedimiento de verificación'].apply(lambda x: GoogleTranslator(source='auto', target='es').translate(x))
        
    def __joinConfigs(self):
        self.DF['Procedimiento de implementación']=self.DF['Procedimiento de implementación'] + '\n' + self.DF['Config implementación']
        self.DF['Procedimiento de verificación']=self.DF[['Procedimiento de verificación', 'Config verificación', 'Config implementación']].apply(
            lambda x:
                x['Procedimiento de verificación'] + '\n' + x['Config implementación'] if x['Config verificación'] == ''
                else
                x['Procedimiento de verificación'] + '\n' + x['Config verificación']
            , axis=1)
        self.DF.drop(columns=['Config implementación', 'Config verificación'], inplace=True)
    
    def __toExcel(self):
       #Extraer secciones finales
        self.DF['Sección']=self.DF['IDCIS'].apply(lambda x: re.findall(r'(\d{1,2}\.\d{1,2})', x)[0])
        column_width = 50
        try:
            with pd.ExcelWriter('output/Windows/'+self.FILE+'_'+self.LANGUAGE+'.xlsx', engine='openpyxl') as writer:
                for i in self.DF['Sección'].unique():
                    df_seccion=self.DF[self.DF['Sección']==i]
                    df_seccion.drop(columns=['Sección'], inplace=True)
                    df_seccion.to_excel(writer, index=False, sheet_name= 'Sección '+i)

                    # Access the XlsxWriter workbook and worksheet objects
                    workbook  = writer.book
                    worksheet = writer.sheets['Sección '+i]

                    # Set the column width for each column
                    for i, column in enumerate(df_seccion.columns):
                        column_letter = chr(ord('A') + i)
                        worksheet.column_dimensions[column_letter].width = column_width
        except:
            print("El error fue: "+str(sys.exc_info()[0]))
            exit(1)
        
    def cargar(self):
        if(self.LANGUAGE=="es"):
            self.__toSpanish()
        self.__joinConfigs()
        self.__toExcel()
        print("Archivo cargado exitosamente en:"+"output/Windows/"+self.FILE+"_es"+".xlsx")