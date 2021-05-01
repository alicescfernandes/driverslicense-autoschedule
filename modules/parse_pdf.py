import tabula
import numpy as np
from dotenv import dotenv_values

from tabula.io import read_pdf
config = dotenv_values(".env")

def parse_pdf():
    aulas = {}
    df = read_pdf("./assets/horario.pdf", pages=1)[0]

    # Clean the freaking PDF
    df.replace(None,False, regex="M.+", inplace=True)
    df.replace(np.nan,False, inplace=True)
    df.replace(None,"", regex="\D+", inplace=True)
    df.replace('0',False, inplace=True)
    
    # Extract only the classes from 19H
    data = df[10:11]

    # Iterate through the columns, and create a dict with the days & classes
    colunas = data.columns
    for c in colunas[1::]:
        aula = data[c].iloc[0]
        if(aula):
            aulas[int(aula)] = int(c)
    return aulas
    
    # Export to excel, to validate manually
    data.to_excel('./assets/horario.xlsx')

if __name__ == "__main__":
    parse_pdf()