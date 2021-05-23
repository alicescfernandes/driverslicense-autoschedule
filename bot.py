from random import randint
from modules.sheets import Database
from modules.emails import send_email
from modules.parse_pdf import parse_pdf
from modules.scrapper import * 
import schedule
import time
from datetime import date

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
    print("Last Modified", date_modified)
    year = date.today().year
    month = date_modified.month + 1
  

    if(not success): return
    date_iso = date_modified.strftime("%Y-%m-%d")
    (success, file_atualizado) = db.validar_data(date_iso)
    if(not success): return
    if(file_atualizado):
        print("PDF already updated")
        return;
    else:
        print("Scheduling Classes")
        (_,marcadas) = db.get_total_marcacoes()
        if(marcadas >= 3):
            print("Máximo de aulas marcadas")
            return
        marcacoes_disponiveis = 3 - marcadas
        db.get_todas_aulas()
        aulas = parse_pdf()
        aulas_por_marcar = []
        aulas_por_marcar_format = []

        current_dia = date.today().day
        # ver aulas já feitas
        for aula in aulas:
            (_,existe) = db.procurar_aula(aula) 
            dep_marcada = db.verificar_deps(aula)
            if(aulas[aula] > current_dia and not existe and dep_marcada == True):
                aulas_por_marcar_format.append(("Dia {0}".format(aulas[aula]),"Aula {0}".format(aula)))
                aulas_por_marcar.append([aula, aulas[aula]])
                
        aulas_por_marcar = aulas_por_marcar[0:marcacoes_disponiveis]
        aulas_por_marcar_format = aulas_por_marcar_format[0:marcacoes_disponiveis]
        db.upsert_atualizar(date_iso)
        if(len(aulas_por_marcar_format) == 0):
            print("Sem aulas por marcar",aulas_por_marcar_format)
            return 
    
        send_email(aulas_por_marcar_format)

        for aula in aulas_por_marcar:
            print(aula[0], db.adicionar_aula(aula[0],"{0}-{1}-{2}".format(year,str(month).zfill(2),str(aula[1]).zfill(2)))) #TODO: Add proper date

           
schedule.every(30).minutes.do(run_bot)
run_bot()
while True:
    schedule.run_pending()
    time.sleep(1)
