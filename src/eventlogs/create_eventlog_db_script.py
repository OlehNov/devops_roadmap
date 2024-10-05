import os
import subprocess

create_eventlog_database = (f"mysql -h db -u {os.getenv('ROOT_USER')} -p{os.getenv('ROOT_PASSWORD')} -e "
                            f"'CREATE DATABASE IF NOT EXISTS {os.getenv('EVENTLOGS_DATABASE')}; "
                            f"GRANT ALL PRIVILEGES ON {os.getenv('EVENTLOGS_DATABASE')}.* TO \"{os.getenv('EVENTLOGS_DB_USER')}\"@\"%\";'")

subprocess.run(create_eventlog_database, shell=True, check=True)
