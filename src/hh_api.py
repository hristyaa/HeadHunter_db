import json
import os
from typing import Any

import psycopg2
import requests
from dotenv import load_dotenv

load_dotenv()

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
directory = os.path.join(base_dir, "data")
os.makedirs(directory, exist_ok=True)

file_employers = os.path.join(directory, "company.json")
file_vacancies = os.path.join(directory, "vacancy.json")


def get_company(file_employers: str = file_employers, area: int = 106) -> dict[str, Any]:
    """
    Получение данных о топ-10 компаниях с наибольшим количеством вакансий (по умолчанию в Чите)
    и сохранение данных в JSON-файл
    """
    url_employers = "https://api.hh.ru/employers/"
    params: dict[str, str] = {
        "per_page": "10",
        "sort_by": "by_vacancies_open",
        "only_with_vacancies": "True",
        "locale": "RU",
        "area": str(area),
    }
    response = requests.get(url_employers, params=params)
    if response.status_code != 200:
        raise ValueError(f"Ошибка: {response.status_code}")
    employers_json: Any = response.json()
    employers: dict[str, Any] = dict(employers_json)

    with open(file_employers, "w", encoding="utf-8") as f:
        json.dump(employers, f, ensure_ascii=False, indent=4)
    return employers


def get_employers_id(employers: dict) -> list:
    """Получение списка employers_id"""
    employers_items = employers["items"]
    employers_id = []
    for employer in employers_items:
        employers_id.append(employer["id"])
    return employers_id


def insert_employers_from_json(file_employers: str = file_employers) -> None:
    """Вставка данных по API-запросу о работодателях в таблицу employers"""

    with open(file_employers, "r", encoding="utf-8") as f:
        json_employers = json.load(f)

    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)

    cur = conn.cursor()

    for item in json_employers["items"]:
        try:
            cur.execute(
                """
                    INSERT INTO employers
                    (id, name, url, alternate_url, vacancies_url, open_vacancies)
                    VALUES (%s,%s,%s,%s,%s,%s)
                    ON CONFLICT (id) DO NOTHING
                    """,
                (
                    int(item["id"]),
                    item["name"],
                    item["url"],
                    item["alternate_url"],
                    item["vacancies_url"],
                    item["open_vacancies"],
                ),
            )
        except Exception as e:
            print(f"Ошибка при вставке {item['id']}: {e}")

    conn.commit()
    cur.close()
    conn.close()


def get_vacancy(employers_id: list, file_vacancies: str = file_vacancies) -> None:
    """
    Получение данных о вакансиях топ-10 работодателей
    """
    vacancies = []
    for employer_id in employers_id:
        page = 0
        while True:

            url_vacancies = "https://api.hh.ru/vacancies/"
            params = {"employer_id": employer_id, "per_page": 100, "page": page}
            response = requests.get(url_vacancies, params=params)
            if response.status_code != 200:
                raise ValueError(f"Ошибка: {response.status_code}")
            data = response.json()
            data_vacancies = data.get("items", [])
            vacancies.extend(data_vacancies)

            if page >= data.get("pages", 0) - 1:
                break
            page += 1

    with open(file_vacancies, "w", encoding="utf-8") as f:
        json.dump(vacancies, f, ensure_ascii=False, indent=4)


def insert_vacancies_from_json(file_vacancies: str = file_vacancies) -> None:
    """Вставка данных по API-запросу о вакансиях в таблицу vacancies"""

    with open(file_vacancies, "r", encoding="utf-8") as f:
        json_vacancies = json.load(f)

    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)

    cur = conn.cursor()

    for vacancy in json_vacancies:
        area_name = vacancy.get("area", {}).get("name")
        vacancy_type = vacancy.get("type", {}).get("name")
        employer_id = vacancy.get("employer", {}).get("id")
        employer_name = vacancy.get("employer", {}).get("name")

        if vacancy.get("salary"):
            vacancy_salary = vacancy["salary"].get("from")
        else:
            vacancy_salary = None
        try:
            cur.execute(
                """
                    INSERT INTO vacancies
                    (id, name, salary, url, area, type, employer_id, employer_name)
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
                    ON CONFLICT (id) DO NOTHING
                    """,
                (
                    int(vacancy["id"]),
                    vacancy["name"],
                    vacancy_salary,
                    vacancy["url"],
                    area_name,
                    vacancy_type,
                    employer_id,
                    employer_name,
                ),
            )
        except Exception as e:
            print(f"Ошибка при вставке {vacancy['id']}: {e}")

    conn.commit()
    cur.close()
    conn.close()


# employers_id = get_employers_id(get_company())
# print(employers_id)
# get_vacancy(employers_id)
