from modules.database import Database
from modules.emails import send_email
from modules.parse_pdf import parse_pdf
from modules.scrapper import * 
import schedule
import time


# TODO: Send notification to phone

#config = dotenv_values(".env")
"""
Fetch the file
Check for headers update
Update the DB to the same header file
"""
#send_email()
"""
If the file has changed, 
get the first 3 classes by 19h
send email
add them to the db 

"""

db = Database()
def run_bot():
    (success, is_posted) =  check_facebook()
    if(not success or  not is_posted): return
    
    (success, date_modified) = download_pdf()
    if(not success): return
    date_iso = date_modified.strftime("%Y-%m-%d")
    (success, file_atualizado) = db.validar_data(date_iso)
    if(not success): return
    if(file_atualizado):
        print("PDF already updated")
        return;
    else:
        aulas = parse_pdf()
        aulas_por_marcar = []
        aulas_por_marcar_format = []
        # ver aulas já feitas
        for aula in aulas:
            (_,existe) = db.procurar_aula(aula) 
            dep_marcada = db.verificar_deps(aula)
            if(not existe and dep_marcada == True):
                aulas_por_marcar_format.append(("Dia {0}".format(aulas[aula]),"Aula {0}".format(aula)))
                aulas_por_marcar.append(aula)
        
        aulas_por_marcar = aulas_por_marcar[0:3]
        aulas_por_marcar_format = aulas_por_marcar_format[0:3]
        db.upsert_atualizar(date_iso)
        send_email(aulas_por_marcar_format)

        for aula in aulas_por_marcar:
            print(aula, db.adicionar_aula(aula,"1970-01-01")) #TODO: Add proper date

           
schedule.every(5).minutes.do(run_bot)
run_bot()
while True:
    schedule.run_pending()
    time.sleep(1)
