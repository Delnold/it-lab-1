# database.py
from table import Table
from table import Schema

class Database:
    def __init__(self, name: str):
        self.name = name
        self.tables = {}  # Key: Table name, Value: Table instance

    def create_table(self, table: Table):
        self.tables[table.name] = table

    def get_table(self, table_name: str) -> Table:
        return self.tables.get(table_name)
