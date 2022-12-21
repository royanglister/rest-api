import sys
import time
import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker


USERNAME = "postgres"
PASSWORD = "postgres"
DB_NAME = "postgres"
LOCAL_HOST = "localhost"
PORT = "5432"
DB_URI = f"postgresql://{USERNAME}:{PASSWORD}@localhost/{DB_NAME}"


def create_db_if_not_exists():
    try:
        # Establishing the connection
        conn = psycopg2.connect(database=DB_NAME, user=USERNAME, password=PASSWORD, host=LOCAL_HOST, port=PORT)
        cursor = conn.cursor()  # Creating a cursor object
    except:
        print("Error while connecting to postgres")
        sys.exit(-1)

    sql_query = ''' CREATE database users_db ''';
    cursor.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{DB_NAME}'")
    exists = cursor.fetchone()
    if exists:
        return
    else:
        cursor.execute(sql_query)

    print("Database created successfully")
    conn.close()


def wait_for_db(db_uri):  # Checks if database connection is established
    _local_engine = create_engine(db_uri)
    _LocalSessionLocal = sessionmaker(bind=_local_engine, autocommit=False, autoflush=False)

    up = False
    while not up:
        try:
            # Trying to create session to check if DB is awake
            db_session = _LocalSessionLocal()

            # Trying a basic query
            db_session.execute("SELECT 1")
            db_session.commit()

        except Exception as err:
            print(f"Connection error: {err}")
            up = False

        else:
            up = True
        
        time.sleep(2)


create_db_if_not_exists()
wait_for_db(DB_URI)

engine = create_engine(DB_URI)
Base = declarative_base()
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
