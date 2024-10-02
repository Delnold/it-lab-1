# operations.py
from row import Row
from schema import Schema
from table import Table


def table_product(table1: Table, table2: Table) -> Table:
    new_attributes = table1.schema.attributes + table2.schema.attributes
    new_schema = Schema(new_attributes)
    new_table = Table(name=f"{table1.name}_x_{table2.name}", schema=new_schema)

    for row1 in table1.rows:
        for row2 in table2.rows:
            combined_data = {**row1.data, **row2.data}
            new_row = Row(combined_data)
            new_table.insert_row(new_row)

    return new_table
