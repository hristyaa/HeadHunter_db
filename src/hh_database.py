import psycopg2
import os
from dotenv import load_dotenv
import json

load_dotenv()

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")


def create_database():
    """Создание базы данных"""
    try:
        conn = psycopg2.connect(
                dbname="postgres",
                user=DB_USER,
                password=DB_PASSWORD,
                host=DB_HOST,
                port=DB_PORT
        )

        conn.autocommit = True

        cur = conn.cursor()

        cur.execute(f"SELECT 1 FROM pg_database WHERE datname = '{DB_NAME}';")
        exists = cur.fetchone()

        if not exists:

            cur.execute(f"CREATE DATABASE {DB_NAME};")
            print(f"База данных '{DB_NAME}' успешно создана.")
        else:
            print(f"База данных '{DB_NAME}' уже существует.")

    finally:
        cur.close()
        conn.close()

def create_tables():
    """ Создание SQL-таблиц"""
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )

    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS employers (
            id BIGINT PRIMARY KEY,
            name VARCHAR NOT NULL,
            url TEXT,
            alternate_url TEXT,
            vacancies_url TEXT,
            open_vacancies INT
                    )
        """)

    cur.execute("""
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
       """)

    conn.commit()
    cur.close()
    conn.close()

    # with open(file_name, 'r', encoding='utf-8') as file:
    #     json_reader = json.loads(file)
    #     header = next(json_reader)
    #     for row in json_reader:
    #         query = f'INSERT INTO {table_name} ({', '.join(header)}) VALUES ({', '.join(["%s"] * len(row))})'
    #         cur.execute(query, row)

#
# create_database()
# create_tables()






