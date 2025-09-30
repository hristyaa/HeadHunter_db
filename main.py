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

    db = DBManager(DB_NAME,DB_USER,DB_PASSWORD,DB_HOST,DB_PORT)
    db.connect()
    employers_db = db.get_companies_and_vacancies_count()
    for emloyer_name, count_vacancies in employers_db:
        print(f'{emloyer_name} - количество вакансий: {count_vacancies}')
    db.close()
