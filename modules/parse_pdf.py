import tabula
import numpy as np
from dotenv import dotenv_values

from tabula.io import read_pdf
config = dotenv_values(".env")

def parse_pdf():
    aulas = {}
    df = None
    dataframes = read_pdf("./assets/horario.pdf", pages=1)

    # read_pdf returns multiple dataframes, we should only use the one with proper rows and columns
    for d in dataframes:
        if(d.empty is not True and 'DIA' in d.columns):
            df = d
    
  
    # Clean the freaking PDF
    df.replace(None,False, regex="M.+", inplace=True)
    df.replace(np.nan,False, inplace=True)
    df.replace(None,"", regex="\D+", inplace=True)
    df.replace('0',False, inplace=True)

   
    # Extract only the classes from 19H    
    data = df.query("DIA == '19'")

    # Iterate through the columns, and create a dict with the days & classes
    colunas = data.columns
    for c in colunas[1::]:
        aula = data[c].iloc[0]
        if(aula):
            aulas[int(aula)] = int(c)

    # Export to excel, to validate manually
    data.to_excel('./assets/horario.xlsx')

    return aulas

   

if __name__ == "__main__":
    parse_pdf()