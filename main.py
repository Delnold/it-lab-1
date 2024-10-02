from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.responses import Response, RedirectResponse

from data_types import parse_data
from database import Database
from table import Table
from schema import Schema
from attributes import Attribute
from row import Row
from operations import table_product

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Mount static files (CSS, JS)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize database
db = Database('my_database')


@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "tables": db.tables})


@app.get("/create_table")
def get_create_table(request: Request):
    return templates.TemplateResponse("create_table.html", {"request": request})


@app.post("/create_table")
def post_create_table(request: Request, table_name: str = Form(...), attributes: str = Form(...)):
    """
    attributes: A comma-separated list of attribute_name:data_type pairs
    Example: "id:integer,name:string,age:integer"
    """
    attr_list = []
    try:
        for attr in attributes.split(','):
            name, data_type = attr.strip().split(':')
            attr_list.append(Attribute(name.strip(), data_type.strip()))
        schema = Schema(attr_list)
        table = Table(table_name, schema)
        db.create_table(table)
    except Exception as e:
        return templates.TemplateResponse("create_table.html", {"request": request, "error": str(e)})
    return RedirectResponse("/", status_code=303)


@app.get("/tables/{table_name}")
def view_table(request: Request, table_name: str):
    table = db.get_table(table_name)
    if not table:
        return templates.TemplateResponse("view_table.html",
                                          {"request": request, "error": f"Table {table_name} not found."})
    return templates.TemplateResponse("view_table.html", {"request": request, "table": table})


@app.get("/tables/{table_name}/insert_row")
def get_insert_row(request: Request, table_name: str):
    table = db.get_table(table_name)
    if not table:
        return templates.TemplateResponse("insert_row.html",
                                          {"request": request, "error": f"Table {table_name} not found."})
    return templates.TemplateResponse("insert_row.html", {"request": request, "table": table})


@app.get("/product_tables")
def get_product_tables(request: Request):
    return templates.TemplateResponse("product_tables.html", {"request": request, "tables": list(db.tables.keys())})


@app.post("/product_tables")
def post_product_tables(request: Request, table1_name: str = Form(...), table2_name: str = Form(...)):
    table1 = db.get_table(table1_name)
    table2 = db.get_table(table2_name)
    if not table1 or not table2:
        return templates.TemplateResponse("product_tables.html",
                                          {"request": request, "error": "One or both tables not found.",
                                           "tables": list(db.tables.keys())})
    new_table = table_product(table1, table2)
    db.create_table(new_table)
    return RedirectResponse("/", status_code=303)


@app.get("/tables/{table_name}/edit_row/{row_index}")
def get_edit_row(request: Request, table_name: str, row_index: int):
    table = db.get_table(table_name)
    if not table:
        return templates.TemplateResponse("edit_row.html", {
            "request": request, "error": f"Table {table_name} not found."
        })
    try:
        row = table.rows[row_index]
    except IndexError:
        return templates.TemplateResponse("edit_row.html", {
            "request": request, "error": f"Row not found.", "table": table
        })
    return templates.TemplateResponse("edit_row.html", {
        "request": request, "table": table, "row": row, "row_index": row_index
    })


@app.post("/tables/{table_name}/edit_row/{row_index}")
async def post_edit_row(request: Request, table_name: str, row_index: int):
    table = db.get_table(table_name)
    if not table:
        return templates.TemplateResponse("edit_row.html", {
            "request": request, "error": f"Table {table_name} not found."
        })
    form_data = await request.form()
    try:
        parsed_data = {}
        for attr in table.schema.attributes:
            value = form_data.get(attr.name)
            parsed_value = parse_data(value, attr.data_type)
            parsed_data[attr.name] = parsed_value
        updated_row = Row(parsed_data)
        table.update_row(row_index, updated_row)
    except Exception as e:
        row = table.rows[row_index] if row_index < len(table.rows) else None
        return templates.TemplateResponse("edit_row.html", {
            "request": request, "table": table, "row": row, "row_index": row_index, "error": str(e)
        })
    return RedirectResponse(f"/tables/{table_name}", status_code=303)


@app.get("/tables/{table_name}/delete_row/{row_index}")
def delete_row(request: Request, table_name: str, row_index: int):
    table = db.get_table(table_name)
    if not table:
        return RedirectResponse(f"/tables/{table_name}", status_code=303)
    try:
        table.delete_row(row_index)
    except IndexError:
        pass  # Ignore if row doesn't exist
    return RedirectResponse(f"/tables/{table_name}", status_code=303)


@app.post("/tables/{table_name}/insert_row")
async def post_insert_row(request: Request, table_name: str):
    table = db.get_table(table_name)
    if not table:
        return templates.TemplateResponse("insert_row.html", {
            "request": request, "error": f"Table {table_name} not found."
        })
    form_data = await request.form()
    try:
        parsed_data = {}
        for attr in table.schema.attributes:
            value = form_data.get(attr.name)
            parsed_value = parse_data(value, attr.data_type)
            parsed_data[attr.name] = parsed_value
        row = Row(parsed_data)
        table.insert_row(row)
    except Exception as e:
        return templates.TemplateResponse("insert_row.html", {
            "request": request, "table": table, "error": str(e)
        })
    return RedirectResponse(f"/tables/{table_name}", status_code=303)
