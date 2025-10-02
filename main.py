import os
import re

from dotenv import load_dotenv

from src.db_manager import DBManager
from src.hh_api import (
    get_company,
    get_employers_id,
    get_vacancy,
    insert_employers_from_json,
    insert_vacancies_from_json,
)
from src.hh_database import clear_table, create_database, create_tables

load_dotenv()

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

if __name__ == "__main__":
    create_database()
    create_tables()
    clear_table("vacancies")
    clear_table("employers")
    while True:
        user_area = int(
            input(
                """Привет!
Для получения данных о работодателях и их вакансиях с сайта hh.ru набери цифру региона из представленных:
    1 - Чита
    2 - Иркутск
    3 - Улан-Удэ
    4 - Владивосток
    5 - Новосибирск
Вы выбираете регион: """
            )
        )
        try:
            if user_area in [1, 2, 3, 4, 5]:
                if user_area == 1:
                    area = 106
                    break
                elif user_area == 2:
                    area = 35
                    break
                elif user_area == 3:
                    area = 20
                    break
                elif user_area == 4:
                    area = 22
                    break
                elif user_area == 5:
                    area = 4
                    break
            else:
                print("Ошибка: выбран неверный регион, попробуйте снова.")
        except ValueError:
            print("Ошибка: нужно ввести число от 1 до 5, попробуйте снова.")

    employers = get_company(area=area)
    insert_employers_from_json()

    employers_id = get_employers_id(employers)

    vacancies = get_vacancy(employers_id)

    insert_vacancies_from_json()

    print(
        """\nОтлично! Регион выбран!
Получены топ-10 работодателей в регионе по количеству открытых вакансий.
Загружены вакансии полученных работодателей.\n"""
    )
    while True:
        user_input = int(
            input(
                """Для получения:
- списка всех компаний и количества вакансий у каждой компании
введите 1;
- списка всех вакансий с указанием названия компании, названия вакансии, зарплаты и ссылки на вакансию
введите 2;
- средней зарплаты по вакансиям
введите 3;
- списка всех вакансий, у которых зарплата выше средней по всем вакансиям
введите 4;
- списка всех вакансий, в названии которых содержатся переданные слова
введите 5.
Для завершения работы введите 0.
Введите выбранный пункт меню: """
            )
        )
        print("")
        try:
            if user_input in [1, 2, 3, 4, 5]:
                db = DBManager(DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT)
                db.connect()

                if user_input == 1:
                    employers_db = db.get_companies_and_vacancies_count()
                    for emloyer_name, count_vacancies in employers_db:
                        print(f"{emloyer_name} - количество вакансий: {count_vacancies}")
                    print("")
                elif user_input == 2:
                    all_vacancies_db = db.get_all_vacancies()
                    for employer_name, name, salary, url in all_vacancies_db:
                        print(f"{employer_name} | {name} | {salary} | {url}")
                    print("")
                elif user_input == 3:
                    avg_salary_db = db.get_avg_salary()
                    print(f"\nСредняя зарплата по вакансиям: {round(avg_salary_db, 2)} руб.\n")

                elif user_input == 4:
                    vacancies_avg_salary = db.get_vacancies_with_higher_salary()
                    for employer_name, name, salary, url in vacancies_avg_salary:
                        print(f"{employer_name} | {name} | {salary} | {url}")
                    print("")
                elif user_input == 5:
                    keywords = input(
                        """Введите слова для поиска вакансий через запятую, например:
'лаборант, материал, сварщик'\n"""
                    )
                    keywords_list = [word.strip() for word in re.split(r"[,\s]+", keywords)]
                    for word in keywords_list:
                        vacancies_keyword = db.get_vacancies_with_keyword(word)
                        if vacancies_keyword:
                            for employer_name, name, salary, url in vacancies_keyword:
                                print(f"{employer_name} | {name} | {salary} | {url}")
                        else:
                            print(f"Вакансии, содержащие слово '{word}', не найдены")
                    print("")
                db.close()
            elif user_input == 0:
                print("Программа завершена. До скорой встречи!")
                break
            else:
                print("\nОшибка: выюбранного пункта не существует, попробуйте снова.\n")
        except ValueError:
            print("\nОшибка: нужно ввести число от 0 до 5, попробуйте снова.\n")

    # db = DBManager(DB_NAME,DB_USER,DB_PASSWORD,DB_HOST,DB_PORT)
    # db.connect()
    # employers_db = db.get_companies_and_vacancies_count()
    # for emloyer_name, count_vacancies in employers_db:
    #     print(f'{emloyer_name} - количество вакансий: {count_vacancies}')
    # db.close()
    #
    # db = DBManager(DB_NAME,DB_USER,DB_PASSWORD,DB_HOST,DB_PORT)
    # db.connect()
    # all_vacancies_db = db.get_all_vacancies()
    # for employer_name, name, salary, url in all_vacancies_db:
    #     print(f"{employer_name} | {name} | {salary} | {url}")
    # db.close()
    #
    # db = DBManager(DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT)
    # db.connect()
    # avg_salary_db = db.get_avg_salary()
    # print(f"Средняя зарплата по вакансиям: {round(avg_salary_db, 2)} руб.")
    # db.close()
    #
    # db = DBManager(DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT)
    # db.connect()
    # vacancies_avg_salary = db.get_vacancies_with_higher_salary()
    # for employer_name, name, salary, url in vacancies_avg_salary:
    #     print(f"{employer_name} | {name} | {salary} | {url}")
    # db.close()
    #
    # db = DBManager(DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT)
    # db.connect()
    # keywords = 'лаборант, материал, сварщик'
    # keywords_list = [word.strip() for word in keywords.split(",")]
    # for word in keywords_list:
    #     vacancies_keyword = db.get_vacancies_with_keyword(word)
    #     for employer_name, name, salary, url in vacancies_keyword:
    #         print(f"{employer_name} | {name} | {salary} | {url}")
    # db.close()
