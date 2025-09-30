from src.hh_database import create_database, create_tables
from src.hh_api import get_company,insert_employers_from_json, insert_vacancies_from_json, get_employers_id, get_vacancy
import json
import os
import psycopg2


if __name__ == "__main__":
    create_database()
    create_tables()

    employers = get_company()
    insert_employers_from_json()

    employers_id = get_employers_id(employers)

    vacancies = get_vacancy(employers_id)

    insert_vacancies_from_json()
