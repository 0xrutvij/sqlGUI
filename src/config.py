import os

IMPORT_SOURCE = f"{os.path.abspath('resources/contacts.csv')}"
IMPORT_TEST_SOURCE = f"{os.path.abspath('resources/contacts_test.csv')}"
DATABASE_LOC = f"sqlite+pysqlite:///{os.path.abspath('resources/contacts.db')}"
