import smtplib
from email.message import EmailMessage
from dotenv import dotenv_values
from functools import reduce

config = dotenv_values(".env")


def send_email(aulas):
    reduce_fn = lambda accum, aula: accum + "{0}, {1}\n".format(
        aula[0], aula[1])

    aulas_text = reduce(reduce_fn, aulas, "")

    with open("./assets/email.txt") as fp:
        email_body = fp.read().replace("<aulas>", aulas_text)
        msg = EmailMessage()
        msg.set_content(email_body)

        msg['Subject'] = 'Marcação de Aulas'
        msg['From'] = config["SMTP_SENDER"]
        msg['To'] = config["SMTP_SENDER"]

        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.ehlo()
        s.starttls()
        s.login(config["SMTP_SENDER"], config["SMTP_PWD"])
        s.send_message(msg)
        s.quit()


if __name__ == "__main__":
    aulas = [("Dia 3", " Aula 20"), ("Dia 4", "Aula 1"), ("Dia 5", "Aula 21")]
    send_email(aulas)