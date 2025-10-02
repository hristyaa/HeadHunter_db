import os

import psycopg2
from dotenv import load_dotenv

load_dotenv()

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")


def create_database() -> None:
    """Создание базы данных"""
    try:
        conn = psycopg2.connect(dbname="postgres", user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)

        conn.autocommit = True

        cur = conn.cursor()

        cur.execute(f"SELECT 1 FROM pg_database WHERE datname = '{DB_NAME}';")
        exists = cur.fetchone()

        if not exists:
            cur.execute(f"CREATE DATABASE {DB_NAME};")

    finally:
        cur.close()
        conn.close()


def create_tables() -> None:
    """Создание SQL-таблиц"""
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)

    cur = conn.cursor()

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS employers (
            id BIGINT PRIMARY KEY,
            name VARCHAR NOT NULL,
            url TEXT,
            alternate_url TEXT,
            vacancies_url TEXT,
            open_vacancies INT
                    )
        """
    )

    cur.execute(
        """
       CREATE TABLE IF NOT EXISTS vacancies (
           id BIGINT PRIMARY KEY,
           name VARCHAR NOT NULL,
           salary NUMERIC,
           url TEXT,
           area TEXT,
           type TEXT,
           employer_id BIGINT REFERENCES employers(id) ON DELETE CASCADE,
           employer_name VARCHAR
       )
       """
    )

    conn.commit()
    cur.close()
    conn.close()


def clear_table(table_name: str) -> None:
    """Очистка таблицы"""
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)

    cur = conn.cursor()

    cur.execute(f"TRUNCATE TABLE {table_name} CASCADE;")

    conn.commit()
    cur.close()
    conn.close()
