from pysqlcipher3 import dbapi2 as sqlite3
from dotenv import dotenv_values

config = dotenv_values("./../.env")


class Database:
    connection = None
    db_name = './assets/aulas.sql'
    cursor = None

    def __init__(self):
        # TODO: Try catch
        self.connection = sqlite3.connect(self.db_name)
        cursor = self.connection.cursor()
        cursor.execute("PRAGMA key='" + config["DB_PASSWORD"] + "'")

        sql_command = 'CREATE TABLE  IF NOT EXISTS `aulas` ( `numero` number INTEGER NOT NULL PRIMARY KEY, `marcacao` date); CREATE TABLE IF NOT EXISTS `horario` ( `id` number INTEGER NOT NULL PRIMARY KEY, `atualizacao` date );'
        cursor.executescript(sql_command)
        self.connection.commit()
        self.connection.close()

    def adicionar_aula(self, numero, marcacao):
        success = True

        self.connection = sqlite3.connect(self.db_name)
        cursor = self.connection.cursor()
        cursor.execute("PRAGMA key='" + config["DB_PASSWORD"] + "'")

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
        cursor.execute("PRAGMA key='" + config["DB_PASSWORD"] + "'")
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
        cursor.execute("PRAGMA key='" + config["DB_PASSWORD"] + "'")
        try:
            sql_command = 'select exists (select * from aulas where numero = ?)'
            result = cursor.execute(sql_command, (numero, ))
            [exists] = result.fetchone()  # destructuring objects
        except Exception as e:
            ""
        self.connection.close()
        return (success, exists == 1)

    def upsert_atualizar(self):
        success = False
        exists = False

        self.connection = sqlite3.connect(self.db_name)
        cursor = self.connection.cursor()
        cursor.execute("PRAGMA key='" + config["DB_PASSWORD"] + "'")
        try:
            sql_command = 'select exists (select * from horario)'
            result = cursor.execute(sql_command)
            [exists] = result.fetchone()  # destructuring objects
            if (exists == 1):
                sql_command = "update  horario set atualizacao = ?  where id = 1"
            else:
                sql_command = 'insert into horario(id,atualizacao) VALUES (1,?);'

            cursor.execute(sql_command, ("2021-04-11 25:00:00.00", ))
            self.connection.commit()
            print(1)
        except Exception as e:
            print(e)

        self.connection.close()
        return (success)


if __name__ == "__main__":
    db = Database()
    print(db.upsert_atualizar())
    print(db.adicionar_aula(23, "2021-04-11 14:00:00.00"))
    print(db.procurar_aula(23))
    db.adicionar_aula(24, "2021-04-11 14:00:00.00")
    db.procurar_aula(24)
