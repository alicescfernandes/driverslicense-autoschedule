import gspread
from dotenv import dotenv_values

# TODO: Marcar as restantes aulas por dia

config = dotenv_values("./.env")

# Restrições para as aulas sequenciais
aulas_dependencias = {
    2:1,
    3:2,
    4:3,
    5:4,
    6:5,
    7:6,
    8:7,
    9:7,
    10:7,
    11:7,
    12:7,
    13:7,
    14:7,
    16:7,
    17:7,
    18:7,
    19:7,
    20:7,
    21:7,
    22:7,
    23:7,
    24:7,
    25:24,
    26:25,
    27:26,
    28:27,
}

# Restrições para as aulas que precisem de horas praticas
aulas_praticas_dependencias = {
    24:16,
    25:16,
    26:16,
    26:16,
    28:16
}

class Database:
    gc = None
    aulas = []

    def __init__(self):
        self.gc = gspread.service_account("./credentials.json")
    
    # Retorna uma google sheet
    def get_worksheet(self, name="teoricas"):
        sheets = self.gc.open_by_key(config["SHEET_NAME"])
        return sheets.worksheet(name)
    
    # Retorna todas as aulas práticas marcadas
    def get_praticas(self):
        sh = self.get_worksheet(name="praticas")
        res = []
        try:
            [res] = sh.get("A2:A33",major_dimension="COLUMNS")
        except Exception as e:
            ''' '''
        return  res


    # Retorna true se aula pode ser marcada, false se aula não pode ser marcada
    def verificar_deps(self,aula, premarcacao):
        # Verificar horas práticas
        if(aula in aulas_praticas_dependencias):
            horas = aulas_praticas_dependencias[aula]
            praticas_marcadas = len(self.get_praticas())
            if(horas > praticas_marcadas):
                return False

        # Verificar aulas sequenciais
        if(aula in aulas_dependencias):
            existe = False
            dependencia = aulas_dependencias[aula]
            (_,existe) = self.procurar_aula(dependencia)
     
            if(existe == False):
                dependencia = aulas_dependencias[aula]
                existe = dependencia in premarcacao

            return existe
        else:
            return True #Sem deps

    def adicionar_aula(self, numero, marcacao):
        success = True
      
        (_,existe) = self.procurar_aula(numero);
        if existe:return success

        sh = self.get_worksheet()
       
        try:
            sh.append_row([numero,marcacao],value_input_option="USER_ENTERED",insert_data_option='INSERT_ROWS')
        except Exception as e:
            print(e)
            success = False

        return success

    def remover_aula(self, numero, marcacao):
        '''TODO'''
        success = False
        return success

    def get_todas_aulas(self):
        success = False
        result = []
        sh = self.get_worksheet()
        try:
            [result] = sh.get("A2:A99",major_dimension="COLUMNS")
            self.aulas = result
        except Exception as e:
            ""
        return (success, result)

    def procurar_aula(self, numero):
        if(self.aulas is None): self.get_todas_aulas()
        success = False
        exists = False
        try:
            exists = str(numero) in self.aulas
            success = True

        except Exception as e:
            ""
        return (success, exists)

    def upsert_atualizar(self, data):
        success = False
        exists = False
        sh = self.get_worksheet(name="config")
        
        try:
            sh.update_cell(2,1,data)
            success = True
            print("PDF Atualizado")
        except Exception as e:
            print(e)
        return (success)
    
    def validar_data(self, data):
        success = False
        date = False
        sh = self.get_worksheet(name="config")

        try:
            [[date]] = sh.get("A2")
            success = True
        except Exception as e:
            print(e)

        return (success,data == date)
   
    def get_total_marcacoes(self):
        success = False
        result = False
        sh = self.get_worksheet(name="config")
        
        try:
            [[result]] = sh.get("B2")
            success = True
        except Exception as e:
            print(e)

        return (success,int(result))


if __name__ == "__main__":
    db = Database()
    print(db.get_todas_aulas())
    print(db.upsert_atualizar("2021-05-01"))
    print(db.adicionar_aula(23, "2021-05-22 14:00:00.00"))
    print(db.procurar_aula(23))
    
    print(db.adicionar_aula(24, "2021-05-22 14:00:00.00"))
    print(db.procurar_aula(20))
    print(db.procurar_aula(1))
    
    print(db.procurar_aula(23))
    print(db.get_total_marcacoes())
    print(db.get_praticas())
    print(db.validar_data("2021-05-03"))
   
    print(db.verificar_deps(17))
    print(db.verificar_deps(2))
    print(db.verificar_deps(24))
    print(db.verificar_deps(28))
