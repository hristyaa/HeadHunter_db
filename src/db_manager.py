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
                SELECT employer_name, count(*) FROM employers
                LEFT JOIN vacancies ON employers.id = vacancies.employer_id
                GROUP BY employer_name
                ORDER BY count (*) DESC;""")
            return self.cur.fetchall()

        except Exception as e:
            print(f"Ошибка при запросе: {e}")
            return []

    def get_all_vacancies(self):
        '''
        Получение списка всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию
        '''
        try:
            self.cur.execute("""
                SELECT vacancies.employer_name, vacancies.name, vacancies.salary, vacancies.url
                FROM vacancies
                LEFT JOIN employers ON employers.id = vacancies.employer_id
                ORDER BY employer_name;
""")

            return self.cur.fetchall()

        except Exception as e:
            print(f"Ошибка при запросе: {e}")
            return []

    def get_avg_salary(self):
        ''' Получение средней зарплаты по вакансиям '''
        try:
            self.cur.execute("""
                SELECT AVG(salary) FROM vacancies
                WHERE salary IS NOT NULL;
        """)
            result = self.cur.fetchone()
            return result[0] if result and result[0] is not None else 0

        except Exception as e:
            print(f"Ошибка при запросе: {e}")
            return []

    def get_vacancies_with_higher_salary(self):
        ''' Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям'''
        try:
            self.cur.execute(f"""
                SELECT employer_name, name, salary, url FROM vacancies
                WHERE salary > (SELECT AVG(salary) FROM vacancies WHERE salary IS NOT NULL);
        """)
            return self.cur.fetchall()

        except Exception as e:
            print(f"Ошибка при запросе: {e}")
            return []

    def get_vacancies_with_keyword(self, keyword):
        ''' Получает список всех вакансий, в названии которых содержатся переданные в метод слова'''
        if not keyword:
            return []
        try:
            query = f"""
                SELECT employer_name, name, salary, url FROM vacancies
                WHERE lower(name) LIKE  lower(%s) ;
        """
            param = (f"%{keyword}%",)
            self.cur.execute(query, param)
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
