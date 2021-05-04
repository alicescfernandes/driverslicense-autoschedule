import gspread
from dotenv import dotenv_values
"""
gc = gspread.service_account("./credentials.json")

# Open a sheet from a spreadsheet in one go
# Update a range of cells using the top left corner address
"""



# TODO: Marcar as restantes aulas por dia

config = dotenv_values("./.env")
aulas_dependencias = {
    2:1,
    3:2,
    4:3,
    5:4,
    6:5,
    7:6,
    25:24,
    26:25,
    27:26,
    28:27,
}

class Database:
    gc = None

    def __init__(self):
        self.gc = gspread.service_account("./credentials.json")

    def get_worksheet(self, name="aulas"):
        sheets = self.gc.open_by_key(config["SHEET_NAME"])
        return sheets.worksheet(name)

    def verificar_deps(self,aula):
        if(aula in aulas_dependencias):
            dependencia = aulas_dependencias[aula]
            (_,existe) = self.procurar_aula(dependencia)
            return existe
        else:
            return True #Sem deps

    def adicionar_aula(self, numero, marcacao):
        success = True
      
        (_,existe) = self.procurar_aula(numero);
        if existe:return success

        sh = self.get_worksheet()
       
        try:
            sh.insert_row([numero,marcacao])
            sh.sort((1,'asc'))
        except Exception as e:
            success = False

        return success

    def remover_aula(self, numero, marcacao):
        '''TODO'''
        success = False
        return success

    def procurar_aula(self, numero):
        success = False
        exists = False
        sh = self.get_worksheet()
        try:
            result = sh.find(str(numero))
            exists = result is not None
        except Exception as e:
            ""
        return (success, exists)

    def upsert_atualizar(self, data):
        success = False
        exists = False
        sh = self.get_worksheet(name="update")

        try:
            sh.update_cell(1,1,data)
            success = True
        except Exception as e:
            print(e)
        return (success)
    
    def validar_data(self, data):
        success = False
        date = False
        sh = self.get_worksheet(name="update")

        try:
            [[date]] = sh.get("A1")
            success = True
        except Exception as e:
            print(e)

        return (success,data == date)


if __name__ == "__main__":
    db = Database()
    #print(db.upsert_atualizar("2021-05-01"))
    #print(db.adicionar_aula(23, "2021-05-22 14:00:00.00"))
    #print(db.procurar_aula(23))
    #db.adicionar_aula(24, "2021-05-22 14:00:00.00")
    #print(db.procurar_aula(20))
    #print(db.procurar_aula(1))
    print(db.validar_data("2021-05-03"))
    print(db.verificar_deps(17))
    print(db.verificar_deps(2))
    print(db.verificar_deps(28))