import tabula

df = tabula.read_pdf('cenas.pdf')[0]

df.columns = df.columns.str.replace('\r', '')
print(df[10:11])
data = df[10:11]
data.to_excel('data.xlsx')