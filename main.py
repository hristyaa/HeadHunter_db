from src.hh_database import create_database, create_tables, clear_table
from src.hh_api import get_company, insert_employers_from_json, insert_vacancies_from_json, get_employers_id, \
    get_vacancy
from src.db_manager import DBManager
import json
import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")


if __name__ == "__main__":
    create_database()
    create_tables()
    clear_table('vacancies')
    clear_table('employers')

    employers = get_company()
    insert_employers_from_json()

    employers_id = get_employers_id(employers)

    vacancies = get_vacancy(employers_id)

    insert_vacancies_from_json()

    # db = DBManager(DB_NAME,DB_USER,DB_PASSWORD,DB_HOST,DB_PORT)
    # db.connect()
    # employers_db = db.get_companies_and_vacancies_count()
    # for emloyer_name, count_vacancies in employers_db:
    #     print(f'{emloyer_name} - количество вакансий: {count_vacancies}')
    # db.close()

    # db = DBManager(DB_NAME,DB_USER,DB_PASSWORD,DB_HOST,DB_PORT)
    # db.connect()
    # all_vacancies_db = db.get_all_vacancies()
    # for employer_name, name, salary, url in all_vacancies_db:
    #     print(f"{employer_name} | {name} | {salary} | {url}")
    # db.close()

    # db = DBManager(DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT)
    # db.connect()
    # avg_salary_db = db.get_avg_salary()
    # print(f"Средняя зарплата по вакансиям: {round(avg_salary_db, 2)} руб.")
    # db.close()

    # db = DBManager(DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT)
    # db.connect()
    # vacancies_avg_salary = db.get_vacancies_with_higher_salary()
    # for employer_name, name, salary, url in vacancies_avg_salary:
    #     print(f"{employer_name} | {name} | {salary} | {url}")
    # db.close()

    db = DBManager(DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT)
    db.connect()
    keywords = 'лаборант, материал, сварщик'
    keywords_list = [word.strip() for word in keywords.split(",")]
    for word in keywords_list:
        vacancies_keyword = db.get_vacancies_with_keyword(word)
        for employer_name, name, salary, url in vacancies_keyword:
            print(f"{employer_name} | {name} | {salary} | {url}")
    db.close()

