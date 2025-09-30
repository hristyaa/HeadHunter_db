import psycopg2

class DBManager():
    """ Класс для работы с БД (таблицами employers и vacancies)"""
    def __init__(self, db_name, user, password, host, port):
        """Инициализация класса"""
        self.__db_name = db_name
        self.__user = user
        self.__password = password
        self.__host = host
        self.__port = port


    def connect(self):
        """Установка соединения с БД"""
        try:
            self.conn = psycopg2.connect(
                dbname=self.__db_name,
                user=self.__user,
                password=self.__password,
                host=self.__host,
                port=self.__port
            )
            self.cur = self.conn.cursor()
        except psycopg2.OperationalError as e:
            print(f"Ошибка подключения: {e}")

    def get_companies_and_vacancies_count(self):
        """ Метод получения списка всех компаний и количества вакансий у каждой компании"""
        try:
            self.cur.execute("""
                SELECT vacancies.employer_name, count(*) FROM vacancies
                GROUP BY vacancies.employer_name
                ORDER BY count (*) DESC;""")
            return self.cur.fetchall()

        except Exception as e:
            print(f"Ошибка при запросе: {e}")
            return []



    def close(self):
        """Закрывает соединение"""
        if self.cur:
            self.cur.close()
        if self.conn:
            self.conn.close()










