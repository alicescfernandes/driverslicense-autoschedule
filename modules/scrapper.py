import requests
from dateutil.parser import parse
from dotenv import dotenv_values
from datetime import datetime

meses = ["Janeiro", "Fevereiro", "Março","Abril","Maio","Junho","Julho","Agosto","Setempro"]
config = dotenv_values(".env")

def download_pdf():
    success = False
    url = config["HORARIO_PDF"]
    r = requests.get(url)
    date_modified = None
    print('Downloading PDF')

    if (r.status_code == 200):
        with open('./assets/horario.pdf', 'wb') as f:
            f.write(r.content)
            date_modified = parse(r.headers['Last-Modified'])
            success = True
            print('PDF Downloaded')

    return (success, date_modified)


def check_facebook():
    success = False
    next_month_online = False
    url = config["FACEBOOK_URL"]
    r = requests.get(url)
    if (r.status_code == 200):
        success = True
        today = datetime.today()
        #current_day = today.day
        current_day = 28
        print('Current Day: {0}'.format(current_day))

        if(current_day >= 27):
            #mes = meses[today.month]
            mes = meses[today.month-1]
            print('Checking for {0} de 2021'.format(mes))
            next_month_online = '{0} de 2021'.format(mes) in str(r.content)

    return (success,next_month_online)  
      

if __name__ == "__main__":
    print(download_pdf())
    print(check_facebook())