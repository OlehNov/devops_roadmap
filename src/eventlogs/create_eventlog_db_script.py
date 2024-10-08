import os
import subprocess

root_user = os.getenv('ROOT_USER')
root_password = os.getenv('ROOT_PASSWORD')
eventlogs_database_name = os.getenv('EVENTLOGS_DATABASE')
eventlogs_database_user = os.getenv('EVENTLOGS_DB_USER')

create_eventlog_database = (f"mysql -h db -u {root_user} -p{root_password} -e "
                            f"'CREATE DATABASE IF NOT EXISTS {eventlogs_database_name}; "
                            f"GRANT ALL PRIVILEGES ON {eventlogs_database_name}.* TO \"{eventlogs_database_user}\"@\"%\";'")

subprocess.run(create_eventlog_database, shell=True, check=True)
