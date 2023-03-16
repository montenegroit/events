import os

from dotenv import load_dotenv

load_dotenv()

db_name = os.environ.get("db_name")
db_host = os.environ.get("db_host")
db_port = os.environ.get("db_port")
db_user = os.environ.get("db_user")
db_pass = os.environ.get("db_pass")

test_db_name = os.environ.get("test_db_name")
test_db_host = os.environ.get("test_db_host")
test_db_port = os.environ.get("test_db_port")
test_db_user = os.environ.get("test_db_user")
test_db_pass = os.environ.get("test_db_pass")
