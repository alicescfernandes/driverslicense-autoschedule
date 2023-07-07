import random
import requests
from dateutil.parser import parse
from dotenv import dotenv_values
from datetime import datetime
import re
meses = ["Janeiro", "Fevereiro", "Março","Abril","Maio","Junho","Julho","Agosto","Setempro"]
config = dotenv_values(".env")

user_agents = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
    "Mozilla/5.0 (iPad; CPU OS 8_0_1 like Mac OS X; sl-SI) AppleWebKit/531.24.7 (KHTML, like Gecko) Version/3.0.5 Mobile/8B116 Safari/6531.24.7",
    ]


def download_pdf():
    r = random.randrange(0,len(user_agents))
    headers = {
        "user-agent":user_agents[r],
        "pragma":"no-cache",
        "cache-control":"no-cache",
        "upgrade-insecure-requests": "1"
    }


    success = False
    url = config["HORARIO_PDF"]
    print("Reading from ", url)
    r = requests.get(url,headers=headers)
    date_modified = None

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
        current_day = today.day
        
        print('Current Day: {0}'.format(current_day))
        if(current_day >= 25):
            mes = meses[today.month]
            print('Checking for {0} de 2021'.format(mes))
            next_month_online = re.search('{0}.*2021'.format(mes),str(r.content))
        else:
            print('Not checking for new FB post')


    return (success,next_month_online)  
      

if __name__ == "__main__":
    print(download_pdf())
    print(check_facebook())