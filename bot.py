import tabula
import modules.database
from modules.emails import send_email

#config = dotenv_values(".env")
"""
Fetch the file
Check for headers update
Update the DB to the same header file
"""
send_email()
"""
If the file has changed, 
get the first 3 classes by 19h
send email
add them to the db 

df = tabula.read_pdf('elite.pdf')[0]

df.columns = df.columns.str.replace('\r', '')
print(df[10:11])
data = df[10:11]
data.to_excel('data.xlsx')
"""
