import pymysql
import traceback
from datetime import datetime
from decouple import config

vars={
    "host":config("MYSQL_HOST"),
    "db_name":config("MYSQL_DB"),
    "user":config("MYSQL_USER"),
    "password":config("MYSQL_PASS"),
    "port":config("MYSQL_PORT"),
}
def create_database(db_name):
    try:
        mysql_conn = pymysql.connect(
            host=vars["host"],
            user=vars["user"],
            password=vars["password"],
            port=int(vars["port"]),
        )
        cur = mysql_conn.cursor()
        cur.execute("SHOW DATABASES")
        dbs = []
        for i in cur.fetchall():
            dbs += i
        if db_name not in dbs:
            cur.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
            print(f"INFO : {datetime.now()} {db_name} database successfully created...")
        else:
            print(f"ERROR : {datetime.now()} {db_name} database already existed...")
        mysql_conn.close()
    except Exception:
        print(traceback.format_exc())


db_name = vars["db_name"]
create_database(db_name=db_name)