import os
import subprocess

from dotenv import load_dotenv


load_dotenv()

root_user = os.getenv("ROOT_USER", "root")
root_password = os.getenv("ROOT_PASSWORD", "root")
eventlog_database_name = os.getenv("EVENTLOG_DATABASE", "eventlog")
eventlog_database_user = os.getenv("EVENTLOG_DB_USER", "glamp_user")


create_eventlog_database = (
    f"mysql -h db -u {root_user} -p{root_password} -e "
    f"'CREATE DATABASE IF NOT EXISTS {eventlog_database_name}; "
    f'GRANT ALL PRIVILEGES ON {eventlog_database_name}.* TO "{eventlog_database_user}"@"%";\''
    f"exit;"
)

subprocess.run(create_eventlog_database, shell=True, check=True)
