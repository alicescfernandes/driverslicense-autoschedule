from pysqlcipher3 import dbapi2 as sqlite3
from dotenv import dotenv_values

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
    connection = None
    db_name = './assets/aulas.sql'
    cursor = None

    def __init__(self):
        # TODO: Try catch
        self.connection = sqlite3.connect(self.db_name)
        cursor = self.connection.cursor()
        #cursor.execute("PRAGMA key='" + config["DB_PASSWORD"] + "'")

        sql_command = 'CREATE TABLE  IF NOT EXISTS `aulas` ( `numero` number INTEGER NOT NULL PRIMARY KEY, `marcacao` date); CREATE TABLE IF NOT EXISTS `horario` ( `id` number INTEGER NOT NULL PRIMARY KEY, `atualizacao` date );'
        cursor.executescript(sql_command)
        self.connection.commit()
        self.connection.close()

    def verificar_deps(self,aula):
        if(aula in aulas_dependencias):
            dependencia = aulas_dependencias[aula]
            (_,existe) = self.procurar_aula(dependencia)
            return existe
        else:
            return True #Sem deps

    def adicionar_aula(self, numero, marcacao):
        success = True

        self.connection = sqlite3.connect(self.db_name)
        cursor = self.connection.cursor()
        #cursor.execute("PRAGMA key='" + config["DB_PASSWORD"] + "'")

        try:
            sql_command = 'insert into aulas(numero,marcacao) VALUES (?, ?)'
            cursor.execute(sql_command, (numero, marcacao))
            self.connection.commit()
        except Exception as e:
            success = False

        self.connection.close()
        return success

    def remover_aula(self, numero, marcacao):
        success = True
        self.connection = sqlite3.connect(self.db_name)
        cursor = self.connection.cursor()
        #cursor.execute("PRAGMA key='" + config["DB_PASSWORD"] + "'")
        try:
            sql_command = 'insert into aulas(numero,marcacao) VALUES (?, ?)'
            cursor.execute(sql_command, (numero, marcacao))
            self.connection.commit()
        except Exception as e:
            success = False

        self.connection.close()
        return success

    def procurar_aula(self, numero):
        success = False
        exists = False

        self.connection = sqlite3.connect(self.db_name)

        cursor = self.connection.cursor()
        #cursor.execute("PRAGMA key='" + config["DB_PASSWORD"] + "'")
        try:
            sql_command = 'select exists (select * from aulas where numero = ?)'
            result = cursor.execute(sql_command, (numero, ))
            [exists] = result.fetchone()  # destructuring objects
        except Exception as e:
            ""
        self.connection.close()
        return (success, exists == 1)

    def upsert_atualizar(self, data):
        success = False
        exists = False

        self.connection = sqlite3.connect(self.db_name)
        cursor = self.connection.cursor()
        #cursor.execute("PRAGMA key='" + config["DB_PASSWORD"] + "'")
        try:
            sql_command = 'select exists (select * from horario)'
            result = cursor.execute(sql_command)
            [exists] = result.fetchone()  # destructuring objects
            if (exists == 1):
                sql_command = "update  horario set atualizacao = ?  where id = 1"
            else:
                sql_command = 'insert into horario(id,atualizacao) VALUES (1,?);'

            cursor.execute(sql_command, (data, ))
            self.connection.commit()
        except Exception as e:
            print(e)

        self.connection.close()
        return (success)
    
    def validar_data(self, data):
        success = False
        date = False

        self.connection = sqlite3.connect(self.db_name)
        cursor = self.connection.cursor()
        #cursor.execute("PRAGMA key='" + config["DB_PASSWORD"] + "'")
        try:
            sql_command = 'select exists(SELECT * FROM horario where atualizacao = "{0}");'.format(data)
            result = cursor.execute(sql_command)
            [date] = result.fetchone()  # destructuring objects
            success = True
        except Exception as e:
            print(e)

        self.connection.close()
        return (success,date == 1)


if __name__ == "__main__":
    db = Database()
    print(db.upsert_atualizar("2021-05-01 14:00:00.00"))
    print(db.adicionar_aula(23, "2021-05-22 14:00:00.00"))
    print(db.procurar_aula(23))
    db.adicionar_aula(24, "2021-05-22 14:00:00.00")
    db.procurar_aula(24)
    db.validar_data("2021-05-23")
    db.verificar_deps(17)
    db.verificar_deps(2)
    db.verificar_deps(28)
