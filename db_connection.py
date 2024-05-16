import psycopg2
from typing import Optional
from colorama import Fore

# connect database -----------------------------------------------------------------------------------------------------

db_info: dict[str, str] = {'username': 'postgres',
                           'password': 'Mer1',
                           'host': 'localhost',
                           'port': '5432',
                           'database': 'my_db'}

connection = psycopg2.connect(host=db_info['host'],
                              database=db_info['database'],
                              user=db_info['username'],
                              password=db_info['password'],
                              port=db_info['port'])

cursor1 = connection.cursor()

default_users_table = ("CREATE TABLE IF NOT EXISTS users("
                       "username VARCHAR(25) NOT NULL PRIMARY KEY,"
                       "password VARCHAR(16) NOT NULL,"
                       "email    VARCHAR(20),"
                       "active   BOOLEAN NOT NULL DEFAULT FALSE);")
cursor1.execute(default_users_table)
connection.commit()


# main class -----------------------------------------------------------------------------------------------------------
class User:
    def __init__(self, username: str, password: str, active, email: Optional[str] = None):
        self.username = username
        self.password = password
        self.email = email
        self.active = active

    @staticmethod
    def creating_database(table_name: str, column1: str, column2: str, column3: str, column4: str):
        cursor1.execute("CREATE TABLE IF NOT EXISTS {}("
                        "{} VARCHAR(55) NOT NULL PRIMARY KEY,"
                        "{} VARCHAR(25) NOT NULL,"
                        "{} VARCHAR(25)"
                        "{} BOOLEAN NOT NULL DEFAULT FALSE"
                        ")".format(table_name, column1, column2, column3, column4))
        connection.commit()
        print(Fore.GREEN + "Database created successfully✅" + Fore.RESET)

    @staticmethod
    def get_all(table_name: str):
        cursor1.execute("SELECT * FROM {};".format(table_name))
        db = cursor1.fetchall()
        count = 0
        if db:
            for i in db:
                print(f"Data {count}: {i}")
                count += 1
        else:
            print(Fore.RED + "Database is empty⁉️" + Fore.RESET)

    def insert(self):
        cursor1.execute("INSERT INTO users(username, password, email, active)"
                        "VALUES(%s, %s, %s, %s);", (self.username, self.password, self.email, self.active))
        connection.commit()
        print(Fore.GREEN + "{}'s information inserted successfully✅".format(ent_username) + Fore.RESET)

    def update(self, ent_table1: str, old_username: str):
        cursor1.execute("UPDATE {} SET username=%s, password=%s, email=%s, active=%s "
                        "WHERE username=%s".format(ent_table1),
                        (self.username, self.password, self.email, self.active, old_username))
        connection.commit()
        print(Fore.GREEN + "Updated User, Successfully✅" + Fore.RESET)

    @staticmethod
    def delete(ent_table2: str, ent_username1: str):
        cursor1.execute("DELETE FROM {} WHERE username=%s".format(ent_table2), (ent_username1,))
        connection.commit()
        print(Fore.GREEN + "Deleted User, Successfully✅" + Fore.RESET)


# running in loop ------------------------------------------------------------------------------------------------------


if __name__ == '__main__':
    while True:
        try:
            print(Fore.LIGHTCYAN_EX + "1. Create User🆕 \n2. Update User⬆️"
                                      " \n3. Delete User❌ \n4. Display Users💹 \n5. Exit🔚" + Fore.RESET)
            choice: int = int(input(Fore.LIGHTBLUE_EX + "What would you like to do❓..." + Fore.RESET))
        except ValueError as e:
            print(Fore.LIGHTRED_EX + f"{e}" + Fore.RESET,
                  Fore.RED + "\nPlease enter a valid number." + Fore.RESET)

        else:
            try:
                if choice == 1:
                    ent_username: str = input("Enter new username: ")
                    ent_password: str = input("Enter new password: ")
                    ent_email: str = input("Enter new email: ")
                    ent_active = input("Would you like to activate your account? (0/1): ")
                    User(ent_username, ent_password, ent_active, ent_email).insert()

                elif choice == 2:
                    ent_table = input(Fore.LIGHTMAGENTA_EX + "Enter table name: " + Fore.RESET)
                    ent_old_username = input(Fore.LIGHTMAGENTA_EX + "Enter old username: " + Fore.RESET)
                    ent_username = input("Enter new username: ")
                    ent_password = input("Enter new password: ")
                    ent_email = input("Enter new email: ")
                    ent_active = input("Would you like to activate your account? (0/1): ")
                    User(ent_username, ent_password, ent_active, ent_email).update(ent_table, ent_old_username)

                elif choice == 3:
                    ent_table: str = input(Fore.LIGHTMAGENTA_EX + "Enter table name: " + Fore.RESET)
                    ent_old_username: str = input(Fore.LIGHTMAGENTA_EX + "Enter old username: " + Fore.RESET)
                    User.delete(ent_table, ent_old_username)

                elif choice == 4:
                    User.get_all(input(Fore.LIGHTMAGENTA_EX + "Enter table name to show all data: " + Fore.RESET))

                elif choice == 5:
                    print(Fore.MAGENTA + "Thank you for using our service🫡" + Fore.RESET)
                    quit()

                else:
                    print(Fore.LIGHTYELLOW_EX + "Please enter a valid number." + Fore.RESET)

            except Exception as e:
                print(Fore.LIGHTRED_EX + "Table is not found.\nTry again" + Fore.RESET)
                print(Fore.YELLOW + "More: {error}".format(error=e) + Fore.RESET)
                connection.rollback()
